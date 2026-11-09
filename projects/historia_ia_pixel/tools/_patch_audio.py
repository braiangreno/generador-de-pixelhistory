import os, re
os.chdir(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "engine"))
a = open('audio.py', encoding='utf-8', newline='').read().replace('\r\n', '\n')
a = a.replace('    beat = 60.0 / bpm\n', '    beat = 60.0 / (bpm * BPM_MUL)\n', 1)
a = a.replace('def section(t0, t1, bpm, chords, style, beats_per_chord=4):',
              'BPM_MUL = 1.12  # todo un poco más rápido (ritmo)\n\n\ndef section(t0, t1, bpm, chords, style, beats_per_chord=4):', 1)
a = a.replace('''    sting(c_ch2 + 0.45, [64, 63, 59, 57], vol=0.05, step=0.22, hold=2.0)
    section(c_ch2 + 1.5, TL.total - 0.2, 70, [("A", "min"), ("D", "min")], st_winter)
''', '')
a = a.replace('    wind(s("s12") - 0.1, TL.total)\n', '    wind(s("s12") - 0.1, TL.s("c2_01"))\n')
a = a.replace('''    whoosh(s("s13") - 0.6, 0.4, 0.05)
    text_blips(s("s13"), 20, 26, 0.018)
''', '')
a = a.replace('''def main():
    compose()
    design_sfx()
''', '''CARD_IDS = ["s13", "c3_00", "c4_00", "c5_00", "c6_00", "c7_00", "c8_00"]


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
    for name in ["ch02", "ch03", "ch04", "ch05", "ch06", "ch07", "ch08"]:
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
''')
open('audio.py', 'w', encoding='utf-8', newline='').write(a)
print('BPM_MUL' in a, 'chapter_hooks' in a, 'TL.total - 0.2, 70' in a)
