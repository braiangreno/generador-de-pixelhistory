"""Línea de tiempo de UN CABALLO EN EL AIRE (La historia del cine):
arma la locución frase por frase con pausas dramáticas y expone tiempos absolutos de palabras."""
import json
import os
import subprocess
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VO = os.path.join(ROOT, "audio", "vo")
LINES = json.load(open(os.path.join(ROOT, "script_full.json"), encoding="utf-8"))

CARDS = {"c1_00", "c2_00", "c3_00", "c4_00", "c5_00", "c6_00", "c7_00"}

# Pausas ANTES de cada frase (segundos). Incluye los silencios dramáticos antes de cada remate del guion.
GAP_BEFORE = {
    "s01": 0.75,
    "s04": 0.70,   # La respuesta fue sí. Y sin buscarlo, abrió la puerta al cine.
    "s05": 0.65,   # Esta es la historia del cine...
    "c1_06": 0.45, # entrada a La Pizarra 1 (El cerebro rellena los huecos)
    "c1_08": 0.90, # silencio -> Ya había movimiento. Faltaba mostrarlo a una sala llena.
    "c2_09": 0.90, # silencio -> Treinta y tres espectadores. El público más chico... y el primero.
    "c3_10": 0.90, # silencio -> Los Lumière filmaron la realidad. Méliès filmó los sueños. El cine necesitó a los dos.
    "c4_06": 0.90, # silencio -> Hollywood no nació por los abogados. Nació por la luz.
    "c5_03": 0.45, # entrada a La Pizarra 2 (Dónde iba el sonido + 24 fps)
    "c5_07": 0.90, # silencio -> Las veinticuatro imágenes por segundo se eligieron para que la voz no desafinara.
    "c6_02": 0.45, # entrada a La Pizarra 3 (Tres colores RGB y Technicolor)
    "c6_08": 0.90, # silencio -> Cada vez que apareció una pantalla rival, el cine se hizo más grande.
    "c7_06": 0.95, # silencio -> El cine sigue siendo un caballo que, por un instante, vuela.
    "c7_07": 0.95, # invitación a comentar el próximo episodio antes del cierre de Pixeloide
}

TEMPO = 1.04
GAP_CARD = 0.85     # antes de cada placa de capítulo (c1_00..c7_00)
GAP_AFTER_CARD = 0.35
DEFAULT_GAP = 0.20
TAIL = 12.0         # espacio reservado para el cierre oficial de Pixeloide Studios (outro.py)


def _dur(path):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                   "-of", "csv=p=0", path])
    return float(out.decode().strip())


def _norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def chapter_of(lid):
    if lid.startswith("c"):
        return int(lid[1])
    return 0


class Timeline:
    def __init__(self):
        os.makedirs(VO, exist_ok=True)
        cache = os.path.join(VO, "_durations.json")
        durs = json.load(open(cache)) if os.path.exists(cache) else {}
        changed = False
        self.lines = {}
        self.order = []
        self.chapters = [1, 2, 3, 4, 5, 6, 7]
        t = 0.0
        prev = None
        for ln in LINES:
            lid = ln["id"]
            mp3 = os.path.join(VO, f"{lid}.mp3")
            if not os.path.exists(mp3):
                continue
            key = f"{lid}:{os.path.getmtime(mp3):.0f}"
            if key not in durs:
                durs[key] = _dur(mp3)
                changed = True
            d = durs[key] / TEMPO
            if lid in CARDS:
                gap = GAP_CARD
            elif prev in CARDS:
                gap = GAP_AFTER_CARD
            else:
                gap = GAP_BEFORE.get(lid, DEFAULT_GAP)
            t += gap
            al = json.load(open(os.path.join(VO, f"{lid}.json"), encoding="utf-8"))
            for k in ("character_start_times_seconds", "character_end_times_seconds"):
                al[k] = [v / TEMPO for v in al[k]]
            self.lines[lid] = dict(start=t, end=t + d, dur=d, text=ln["speak"], sub=ln.get("sub", ln["speak"]),
                                   align=al, chapter=chapter_of(lid))
            self.order.append(lid)
            t += d
            prev = lid
        self.total = t + TAIL
        if changed:
            json.dump(durs, open(cache, "w"))

    def s(self, lid):
        return self.lines[lid]["start"]

    def e(self, lid):
        return self.lines[lid]["end"]

    def word(self, lid, needle, occurrence=1, end=False):
        L = self.lines[lid]
        chars = L["align"]["characters"]
        text = _norm("".join(chars))
        n = _norm(needle)
        idx = -1
        for _ in range(occurrence):
            idx = text.find(n, idx + 1)
        if idx < 0:
            return L["start"] + L["dur"] * (0.65 if end else 0.35)
        if end:
            j = min(len(chars) - 1, idx + len(n) - 1)
            return L["start"] + L["align"]["character_end_times_seconds"][j]
        return L["start"] + L["align"]["character_start_times_seconds"][idx]

    def chapter_start(self, ch):
        card = {1: "c1_00", 2: "c2_00", 3: "c3_00", 4: "c4_00", 5: "c5_00", 6: "c6_00", 7: "c7_00"}
        return 0.0 if ch == 0 else self.s(card[ch])

    def speaking(self, t):
        for lid, L in self.lines.items():
            if L["start"] <= t <= L["end"]:
                return lid
        return None


TL = Timeline()

if __name__ == "__main__":
    for lid in TL.order:
        L = TL.lines[lid]
        print(f"{lid:6s} {L['start']:7.2f} -> {L['end']:7.2f}  {L['text'][:60]}")
    print("total", round(TL.total, 2))
