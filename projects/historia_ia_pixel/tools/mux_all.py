"""Muxing de los masters en Espanol, Ingles y Portugues."""
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDEO = os.path.join(ROOT, "renders", "video_mudo.mp4")

LANGS = [
    {
        "code": "ES",
        "video": os.path.join(ROOT, "renders", "video_mudo.mp4"),
        "audio": os.path.join(ROOT, "audio", "mix.wav"),
        "output": os.path.join(ROOT, "renders", "Historia_IA_PixelArt_ES.mp4"),
        "copies": [
            os.path.join(ROOT, "renders", "Historia_IA_PixelArt_Completo.mp4"),
            os.path.join(ROOT, "renders", "Piloto_Historia_IA_PixelArt.mp4")
        ]
    },
    {
        "code": "EN",
        "video": os.path.join(ROOT, "renders", "video_mudo_en.mp4"),
        "audio": os.path.join(ROOT, "audio", "mix_en.wav"),
        "output": os.path.join(ROOT, "renders", "Historia_IA_PixelArt_EN.mp4"),
        "copies": []
    },
    {
        "code": "PT",
        "video": os.path.join(ROOT, "renders", "video_mudo_pt.mp4"),
        "audio": os.path.join(ROOT, "audio", "mix_pt.wav"),
        "output": os.path.join(ROOT, "renders", "Historia_IA_PixelArt_PT.mp4"),
        "copies": []
    }
]

def main():
    for item in LANGS:
        vpath = item["video"]
        if not os.path.isfile(vpath):
            print(f"Skipping {item['code']}: {vpath} not found!", file=sys.stderr)
            continue
        print(f"=== MUXING {item['code']} ({os.path.basename(vpath)}) ===")
        cmd = [
            "ffmpeg", "-y", "-loglevel", "info",
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
            item["output"]
        ]
        subprocess.check_call(cmd)
        print(f"Created: {item['output']} ({os.path.getsize(item['output']) / (1024*1024):.1f} MB)")
        for cp in item["copies"]:
            shutil.copyfile(item["output"], cp)
            print(f"Copied to: {cp}")

if __name__ == "__main__":
    main()
