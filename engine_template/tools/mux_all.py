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


def _medir(path, pre=""):
    af = (pre + "," if pre else "") + "loudnorm=I=-14:TP=-1.0:LRA=11:print_format=json"
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", af, "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    t = r.stderr
    return json.loads(t[t.rfind("{"):t.rfind("}") + 1])


def filtro_14_lufs(apath):
    """-14 LUFS de verdad (una sola pasada de loudnorm se queda corta: medido -16 en EN).
    1) mide la mezcla, 2) ajusta la ganancia y limita los picos, 3) loudnorm lineal con la medición nueva.
    Resultado medido en la prueba: -13.9/-14.2/-13.9 LUFS con picos <= -1 dBFS después del AAC."""
    try:
        m = _medir(apath)
        gain = -14.0 - float(m["input_i"]) + 0.5  # margen: el limitador baja un poco el nivel
        pre = f"volume={gain:.2f}dB,alimiter=limit=0.71:attack=5:release=60:level=0"
        m2 = _medir(apath, pre)
        return (pre + ",loudnorm=I=-14:TP=-1.5:LRA=11"
                f":measured_I={m2['input_i']}:measured_TP={m2['input_tp']}:measured_LRA={m2['input_lra']}"
                f":measured_thresh={m2['input_thresh']}:offset={m2['target_offset']}:linear=true")
    except Exception as e:  # si no se puede medir, queda la normalización de una pasada
        print(f"(no pude medir {os.path.basename(apath)}: {e}; uso loudnorm de una pasada)", file=sys.stderr)
        return "loudnorm=I=-14:TP=-1.0:LRA=11"


def main():
    os.makedirs(os.path.join(ROOT, "renders"), exist_ok=True)
    pedidos = [a.upper() for a in sys.argv[1:]] or [x["code"] for x in LANGS]
    for item in LANGS:
        if item["code"] not in pedidos:
            continue
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
            "-af", filtro_14_lufs(apath),
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
