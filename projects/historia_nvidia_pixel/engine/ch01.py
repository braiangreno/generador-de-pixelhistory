"""Apertura (La mesa del restaurante, 1993) + Capítulo 1 (El chip equivocado: NV1, curvas vs triángulos, Sega y 30 días de caja)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa


def s0_s01_diner_and_napkin(t):
    """s01..s03: Restaurante de ruta en San José (1993), Jensen Huang lavaplatos a los 15, servilleta con triángulo y US$40.000."""
    t0 = TL.s("s01")
    t_s02 = TL.s("s02")
    t_s03 = TL.s("s03")
    t_40k = TL.word("s03", "cuarenta")

    cv = bg("diner_1993").copy()
    d = ImageDraw.Draw(cv)

    draw_place_only(cv, "SAN JOSÉ, CALIFORNIA · 1993", t, t0, border=GOLD)

    # Tres ingenieros alrededor de la mesa del restaurante de ruta
    state_tbl = 1.0 if t >= t_40k - 0.25 else 0.0
    draw_nvidia_prop(cv, 240, 248, kind="diner_table", t=t, state=state_tbl)
    char(cv, "cofounder_a", 156, 248, t, scale=2, arms="note", look=1, mood="happy")
    char(cv, "huang_young", 240, 248, t, scale=2,
         arms="write" if t < t_s03 else "cheer", look=1, mood="happy",
         talk=talk_v(t, t0 <= t < TL.e("s03")))
    char(cv, "cofounder_b", 324, 248, t, scale=2,
         arms="think" if t < t_40k else "wave", look=-1, mood="happy")

    if t < t_s02 - 0.12:
        a, dy = pop(t, t0 + 0.15)
        window(cv, 108, 42 + dy, 264, 78, fill=(24, 18, 28), border=GOLD, alpha=0.95)
        draw_text(cv, "LA MESA DEL RESTAURANTE", 240, 52 + dy, "press", 8, GOLD, align="center")
        draw_text(cv, "TRES INGENIEROS · SAN JOSÉ, 1993", 240, 72 + dy, "silk", 8, CREAM, align="center")
        draw_text(cv, "PIDEN CAFÉ. MUCHO CAFÉ.", 240, 92 + dy, "silk", 8, CHALK_YELLOW, align="center")
    elif t < t_s03 - 0.12:
        a, dy = pop(t, t_s02 - 0.1)
        window(cv, 108, 42 + dy, 264, 86, fill=(24, 18, 28), border=TESLA_CYAN, alpha=0.95)
        draw_text(cv, "JENSEN HUANG", 240, 52 + dy, "press", 8, TESLA_CYAN, align="center")
        draw_text(cv, "CONOCE BIEN ESA CADENA:", 240, 72 + dy, "silk", 8, CREAM, align="center")
        draw_text(cv, "A LOS 15 AÑOS LAVÓ PLATOS AHÍ", 240, 92 + dy, "silk", 8, GOLD, align="center")
    else:
        a, dy = pop(t, t_s03 - 0.1)
        window(cv, 108, 42 + dy, 264, 92, fill=(18, 26, 22), border=GPU_GREEN, alpha=0.95)
        draw_text(cv, "UN CHIP PARA JUEGOS EN 3D", 240, 50 + dy, "press", 8, GPU_GREEN, align="center")
        # Servilleta ampliada con un triángulo y una pantalla + contador US$40.000
        d.rectangle([144, 68 + dy, 212, 114 + dy], fill=(248, 244, 234, 255), outline=(*INK, 255))
        d.polygon([(178, 74 + dy), (158, 106 + dy), (198, 106 + dy)], outline=(*GPU_GREEN, 255), fill=(26, 56, 38, 255))
        cnt = int(round(40000 * clamp01((t - (t_40k - 0.6)) / 1.1)))
        draw_text(cv, "CAPITAL INICIAL:", 288, 74 + dy, "silk", 8, CREAM, align="center")
        draw_text(cv, f"US$ {cnt:,}".replace(",", "."), 288, 94 + dy, "press", 8, GOLD, align="center")

    return vignette(cv, 0.34)


def s0_s02_six_trillion_and_title(t):
    """s04..s06: El chip se multiplica en un centro de datos de US$6 billones -> línea roja cae -> título A TREINTA DÍAS DE QUEBRAR."""
    t_s04 = TL.s("s04")
    t_s05 = TL.s("s05")
    t_s06 = TL.s("s06")

    if t < t_s05 - 0.12:
        cv = bg("datacenter_gold").copy()
        draw_place_only(cv, "33 AÑOS DESPUÉS · CASI US$ 6 BILLONES", t, t_s04, border=GOLD)
        draw_nvidia_prop(cv, 240, 248, kind="gpu_pedestal", t=t, state=2.0)
        a, dy = pop(t, t_s04 + 0.1)
        window(cv, 104, 42 + dy, 272, 92, fill=(22, 18, 12), border=GOLD, alpha=0.95)
        draw_text(cv, "LA EMPRESA MÁS VALIOSA", 240, 52 + dy, "press", 8, GOLD, align="center")
        draw_text(cv, "LLEGÓ A VALER CASI US$ 6 BILLONES", 240, 74 + dy, "silk", 8, CREAM, align="center")
        draw_text(cv, "NUNCA NINGUNA HABÍA VALIDO TANTO", 240, 96 + dy, "silk", 8, GPU_GREEN, align="center")
        return vignette(cv, 0.32)

    if t < t_s06 - 0.12:
        # s05: Negro con una sola línea roja de bolsa que cae ("Y esta semana, el hombre de aquella mesa se fue.")
        cv = vgradient((8, 6, 12), (22, 8, 14), 8)
        draw_place_only(cv, "ESTA SEMANA · NOVIEMBRE DE 2026", t, t_s05, border=STOCK_RED)
        p_drop = clamp01((t - t_s05) / max(0.8, (t_s06 - t_s05) * 0.75))
        pts = [0.22, 0.28, 0.36, 0.48, 0.64, 0.82, 0.94, 0.68, 0.38, 0.14]
        draw_stock_chart(cv, 84, 46, 312, 118, pts, progress=p_drop, col_up=GPU_GREEN, col_down=STOCK_RED, split_idx=6)
        window(cv, 104, 178, 272, 46, fill=(28, 10, 14), border=STOCK_RED, alpha=0.96)
        draw_text(cv, "EL HOMBRE DE AQUELLA MESA SE FUE", 240, 196, "silk", 8, STOCK_RED, align="center")
        return vignette(cv, 0.42)

    # s06: Título principal sobre la mesa vacía del restaurante de 1993
    cv = bg("diner_1993").copy()
    cv = grade(cv, mul=(0.76, 0.82, 0.92))
    draw_nvidia_prop(cv, 240, 248, kind="diner_table", t=t, state=0.0)
    a, dy = pop(t, t_s06 - 0.05)
    window(cv, 76, 44 + dy, 328, 118, fill=(14, 20, 28), border=GOLD, alpha=0.96, inner=GPU_GREEN)
    draw_text(cv, "LA HISTORIA DE NVIDIA", 240, 56 + dy, "silk", 8, GPU_GREEN, align="center")
    draw_text(cv, "A TREINTA DÍAS", 240, 76 + dy, "press", 16, GOLD, align="center", gradient=GOLD_RAMP)
    draw_text(cv, "DE QUEBRAR", 240, 98 + dy, "press", 16, CREAM, align="center", gradient=CREAM_RAMP)
    draw_text(cv, "DE US$ 40.000 A LA RENUNCIA DE SU FUNDADOR", 240, 128 + dy, "silk", 8, TESLA_CYAN, align="center")
    return vignette(cv, 0.36)


c1_card = make_card(1, ["EL CHIP", "EQUIVOCADO"], "1995 - 1996 · CALIFORNIA")


def c1_s01_nv1_curves_vs_triangles(t):
    """c1_01..c1_03: De invidia al NV1 (1995), superficies curvas vs triángulos, y el estándar de Microsoft."""
    t0 = TL.s("c1_01")
    t_c1_02 = TL.s("c1_02")
    t_c1_03 = TL.s("c1_03")

    cv = bg("startup_office_1995").copy()
    draw_place_only(cv, "CALIFORNIA · 1995 · EL PRIMER CHIP (NV1)", t, t0, border=BEIGE_90S)

    draw_nvidia_prop(cv, 240, 248, kind="crt_pair", t=t, state=1.0)
    char(cv, "huang_young", 132, 248, t, scale=2,
         arms="point" if t < t_c1_03 else "think", look=1, mood="sad" if t >= t_c1_02 else "neutral",
         talk=talk_v(t, t0 <= t < TL.e("c1_03")))
    char(cv, "cofounder_a", 348, 248, t, scale=2,
         arms="work" if t < t_c1_03 else "shrug", look=-1, mood="sad" if t >= t_c1_03 else "neutral")

    if t < t_c1_02 - 0.12:
        a, dy = pop(t, t0 + 0.1)
        window(cv, 104, 40 + dy, 272, 84, fill=(24, 22, 32), border=GOLD, alpha=0.95)
        draw_text(cv, "1995 · PRIMER CHIP: NV1", 240, 50 + dy, "press", 8, GOLD, align="center")
        draw_text(cv, "ORIGEN: «INVIDIA» (ENVIDIA EN LATÍN)", 240, 72 + dy, "silk", 8, CREAM, align="center")
        draw_text(cv, "PRIMER INTENTO DE ACELERAR 3D", 240, 92 + dy, "silk", 8, TESLA_CYAN, align="center")
    elif t < t_c1_03 - 0.12:
        a, dy = pop(t, t_c1_02 - 0.1)
        window(cv, 98, 40 + dy, 284, 92, fill=(24, 20, 30), border=STOCK_RED, alpha=0.95)
        draw_text(cv, "CURVAS VS. TRIÁNGULOS", 240, 50 + dy, "press", 8, STOCK_RED, align="center")
        draw_text(cv, "NV1: DIBUJABA CON SUPERFICIES CURVAS", 240, 72 + dy, "silk", 8, CREAM, align="center")
        draw_text(cv, "LA INDUSTRIA ELIGIÓ LOS TRIÁNGULOS", 240, 94 + dy, "silk", 8, GPU_GREEN, align="center")
    else:
        a, dy = pop(t, t_c1_03 - 0.1)
        window(cv, 98, 40 + dy, 284, 92, fill=(28, 16, 22), border=STOCK_RED, alpha=0.95)
        draw_text(cv, "EL ESTÁNDAR DE WINDOWS", 240, 50 + dy, "press", 8, GOLD, align="center")
        draw_text(cv, "MICROSOFT ARMÓ SU ESTÁNDAR CON TRIÁNGULOS", 240, 72 + dy, "silk", 8, CREAM, align="center")
        draw_text(cv, "EL NV1 QUEDÓ DEL LADO EQUIVOCADO", 240, 94 + dy, "silk", 8, STOCK_RED, align="center")

    return vignette(cv, 0.34)


def c1_s02_sega_fax_and_30_days(t):
    """c1_04..c1_05: El contrato con Sega para su próxima consola y el calendario con 30 días de caja."""
    t_c1_04 = TL.s("c1_04")
    t_c1_05 = TL.s("c1_05")

    cv = bg("startup_office_1995").copy()
    if t >= t_c1_05 - 0.1:
        cv = grade(cv, mul=(0.78, 0.72, 0.76))

    draw_place_only(cv, "CALIFORNIA · 1996 · 30 DÍAS DE CAJA", t, t_c1_04, border=STOCK_RED)
    fax_p = clamp01((t - t_c1_04) / 2.2)
    draw_nvidia_prop(cv, 240, 248, kind="fax_desk", t=t, state=fax_p)
    draw_calendar_30(cv, 62, 68, t, scale=1, tear_p=0.0, highlight_30=True)

    char(cv, "huang_young", 152, 248, t, scale=2, arms="think", look=1, mood="sad",
         talk=talk_v(t, t_c1_04 <= t < TL.e("c1_05")))
    char(cv, "cofounder_b", 328, 248, t, scale=2, arms="hips", look=-1, mood="sad")

    if t < t_c1_05 - 0.12:
        a, dy = pop(t, t_c1_04 - 0.05)
        window(cv, 104, 42 + dy, 272, 86, fill=(24, 20, 30), border=GOLD, alpha=0.95)
        draw_text(cv, "CONTRATO CON SEGA", 240, 52 + dy, "press", 8, GOLD, align="center")
        draw_text(cv, "CHIP PARA SU PRÓXIMA CONSOLA", 240, 74 + dy, "silk", 8, CREAM, align="center")
        draw_text(cv, "PERO CON LA TECNOLOGÍA EQUIVOCADA", 240, 94 + dy, "silk", 8, STOCK_RED, align="center")
    else:
        a, dy = pop(t, t_c1_05 - 0.05)
        window(cv, 104, 42 + dy, 272, 92, fill=(32, 12, 18), border=STOCK_RED, alpha=0.96)
        draw_text(cv, "30 DÍAS DE CAJA", 240, 52 + dy, "press", 16, STOCK_RED, align="center")
        draw_text(cv, "CUENTA BANCARIA AL LÍMITE", 240, 78 + dy, "silk", 8, CREAM, align="center")
        draw_text(cv, "DINERO PARA UNOS TREINTA DÍAS", 240, 98 + dy, "silk", 8, CHALK_YELLOW, align="center")

    return vignette(cv, 0.38)


def scenes():
    return [
        (0.0, s0_s01_diner_and_napkin,
         lambda t: cam_push(t, 0.0, TL.s("s04"), 1.0, 1.03, (240, 135), (240, 134))),
        (TL.s("s04"), s0_s02_six_trillion_and_title,
         lambda t: cam_push(t, TL.s("s04"), TL.s("c1_00"), 1.0, 1.03, (240, 135), (240, 134))),
        (TL.s("c1_00") - 0.15, c1_card),
        (TL.s("c1_01"), c1_s01_nv1_curves_vs_triangles,
         lambda t: cam_push(t, TL.s("c1_01"), TL.s("c1_04"), 1.0, 1.03, (240, 135), (240, 134))),
        (TL.s("c1_04"), c1_s02_sega_fax_and_30_days,
         lambda t: cam_push(t, TL.s("c1_04"), TL.s("c2_00"), 1.0, 1.03, (240, 135), (240, 134))),
    ]


def music(A):
    A.add_pad(TL.s("s01"), TL.e("c1_05") - TL.s("s01"), (220.0, 261.63, 329.63), amp=0.016)


def sfx(A):
    A.fx_pop(TL.s("s01") + 0.2, 0.05)
    A.fx_chime(TL.word("s03", "cuarenta"), 0.06)
    A.fx_sparkle(TL.s("s04") + 0.3, 0.06)
    A.fx_thud(TL.s("s05") + 0.1, 0.07)
    A.fx_pop(TL.s("c1_02") + 0.1, 0.05)
    A.fx_thud(TL.s("c1_05") + 0.1, 0.07)
