"""Banda sonora chiptune original + efectos de sonido + mezcla con la locución.

Genera audio/mix.wav (y stems) sincronizado con la línea de tiempo del piloto.
"""
import math
import os
import subprocess
import sys
import wave

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from timeline import TL, ROOT, TEMPO

SR = 44100
N = int(TL.total * SR) + SR
rng = np.random.default_rng(7)

NOTE = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7,
        "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}


def hz(name):
    """'A4' -> 440"""
    n, o = name[:-1], int(name[-1])
    midi = 12 * (o + 1) + NOTE[n]
    return 440.0 * 2 ** ((midi - 69) / 12)


def midi_hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def chord_notes(root, kind, octave=3):
    base = 12 * (octave + 1) + NOTE[root]
    iv = {"maj": [0, 4, 7], "M": [0, 4, 7], "min": [0, 3, 7], "m": [0, 3, 7], "sus": [0, 5, 7],
          "maj7": [0, 4, 7, 11], "min7": [0, 3, 7, 10], "dim": [0, 3, 6], "add9": [0, 4, 7, 14]}[kind]
    return [base + i for i in iv]


# --------------------------------------------------------------------------- osciladores

def env_adsr(n, a=0.005, d=0.08, s=0.6, r=0.06):
    e = np.ones(n) * s
    na, nd, nr = int(a * SR), int(d * SR), int(r * SR)
    na = min(na, n); e[:na] = np.linspace(0, 1, na, endpoint=False) if na else e[:na]
    nd2 = min(nd, max(0, n - na))
    if nd2:
        e[na:na + nd2] = np.linspace(1, s, nd2, endpoint=False)
    nr = min(nr, n)
    if nr:
        e[n - nr:] *= np.linspace(1, 0, nr)
    return e


def pulse(f, dur, duty=0.25, vib=0.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    ph = f * t
    if vib:
        ph = ph + vib * np.sin(2 * np.pi * 5.5 * t) * np.clip(t * 3 - 0.3, 0, 1) / (2 * np.pi)
    return np.where((ph % 1.0) < duty, 1.0, -1.0)


def tri(f, dur):
    n = int(dur * SR)
    ph = (f * np.arange(n) / SR) % 1.0
    v = 4 * np.abs(ph - 0.5) - 1
    return np.round(v * 8) / 8  # triángulo cuantizado (4 bits, tipo NES)


def noise(dur, period=1):
    n = int(dur * SR)
    v = rng.choice([-1.0, 1.0], size=max(1, n // period + 1))
    return np.repeat(v, period)[:n]


class Track:
    def __init__(self):
        self.buf = np.zeros(N, dtype=np.float64)

    def add(self, t, sig, vol=1.0):
        i = int(t * SR)
        if i >= N or i + len(sig) <= 0:
            return
        if i < 0:
            sig = sig[-i:]; i = 0
        j = min(N, i + len(sig))
        self.buf[i:j] += sig[: j - i] * vol


music = Track()
sfx = Track()


def note(tr, t, f, dur, inst="pulse", vol=0.15, duty=0.25, a=0.004, d=0.08, s=0.55, r=0.05, vib=0.0):
    if inst == "pulse":
        sig = pulse(f, dur, duty, vib)
    elif inst == "tri":
        sig = tri(f, dur)
    else:
        sig = pulse(f, dur, duty)
    tr.add(t, sig * env_adsr(len(sig), a, d, s, r), vol)


def kick(tr, t, vol=0.5):
    dur = 0.16
    n = int(dur * SR)
    tt = np.arange(n) / SR
    f = 120 * np.exp(-tt * 28) + 45
    ph = np.cumsum(f) / SR
    sig = np.sign(np.sin(2 * np.pi * ph)) * np.exp(-tt * 18)
    tr.add(t, sig, vol)


def snare(tr, t, vol=0.25):
    sig = noise(0.14, 2) * np.exp(-np.arange(int(0.14 * SR)) / SR * 22)
    tr.add(t, sig, vol)


def hat(tr, t, vol=0.08, open_=False):
    dur = 0.12 if open_ else 0.04
    sig = noise(dur, 1) * np.exp(-np.arange(int(dur * SR)) / SR * (25 if open_ else 80))
    tr.add(t, sig, vol)


def crash(tr, t, vol=0.25):
    dur = 1.6
    sig = noise(dur, 1) * np.exp(-np.arange(int(dur * SR)) / SR * 2.6)
    tr.add(t, sig, vol)


# --------------------------------------------------------------------------- secciones

BPM_MUL = 0.94  # ritmo pausado y cinematográfico para acompañar la voz


def section(t0, t1, bpm, chords, style, beats_per_chord=4):
    """Escribe la música de una sección entre t0 y t1."""
    beat = 60.0 / (bpm * BPM_MUL)
    nb = int((t1 - t0) / beat)
    for b in range(nb):
        tb = t0 + b * beat
        ci = (b // beats_per_chord) % len(chords)
        root, kind = chords[ci]
        notes = chord_notes(root, kind, 3)
        first = b % beats_per_chord == 0
        fade = min(1.0, (t1 - tb) / 0.8)  # cola suave al final de la sección
        style(tb, beat, b, notes, first, root, fade)


def st_mystery(tb, beat, b, notes, first, root, fade):
    # arpegio suave a mitad de velocidad + bajo triángulo cálido
    for k in range(2):
        m = notes[[0, 2][k]] + 12
        note(music, tb + k * beat / 2, midi_hz(m), beat / 2 * 0.92, duty=0.25,
             vol=0.026 * fade, a=0.025, s=0.45, r=0.12)
    if first:
        note(music, tb, midi_hz(notes[0] - 12), beat * 3.8, "tri", vol=0.16 * fade, a=0.03, s=0.85, r=0.25)
    if b % 8 == 4:
        note(music, tb, midi_hz(notes[2] + 12), beat * 2, duty=0.5, vol=0.018 * fade, a=0.18, s=0.65, r=0.5, vib=0.25)


def st_build(tb, beat, b, notes, first, root, fade):
    st_mystery(tb, beat, b, notes, first, root, fade)
    if b % 2 == 0:
        kick(music, tb, 0.075 * fade)


def st_bright(tb, beat, b, notes, first, root, fade):
    for k in range(2):
        m = notes[[0, 2][k]] + 12
        note(music, tb + k * beat / 2, midi_hz(m), beat / 2 * 0.88, duty=0.5,
             vol=0.028 * fade, a=0.02, s=0.45, r=0.10)
    if b % 2 == 0:
        note(music, tb, midi_hz(notes[0] - 12), beat * 1.85, "tri", vol=0.16 * fade, a=0.02, s=0.8, r=0.15)
        kick(music, tb, 0.07 * fade)
    elif b % 4 == 2:
        snare(music, tb, 0.018 * fade)


MELODY_SUMMER = [76, 79, 81, 79, 76, 74, 72, 74, 76, 76, 74, 72, 71, 72, 74, 72]


def st_summer_lead(tb, beat, b, notes, first, root, fade):
    st_bright(tb, beat, b, notes, first, root, fade)
    if b % 2 == 0:
        m = MELODY_SUMMER[(b // 2) % len(MELODY_SUMMER)]
        note(music, tb, midi_hz(m - 12), beat * 1.7, duty=0.5, vol=0.022 * fade, a=0.04, s=0.55, r=0.2, vib=0.2)


def st_rain(tb, beat, b, notes, first, root, fade):
    for k in range(2):
        m = notes[[0, 2][k]] + 12
        note(music, tb + k * beat / 2, midi_hz(m), beat / 2 * 0.95, duty=0.25,
             vol=0.025 * fade, a=0.03, s=0.35, r=0.2)
    if first:
        note(music, tb, midi_hz(notes[0] - 12), beat * 3.9, "tri", vol=0.15 * fade, a=0.03, s=0.85, r=0.3)
    mel = [69, 72, 74, 72, 69, 67, 65, 67]
    if b % 4 == 0:
        note(music, tb, midi_hz(mel[(b // 4) % len(mel)] - 12), beat * 3.2, duty=0.5, vol=0.020 * fade, a=0.10,
             s=0.65, r=0.4, vib=0.3)


def st_puzzle(tb, beat, b, notes, first, root, fade):
    seq = [0, 2, 1, 2]
    m = notes[seq[b % 4]] + 12
    note(music, tb, midi_hz(m), beat * 0.65, duty=0.5, vol=0.026 * fade, a=0.02, s=0.35, r=0.08)
    if b % 2 == 0:
        note(music, tb, midi_hz(notes[0] - 12), beat * 1.8, "tri", vol=0.15 * fade, a=0.02, s=0.65, r=0.15)


def st_triumph(tb, beat, b, notes, first, root, fade):
    st_bright(tb, beat, b, notes, first, root, fade)
    if first:
        for m in notes:
            note(music, tb, midi_hz(m), beat * 3.6, duty=0.5, vol=0.020 * fade, a=0.06, s=0.65, r=0.35)


def st_winter(tb, beat, b, notes, first, root, fade):
    if first:
        for m in notes:
            note(music, tb, midi_hz(m), beat * 3.9, duty=0.5, vol=0.018 * fade, a=0.4, s=0.75, r=0.8, vib=0.15)
        note(music, tb, midi_hz(notes[0] - 12), beat * 3.9, "tri", vol=0.15 * fade, a=0.2, s=0.85, r=0.6)
    if b % 4 == 2:
        note(music, tb, midi_hz(notes[2] + 12), beat * 0.8, duty=0.25, vol=0.016 * fade, a=0.03, s=0.3, r=0.3)


def sting(t, notes, inst_duty=0.5, vol=0.04, step=0.14, hold=1.2):
    for i, m in enumerate(notes):
        last = i == len(notes) - 1
        note(music, t + i * step, midi_hz(m), hold if last else step * 0.9, duty=inst_duty, vol=vol * 0.72,
             a=0.015, s=0.65, r=0.4 if last else 0.04, vib=0.25 if last else 0)


def sand_hiss(t0, dur=1.8, vol=0.025):
    """Siseo suave ambiental."""
    n = int(dur * SR)
    if n <= 0:
        return
    x = rng.standard_normal(n)
    y = np.convolve(x, np.ones(14) / 14, mode="same") - np.convolve(x, np.ones(60) / 60, mode="same")
    tt = np.arange(n) / SR
    env = np.sin(np.linspace(0, np.pi, n)) ** 1.4
    shimmer = 0.75 + 0.25 * np.sin(2 * np.pi * 3.2 * tt)
    sfx.add(t0, y * env * shimmer * 1.6, vol)


def add_note(t, dur, f, wave="pulse25", amp=0.05, vibrato=0.0):
    # Desactivamos los arpegios secundarios de chNN.music para que no choquen con compose()
    return


def add_pad(t, dur, freqs, amp=0.035):
    if dur <= 0:
        return
    for f in freqs:
        note(music, t, f, dur, inst="pulse", vol=amp * 0.22, duty=0.5, a=0.22, d=0.25, s=0.70, r=0.35)


def add_bass(t, dur, f, amp=0.05):
    if dur <= 0:
        return
    note(music, t, f, dur, inst="tri", vol=amp * 0.45, a=0.03, d=0.08, s=0.75, r=0.12)


def fx_pop(t, amp=0.08):
    pop_sfx(t, f0=420, vol=amp * 0.35)


def fx_thud(t, amp=0.09):
    stamp_hit(t, vol=amp * 0.35)


def fx_chime(t, amp=0.10):
    join_jingle(t, vol=amp * 0.26)


def fx_sweep(t, dur=0.5, f0=150, f1=440, amp=0.07):
    whoosh(t, dur=dur, vol=amp * 0.32)


def fx_sparkle(t, amp=0.10):
    coin(t, vol=amp * 0.25)


def compose():
    # Apertura (0:00 -> Cap 1): Sexta Avenida de Nueva York 1973 y llamada a Joel Engel
    section(0.0, TL.s("s03"), 88, [("A", "m"), ("F", "M"), ("C", "M"), ("E", "M")], st_mystery)
    section(TL.s("s03"), TL.s("c1_00"), 96, [("A", "m"), ("F", "M"), ("C", "M"), ("G", "M")], st_build)

    # Capítulo 1 (El ladrillo: teléfonos de auto vs el prototipo DynaTAC de Martin Cooper)
    section(TL.s("c1_00"), TL.s("c2_00"), 94, [("A", "m"), ("D", "m"), ("F", "M"), ("E", "M")], st_rain)

    # Capítulo 2 (El panal: 12 canales saturados + La Pizarra 1: Panal celular + Bell Labs)
    section(TL.s("c2_00"), TL.s("c2_03"), 96, [("A", "m"), ("F", "M"), ("C", "M"), ("G", "M")], st_build)
    section(TL.s("c2_03"), TL.s("c3_00"), 106, [("C", "M"), ("G", "M"), ("A", "m"), ("F", "M")], st_puzzle)

    # Capítulo 3 (Escribir y mirar: primer SMS 1992 en Inglaterra + primera foto 1997 en California)
    section(TL.s("c3_00"), TL.s("c3_06"), 92, [("D", "m"), ("A", "m"), ("Bb", "M"), ("A", "M")], st_winter)
    section(TL.s("c3_06"), TL.s("c4_00"), 104, [("D", "m"), ("F", "M"), ("C", "M"), ("G", "M")], st_triumph)

    # Capítulo 4 (Simon: el primer smartphone de IBM en 1994 y por qué llegó demasiado temprano)
    section(TL.s("c4_00"), TL.s("c4_03"), 98, [("E", "m"), ("C", "M"), ("D", "M"), ("B", "m")], st_build)
    section(TL.s("c4_03"), TL.s("c5_00"), 92, [("A", "m"), ("F", "M"), ("D", "m"), ("E", "M")], st_rain)

    # Capítulo 5 (Una pantalla que siente: San Francisco 2007 + La Pizarra 2: Pantalla Capacitiva)
    section(TL.s("c5_00"), TL.s("c5_05"), 106, [("C", "M"), ("G", "M"), ("A", "m"), ("F", "M")], st_triumph)
    section(TL.s("c5_05"), TL.s("c6_00"), 106, [("C", "M"), ("G", "M"), ("A", "m"), ("F", "M")], st_puzzle)

    # Capítulo 6 (Quinientas aplicaciones: App Store 2008 + llegada de Android)
    section(TL.s("c6_00"), TL.s("c6_04"), 104, [("E", "m"), ("G", "M"), ("D", "M"), ("A", "M")], st_bright)
    section(TL.s("c6_04"), TL.s("c7_00"), 104, [("F", "M"), ("C", "M"), ("G", "M"), ("A", "m")], st_summer_lead)

    # Capítulo 7 (Einstein en el bolsillo: satélites a 20.000 km + La Pizarra 3: GPS y Relatividad)
    section(TL.s("c7_00"), TL.s("c7_03"), 96, [("D", "m"), ("Bb", "M"), ("F", "M"), ("A", "M")], st_build)
    section(TL.s("c7_03"), TL.s("c8_00"), 106, [("C", "M"), ("G", "M"), ("A", "m"), ("F", "M")], st_puzzle)

    # Capítulo 8 (Una llamada al rival: del ladrillo al bolsillo -> regreso a 1973 -> CTA comentarios)
    section(TL.s("c8_00"), TL.s("c8_05"), 94, [("A", "m"), ("F", "M"), ("D", "m"), ("E", "M")], st_bright)
    section(TL.s("c8_05"), TL.e("c8_07") + 0.5, 102, [("A", "m"), ("F", "M"), ("C", "M"), ("G", "M")], st_triumph)


# --------------------------------------------------------------------------- efectos

def plic(t, f=980, vol=0.085):
    """El 'plic' analógico original de Tennis for Two (1958): pulso corto resonante + clic de relé."""
    note(sfx, t, f, 0.045, "tri", vol=vol, a=0.001, d=0.02, s=0.3, r=0.02)
    note(sfx, t, f * 2.0, 0.018, duty=0.5, vol=vol * 0.35, a=0.001, d=0.01, s=0.2, r=0.01)


def hum_1958(t0, t1, vol=0.022):
    """Zumbido eléctrico suave de 60 Hz + armónico de osciloscopio de bulbos."""
    if t1 <= t0:
        return
    n = int((t1 - t0) * SR)
    tt = np.arange(n) / SR
    sig = 0.65 * np.sin(2 * np.pi * 60 * tt) + 0.25 * np.sin(2 * np.pi * 120 * tt) + 0.10 * np.sin(2 * np.pi * 180 * tt)
    env = np.minimum(1.0, np.minimum(tt / 0.3, (n - np.arange(n)) / (0.3 * SR)))
    sfx.add(t0, sig * env, vol)


def crt_off(t, vol=0.09):
    """Apagado de televisor de tubo y cinta que se frena (Crash de 1983)."""
    n = int(1.1 * SR)
    tt = np.arange(n) / SR
    f = 440 * np.exp(-tt * 3.2) + 55
    ph = np.cumsum(f) / SR
    sig = np.where((ph % 1) < 0.5, 1.0, -1.0) * np.exp(-tt * 2.4)
    sfx.add(t, sig, vol)
    note(sfx, t, 3200, 0.08, duty=0.125, vol=vol * 0.7, a=0.001, d=0.03, s=0.2, r=0.04)


def cartridge_slam(t, vol=0.11):
    """Golpe seco mecánico de un cartucho entrando en la consola (NES 1985)."""
    sig1 = noise(0.045, 2) * np.exp(-np.arange(int(0.045 * SR)) / SR * 90)
    sfx.add(t, sig1, vol)
    note(sfx, t + 0.01, 110, 0.08, "tri", vol=vol * 1.4, a=0.001, d=0.03, s=0.3, r=0.03)
    sig2 = noise(0.03, 1) * np.exp(-np.arange(int(0.03 * SR)) / SR * 130)
    sfx.add(t + 0.065, sig2, vol * 0.8)


def coin_cascade(t0, dur=1.8, count=22, vol=0.055):
    """Cascada de monedas cayendo al abrir la máquina de Pong."""
    for i in range(count):
        tc = t0 + (i / count) * dur * 0.85 + rng.random() * 0.06
        f0 = 1350 + (i % 5) * 140
        note(sfx, tc, f0, 0.035, duty=0.5, vol=vol, a=0.001, d=0.01, s=0.6, r=0.01)
        note(sfx, tc + 0.03, f0 * 1.33, 0.09, duty=0.5, vol=vol * 0.85, a=0.001, d=0.02, s=0.5, r=0.05)


def ps1_boot(t, dur=2.6, vol=0.055):
    """Arranque poligonal de 1994: acorde profundo de sintetizador FM / pad cristalino."""
    for m in [38, 45, 50, 57, 62, 66, 69]:
        note(music, t, midi_hz(m), dur, "saw", vol=vol * 0.55, a=0.18, d=0.4, s=0.75, r=0.6)
    for i, m in enumerate([74, 78, 81, 86]):
        note(sfx, t + 0.35 + i * 0.14, midi_hz(m), 1.4, "tri", vol=vol * 0.9, a=0.02, d=0.2, s=0.6, r=0.4)


def stamp_hit(t, vol=0.10):
    """Golpe pesado de sello sobre calendario ('POSTERGADO')."""
    sig = noise(0.06, 3) * np.exp(-np.arange(int(0.06 * SR)) / SR * 70)
    sfx.add(t, sig, vol)
    note(sfx, t, 85, 0.11, "tri", vol=vol * 1.5, a=0.001, d=0.04, s=0.3, r=0.04)


def blip(t, f=1200, dur=0.03, vol=0.05, duty=0.5):
    note(sfx, t, f, dur, duty=duty, vol=vol, a=0.001, d=0.01, s=0.8, r=0.01)


def pop_sfx(t, f0=500, vol=0.08):
    n = int(0.09 * SR)
    tt = np.arange(n) / SR
    f = f0 * (1 + tt * 18)
    ph = np.cumsum(f) / SR
    sfx.add(t, np.where((ph % 1) < 0.5, 1.0, -1.0) * np.exp(-tt * 30), vol)


def coin(t, vol=0.07):
    note(sfx, t, hz("B5"), 0.07, duty=0.5, vol=vol, s=0.9, r=0.01)
    note(sfx, t + 0.07, hz("E6"), 0.3, duty=0.5, vol=vol, s=0.7, r=0.25)


def join_jingle(t, vol=0.06):
    for i, m in enumerate([72, 76, 79, 84]):
        note(sfx, t + i * 0.06, midi_hz(m), 0.06 if i < 3 else 0.25, duty=0.25, vol=vol, s=0.8, r=0.1)


def whoosh(t, dur=0.4, vol=0.06):
    n = int(dur * SR)
    sig = noise(dur, 2) * np.sin(np.linspace(0, np.pi, n))
    sfx.add(t, sig, vol)


def typewriter(t0, t1, rate=12, vol=0.05):
    tt = t0
    while tt < t1:
        sig = noise(0.02, 1) * np.exp(-np.arange(int(0.02 * SR)) / SR * 200)
        sfx.add(tt, sig, vol)
        tt += 1 / rate * (0.7 + rng.random() * 0.6)


def text_blips(t0, nchars, rate, vol=0.022, f=1500):
    for i in range(nchars):
        if i % 2 == 0:
            blip(t0 + i / rate, f + (i % 3) * 60, 0.018, vol)


def rain_amb(t0, t1, vol=0.035):
    n = int((t1 - t0) * SR)
    x = rng.standard_normal(n)
    # ruido rosado aproximado (filtro simple)
    y = np.convolve(x, np.ones(6) / 6, mode="same")
    env = np.minimum(1, np.minimum(np.arange(n) / (0.4 * SR), (n - np.arange(n)) / (0.4 * SR)))
    sfx.add(t0, y * env, vol)


def wind(t0, t1, vol=0.05):
    n = int((t1 - t0) * SR)
    x = rng.standard_normal(n)
    y = np.convolve(x, np.ones(40) / 40, mode="same") * 4
    tt = np.arange(n) / SR
    mod = 0.6 + 0.4 * np.sin(2 * np.pi * 0.23 * tt) * np.sin(2 * np.pi * 0.07 * tt + 1)
    env = np.minimum(1, np.minimum(tt / 1.5, (n - np.arange(n)) / (1.2 * SR)))
    sfx.add(t0, y * mod * env, vol)


def chalk(t0, t1, vol=0.04):
    tt = t0
    while tt < t1:
        d = 0.05 + rng.random() * 0.05
        n = int(d * SR)
        sig = noise(d, 1) * np.sin(np.linspace(0, np.pi, n)) * (0.5 + 0.5 * np.sin(np.arange(n) / SR * 2 * np.pi * 900))
        sfx.add(tt, sig, vol)
        tt += d + 0.015


def freeze(t, vol=0.09):
    for i in range(10):
        f = 3000 - i * 220
        note(sfx, t + i * 0.025, f, 0.03, duty=0.125, vol=vol * (1 - i / 12), s=0.6, r=0.01)
    sig = noise(0.5, 1) * np.exp(-np.arange(int(0.5 * SR)) / SR * 9)
    sfx.add(t, sig, vol * 0.6)


def robot_beep(t, vol=0.05):
    for i, f in enumerate([880, 1320, 990]):
        note(sfx, t + i * 0.07, f, 0.06, duty=0.5, vol=vol, s=0.8, r=0.01)


def design_sfx():
    # Apertura: pulsos suaves de marcado y acorde de título en s05
    for k in range(3):
        blip(TL.s("s02") + 0.6 + k * 0.22, 880 + k * 110, 0.045, 0.016)
    sting(TL.s("s05"), [57, 64, 69, 72, 76], vol=0.035, step=0.14, hold=1.6)

    # Cap 1: zumbido suave de laboratorio de Motorola
    hum_1958(TL.s("c1_03"), TL.e("c1_04"), vol=0.008)

    # Cap 2: La Pizarra 1 (El Panal Celular: tiza suave)
    chalk(TL.s("c2_03") + 0.4, TL.s("c2_04") + 1.8, vol=0.012)

    # Cap 3: lluvia suave de diciembre en Inglaterra (1992)
    rain_amb(TL.s("c3_03"), TL.e("c3_04"), vol=0.011)

    # Cap 4: IBM Simon (1994)
    hum_1958(TL.s("c4_01"), TL.e("c4_02"), vol=0.008)

    # Cap 5: La Pizarra 2 (Pantalla Capacitiva: tiza suave)
    chalk(TL.s("c5_05") + 0.4, TL.s("c5_06") + 1.8, vol=0.012)

    # Cap 6: App Store (2008) y llegada de Android
    join_jingle(TL.s("c6_02") + 0.3, vol=0.024)

    # Cap 7: pulsos suaves de satélite GPS + La Pizarra 3 (GPS y Einstein)
    for k in range(3):
        blip(TL.s("c7_02") + 0.8 + k * 0.28, 980, 0.045, 0.016)
    chalk(TL.s("c7_03") + 0.4, TL.s("c7_04") + 1.8, vol=0.012)

    # Cap 8: regreso a 1973 y CTA de comentarios
    sting(TL.s("c8_06"), [57, 64, 69, 73, 76, 81], vol=0.038, step=0.14, hold=2.0)
    join_jingle(TL.s("c8_07"), vol=0.025)


# --------------------------------------------------------------------------- voz y mezcla

def load_mp3(path):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", path, "-af", f"atempo={TEMPO}", "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"])
    return np.frombuffer(raw, dtype=np.int16).astype(np.float64) / 32768.0


def build_voice():
    vo = np.zeros(N)
    for lid, L in TL.lines.items():
        x = load_mp3(os.path.join(ROOT, "audio", "vo", f"{lid}.mp3"))
        i = int(L["start"] * SR)
        j = min(N, i + len(x))
        vo[i:j] += x[: j - i]
    return vo


def movavg(x, k):
    """Media móvil centrada O(N) (reemplaza np.convolve con kernels grandes)."""
    k = max(1, int(k))
    c = np.cumsum(np.concatenate([np.zeros(1), x]))
    y = (c[k:] - c[:-k]) / k
    pad_l = (len(x) - len(y)) // 2
    return np.concatenate([np.full(pad_l, y[0]), y, np.full(len(x) - len(y) - pad_l, y[-1])])


def envelope(x, win=0.05):
    return np.sqrt(movavg(x ** 2, win * SR))


def write_wav(path, x, stereo=True):
    x = np.clip(x, -1, 1)
    data = (x * 32767).astype(np.int16)
    if stereo:
        data = np.stack([data, data], axis=1).reshape(-1)
    with wave.open(path, "wb") as wf:
        wf.setnchannels(2 if stereo else 1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(data.tobytes())


def lowpass(x, k=3):
    return np.convolve(x, np.ones(k) / k, mode="same")


CARD_IDS = ["c1_00", "c2_00", "c3_00", "c4_00", "c5_00", "c6_00", "c7_00", "c8_00"]


def card_audio():
    """Sonido suave de cada transición de capítulo (1..8): acorde cálido sin pitidos de tipeo."""
    for lid in CARD_IDS:
        if lid not in TL.lines:
            continue
        t0 = TL.s(lid) - 0.15
        whoosh(t0, 0.42, 0.022)
        sting(t0 + 0.20, [57, 64, 69, 76], vol=0.028, step=0.12, hold=1.1)
        note(music, t0 + 0.20, midi_hz(45), 1.6, "tri", vol=0.12, a=0.04, s=0.85, r=0.5)


def chapter_hooks():
    """Cada módulo chNN.py puede definir music(A) y sfx(A); A es este módulo."""
    import importlib
    me = sys.modules[__name__]
    for name in ["ch01", "ch02", "ch03", "ch04", "ch05", "ch06", "ch07", "ch08", "outro"]:
        try:
            mod = importlib.import_module(name)
        except ModuleNotFoundError as e:
            if e.name == name:
                continue
            raise
        if hasattr(mod, "music"):
            mod.music(me)
        if hasattr(mod, "sfx"):
            mod.sfx(me)
        print("hooks", name)


def main():
    compose()
    design_sfx()
    card_audio()
    chapter_hooks()
    vo = build_voice()
    # Filtro pasa-bajos cálido para redondear armónicos agudos del chiptune y dejar libre la banda de la voz
    m_warm = lowpass(lowpass(music.buf, 8), 5)
    s_warm = lowpass(sfx.buf, 4)

    # Ducking profundo: cuando habla el narrador, la música y los efectos bajan suavemente para acompañar sin competir
    env = envelope(vo, 0.08)
    duck = np.clip(env / 0.04, 0, 1)
    duck = movavg(duck, 0.32 * SR)

    m_ducked = m_warm * (1.0 - 0.72 * duck) * 0.36
    s_ducked = s_warm * (1.0 - 0.55 * duck) * 0.42
    mix = vo * 0.98 + m_ducked + s_ducked
    # fade final
    nf = int(1.5 * SR)
    end = int(TL.total * SR)
    mix[end - nf:end] *= np.linspace(1, 0, nf)
    mix[end:] = 0
    mix = mix[:end]
    peak = np.max(np.abs(mix))
    if peak > 0.97:
        mix *= 0.97 / peak
    out = os.path.join(ROOT, "audio")
    write_wav(os.path.join(out, "mix.wav"), mix)
    # Guardamos los stems ya suavizados (sin el ducking de ES) para que mix_multilingual aplique el ducking de EN y PT
    write_wav(os.path.join(out, "music_stem.wav"), (m_warm * 0.36)[:end])
    write_wav(os.path.join(out, "sfx_stem.wav"), (s_warm * 0.42)[:end])
    write_wav(os.path.join(out, "voice_stem.wav"), (vo * 0.98)[:end])
    print("audio ok", round(TL.total, 2), "peak", round(float(peak), 3))


if __name__ == "__main__":
    main()
