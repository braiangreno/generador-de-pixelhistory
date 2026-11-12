"""Muxing de los masters 1080p en Español, Inglés y Portugués para Nikola Tesla (sin subtítulos pegados)
+ generación de archivos .srt independientes en renders/subtitulos/.
"""
import json
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
from timeline import TL

LANGS = [
    {
        "code": "ES",
        "script": "script_full.json",
        "video": os.path.join(ROOT, "renders", "video_mudo.mp4"),
        "audio": os.path.join(ROOT, "audio", "mix.wav"),
        "output": os.path.join(ROOT, "renders", "Historia_Tesla_PixelArt_ES.mp4"),
        "copies": [
            os.path.join(ROOT, "renders", "El_Dibujo_Que_Encendio_El_Mundo_ES.mp4"),
        ],
    },
    {
        "code": "EN",
        "script": "script_full_en.json",
        "video": os.path.join(ROOT, "renders", "video_mudo_en.mp4"),
        "audio": os.path.join(ROOT, "audio", "mix_en.wav"),
        "output": os.path.join(ROOT, "renders", "Historia_Tesla_PixelArt_EN.mp4"),
        "copies": [
            os.path.join(ROOT, "renders", "El_Dibujo_Que_Encendio_El_Mundo_EN.mp4"),
            os.path.join(ROOT, "renders", "The_Drawing_That_Lit_Up_The_World_EN.mp4"),
        ],
    },
    {
        "code": "PT",
        "script": "script_full_pt.json",
        "video": os.path.join(ROOT, "renders", "video_mudo_pt.mp4"),
        "audio": os.path.join(ROOT, "audio", "mix_pt.wav"),
        "output": os.path.join(ROOT, "renders", "Historia_Tesla_PixelArt_PT.mp4"),
        "copies": [
            os.path.join(ROOT, "renders", "El_Dibujo_Que_Encendio_El_Mundo_PT.mp4"),
            os.path.join(ROOT, "renders", "O_Desenho_Que_Acendeu_O_Mundo_PT.mp4"),
        ],
    },
]


def _fmt_srt(sec):
    ms = int(round(max(0.0, sec) * 1000))
    hh = ms // 3600000
    mm = (ms % 3600000) // 60000
    ss = (ms % 60000) // 1000
    rem = ms % 1000
    return f"{hh:02d}:{mm:02d}:{ss:02d},{rem:03d}"


def build_srt(script_name, out_paths):
    data = json.load(open(os.path.join(ROOT, script_name), encoding="utf-8"))
    blocks = []
    for idx, item in enumerate(data, 1):
        lid = item["id"]
        st = TL.s(lid)
        en = TL.e(lid)
        txt = item.get("sub") or item.get("text") or item.get("speak") or ""
        blocks.append(f"{idx}\n{_fmt_srt(st)} --> {_fmt_srt(en)}\n{txt}\n")
    content = "\n".join(blocks)
    subs_dir = os.path.join(ROOT, "renders", "subtitulos")
    os.makedirs(subs_dir, exist_ok=True)
    for p in out_paths:
        with open(os.path.join(subs_dir, p), "w", encoding="utf-8") as f:
            f.write(content)


def main():
    for item in LANGS:
        code = item["code"]
        build_srt(
            item["script"],
            [
                f"Historia_Tesla_PixelArt_{code}.srt",
                f"El_Dibujo_Que_Encendio_El_Mundo_{code}.srt",
            ],
        )
        vpath = item["video"]
        if not os.path.isfile(vpath):
            print(f"Skipping {code}: {vpath} not found!", file=sys.stderr)
            continue
        print(f"=== MUXING {code} ({os.path.basename(vpath)}) ===")
        cmd = [
            "ffmpeg", "-y", "-loglevel", "error",
            "-i", vpath,
            "-i", item["audio"],
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
        print(f"Created: {item['output']} ({os.path.getsize(item['output']) / (1024 * 1024):.1f} MB)")
        for cp in item["copies"]:
            shutil.copyfile(item["output"], cp)
            print(f"Copied to: {cp}")


if __name__ == "__main__":
    main()
