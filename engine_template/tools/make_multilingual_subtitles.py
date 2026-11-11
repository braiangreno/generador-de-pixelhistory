"""Genera subtítulos externos .srt en ES, EN y PT (nunca quemados en el video)."""
import json
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
from timeline import TL, TEMPO

_ATEMPO = {}


def _escala(lang, vo_dir, lid):
    """Los tiempos de ElevenLabs son de la voz original; en la mezcla el español va acelerado por TEMPO
    y EN/PT por el atempo que eligió mix_multilingual.py para esa frase. Se corrige para que no se desfasen."""
    if lang == "es":
        return 1.0 / TEMPO
    if vo_dir not in _ATEMPO:
        p = os.path.join(ROOT, vo_dir, "_atempo.json")
        _ATEMPO[vo_dir] = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
    return 1.0 / float(_ATEMPO[vo_dir].get(lid, 1.0) or 1.0)


PLAN_PATH = os.path.join(ROOT, "production_plan.json")
PLAN = json.load(open(PLAN_PATH, encoding="utf-8")) if os.path.exists(PLAN_PATH) else {}
SLUG = re.sub(r"[^A-Za-z0-9_]+", "_", PLAN.get("slug", "Documental_Pixeloide")).strip("_") or "Documental_Pixeloide"


def ts(t):
    ms = int(round(max(0, t) * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def generate_srt(lang, script_file, vo_dir, out_file):
    script_path = os.path.join(ROOT, script_file)
    if not os.path.exists(script_path):
        return
    script = json.load(open(script_path, encoding="utf-8"))
    out, i = [], 1
    for row in script:
        lid = row["id"]
        if lid not in TL.lines:
            continue
        slot_start = TL.s(lid)
        slot_end = TL.e(lid)
        json_path = os.path.join(ROOT, vo_dir, f"{lid}.json")
        al = json.load(open(json_path, encoding="utf-8")) if os.path.exists(json_path) else {}
        chars = al.get("characters", [])
        st = al.get("character_start_times_seconds", [])
        en = al.get("character_end_times_seconds", [])
        k = _escala(lang, vo_dir, lid)
        st = [x * k for x in st]
        en = [x * k for x in en]
        text = row.get("sub") or row.get("speak") or "".join(chars)
        if not chars or not st or not en:
            out.append(f"{i}\n{ts(slot_start)} --> {ts(max(slot_start + 0.5, slot_end))}\n{text}\n")
            i += 1
            continue
        full_c = "".join(chars)
        start = 0
        while start < len(full_c):
            end = min(len(full_c), start + 44)
            if end < len(full_c):
                cut = max(full_c.rfind(p, start, end) for p in ", .:?")
                end = cut + 1 if cut > start + 10 else end
            seg = full_c[start:end].strip()
            if seg:
                t_s = slot_start + st[min(start, len(st) - 1)]
                t_e = slot_start + (st[min(end, len(st) - 1)] - 0.02 if end < len(full_c) else en[min(end - 1, len(en) - 1)] + 0.08)
                out.append(f"{i}\n{ts(t_s)} --> {ts(max(t_s + 0.25, t_e))}\n{seg}\n")
                i += 1
            start = end

    sub_dir = os.path.join(ROOT, "renders", "subtitulos")
    os.makedirs(sub_dir, exist_ok=True)
    out_path = os.path.join(sub_dir, out_file)
    open(out_path, "w", encoding="utf-8").write("\n".join(out))
    alias_path = os.path.join(sub_dir, f"Master_PixelArt_{lang.upper()}.srt")
    if os.path.abspath(out_path) != os.path.abspath(alias_path):
        shutil.copyfile(out_path, alias_path)
    print(f"[{lang.upper()}] Generated {i - 1} subtitles in subtitulos/{out_file}")


if __name__ == "__main__":
    pedidos = [a.lower() for a in sys.argv[1:]] or ["es", "en", "pt"]
    for lg, sc, vd in (
        ("es", "script_full.json", "audio/vo"),
        ("en", "script_full_en.json", "audio/vo_en"),
        ("pt", "script_full_pt.json", "audio/vo_pt"),
    ):
        if lg in pedidos:
            generate_srt(lg, sc, vd, f"{SLUG}_{lg.upper()}.srt")
