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
    iv = {"maj": [0, 4, 7], "min": [0, 3, 7], "sus": [0, 5, 7], "maj7": [0, 4, 7, 11], "min7": [0, 3, 7, 10],
          "dim": [0, 3, 6], "add9": [0, 4, 7, 14]}[kind]
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

BPM_MUL = 1.12  # todo un poco más rápido (ritmo)


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
    # arpegio lento 12.5% + bajo triángulo
    for k in range(4):
        m = notes[[0, 1, 2, 1][k]] + 12
        note(music, tb + k * beat / 4, midi_hz(m), beat / 4 * 0.9, duty=0.125, vol=0.05 * fade, s=0.4)
    if first:
        note(music, tb, midi_hz(notes[0] - 12), beat * 3.8, "tri", vol=0.22 * fade, s=0.9, r=0.2)
    if b % 8 == 4:
        note(music, tb, midi_hz(notes[2] + 24), beat * 2, duty=0.5, vol=0.03 * fade, a=0.15, s=0.7, r=0.5, vib=0.4)


def st_build(tb, beat, b, notes, first, root, fade):
    st_mystery(tb, beat, b, notes, first, root, fade)
    hat(music, tb + beat / 2, 0.035 * fade)
    if b % 2 == 0:
        kick(music, tb, 0.18 * fade)


def st_bright(tb, beat, b, notes, first, root, fade):
    for k in range(4):
        m = notes[[0, 2, 1, 2][k]] + 12
        note(music, tb + k * beat / 4, midi_hz(m), beat / 4 * 0.8, duty=0.25, vol=0.05 * fade, s=0.45)
    note(music, tb, midi_hz(notes[0] - 12 + (7 if b % 2 else 0)), beat * 0.9, "tri", vol=0.22 * fade, s=0.8)
    kick(music, tb, 0.16 * fade) if b % 2 == 0 else snare(music, tb, 0.08 * fade)
    hat(music, tb + beat / 2, 0.03 * fade)


MELODY_SUMMER = [76, 79, 81, 79, 76, 74, 72, 74, 76, 76, 74, 72, 71, 72, 74, 72]


def st_summer_lead(tb, beat, b, notes, first, root, fade):
    st_bright(tb, beat, b, notes, first, root, fade)
    m = MELODY_SUMMER[b % len(MELODY_SUMMER)]
    note(music, tb, midi_hz(m), beat * 0.85, duty=0.5, vol=0.045 * fade, s=0.6, vib=0.3)


def st_rain(tb, beat, b, notes, first, root, fade):
    for k in range(2):
        m = notes[[0, 2][k]] + 12 + (12 if b % 4 == 3 and k == 1 else 0)
        note(music, tb + k * beat / 2, midi_hz(m), beat / 2 * 0.95, duty=0.125, vol=0.045 * fade, s=0.35, r=0.2)
    if first:
        note(music, tb, midi_hz(notes[0] - 12), beat * 3.9, "tri", vol=0.2 * fade, s=0.9, r=0.3)
    mel = [69, 72, 74, 72, 69, 67, 65, 67]
    if b % 2 == 0:
        note(music, tb, midi_hz(mel[(b // 2) % len(mel)]), beat * 1.8, duty=0.5, vol=0.03 * fade, a=0.08,
             s=0.7, r=0.4, vib=0.5)


def st_puzzle(tb, beat, b, notes, first, root, fade):
    seq = [0, 2, 1, 2, 0, 2, 1, 0]
    for k in range(2):
        m = notes[seq[(b * 2 + k) % 8]] + 12
        note(music, tb + k * beat / 2, midi_hz(m), 0.07, duty=0.25, vol=0.06 * fade, s=0.2, r=0.02)
    note(music, tb, midi_hz(notes[0] - 12 + (0 if b % 2 == 0 else 7)), beat * 0.45, "tri", vol=0.22 * fade,
         s=0.6)
    hat(music, tb + beat / 2, 0.025 * fade)
    if b % 4 == 2:
        snare(music, tb, 0.05 * fade)


def st_triumph(tb, beat, b, notes, first, root, fade):
    st_bright(tb, beat, b, notes, first, root, fade)
    if first:
        for m in notes:
            note(music, tb, midi_hz(m + 12), beat * 3.5, duty=0.5, vol=0.03 * fade, a=0.02, s=0.7, r=0.3)
    hat(music, tb + beat / 4 * 3, 0.02 * fade)


def st_winter(tb, beat, b, notes, first, root, fade):
    if first:
        for m in notes:
            note(music, tb, midi_hz(m + 12), beat * 3.9, duty=0.5, vol=0.022 * fade, a=0.4, s=0.8, r=0.8, vib=0.2)
        note(music, tb, midi_hz(notes[0] - 12), beat * 3.9, "tri", vol=0.18 * fade, a=0.2, s=0.9, r=0.6)
    if b % 2 == 1:
        note(music, tb, midi_hz(notes[2] + 24), beat * 0.4, duty=0.125, vol=0.025 * fade, s=0.3, r=0.3)


def sting(t, notes, inst_duty=0.5, vol=0.06, step=0.14, hold=1.2):
    for i, m in enumerate(notes):
        last = i == len(notes) - 1
        note(music, t + i * step, midi_hz(m), hold if last else step * 0.9, duty=inst_duty, vol=vol,
             s=0.7, r=0.4 if last else 0.03, vib=0.4 if last else 0)


def compose():
    s = TL.s
    e = TL.e
    w = TL.word
    c_ten = s("s02") - 0.25
    c_sum = s("s03") - 0.3
    c_title = s("s05") - 0.3
    c_ch1 = s("s06") - 0.45
    c_tur = s("s07") - 0.3
    c_imi = s("s08") - 0.3
    c_dar = s("s09") - 0.3
    c_board = w("s10", "nombre", end=True) + 0.05
    c_win = s("s11") - 0.35
    c_ch2 = s("s13") - 0.5
    Am = [("A", "min"), ("F", "maj"), ("C", "maj"), ("G", "maj")]
    section(0.3, c_ten, 84, Am, st_mystery)
    section(c_ten, c_sum, 96, [("F", "maj"), ("G", "maj"), ("A", "min"), ("C", "maj")], st_build)
    section(c_sum, s("s04") + 0.2, 112, [("C", "maj"), ("F", "maj"), ("A", "min"), ("G", "maj")], st_summer_lead)
    # time-lapse: arpegio que se acelera y sube
    t0, t1 = s("s04") + 0.2, c_title
    tt = t0
    k = 0
    while tt < t1:
        p = (tt - t0) / (t1 - t0)
        step = 0.16 - 0.11 * p
        m = 60 + [0, 4, 7, 12, 16, 19][k % 6] + int(p * 12)
        note(music, tt, midi_hz(m), step * 0.9, duty=0.125, vol=0.05, s=0.4)
        if k % 6 == 0:
            note(music, tt, midi_hz(36 + int(p * 12)), step * 5.5, "tri", vol=0.2, s=0.8)
        tt += step
        k += 1
    # riser de ruido
    n = int((t1 - t0) * SR)
    riser = noise(t1 - t0, 3) * np.linspace(0, 1, n) ** 2
    music.add(t0, riser, 0.05)
    # título: golpes
    t_ia, t_art = w("s05", "inteligencia") + 0.22, w("s05", "artificial") + 0.22
    for tt_, ch in ((t_ia, chord_notes("A", "min", 3)), (t_art, chord_notes("F", "maj7", 3))):
        kick(music, tt_, 0.5); crash(music, tt_, 0.14)
        for m in ch:
            note(music, tt_, midi_hz(m + 12), 1.6, duty=0.5, vol=0.04, s=0.7, r=0.6)
        note(music, tt_, midi_hz(ch[0] - 12), 1.8, "tri", vol=0.3, s=0.9, r=0.6)
    section(t_art + 1.0, c_ch1, 84, [("C", "add9")], st_winter)
    # capítulo 1: sting
    sting(c_ch1 + 0.4, [69, 72, 76, 81], vol=0.055)
    note(music, c_ch1 + 0.4, midi_hz(45), 2.5, "tri", vol=0.25, s=0.9, r=0.8)
    section(c_tur + 0.2, c_imi, 76, [("D", "min"), ("Bb", "maj"), ("F", "maj"), ("C", "maj")], st_rain)
    section(c_imi, c_dar, 112, [("E", "min"), ("C", "maj"), ("A", "min"), ("B", "maj")], st_puzzle)
    section(c_dar, c_board, 120, [("G", "maj"), ("C", "maj"), ("E", "min"), ("D", "maj")], st_summer_lead)
    section(c_board, c_win, 120, [("C", "maj"), ("G", "maj")], st_triumph)
    section(c_win, s("s12") + 0.1, 132, [("C", "maj"), ("F", "maj"), ("G", "maj"), ("C", "maj")], st_triumph)
    # caída: barrido de tono descendente
    td = s("s12") + 0.05
    n = int(1.4 * SR)
    tt = np.arange(n) / SR
    f = 880 * np.exp(-tt * 2.2)
    ph = np.cumsum(f) / SR
    music.add(td, np.where((ph % 1) < 0.5, 1.0, -1.0) * np.exp(-tt * 1.5), 0.05)
    section(td + 0.6, c_ch2, 70, [("A", "min"), ("F", "maj"), ("D", "min"), ("E", "min")], st_winter)


# --------------------------------------------------------------------------- efectos

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
    s, e, w = TL.s, TL.e, TL.word
    # apertura
    whoosh(s("s01") - 0.15, 0.4); sfx_t = s("s01") + 0.35
    note(sfx, sfx_t, hz("A2"), 0.4, "tri", vol=0.25, s=0.5, r=0.2)
    for i in range(4):  # pasos
        t0 = w("s01", "cuatro") - 0.9 + i * 0.22
        for k in range(4):
            sig = noise(0.03, 3) * np.exp(-np.arange(int(0.03 * SR)) / SR * 120)
            sfx.add(t0 + k * 0.38, sig, 0.03)
    coin(w("s01", "dinero"))
    typewriter(w("s01", "dinero") + 0.2, s("s02") - 0.4, vol=0.03)
    for i in range(4):
        pop_sfx(w("s01", "audaz") + i * 0.07, 700 + i * 80, 0.05)
    # diez personas
    text_blips(s("s02"), 9, 22)
    text_blips(w("s02", "diez"), 13, 26)
    pop_sfx(s("s02") + 0.2, 400)
    for i in range(10):
        pop_sfx(w("s02", "diez") + 0.05 + i * 0.11, 500 + i * 60, 0.05)
    robot_beep(w("s02", "maquina") + 0.4)
    coin(w("s02", "pensar") + 0.25, 0.05)
    # verano
    text_blips(s("s03") + 0.1, 16, 30, 0.018)
    # título
    whoosh(w("s05", "inteligencia"), 0.25, 0.07); whoosh(w("s05", "artificial"), 0.25, 0.07)
    text_blips(w("s05", "historia") - 0.2, 17, 24)
    text_blips(e("s05") + 0.2, 26, 30, 0.015, 1800)
    robot_beep(e("s05") + 0.55, 0.035)
    # capítulo 1
    whoosh(s("s06") - 0.35, 0.3, 0.05)
    text_blips(s("s06"), 11, 26)
    # Turing
    rain_amb(s("s07") - 0.3, s("s08") - 0.2)
    whoosh(w("s07", "Alan") - 0.2, 0.3, 0.05)
    pop_sfx(w("s07", "pregunta") + 0.2, 600)
    text_blips(w("s07", "pueden") - 0.1, 14, 18, 0.02, 1100)
    text_blips(w("s07", "maquinas") - 0.3, 13, 18, 0.02, 1100)
    # imitación
    pop_sfx(w("s08", "juego") - 0.1, 500)
    typewriter(w("s08", "conversas") - 1.0, w("s08", "conversas") - 0.2, 14, 0.035)
    text_blips(w("s08", "conversas") - 0.2, 13, 22, 0.025, 900)
    text_blips(w("s08", "maquina") - 0.1, 10, 20, 0.025, 1400)
    pop_sfx(w("s08", "distinguirla") + 0.3, 650)
    whoosh(w("s08", "importa"), 0.6, 0.05)
    # Dartmouth
    for n in ["McCarthy", "Minsky", "Shannon", "Rochester"]:
        join_jingle(w("s09", n) - 0.1)
    whoosh(w("s09", "firman") - 0.2, 0.5, 0.05)
    for i in range(4):
        tt = w("s09", "firman") + 0.3 + i * 0.45
        n = int(0.5 * SR)
        sig = noise(0.5, 2) * (0.5 + 0.5 * np.sin(np.arange(n) / SR * 2 * np.pi * 7)) * np.sin(np.linspace(0, np.pi, n))
        sfx.add(tt, sig, 0.02)
    coin(w("s10", "primera"), 0.06)
    # pizarrón
    chalk(w("s10", "inteligencia") - 0.05, e("s10") + 0.1)
    join_jingle(e("s10") + 0.15, 0.05)
    # optimismo -> invierno
    for i in range(6):
        pop_sfx(s("s11") + i * 0.1, 600 + i * 90, 0.04)
    for i in range(8):
        blip(w("s11", "Demasiado") + i * 0.09, 600 + i * 120, 0.06, 0.04, 0.25)
    wind(s("s12") - 0.1, TL.s("c2_01"))
    freeze(w("s12", "enterrar"))


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


CARD_IDS = ["s13", "c3_00", "c4_00", "c5_00", "c6_00", "c7_00", "c8_00"]


def card_audio():
    """Sonido genérico de cada placa de capítulo (2..8)."""
    for lid in CARD_IDS:
        if lid not in TL.lines:
            continue
        t0 = TL.s(lid) - 0.3
        whoosh(t0, 0.35, 0.05)
        text_blips(TL.s(lid), 18, 28, 0.018)
        sting(t0 + 0.35, [69, 72, 76, 81], vol=0.05, step=0.11, hold=1.2)
        note(music, t0 + 0.35, midi_hz(45), 2.0, "tri", vol=0.22, s=0.9, r=0.6)


def chapter_hooks():
    """Cada módulo chNN.py puede definir music(A) y sfx(A); A es este módulo."""
    import importlib
    me = sys.modules[__name__]
    for name in ["ch02", "ch03", "ch04", "ch05", "ch06", "ch07", "ch08", "outro"]:
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
    # ducking: la música baja cuando habla el narrador
    env = envelope(vo, 0.08)
    duck = np.clip(env / 0.05, 0, 1)
    duck = movavg(duck, 0.25 * SR)
    m = lowpass(music.buf, 2) * (1 - 0.45 * duck)
    s = sfx.buf * 0.9
    mix = vo * 0.95 + m * 0.6 + s
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
    write_wav(os.path.join(out, "music_stem.wav"), (m * 0.6)[:end])
    write_wav(os.path.join(out, "sfx_stem.wav"), s[:end])
    write_wav(os.path.join(out, "voice_stem.wav"), (vo * 0.95)[:end])
    print("audio ok", round(TL.total, 2), "peak", round(float(peak), 3))


if __name__ == "__main__":
    main()
