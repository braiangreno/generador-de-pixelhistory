"""Genera las miniaturas de YouTube (1920x1080) en ES, EN y PT + YOUTUBE_DESCRIPCION.txt
con los capítulos cronometrados y las fuentes verificadas del guion de NVIDIA.
"""
import os
import sys
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))

from common import *  # noqa
from timeline import TL
import i18n


def make_thumbnail(lang="es"):
    i18n.set_lang(lang)
    cv = bg("diner_1993").copy()
    # Mitad derecha: centro de datos y caída roja en bolsa
    bg_right = bg("empty_ceo_office").copy()
    cv.paste(bg_right.crop((W // 2, 0, W, H)), (W // 2, 0))
    d = ImageDraw.Draw(cv)
    d.line([(W // 2, 0), (W // 2, H)], fill=(*GOLD, 255), width=2)

    draw_nvidia_prop(cv, 128, 248, kind="diner_table", t=1.2, state=2.0)
    draw_nvidia_prop(cv, 352, 248, kind="ceo_desk", t=1.2, state=2.0)
    char(cv, "huang", 240, 248, 1.2, scale=3, arms="cross", look=1, mood="neutral")

    draw_calendar_30(cv, 58, 72, 1.2, scale=2, tear_p=0.35, highlight_30=True)
    draw_gpu_card(cv, 418, 92, 1.2, scale=2, fan_speed=12.0, led_col=GPU_GREEN)

    titles = {
        "es": ("A 30 DÍAS", "DE QUEBRAR", "1993 - 2026 · LA HISTORIA DE NVIDIA"),
        "en": ("30 DAYS FROM", "BANKRUPTCY", "1993 - 2026 · THE STORY OF NVIDIA"),
        "pt": ("A 30 DIAS", "DE FALIR", "1993 - 2026 · A HISTÓRIA DA NVIDIA"),
    }[lang]

    window(cv, 84, 14, 312, 82, fill=(14, 18, 28), border=GOLD, alpha=0.95)
    draw_text(cv, titles[0], 240, 22, "press", 16, align="center", gradient=GOLD_RAMP, outline_w=2)
    draw_text(cv, titles[1], 240, 44, "press", 16, align="center", gradient=GOLD_RAMP, outline_w=2)
    draw_text(cv, titles[2], 240, 72, "press", 8, GPU_GREEN, align="center")

    out_im = vignette(cv, 0.32).resize((1920, 1080), Image.NEAREST).convert("RGB")
    os.makedirs(os.path.join(ROOT, "renders"), exist_ok=True)
    out_path = os.path.join(ROOT, "renders", f"Miniatura_YouTube_{lang.upper()}.png")
    out_im.save(out_path)
    if lang == "es":
        out_im.save(os.path.join(ROOT, "renders", "Miniatura_YouTube.png"))
    print("Thumbnail saved:", out_path)


def _mmss(sec):
    s = int(round(max(0.0, sec)))
    return f"{s // 60:02d}:{s % 60:02d}"


def make_description():
    ch_lines = [
        (0.0, "Apertura — La empresa más valiosa del mundo y la renuncia"),
        (TL.s("c1_00"), "Capítulo 1 — El chip equivocado (1993–1995)"),
        (TL.s("c2_00"), "Capítulo 2 — Treinta días (Tokio, 1996 y RIVA 128)"),
        (TL.s("c3_00"), "Capítulo 3 — Miles de manos (GeForce 256 y qué es una GPU)"),
        (TL.s("c4_00"), "Capítulo 4 — La apuesta que nadie quería (CUDA, 2006)"),
        (TL.s("c5_00"), "Capítulo 5 — Dos placas en un dormitorio (Toronto, 2012 e IA)"),
        (TL.s("c6_00"), "Capítulo 6 — La fiebre del oro (OpenAI, ChatGPT y US$ 6 billones)"),
        (TL.s("c7_00"), "Capítulo 7 — Lo que vale una empresa (La Pizarra)"),
        (TL.s("c8_00"), "Capítulo 8 — La semana (Noviembre de 2026: la renuncia de Jensen Huang)"),
        (TL.s("c9_00"), "Capítulo 9 — ¿El final?"),
    ]
    ts_block = "\n".join(f"{_mmss(t)} {label}" for t, label in ch_lines)

    desc = f"""A TREINTA DÍAS DE QUEBRAR — La historia de NVIDIA (1993–2026) | Documental Animado en Pixel Art 16-Bit

En octubre de 2026, NVIDIA era la empresa más valiosa del mundo: valía casi seis billones de dólares y sus chips movían casi toda la inteligencia artificial del planeta. Tres semanas después, su fundador renunció después de treinta y tres años, el Congreso de los Estados Unidos lo citó a declarar y la empresa perdió un billón setecientos mil millones de dólares en la bolsa. Esta es la historia de cómo empezó todo en un restaurante de ruta en 1993... y de cómo una frase («Estamos a treinta días de quebrar») atravesó toda su historia.

CAPÍTULOS:
{ts_block}

FUENTES Y LECTURAS RECOMENDADAS:
• Stephen Witt — «The Thinking Machine: Jensen Huang, Nvidia, and the World's Most Coveted Microchip» (Viking, 2025).
• Tae Kim — «The Nvidia Way: Jensen Huang and the Making of a Tech Giant» (W. W. Norton, 2024).
• Conferencia de Jensen Huang en la Universidad de Stanford (SIEPR, 2024) y entrevista en el podcast Acquired (2023) sobre el acuerdo con Shoichiro Irimajiri y Sega en 1996.
• Cobertura periodística de noviembre de 2026 sobre la renuncia de Jensen Huang el 12 de noviembre de 2026, la designación de Colette Kress como directora ejecutiva interina y la citación del Congreso de los Estados Unidos: The New York Times, Reuters, CNBC, Fortune y TechCrunch (noviembre de 2026).

CRÉDITOS:
• Idea Original, Producción y Dirección: Braian Greno
• Estudio: Pixeloide Studios (Montevideo · São Paulo) — https://pixeloide.com
• Narración en español: Carlos Aguilar

¿Qué otra historia te gustaría ver en el próximo episodio? ¡Dejalo en los comentarios!
"""
    out_txt = os.path.join(ROOT, "renders", "YOUTUBE_DESCRIPCION.txt")
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write(desc)
    print("Description saved:", out_txt)


if __name__ == "__main__":
    for lg in ("es", "en", "pt"):
        make_thumbnail(lg)
    make_description()
