"""Inicializa un nuevo proyecto de documental 16-bit de Pixeloide Studios
copiando el motor base (engine/core.py, common.py, timeline.py, i18n.py, outro.py,
audio.py, video.py) y las herramientas de producción (batch_tts.py, prep_assets.py,
tools/*) listas para recibir un nuevo guion.

Uso:
  python tools/new_project.py <nombre_carpeta_destino>
"""
import os
import shutil
import sys

TEMPLATE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CORE_ENGINE_FILES = [
    "engine/core.py",
    "engine/common.py",
    "engine/sprites.py",
    "engine/timeline.py",
    "engine/i18n.py",
    "engine/outro.py",
    "engine/audio.py",
    "engine/video.py",
]

CORE_TOOL_FILES = [
    "ENGINE_GUIDE.md",
    "tools/tts.py",
    "tools/prep_assets.py",
    "tools/make_srt.py",
    "tools/make_multilingual_subtitles.py",
    "tools/batch_tts_multilingual.py",
    "tools/mix_multilingual.py",
    "tools/mux_all.py",
    "tools/update_outro_video.py",
    ".gitignore",
    ".gitattributes",
    ".env.example",
]


def create_project(target_name):
    if os.path.isabs(target_name):
        dest = target_name
    else:
        parent = os.path.dirname(TEMPLATE_ROOT)
        dest = os.path.join(parent, target_name)

    os.makedirs(dest, exist_ok=True)
    for sub in ["engine", "tools", "assets/bg", "assets/portraits", "audio/vo", "audio/vo_en", "audio/vo_pt", "frames", "renders", "fonts"]:
        os.makedirs(os.path.join(dest, sub), exist_ok=True)

    fonts_src = os.path.join(TEMPLATE_ROOT, "fonts")
    if os.path.exists(fonts_src):
        for fn in os.listdir(fonts_src):
            shutil.copy2(os.path.join(fonts_src, fn), os.path.join(dest, "fonts", fn))

    for rel in CORE_ENGINE_FILES + CORE_TOOL_FILES:
        src = os.path.join(TEMPLATE_ROOT, rel)
        dst = os.path.join(dest, rel)
        if os.path.exists(src):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)

    # Copy .env if present so ElevenLabs API key works out of the box
    env_src = os.path.join(TEMPLATE_ROOT, ".env")
    env_dst = os.path.join(dest, ".env")
    if os.path.exists(env_src) and not os.path.exists(env_dst):
        shutil.copy2(env_src, env_dst)

    print(f"Proyecto Pixeloide Video Engine creado en: {dest}")
    print("Siguientes pasos:")
    print("  1. Guarda el guion estructurado en script_full.json (+ script_full_en.json y script_full_pt.json)")
    print("  2. Ejecuta: python batch_tts.py && python tools/batch_tts_multilingual.py")
    print("  3. Crea los capítulos engine/ch01.py .. engine/chNN.py (el cierre engine/outro.py ya está incluido)")
    print("  4. Ejecuta: python engine/audio.py && python tools/mix_multilingual.py")
    print("  5. Ejecuta: python engine/video.py render 8 && python tools/render_multilingual.py && python tools/mux_all.py")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python tools/new_project.py <nombre_proyecto>")
        sys.exit(1)
    create_project(sys.argv[1])
