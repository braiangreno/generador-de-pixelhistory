"""Banda sonora chiptune original + efectos de sonido + mezcla con la locución
para EL EMPLEADO NÚMERO CERO (La historia de Apple y Steve Jobs)."""
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


def env_adsr(n, a=0.005, d=0.08, s=0.6, r=0.06):
    e = np.ones(n) * s
    na, nd, nr = int(a * SR), int(d * SR), int(r * SR)
    na = min(na, n)
    if na:
        e[:na] = np.linspace(0, 1, na, endpoint=False)
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
    return np.round(v * 8) / 8


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
            sig = sig[-i:]
            i = 0
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


BPM_MUL = 0.94


def section(t0, t1, bpm, chords, style, beats_per_chord=4):
    beat = 60.0 / (bpm * BPM_MUL)
    nb = int((t1 - t0) / beat)
    for b in range(nb):
        tb = t0 + b * beat
        ci = (b // beats_per_chord) % len(chords)
        root, kind = chords[ci]
        notes = chord_notes(root, kind, 3)
        first = b % beats_per_chord == 0
        fade = min(1.0, (t1 - tb) / 0.8)
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


def tictac(t, count=4, reverse=False, vol=0.05):
    """Sonido firma del episodio: tic-tac de reloj de bolsillo (normal o invertido)."""
    for k in range(count):
        f = (920 if k % 2 == 0 else 1280) if reverse else (1280 if k % 2 == 0 else 920)
        d = 0.035
        n = int(d * SR)
        tt = np.arange(n) / SR
        sig = np.sin(2 * np.pi * f * tt) * (np.exp((tt - d) * 45) if reverse else np.exp(-tt * 65))
        sfx.add(t + k * 0.28, sig, vol)


def coil_hum(t0, t1, vol=0.035):
    """Zumbido eléctrico de bobina de Tesla que se apaga al final."""
    dur = max(0.2, t1 - t0)
    n = int(dur * SR)
    tt = np.arange(n) / SR
    sig = (np.sin(2 * np.pi * 120 * tt) * 0.6 + np.sin(2 * np.pi * 240 * tt) * 0.3) * env_adsr(n, 0.2, 0.2, 0.8, 0.6)
    sfx.add(t0, sig, vol)


def rewind_sfx(t, dur=0.85, vol=0.06):
    """Efecto de cinta rebobinando al revés (Cap 7 hacia la fiesta de Hawking)."""
    n = int(dur * SR)
    tt = np.arange(n) / SR
    f = 420 + 1400 * (tt / dur) ** 1.5
    ph = np.cumsum(f) / SR
    sig = np.sin(2 * np.pi * ph) * np.sin(np.linspace(0, np.pi, n)) * (0.6 + 0.4 * np.sin(2 * np.pi * 28 * tt))
    sfx.add(t, sig, vol)


def compose():
    # Acto 1 (Apertura + Caps 1, 2): Caja de música / misterio de época siglo XIX
    section(0.0, TL.s("s06"), 88, [("D", "m"), ("Bb", "M"), ("F", "M"), ("A", "m")], st_mystery)
    section(TL.s("s07"), TL.s("c1_00"), 96, [("D", "m"), ("G", "m"), ("Bb", "M"), ("A", "M")], st_build)
    section(TL.s("c1_00"), TL.s("c2_00"), 92, [("D", "m"), ("F", "M"), ("C", "M"), ("A", "m")], st_mystery)
    section(TL.s("c2_00"), TL.s("c3_00"), 98, [("A", "m"), ("F", "M"), ("D", "m"), ("E", "M")], st_build)

    # Cap 3: La Pizarra 1 (Paradoja del cumpleaños y Ley de los Números Grandes)
    section(TL.s("c3_00"), TL.s("c4_00"), 104, [("C", "M"), ("G", "M"), ("A", "m"), ("F", "M")], st_puzzle)

    # Acto 2 (Caps 4, 5): Misterio eléctrico años 40 + foros 2017
    section(TL.s("c4_00"), TL.s("c5_00"), 90, [("E", "m"), ("C", "M"), ("A", "m"), ("B", "m")], st_winter)
    section(TL.s("c5_00"), TL.s("c6_00"), 98, [("A", "m"), ("F", "M"), ("C", "M"), ("G", "M")], st_build)

    # Acto 3 (Caps 6, 7): Electrónica espacial tranquila + Pizarras 2 y 3
    section(TL.s("c6_00"), TL.s("c6_02"), 86, [("C", "M"), ("A", "m"), ("F", "M"), ("G", "M")], st_winter)
    section(TL.s("c6_02"), TL.s("c7_00"), 104, [("C", "M"), ("G", "M"), ("A", "m"), ("F", "M")], st_puzzle)
    section(TL.s("c7_00"), TL.s("c7_05"), 102, [("A", "m"), ("F", "M"), ("C", "M"), ("G", "M")], st_puzzle)
    section(TL.s("c7_05"), TL.s("c8_00"), 90, [("D", "m"), ("Bb", "M"), ("F", "M"), ("A", "m")], st_rain)

    # Cap 8: Regreso a la biblioteca (vuelve el tema; corta antes del remate c8_07)
    section(TL.s("c8_00"), TL.s("c8_07") - 0.8, 92, [("D", "m"), ("Bb", "M"), ("F", "M"), ("A", "m")], st_mystery)
    section(TL.s("c8_08"), TL.e("c8_08") + 0.5, 98, [("C", "M"), ("G", "M"), ("A", "m"), ("F", "M")], st_bright)


def design_sfx():
    # Apertura: tic-tac en biblioteca + tic-tac invertido en s06
    tictac(TL.s("s01") + 0.3, count=5, reverse=False, vol=0.045)
    tictac(TL.s("s06") - 0.7, count=4, reverse=True, vol=0.065)

    # Cap 2: hilos cortándose en c2_08
    stamp_hit(TL.s("c2_03") + 0.6, vol=0.055)
    whoosh(TL.s("c2_08") - 0.3, 0.35, 0.05)

    # Cap 3: tiza en La Pizarra 1
    chalk(TL.s("c3_01"), TL.s("c3_01") + 1.4, vol=0.025)
    chalk(TL.s("c3_03"), TL.s("c3_03") + 1.4, vol=0.025)
    chalk(TL.s("c3_06"), TL.s("c3_06") + 1.2, vol=0.025)

    # Cap 4: zumbido eléctrico de bobina de Tesla que se apaga en c4_08
    coil_hum(TL.s("c4_01"), TL.s("c4_03"), vol=0.032)
    coil_hum(TL.s("c4_07"), TL.s("c4_08"), vol=0.036)
    stamp_hit(TL.s("c4_05") + 0.5, vol=0.065)

    # Cap 5: sellos de verificado/falso en Snopes
    coin(TL.s("c5_05") + 0.5, vol=0.045)
    stamp_hit(TL.s("c5_05") + 1.6, vol=0.060)

    # Cap 6: tiza en La Pizarra 2 (Dilatación del tiempo)
    chalk(TL.s("c6_02"), TL.s("c6_02") + 1.4, vol=0.025)
    chalk(TL.s("c6_04"), TL.s("c6_04") + 1.2, vol=0.025)

    # Cap 7: tiza en La Pizarra 3 + rebobinado hacia Cambridge 2009
    chalk(TL.s("c7_01"), TL.s("c7_01") + 1.2, vol=0.025)
    rewind_sfx(TL.s("c7_05") - 0.55, dur=0.85, vol=0.068)

    # Cap 8: tic-tac invertido en c8_05 + jingle suave en CTA
    tictac(TL.s("c8_05") + 0.2, count=5, reverse=True, vol=0.058)
    join_jingle(TL.s("c8_08") + 0.4, vol=0.042)


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


CARD_IDS = ["c1_00", "c2_00", "c3_00", "c4_00", "c5_00", "c6_00", "c7_00", "c8_00"]


def card_audio():
    for lid in CARD_IDS:
        if lid not in TL.lines:
            continue
        t0 = TL.s(lid) - 0.15
        tictac(t0, count=2, reverse=True, vol=0.048)
        sting(t0 + 0.20, [57, 64, 69, 76], vol=0.038, step=0.12, hold=1.1)
        note(music, t0 + 0.20, midi_hz(45), 1.6, "tri", vol=0.14, a=0.04, s=0.85, r=0.5)


def chapter_hooks():
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
    m_warm = lowpass(lowpass(music.buf, 8), 5)
    s_warm = lowpass(sfx.buf, 2)

    env = envelope(vo, 0.08)
    duck = np.clip(env / 0.04, 0, 1)
    duck = movavg(duck, 0.32 * SR)

    m_ducked = m_warm * (1.0 - 0.70 * duck) * 0.36
    s_ducked = s_warm * (1.0 - 0.38 * duck) * 0.68
    mix = vo * 0.98 + m_ducked + s_ducked
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
