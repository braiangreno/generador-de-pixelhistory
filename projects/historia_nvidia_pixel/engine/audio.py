"""Banda sonora chiptune original + efectos de sonido + mezcla con la locución.

Genera audio/mix.wav (y stems) sincronizado con la línea de tiempo de NVIDIA (Apertura + 9 capítulos).
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
    return


def add_pad(t, dur, freqs, amp=0.035):
    if dur <= 0:
        return
    for f in freqs:
        note(music, t, f, dur, inst="pulse", vol=amp * 0.28, duty=0.5, a=0.22, d=0.25, s=0.70, r=0.35)


def add_bass(t, dur, f, amp=0.05):
    if dur <= 0:
        return
    note(music, t, f, dur, inst="tri", vol=amp * 0.48, a=0.03, d=0.08, s=0.75, r=0.12)


def fx_pop(t, amp=0.08):
    pop_sfx(t, f0=440, vol=amp * 0.65)


def fx_thud(t, amp=0.09):
    stamp_hit(t, vol=amp * 0.65)


def fx_chime(t, amp=0.10):
    join_jingle(t, vol=amp * 0.55)


def fx_sweep(t, dur=0.5, f0=150, f1=440, amp=0.07):
    whoosh(t, dur=dur, vol=amp * 0.60)


def fx_sparkle(t, amp=0.10):
    coin(t, vol=amp * 0.52)


def compose():
    # Apertura (0:00 -> Cap 1): Octubre 2026 (US$6 billones) -> Noviembre 2026 (renuncia) -> 1993 mesa de restaurante
    section(0.0, TL.s("s03"), 96, [("A", "m"), ("F", "M"), ("C", "M"), ("G", "M")], st_triumph)
    section(TL.s("s03"), TL.s("s05"), 90, [("D", "m"), ("A", "m"), ("Bb", "M"), ("A", "M")], st_winter)
    section(TL.s("s05"), TL.s("c1_00"), 94, [("A", "m"), ("D", "m"), ("F", "M"), ("E", "M")], st_mystery)

    # Acto 1 · Cap 1 (El chip equivocado: San José 1993 -> NV1 1995 -> Sega Saturn)
    section(TL.s("c1_00"), TL.s("c1_03"), 96, [("C", "M"), ("G", "M"), ("A", "m"), ("F", "M")], st_rain)
    section(TL.s("c1_03"), TL.s("c2_00"), 92, [("A", "m"), ("F", "M"), ("D", "m"), ("E", "M")], st_winter)

    # Acto 1 · Cap 2 (Treinta días: Tokio 1996, cheque de US$5M de Irimajiri, despidos y RIVA 128 en 1997)
    section(TL.s("c2_00"), TL.s("c2_04"), 92, [("D", "m"), ("A", "m"), ("F", "M"), ("E", "M")], st_winter)
    section(TL.s("c2_04"), TL.s("c3_00"), 104, [("A", "m"), ("F", "M"), ("C", "M"), ("G", "M")], st_build)

    # Acto 2 · Cap 3 (Miles de manos: GeForce 256 en 1999 + LA PIZARRA 1: GPU vs CPU)
    section(TL.s("c3_00"), TL.s("c3_02"), 102, [("C", "M"), ("G", "M"), ("A", "m"), ("F", "M")], st_bright)
    section(TL.s("c3_02"), TL.s("c4_00"), 106, [("A", "m"), ("F", "M"), ("C", "M"), ("G", "M")], st_puzzle)

    # Acto 2 · Cap 4 (La apuesta que nadie quería: CUDA 2006, laboratorios científicos vs Wall Street)
    section(TL.s("c4_00"), TL.s("c4_03"), 100, [("E", "m"), ("C", "M"), ("G", "M"), ("D", "M")], st_build)
    section(TL.s("c4_03"), TL.s("c5_00"), 94, [("A", "m"), ("F", "M"), ("D", "m"), ("E", "M")], st_rain)

    # Acto 2 · Cap 5 (Dos placas en un dormitorio: Toronto 2012, ImageNet + LA PIZARRA 2: IA)
    section(TL.s("c5_00"), TL.s("c5_04"), 104, [("C", "M"), ("G", "M"), ("A", "m"), ("F", "M")], st_summer_lead)
    section(TL.s("c5_04"), TL.s("c6_00"), 106, [("A", "m"), ("F", "M"), ("C", "M"), ("G", "M")], st_puzzle)

    # Acto 3 · Cap 6 (La fiebre del oro: OpenAI 2016, ChatGPT, mineros y palas, US$5 billones, DeepSeek, casi US$6 billones)
    section(TL.s("c6_00"), TL.s("c6_05"), 108, [("F", "M"), ("C", "M"), ("G", "M"), ("A", "m")], st_triumph)
    section(TL.s("c6_05"), TL.s("c6_06"), 92, [("D", "m"), ("Bb", "M"), ("G", "m"), ("A", "M")], st_winter)
    section(TL.s("c6_06"), TL.s("c7_00"), 106, [("C", "M"), ("G", "M"), ("A", "m"), ("F", "M")], st_triumph)

    # Acto 3 · Cap 7 (Lo que vale una empresa: LA PIZARRA 3)
    section(TL.s("c7_00"), TL.s("c8_00"), 98, [("A", "m"), ("F", "M"), ("D", "m"), ("E", "M")], st_puzzle)

    # Acto 3 · Cap 8 (La semana: NYT/Reuters, carta, renuncia 12 nov 2026, Colette Kress, citación Congreso)
    section(TL.s("c8_00"), TL.s("c8_05"), 88, [("D", "m"), ("A", "m"), ("Bb", "M"), ("A", "M")], st_winter)
    section(TL.s("c8_05"), TL.s("c9_00"), 86, [("A", "m"), ("F", "M"), ("D", "m"), ("E", "M")], st_mystery)

    # Acto 3 · Cap 9 (¿El final?: caída de US$1,7 billones vs ventas de US$108.000M, calendario de 30 días, mesa vacía de 1993 y CTA)
    section(TL.s("c9_00"), TL.s("c9_04"), 92, [("A", "m"), ("D", "m"), ("F", "M"), ("E", "M")], st_rain)
    section(TL.s("c9_04"), TL.e("c9_06") + 0.5, 96, [("A", "m"), ("F", "M"), ("C", "M"), ("G", "M")], st_mystery)


# --------------------------------------------------------------------------- efectos

def plic(t, f=980, vol=0.085):
    note(sfx, t, f, 0.045, "tri", vol=vol, a=0.001, d=0.02, s=0.3, r=0.02)
    note(sfx, t, f * 2.0, 0.018, duty=0.5, vol=vol * 0.35, a=0.001, d=0.01, s=0.2, r=0.01)


def hum_1958(t0, t1, vol=0.022):
    """Zumbido suave de ventilador de placa de video / servidores."""
    if t1 <= t0:
        return
    n = int((t1 - t0) * SR)
    tt = np.arange(n) / SR
    sig = 0.65 * np.sin(2 * np.pi * 60 * tt) + 0.25 * np.sin(2 * np.pi * 120 * tt) + 0.10 * np.sin(2 * np.pi * 180 * tt)
    env = np.minimum(1.0, np.minimum(tt / 0.3, (n - np.arange(n)) / (0.3 * SR)))
    sfx.add(t0, sig * env, vol)


def crt_off(t, vol=0.09):
    """Frenado y apagado del ventilador de la GPU (cuando Huang renuncia el 12 de noviembre de 2026)."""
    n = int(1.1 * SR)
    tt = np.arange(n) / SR
    f = 440 * np.exp(-tt * 3.2) + 55
    ph = np.cumsum(f) / SR
    sig = np.where((ph % 1) < 0.5, 1.0, -1.0) * np.exp(-tt * 2.4)
    sfx.add(t, sig, vol)
    note(sfx, t, 3200, 0.08, duty=0.125, vol=vol * 0.7, a=0.001, d=0.03, s=0.2, r=0.04)


def stamp_hit(t, vol=0.10):
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


def chalk(t0, t1, vol=0.04):
    tt = t0
    while tt < t1:
        d = 0.05 + rng.random() * 0.05
        n = int(d * SR)
        sig = noise(d, 1) * np.sin(np.linspace(0, np.pi, n)) * (0.5 + 0.5 * np.sin(np.arange(n) / SR * 2 * np.pi * 900))
        sfx.add(tt, sig, vol)
        tt += d + 0.015


def design_sfx():
    # Apertura: servidores zumbando -> golpe de diarios en noviembre 2026 -> título A TREINTA DÍAS DE QUEBRAR
    hum_1958(0.05, TL.e("s02"), vol=0.013)
    stamp_hit(TL.s("s03") + 0.35, vol=0.046)
    whoosh(TL.s("s04") + 0.25, dur=0.45, vol=0.038)
    sting(TL.s("s06"), [57, 64, 69, 72, 76], vol=0.042, step=0.14, hold=1.6)

    # Cap 1: restaurante 1993 + monitores CRT 1995 + fax de Sega
    pop_sfx(TL.s("c1_01") + 0.3, f0=480, vol=0.036)
    hum_1958(TL.s("c1_02"), TL.e("c1_03"), vol=0.011)
    stamp_hit(TL.s("c1_04") + 0.35, vol=0.042)

    # Cap 2: Tokio 1996 + cheque de US$5M + hoja arrancada del calendario + RIVA 128
    join_jingle(TL.s("c2_03") + 0.35, vol=0.040)
    whoosh(TL.s("c2_05") + 0.30, dur=0.38, vol=0.038)
    coin(TL.s("c2_06") + 0.45, vol=0.042)

    # Cap 3: ventiladores GeForce 256 + tiza en La Pizarra 1 (GPU vs CPU)
    hum_1958(TL.s("c3_01"), TL.e("c3_01"), vol=0.014)
    chalk(TL.s("c3_02"), TL.e("c3_05"), vol=0.017)

    # Cap 4: escenario CUDA 2006 + laboratorios científicos + niebla del puente verde
    hum_1958(TL.s("c4_01"), TL.e("c4_02"), vol=0.013)
    stamp_hit(TL.s("c4_03") + 0.35, vol=0.042)

    # Cap 5: dos placas en dormitorio de Toronto 2012 + tiza en La Pizarra 2 (IA)
    hum_1958(TL.s("c5_01"), TL.e("c5_03"), vol=0.015)
    join_jingle(TL.s("c5_02") + 0.35, vol=0.040)
    chalk(TL.s("c5_04"), TL.e("c5_06"), vol=0.017)

    # Cap 6: OpenAI 2016 + fiebre del oro + ola de DeepSeek (enero 2025) + récord de US$6 billones
    coin(TL.s("c6_04") + 0.35, vol=0.042)
    stamp_hit(TL.s("c6_05") + 0.55, vol=0.052)
    whoosh(TL.s("c6_05") + 0.60, dur=0.65, vol=0.042)
    join_jingle(TL.s("c6_06") + 0.35, vol=0.040)

    # Cap 7: tiza en La Pizarra 3 (Lo que vale una empresa)
    chalk(TL.s("c7_01"), TL.e("c7_05"), vol=0.017)

    # Cap 8: diarios cayendo sobre el escritorio + el ventilador de la GPU que se detiene el 12 de noviembre (c8_05) + hoja del calendario
    stamp_hit(TL.s("c8_02") + 0.25, vol=0.048)
    stamp_hit(TL.s("c8_04") + 0.25, vol=0.048)
    crt_off(TL.s("c8_05") + 0.25, vol=0.052)
    stamp_hit(TL.s("c8_07") + 0.30, vol=0.045)
    whoosh(TL.s("c8_08") + 0.25, dur=0.42, vol=0.038)

    # Cap 9: servidores activos vs mesa vacía de 1993 + destello del chip verde + acorde de cierre
    hum_1958(TL.s("c9_02"), TL.e("c9_02"), vol=0.014)
    sting(TL.s("c9_05"), [57, 64, 69, 72, 76], vol=0.042, step=0.14, hold=1.8)
    join_jingle(TL.s("c9_06") + 0.25, vol=0.038)


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


CARD_IDS = ["c1_00", "c2_00", "c3_00", "c4_00", "c5_00", "c6_00", "c7_00", "c8_00", "c9_00"]


def card_audio():
    """Sonido suave de cada transición de capítulo (1..9): hoja de calendario arrancada + acorde cálido."""
    for lid in CARD_IDS:
        if lid not in TL.lines:
            continue
        t0 = TL.s(lid) - 0.15
        whoosh(t0, 0.42, 0.026)
        sting(t0 + 0.20, [57, 64, 69, 76], vol=0.028, step=0.12, hold=1.1)
        note(music, t0 + 0.20, midi_hz(45), 1.6, "tri", vol=0.12, a=0.04, s=0.85, r=0.5)


def chapter_hooks():
    """Cada módulo chNN.py puede definir music(A) y sfx(A); A es este módulo."""
    import importlib
    me = sys.modules[__name__]
    for name in ["ch01", "ch02", "ch03", "ch04", "ch05", "ch06", "ch07", "ch08", "ch09", "outro"]:
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
    m_warm = lowpass(lowpass(music.buf, 8), 5)
    s_warm = lowpass(sfx.buf, 2)

    # Ducking equilibrado (Estándar Tesla)
    env = envelope(vo, 0.08)
    duck = np.clip(env / 0.04, 0, 1)
    duck = movavg(duck, 0.32 * SR)

    m_ducked = m_warm * (1.0 - 0.70 * duck) * 0.36
    s_ducked = s_warm * (1.0 - 0.38 * duck) * 0.68
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
    write_wav(os.path.join(out, "music_stem.wav"), (m_warm * 0.36)[:end])
    write_wav(os.path.join(out, "sfx_stem.wav"), (s_warm * 0.68)[:end])
    write_wav(os.path.join(out, "voice_stem.wav"), (vo * 0.98)[:end])
    print("audio ok", round(TL.total, 2), "peak", round(float(peak), 3))


if __name__ == "__main__":
    main()
