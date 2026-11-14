"""Capítulo 6: La fiebre del oro (OpenAI 2016, ChatGPT, las palas de la fiebre del oro, US$5 billones, el susto de DeepSeek y el récord de casi US$6 billones en octubre de 2026)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa

c6_card = make_card(6, ["LA FIEBRE", "DEL ORO"], "2016 - 2026 · DE OPENAI A US$ 6 BILLONES")


def c6_s01_openai_chatgpt_and_shovels(t):
    """c6_01..c6_03: Huang entrega la primera supercomputadora de IA a OpenAI (2016) -> ChatGPT -> el pueblo minero donde NVIDIA vende las palas."""
    t0 = TL.s("c6_01")
    t_c6_02 = TL.s("c6_02")
    t_c6_03 = TL.s("c6_03")

    if t < t_c6_02 - 0.12:
        cv = bg("sf_ai_lab_2016").copy()
        draw_place_only(cv, "SAN FRANCISCO · 2016 · LABORATORIO DE OPENAI", t, t0, border=GOLD)
        draw_nvidia_prop(cv, 240, 248, kind="gpu_pedestal", t=t, state=2.0)
        dx_h, wph = walk(t, t0, t0 + 1.8, 118, 168)
        char(cv, "huang", dx_h, 248, t, scale=2, walk_phase=wph,
             arms="hold" if wph is not None else "offer", look=1, mood="happy")
        char(cv, "altman", 322, 248, t, scale=2, arms="wave", look=-1, mood="happy")

        a, dy = pop(t, t0 + 0.1)
        window(cv, 98, 42 + dy, 284, 92, fill=(22, 18, 14), border=GOLD, alpha=0.95)
        draw_text(cv, "2016 · ENTREGA EN PERSONA", 240, 52 + dy, "press", 8, GOLD, align="center")
        draw_text(cv, "PRIMERA SUPERCOMPUTADORA DE IA", 240, 74 + dy, "silk", 8, CREAM, align="center")
        draw_text(cv, "EL LABORATORIO SE LLAMABA OPENAI", 240, 94 + dy, "silk", 8, GPU_GREEN, align="center")
        return vignette(cv, 0.32)

    if t < t_c6_03 - 0.12:
        cv = bg("datacenter_gold").copy()
        draw_place_only(cv, "2022 · LANZAMIENTO DE CHATGPT", t, t_c6_02, border=GPU_GREEN)
        draw_nvidia_prop(cv, 240, 248, kind="gpu_pedestal", t=t, state=2.0)
        a, dy = pop(t, t_c6_02 - 0.05)
        window(cv, 98, 42 + dy, 284, 92, fill=(14, 24, 20), border=GPU_GREEN, alpha=0.95)
        draw_text(cv, "SEIS AÑOS DESPUÉS: CHATGPT", 240, 52 + dy, "press", 8, GPU_GREEN, align="center")
        draw_text(cv, "TODAS LAS EMPRESAS DEL MUNDO", 240, 74 + dy, "silk", 8, CREAM, align="center")
        draw_text(cv, "QUISIERON LO MISMO: CHIPS DE NVIDIA", 240, 94 + dy, "silk", 8, GOLD, align="center")
        return vignette(cv, 0.32)

    # c6_03: Pueblo minero en pixel: cientos de mineros corren con el pico; NVIDIA vende las palas
    cv = bg("gold_rush_town").copy()
    draw_place_only(cv, "LA FIEBRE DEL ORO · NVIDIA VENDE LAS PALAS", t, t_c6_03, border=GOLD)
    dx_m1, wph1 = walk(t, t_c6_03, t_c6_03 + 2.4, 96, 178)
    char(cv, "miner_a", dx_m1, 248, t, scale=2, walk_phase=wph1, arms="work", look=1, mood="happy")
    char(cv, "miner_b", 232, 248, t, scale=2, arms="cheer", look=1, mood="happy")
    char(cv, "shopkeeper", 342, 248, t, scale=2, arms="offer", look=-1, mood="happy")

    a, dy = pop(t, t_c6_03 - 0.05)
    window(cv, 98, 42 + dy, 284, 86, fill=(28, 20, 12), border=GOLD, alpha=0.95)
    draw_text(cv, "LA FIEBRE DEL ORO DE LA IA", 240, 52 + dy, "press", 8, GOLD, align="center")
    draw_text(cv, "TODOS BUSCABAN EL ORO DIGITAL", 240, 74 + dy, "silk", 8, CREAM, align="center")
    draw_text(cv, "Y NVIDIA VENDÍA LAS PALAS", 240, 94 + dy, "press", 8, GPU_GREEN, align="center")
    return vignette(cv, 0.32)


def c6_s02_five_trillion_deepseek_and_peak(t):
    """c6_04..c6_07: US$5 billones (2025) -> el barco sacudido por DeepSeek (–US$589.000M en un día) -> casi US$6 billones en octubre de 2026."""
    t_c6_04 = TL.s("c6_04")
    t_c6_05 = TL.s("c6_05")
    t_c6_06 = TL.s("c6_06")
    t_c6_07 = TL.s("c6_07")

    if t < t_c6_05 - 0.12:
        cv = bg("datacenter_gold").copy()
        draw_place_only(cv, "2023 -> 2025 · RÉCORD HISTÓRICO EN BOLSA", t, t_c6_04, border=GOLD)
        pts_up = [0.12, 0.18, 0.28, 0.42, 0.58, 0.76, 0.92]
        draw_stock_chart(cv, 98, 42, 284, 108, pts_up, progress=clamp01((t - t_c6_04) / 2.2), col_up=GOLD, col_down=GOLD)
        draw_text(cv, "2023: US$ 1 BILLÓN -> 2025: US$ 5 BILLONES", 240, 52, "silk", 8, CREAM, align="center")
        draw_text(cv, "US$ 5 BILLONES", 240, 72, "press", 16, GOLD, align="center")
        return vignette(cv, 0.32)

    if t < t_c6_06 - 0.12:
        # c6_05: Barco enorme recibe una ola de frente (DeepSeek, enero 2025: –US$589.000 millones en un día)
        cv = bg("storm_cargo_ship").copy()
        sx, sy = shake(t, t_c6_05 + 0.6, dur=0.55, amp=4)
        cv = offset_canvas(cv, sx, sy)
        draw_place_only(cv, "ENERO DE 2025 · EL SUSTO DE DEEPSEEK", t, t_c6_05, border=STOCK_RED)
        a, dy = pop(t, t_c6_05 + 0.1)
        window(cv, 98, 42 + dy, 284, 96, fill=(28, 12, 16), border=STOCK_RED, alpha=0.96)
        draw_text(cv, "–US$ 589.000 MILLONES EN UN DÍA", 240, 52 + dy, "press", 8, STOCK_RED, align="center")
        draw_text(cv, "EL MODELO CHINO DEEPSEEK ASUSTÓ AL MERCADO", 240, 74 + dy, "silk", 8, CREAM, align="center")
        draw_text(cv, "LA MAYOR CAÍDA DIARIA DE LA HISTORIA", 240, 94 + dy, "silk", 8, GOLD, align="center")
        return vignette(cv, 0.38)

    # c6_06..c6_07: El barco se endereza y en octubre de 2026 roza los US$6 billones (la más valiosa del planeta)
    cv = bg("datacenter_gold").copy()
    draw_place_only(cv, "OCTUBRE DE 2026 · CASI US$ 6 BILLONES", t, t_c6_06, border=GOLD)
    pts_peak = [0.20, 0.38, 0.62, 0.44, 0.68, 0.84, 0.96]
    draw_stock_chart(cv, 98, 42, 284, 108, pts_peak, progress=clamp01((t - t_c6_06) / 1.8), col_up=GPU_GREEN, col_down=GOLD)
    draw_text(cv, "OCTUBRE DE 2026 · ROZÓ LOS US$ 6 BILLONES", 240, 52, "silk", 8, GOLD, align="center")
    if t >= t_c6_07 - 0.1:
        window(cv, 98, 166, 284, 52, fill=(22, 18, 12), border=GOLD, alpha=0.96)
        draw_text(cv, "33 AÑOS DESPUÉS DE AQUELLA MESA:", 240, 176, "silk", 8, CREAM, align="center")
        draw_text(cv, "LA EMPRESA MÁS VALIOSA DEL PLANETA", 240, 194, "press", 8, GOLD, align="center")
    return vignette(cv, 0.32)


def scenes():
    return [
        (TL.s("c6_00") - 0.15, c6_card),
        (TL.s("c6_01"), c6_s01_openai_chatgpt_and_shovels,
         lambda t: cam_push(t, TL.s("c6_01"), TL.s("c6_04"), 1.0, 1.03, (240, 135), (240, 134))),
        (TL.s("c6_04"), c6_s02_five_trillion_deepseek_and_peak,
         lambda t: cam_push(t, TL.s("c6_04"), TL.s("c7_00"), 1.0, 1.03, (240, 135), (240, 134))),
    ]


def music(A):
    A.add_pad(TL.s("c6_00"), TL.e("c6_07") - TL.s("c6_00"), (196.0, 233.08, 293.66), amp=0.017)


def sfx(A):
    A.fx_pop(TL.s("c6_01") + 0.15, 0.05)
    A.fx_chime(TL.s("c6_02") + 0.2, 0.06)
    A.fx_sparkle(TL.s("c6_04") + 0.25, 0.06)
    A.fx_thud(TL.s("c6_05") + 0.6, 0.07)
    A.fx_chime(TL.s("c6_07") + 0.2, 0.06)
