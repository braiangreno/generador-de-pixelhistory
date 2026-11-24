"""Línea de tiempo de UN CHICO LLAMADO BARON TRUMP (Stickman Histórico 2D):
arma la locución frase por frase con pausas dramáticas y expone tiempos absolutos de palabras."""
import json
import os
import subprocess
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VO = os.path.join(ROOT, "audio", "vo")
LINES = json.load(open(os.path.join(ROOT, "script_full.json"), encoding="utf-8"))

CARDS = {"c1_00", "c2_00", "c3_00", "c4_00", "c5_00", "c6_00", "c7_00", "c8_00"}

# Pausas ANTES de cada frase (segundos). Incluye los silencios dramáticos de ~1s antes de cada remate en negrita.
GAP_BEFORE = {
    "s01": 0.75,
    "s06": 0.95,   # silencio 1s -> ¿Y si el libro no era una novela? ¿Y si era un mensaje?
    "s07": 0.55,   # Placa título: Esta es la historia de una teoría...
    "c1_06": 0.95, # silencio 1s -> Tres libros olvidados. Hasta que alguien los leyó con los ojos de 2017.
    "c2_08": 0.95, # silencio 1s -> Las coincidencias existen. Pero hubo que ayudarlas un poco.
    "c3_02": 0.45, # entrada a La Pizarra 1 (Paradoja del cumpleaños)
    "c3_07": 0.95, # silencio 1s -> Entre millones de libros, alguno tenía que acertar.
    "c4_08": 0.95, # silencio 1s -> Lo del tío es verdad. La máquina no aparece en ningún papel.
    "c5_07": 0.95, # silencio 1s -> Una casualidad no se comparte. Una conspiración, sí.
    "c6_02": 0.45, # entrada a La Pizarra 2 (Dilatación del tiempo)
    "c6_07": 0.95, # silencio 1s -> Todos viajamos al futuro. A un segundo por segundo.
    "c7_02": 0.45, # entrada a La Pizarra 3 (Paradoja del abuelo)
    "c7_05": 0.55, # rebobinado a Cambridge, 28 de junio de 2009
    "c7_08": 0.95, # silencio 1s -> Si se pudiera viajar al pasado, esa fiesta estaría llena.
    "c8_07": 0.95, # silencio 1s -> Si algún día alguien viaja al pasado, ya sabe dónde lo espera una fiesta.
    "c8_08": 0.95, # CTA comentarios antes del cierre oficial de Pixeloide Studios
}

TEMPO = 1.04
GAP_CARD = 0.85     # antes de cada placa de capítulo (c1_00..c8_00)
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
        return int(lid[1:].split("_")[0])
    return 0


class Timeline:
    def __init__(self):
        os.makedirs(VO, exist_ok=True)
        cache = os.path.join(VO, "_durations.json")
        durs = json.load(open(cache)) if os.path.exists(cache) else {}
        changed = False
        self.lines = {}
        self.order = []
        self.chapters = [1, 2, 3, 4, 5, 6, 7, 8]
        t = 0.0
        prev = None
        for ln in LINES:
            lid = ln["id"]
            mp3 = os.path.join(VO, f"{lid}.mp3")
            js_file = os.path.join(VO, f"{lid}.json")
            if os.path.exists(mp3):
                key = f"{lid}:{os.path.getmtime(mp3):.0f}"
                if key not in durs:
                    durs[key] = _dur(mp3)
                    changed = True
                d = durs[key] / TEMPO
            else:
                cand = [v for k, v in durs.items() if k == lid or k.startswith(f"{lid}:")]
                if cand:
                    d = cand[-1] / TEMPO
                elif os.path.exists(js_file):
                    al_tmp = json.load(open(js_file, encoding="utf-8"))
                    ends = al_tmp.get("character_end_times_seconds") or [3.0]
                    d = (ends[-1] + 0.15) / TEMPO
                else:
                    continue
            if lid in CARDS:
                gap = GAP_CARD
            elif prev in CARDS:
                gap = GAP_AFTER_CARD
            else:
                gap = GAP_BEFORE.get(lid, DEFAULT_GAP)
            t += gap
            al = json.load(open(js_file, encoding="utf-8")) if os.path.exists(js_file) else {
                "characters": list(ln["speak"]),
                "character_start_times_seconds": [i * (d * TEMPO / max(1, len(ln["speak"]))) for i in range(len(ln["speak"]))],
                "character_end_times_seconds": [(i + 1) * (d * TEMPO / max(1, len(ln["speak"]))) for i in range(len(ln["speak"]))],
            }
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

    start = s
    end = e

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
        for lid in self.order:
            if self.lines[lid]["chapter"] == ch:
                return self.lines[lid]["start"]
        return 0.0

    def chapter_end(self, ch):
        end = 0.0
        for lid in self.order:
            if self.lines[lid]["chapter"] == ch:
                end = self.lines[lid]["end"]
        return end


TL = Timeline()

if __name__ == "__main__":
    for lid in TL.order:
        L = TL.lines[lid]
        print(f"{lid:6s}  {L['start']:6.2f} -> {L['end']:6.2f} ({L['dur']:4.2f}s)  {L['text'][:65]}")
    print(f"TOTAL: {TL.total:.2f}s ({TL.total/60:.2f} min)")
