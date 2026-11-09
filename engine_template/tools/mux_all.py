"""Muxing de los masters en Español, Inglés y Portugués (-14 LUFS, sin subtítulos quemados)."""
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAN_PATH = os.path.join(ROOT, "production_plan.json")
PLAN = json.load(open(PLAN_PATH, encoding="utf-8")) if os.path.exists(PLAN_PATH) else {}
SLUG = re.sub(r"[^A-Za-z0-9_]+", "_", PLAN.get("slug", "Documental_Pixeloide")).strip("_") or "Documental_Pixeloide"

LANGS = [
    {
        "code": "ES",
        "video": os.path.join(ROOT, "renders", "video_mudo.mp4"),
        "audio": os.path.join(ROOT, "audio", "mix.wav"),
        "output": os.path.join(ROOT, "renders", f"{SLUG}_ES.mp4"),
        "alias": os.path.join(ROOT, "renders", "Master_PixelArt_ES.mp4"),
    },
    {
        "code": "EN",
        "video": os.path.join(ROOT, "renders", "video_mudo_en.mp4"),
        "audio": os.path.join(ROOT, "audio", "mix_en.wav"),
        "output": os.path.join(ROOT, "renders", f"{SLUG}_EN.mp4"),
        "alias": os.path.join(ROOT, "renders", "Master_PixelArt_EN.mp4"),
    },
    {
        "code": "PT",
        "video": os.path.join(ROOT, "renders", "video_mudo_pt.mp4"),
        "audio": os.path.join(ROOT, "audio", "mix_pt.wav"),
        "output": os.path.join(ROOT, "renders", f"{SLUG}_PT.mp4"),
        "alias": os.path.join(ROOT, "renders", "Master_PixelArt_PT.mp4"),
    },
]


def main():
    os.makedirs(os.path.join(ROOT, "renders"), exist_ok=True)
    for item in LANGS:
        vpath = item["video"]
        apath = item["audio"]
        if not os.path.isfile(vpath) or not os.path.isfile(apath):
            print(f"Skipping {item['code']}: missing video or audio", file=sys.stderr)
            continue
        print(f"=== MUXING {item['code']} ({os.path.basename(vpath)}) ===")
        cmd = [
            "ffmpeg", "-y", "-loglevel", "error",
            "-i", vpath,
            "-i", apath,
            "-map", "0:v",
            "-map", "1:a",
            "-c:v", "copy",
            "-af", "loudnorm=I=-14:TP=-1.0:LRA=11",
            "-ar", "48000",
            "-c:a", "aac",
            "-b:a", "256k",
            "-shortest",
            "-movflags", "+faststart",
            item["output"],
        ]
        subprocess.check_call(cmd)
        if os.path.abspath(item["output"]) != os.path.abspath(item["alias"]):
            shutil.copyfile(item["output"], item["alias"])
        print(f"Created: {item['output']}")


if __name__ == "__main__":
    main()
