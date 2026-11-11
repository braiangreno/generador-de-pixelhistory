"""Línea de tiempo dinámica del motor Pixeloide: arma la locución frase por frase
y expone tiempos absolutos de palabras (alineación ElevenLabs)."""
import json
import os
import re
import subprocess
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VO = os.path.join(ROOT, "audio", "vo")
SCRIPT_PATH = os.path.join(ROOT, "script_full.json")
LINES = json.load(open(SCRIPT_PATH, encoding="utf-8")) if os.path.exists(SCRIPT_PATH) else []

# Detecta automáticamente todas las placas de capítulo (c1_00, c2_00, ..., cN_00)
CARDS = {ln["id"] for ln in LINES if re.match(r"^c\d+_00$", ln.get("id", ""))}

# Pausas personalizadas antes de cada frase (pueden venir en cada item del JSON como "gap_before" o "pause")
GAP_BEFORE = {
    "s01": 0.8,
}
for ln in LINES:
    lid = ln.get("id", "")
    if "gap_before" in ln:
        GAP_BEFORE[lid] = float(ln["gap_before"])

TEMPO = float(os.environ.get("PX_TEMPO", "1.06"))
# PX_STRICT_WORDS=1 (lo usa scripts/producir.py en las hojas de revisión): si TL.word() no encuentra la
# palabra, falla con un error claro en vez de caer en silencio a la mitad de la frase.
STRICT_WORDS = os.environ.get("PX_STRICT_WORDS") == "1"
GAP_CARD = 0.8      # antes de cada placa de capítulo
GAP_AFTER_CARD = 0.3
DEFAULT_GAP = 0.18
TAIL = 12.0         # espacio reservado para el cierre oficial de Pixeloide Studios (outro.py)


def _dur(path):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                   "-of", "csv=p=0", path])
    return float(out.decode().strip())


def _norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def chapter_of(lid):
    m = re.match(r"^c(\d+)_", lid)
    if m:
        return int(m.group(1))
    return 0


class Timeline:
    def __init__(self):
        os.makedirs(VO, exist_ok=True)
        cache = os.path.join(VO, "_durations.json")
        durs = json.load(open(cache)) if os.path.exists(cache) else {}
        changed = False
        self.lines = {}
        self.order = []
        self.chapters = sorted({chapter_of(ln["id"]) for ln in LINES if chapter_of(ln["id"]) > 0})
        t = 0.0
        prev = None
        prev_pause = None
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
            elif lid in GAP_BEFORE:
                gap = GAP_BEFORE[lid]
            elif prev_pause is not None:
                gap = float(prev_pause)
            else:
                gap = DEFAULT_GAP
            t += gap
            al_path = os.path.join(VO, f"{lid}.json")
            if os.path.exists(al_path):
                al = json.load(open(al_path, encoding="utf-8")) or {}
            else:
                al = {}
            chars = al.get("characters") or list(ln.get("speak", ""))
            n_ch = max(1, len(chars))
            st_arr = al.get("character_start_times_seconds") or [i * (d * TEMPO) / n_ch for i in range(n_ch)]
            en_arr = al.get("character_end_times_seconds") or [(i + 1) * (d * TEMPO) / n_ch for i in range(n_ch)]
            al_norm = {
                "characters": chars,
                "character_start_times_seconds": [v / TEMPO for v in st_arr],
                "character_end_times_seconds": [v / TEMPO for v in en_arr],
            }
            ch_num = ln.get("ch", chapter_of(lid))
            self.lines[lid] = dict(
                start=t,
                end=t + d,
                dur=d,
                text=ln.get("speak", ""),
                sub=ln.get("sub", ln.get("speak", "")),
                align=al_norm,
                chapter=ch_num,
            )
            self.order.append(lid)
            t += d
            prev = lid
            prev_pause = ln.get("pause", None)
        self.total = max(15.0, t + TAIL)
        if changed:
            json.dump(durs, open(cache, "w"))

    def s(self, lid):
        if lid in self.lines:
            return self.lines[lid]["start"]
        return 0.0

    def e(self, lid):
        if lid in self.lines:
            return self.lines[lid]["end"]
        return max(0.0, self.total - TAIL)

    def word(self, lid, needle, occurrence=1, end=False):
        """Tiempo absoluto en que se pronuncia `needle` dentro de la frase `lid`.
        Si no encuentra la palabra exacta, interpola suavemente dentro de la frase."""
        if lid not in self.lines:
            return 0.0
        L = self.lines[lid]
        chars = L["align"]["characters"]
        text = _norm("".join(chars))
        n = _norm(needle)
        idx = -1
        for _ in range(occurrence):
            idx = text.find(n, idx + 1)
        if idx < 0:
            if STRICT_WORDS:
                raise KeyError(f"TL.word: no encuentro {needle!r} (vez {occurrence}) en {lid}: "
                               f"{''.join(chars)[:90]!r}")
            # Fallback seguro a la mitad de la línea para que nunca falle un render automático
            return L["start"] + L["dur"] * (0.65 if end else 0.35)
        if end:
            j = min(len(chars) - 1, idx + len(n) - 1)
            return L["start"] + L["align"]["character_end_times_seconds"][j]
        return L["start"] + L["align"]["character_start_times_seconds"][idx]

    def chapter_start(self, ch):
        """Inicio (s) del capítulo ch (1..N); ch 0 = 0."""
        if ch <= 0:
            return 0.0
        card_id = f"c{ch}_00"
        if card_id in self.lines:
            return self.s(card_id)
        for lid in self.order:
            if self.lines[lid]["chapter"] == ch:
                return self.s(lid)
        return max(0.0, self.total - TAIL)

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
