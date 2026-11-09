import json, os, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def ts(t):
    ms = int(round(max(0, t) * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def generate_srt(lang, script_file, vo_dir, out_file):
    import sys
    sys.path.insert(0, os.path.join(ROOT, "engine"))
    from timeline import TL
    
    script = json.load(open(os.path.join(ROOT, script_file), encoding="utf-8"))
    out, i = [], 1
    for row in script:
        lid = row["id"]
        if lid not in TL.lines:
            continue
        json_path = os.path.join(ROOT, vo_dir, f"{lid}.json")
        if not os.path.exists(json_path):
            continue
        al = json.load(open(json_path, encoding="utf-8"))
        chars = al.get("characters", [])
        st = al.get("character_start_times_seconds", [])
        en = al.get("character_end_times_seconds", [])
        if not chars or not st or not en:
            continue
        text = "".join(chars)
        # determine scaling if audio was slightly compressed
        # in timeline, Spanish line slot starts at TL.s(lid)
        slot_start = TL.s(lid)
        start = 0
        while start < len(text):
            end = min(len(text), start + 42)
            if end < len(text):
                cut = max(text.rfind(p, start, end) for p in ", .:?")
                end = cut + 1 if cut > start + 10 else end
            seg = text[start:end].strip()
            if seg:
                t_s = slot_start + st[start]
                t_e = slot_start + (st[end] - 0.02 if end < len(text) else en[end - 1] + 0.08)
                out.append(f"{i}\n{ts(t_s)} --> {ts(max(t_s + 0.2, t_e))}\n{seg}\n")
                i += 1
            start = end
            
    srt_text = "\n".join(out)
    out_path = os.path.join(ROOT, "renders", out_file)
    open(out_path, "w", encoding="utf-8").write(srt_text)
    print(f"[{lang.upper()}] Generated {i-1} subtitles in {out_file}")

if __name__ == "__main__":
    import shutil
    for lg, sc, vd in (
        ("es", "script_full.json", "audio/vo"),
        ("en", "script_full_en.json", "audio/vo_en"),
        ("pt", "script_full_pt.json", "audio/vo_pt"),
    ):
        main_srt = f"Historia_Videojuegos_PixelArt_{lg.upper()}.srt"
        generate_srt(lg, sc, vd, main_srt)
        src = os.path.join(ROOT, "renders", main_srt)
        for alias in (
            f"Para_Que_No_Se_Aburran_{lg.upper()}.srt",
            f"Para_Que_No_Se_Aburrieran_{lg.upper()}.srt",
        ):
            shutil.copyfile(src, os.path.join(ROOT, "renders", alias))
