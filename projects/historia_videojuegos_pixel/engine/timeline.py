"""Línea de tiempo del video completo: arma la locución frase por frase con pausas
cortas (ritmo ágil) y expone tiempos absolutos de palabras (alineación ElevenLabs)."""
import json
import os
import subprocess
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VO = os.path.join(ROOT, "audio", "vo")
LINES = json.load(open(os.path.join(ROOT, "script_full.json"), encoding="utf-8"))

CARDS = {"c1_00", "c2_00", "c3_00", "c4_00", "c5_00", "c6_00", "c7_00", "c8_00"}
# pausas ANTES de cada frase (segundos). Por defecto: 0.20 s (ritmo documental con silencios en remates)
GAP_BEFORE = {
    "s01": 0.8,
    "s03": 0.3,
    "s05": 0.65,   # remate: Él nunca lo patenta
    "s06": 1.0,    # silencio de 1s tras el remate
    "s08": 0.45,
    "c1_05": 0.7,  # remate: Pero la idea ya estaba suelta
    "c2_06": 0.55, # remate: Estaba llena de monedas
    "c2_07": 0.65, # Se llamaba Pong
    "c3_03": 0.55, # Y entonces, todo se vino abajo
    "c3_07": 0.75, # remate: Y que se había terminado
    "c4_00": 1.5,  # silencio de 1.5s tras el entierro en el desierto
    "c4_03": 0.55, # remate: Vendió un juguete
    "c5_06": 0.65, # remate: Y había ganado un rival
    "c6_05": 0.75, # remate: Recuerda ese nombre. Va a volver
    "c7_06": 0.55, # remate: Ninguna película...
    "c8_08": 0.65, # Todo empezó con un punto de luz...
    "c8_09": 0.9,  # remate final: Y el próximo capítulo de esta historia... está por empezar
}
# aceleración extra aplicada a la voz (atempo, conserva el tono)
TEMPO = 1.06
GAP_CARD = 0.8      # antes de cada placa de capítulo
GAP_AFTER_CARD = 0.3
DEFAULT_GAP = 0.18
TAIL = 12.0


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
        cache = os.path.join(VO, "_durations.json")
        durs = json.load(open(cache)) if os.path.exists(cache) else {}
        changed = False
        self.lines = {}
        self.order = []
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
            self.lines[lid] = dict(start=t, end=t + d, dur=d, text=ln["speak"], align=al, chapter=chapter_of(lid))
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
        """Tiempo absoluto en que se pronuncia `needle` dentro de la frase `lid`."""
        L = self.lines[lid]
        chars = L["align"]["characters"]
        text = _norm("".join(chars))
        n = _norm(needle)
        idx = -1
        for _ in range(occurrence):
            idx = text.find(n, idx + 1)
        if idx < 0:
            raise KeyError(f"{needle!r} not in {lid}: {text}")
        if end:
            j = min(len(chars) - 1, idx + len(n) - 1)
            return L["start"] + L["align"]["character_end_times_seconds"][j]
        return L["start"] + L["align"]["character_start_times_seconds"][idx]

    def chapter_start(self, ch):
        """Inicio (s) de la placa del capítulo ch (1..8); ch 0 = 0."""
        card = {1: "c1_00", 2: "c2_00", 3: "c3_00", 4: "c4_00", 5: "c5_00", 6: "c6_00", 7: "c7_00", 8: "c8_00"}
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
