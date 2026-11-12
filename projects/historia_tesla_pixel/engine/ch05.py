"""Capítulo 5: La ciudad blanca (Feria Mundial de Chicago 1893, Huevo gigante, Niágara y el contrato de regalías)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa


def c5_s01_chicago_fair(t):
    """5:19 - 5:42: Feria Mundial de Chicago 1893; presupuestos US$554.000 vs US$399.000 y encendido de 100.000 lámparas."""
    cv = bg("bg_chicago_fair_1893").copy()
    t0 = TL.s("c5_01")
    t_c5_02 = TL.s("c5_02")
    t_c5_03 = TL.s("c5_03")
    t_bot = TL.word("c5_03", "botón")
    t_cien = TL.word("c5_03", "cien")

    # Al principio la feria está en penumbra hasta que el presidente aprieta el botón
    wave_p = clamp01((t - t_bot) / 1.6) if t >= t_bot else 0.0
    if wave_p < 1.0:
        dark_cv = tint(cv.copy(), (8, 12, 24), 0.68)
        if wave_p <= 0.0:
            cv = dark_cv
        else:
            # Ola de luz dorada de izquierda a derecha
            split_x = int(W * ease_out(wave_p))
            cv_crop = cv.crop((0, 0, split_x, H))
            dark_cv.paste(cv_crop, (0, 0))
            cv = dark_cv
            glow(cv, split_x, 148, 48, GOLD, 0.75)

    draw_place_only(cv, "FERIA MUNDIAL DE CHICAGO · 1893", t, t0, border=GOLD)

    if t_c5_02 - 0.15 <= t < t_c5_03:
        # Dos sobres de presupuesto comparados (dentro de x=118..362)
        a, dy = pop(t, t_c5_02 - 0.15)
        window(cv, 118, 62 + dy, 244, 78, fill=(18, 24, 38), border=GOLD)
        draw_text(cv, "LICITACIÓN PARA ILUMINAR LA FERIA:", 240, 70 + dy, "silk", 8, CREAM, align="center")
        draw_text(cv, "BANDO EDISON: US$554.000", 240, 90 + dy, "silk", 8, CHALK_RED, align="center")
        draw_text(cv, "WESTINGHOUSE (AC): US$399.000", 240, 110 + dy, "silk", 8, CHALK_GREEN, align="center")

    if t >= t_c5_03:
        # Presidente en el palco apretando el botón dorado + contador 100.000 LÁMPARAS
        char(cv, "president_1893", 240, 246, t, scale=2,
             arms="work" if t >= t_bot else "up", look=1, mood="happy")

        def _draw_podium(target_cv, fx, fy):
            d = ImageDraw.Draw(target_cv)
            d.rectangle([fx - 44, fy - 32, fx + 44, fy + 2], fill=(42, 32, 28, 255), outline=(*GOLD, 255))
            btn_dy = -35 if t >= t_bot else -38
            d.rectangle([fx - 6, fy + btn_dy, fx + 6, fy - 32], fill=(*GOLD, 255))

        floor_prop(cv, _draw_podium, 240, 246)

        if t >= t_bot:
            cnt = int(round(100000 * clamp01((t - t_bot) / 1.4)))
            cnt_s = f"{cnt:,} LÁMPARAS".replace(",", ".")
            window(cv, 124, 58, 232, 48, fill=(22, 26, 44), border=GOLD)
            draw_text(cv, "LA CIUDAD BLANCA ENCIENDE:", 240, 66, "silk", 8, CREAM, align="center")
            draw_text(cv, cnt_s, 240, 82, "press", 8, GOLD, align="center")

    return vignette(cv, 0.30)


def c5_s02_giant_egg_and_niagara(t):
    """5:42 - 5:58: Pabellón eléctrico con el huevo de cobre gigante y la central hidroeléctrica del Niágara a Buffalo."""
    t0 = TL.s("c5_04")
    t_c5_05 = TL.s("c5_05")
    t_buf = TL.word("c5_05", "Búfalo")
    t_km = TL.word("c5_05", "treinta")

    if t < t_c5_05:
        cv = bg("bg_electricity_pavilion_1893").copy()
        draw_place_only(cv, "PABELLÓN ELÉCTRICO · CHICAGO 1893", t, t0, border=TESLA_CYAN)
        # Mesa central con patas y el Huevo de Colón gigante girando sobre su punta
        d = ImageDraw.Draw(cv)
        d.rectangle([182, 216, 188, 234], fill=(74, 44, 24, 255), outline=(*INK, 255))
        d.rectangle([292, 216, 298, 234], fill=(74, 44, 24, 255), outline=(*INK, 255))
        d.rectangle([176, 206, 304, 216], fill=(96, 58, 34, 255), outline=(*GOLD, 255))
        draw_rotating_arrows(cv, 240, 224, 14, t * 4.2, color=TESLA_CYAN, pulse=0.85)
        draw_copper_egg(cv, 240, 204, t, spin_speed=1.0, stand_p=1.0, scale=1.45)

        window(cv, 124, 52, 232, 42, fill=(18, 24, 38), border=GOLD)
        draw_text(cv, "EL HUEVO DE COBRE GIGANTE", 240, 60, "silk", 8, GOLD, align="center")
        draw_text(cv, "GIRABA SOLO ANTE EL PÚBLICO", 240, 76, "silk", 8, CREAM, align="center")

        char(cv, "inventor", 148, 248, t, scale=2, arms="point", look=1, mood="happy")
        char(cv, "investor_a", 332, 248, t, scale=2, arms="up", look=-1, mood="happy")
        char(cv, "investor_b", 374, 250, t, scale=2, arms="down", look=-1)
        return vignette(cv, 0.32)

    # Central hidroeléctrica del Niágara -> Línea de 35 km -> Tranvía en Buffalo
    cv = bg("bg_niagara_power_1895").copy()
    draw_place_only(cv, "NIÁGARA -> BUFFALO", t, t_c5_05, border=TESLA_CYAN)

    # Generadores girando en la central
    draw_rotating_arrows(cv, 154, 198, 16, t * 4.5, color=TESLA_CYAN, pulse=0.9)
    draw_rotating_arrows(cv, 204, 198, 16, t * 4.5 + 1.2, color=TESLA_CYAN, pulse=0.9)

    # Panel superior de ruta energética (dentro de x=118..362)
    window(cv, 118, 52, 244, 72, fill=(16, 26, 42), border=TESLA_CYAN)
    draw_text(cv, "NIÁGARA -> BUFFALO (+30 KM)", 240, 60, "silk", 8, TESLA_CYAN, align="center")
    d = ImageDraw.Draw(cv)
    d.rectangle([134, 84, 174, 108], fill=(28, 54, 84, 255), outline=(*TESLA_CYAN, 255))
    draw_text(cv, "NIÁGARA", 154, 92, "silk", 8, CREAM, align="center")
    # Línea de transmisión con pulsos brillantes
    d.line([(174, 96), (294, 96)], fill=(*GOLD, 255), width=2)
    for k in range(4):
        px = 178 + int((t * 85 + k * 28) % 112)
        d.ellipse([px - 2, 94, px + 2, 98], fill=(*TESLA_SPARK, 255))
    # Tranvía iluminado en Buffalo
    d.rectangle([294, 82, 348, 108], fill=(44, 68, 42, 255), outline=(*GOLD, 255))
    draw_text(cv, "BUFFALO", 321, 91, "silk", 8, GOLD, align="center")

    return vignette(cv, 0.32)


def c5_s03_royalties_and_world_map(t):
    """5:58 - 6:34: Deudas de Westinghouse, leyenda del contrato roto vs archivo US$216.000 y red mundial AC."""
    cv = bg("bg_westinghouse_office_1888").copy()
    t0 = TL.s("c5_06")
    t_c5_07 = TL.s("c5_07")
    t_rom = TL.word("c5_07", "rompió")
    t_c5_08 = TL.s("c5_08")
    t_216 = TL.word("c5_08", "doscientos")
    t_c5_09 = TL.s("c5_09")

    if t < t_c5_07:
        # Banqueros exigiendo eliminar los US$2,50 por caballo de fuerza
        window(cv, 120, 52, 240, 56, fill=(32, 18, 24), border=CHALK_RED)
        draw_text(cv, "CRISIS DE DEUDA EN WESTINGHOUSE", 240, 60, "silk", 8, CHALK_RED, align="center")
        draw_text(cv, "ELIMINAR REGALÍA DE US$2,50 / HP", 240, 80, "silk", 8, GOLD, align="center")
        char(cv, "banker_morgan", 136, 250, t, scale=2, arms="point", look=1, mood="angry", talk=talk_v(t, True))
        char(cv, "westinghouse_gen", 240, 250, t, scale=2, arms="shrug", look=-1, mood="sad")
        char(cv, "inventor", 342, 250, t, scale=2, arms="down", look=-1, mood="neutral")
        return vignette(cv, 0.38)

    if t < t_c5_08:
        # Viñeta con marco "LEYENDA": Tesla rompiendo el contrato en dos pedazos por amistad
        window(cv, 118, 46, 244, 112, fill=(36, 28, 22), border=GOLD)
        draw_text(cv, "« LEYENDA POPULAR »", 240, 54, "press", 8, GOLD, align="center")
        draw_text(cv, "ROMPIÓ EL CONTRATO POR AMISTAD", 240, 74, "silk", 8, CREAM, align="center")
        d = ImageDraw.Draw(cv)
        sep = int(16 * clamp01((t - t_rom) / 0.6)) if t >= t_rom - 0.2 else 2
        # Dos mitades de papel separándose
        d.rectangle([196 - sep, 96, 236 - sep, 142], fill=(236, 226, 200, 255), outline=(*INK, 255))
        d.rectangle([244 + sep, 96, 284 + sep, 142], fill=(236, 226, 200, 255), outline=(*INK, 255))
        if sep > 4:
            draw_text(cv, "¡CRAC!", 240, 114, "silk", 8, CHALK_RED, align="center")
        char(cv, "westinghouse_gen", 156, 250, t, scale=2, arms="down", look=1, mood="sad")
        char(cv, "inventor", 324, 250, t, scale=2, arms="up" if sep > 4 else "hold", look=-1)
        return vignette(cv, 0.36)

    if t < t_c5_09:
        # Los documentos históricos: carpeta de archivo y pago único de US$216.000
        a, dy = pop(t, t_c5_08)
        window(cv, 118, 48 + dy, 244, 108, fill=(18, 28, 38), border=TESLA_CYAN)
        draw_text(cv, "ARCHIVO HISTÓRICO (1897):", 240, 56 + dy, "silk", 8, TESLA_CYAN, align="center")
        draw_text(cv, "CESIÓN TOTAL DE PATENTES AC", 240, 74 + dy, "silk", 8, CREAM, align="center")
        draw_text(cv, "PAGO ÚNICO:", 240, 94 + dy, "silk", 8, SOFT_GRAY, align="center")
        draw_text(cv, "US$216.000", 240, 112 + dy, "press", 16, GOLD, align="center", outline_w=2)
        char(cv, "westinghouse_gen", 164, 250, t, scale=2, arms="offer", look=1)
        char(cv, "inventor", 316, 250, t, scale=2, arms="hold", look=-1)
        return vignette(cv, 0.36)

    # Remate c5_09: El mapa del mundo se ilumina con corriente alterna; regalías futuras = US$0
    cv = bg("bg_night_grid_city").copy()
    for gx, gy in ((158, 165), (212, 152), (268, 160), (322, 172)):
        glow(cv, gx, gy, 22, GOLD, 0.55)
    window(cv, 118, 54, 244, 76, fill=(14, 20, 34), border=TESLA_CYAN)
    draw_text(cv, "SISTEMA ELÉCTRICO MUNDIAL: 100% AC", 240, 64, "silk", 8, TESLA_CYAN, align="center")
    draw_text(cv, "REGALÍAS FUTURAS PARA TESLA:", 240, 84, "silk", 8, CREAM, align="center")
    draw_text(cv, "US$0", 240, 102, "press", 16, CHALK_RED, align="center", outline_w=2)
    char(cv, "inventor", 240, 248, t, scale=2, arms="down", look=1, mood="sad")
    return vignette(cv, 0.38)


SCENES = [
    (TL.s("c5_00") - 0.15, TL.s("c5_01"), make_card(5, ["LA CIUDAD", "BLANCA"], "1893 – 1897 · CHICAGO Y NIÁGARA")),
    (TL.s("c5_01") - 0.15, TL.s("c5_04"), c5_s01_chicago_fair),
    (TL.s("c5_04"), TL.s("c5_06"), c5_s02_giant_egg_and_niagara),
    (TL.s("c5_06"), TL.s("c6_00"), c5_s03_royalties_and_world_map),
]


def scenes():
    return [(s[0], s[2], None) for s in SCENES]


def music(A):
    """Acto 2 triunfal: La Ciudad Blanca en Chicago (1893), Niágara y el giro amargo de las regalías."""
    t0 = TL.s("c5_00")
    t_debt = TL.s("c5_06")
    t_end = TL.s("c6_00")
    A.add_pad(t0, t_debt - t0, [130.81, 196.0, 261.63, 329.63], amp=0.044)
    A.add_pad(t_debt, t_end - t_debt, [110.0, 164.81, 220.0, 261.63], amp=0.038)


def sfx(A):
    A.fx_pop(TL.s("c5_02"), 0.08)
    A.fx_chime(TL.word("c5_03", "botón"), 0.13)
    A.fx_sparkle(TL.word("c5_03", "cien"), 0.12)
    A.fx_sweep(TL.s("c5_05"), 0.7, 150, 440, 0.08)
    A.fx_thud(TL.word("c5_07", "rompió"), 0.10)
    A.fx_pop(TL.s("c5_08"), 0.09)

