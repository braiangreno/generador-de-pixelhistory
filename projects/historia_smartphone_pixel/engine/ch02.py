"""Capítulo 2: El panal (Antena única vs celdas hexagonales + La Pizarra 1 + Bell Labs y Joel Engel)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa


def c2_s01_single_antenna_bottleneck(t):
    """c2_01..c2_02: Una sola antena gigante para toda Nueva York, 2.000 abonados para 12 canales."""
    t0 = TL.s("c2_01")
    t_c2_02 = TL.s("c2_02")

    cv = bg("nyc_sixth_ave_1973").copy()
    draw_place_only(cv, "NUEVA YORK · RED ANTERIOR (12 CANALES)", t, t0, border=CHALK_RED)
    d = ImageDraw.Draw(cv)

    window(cv, 118, 44, 244, 118, fill=(20, 22, 38), border=CHALK_RED if t >= t_c2_02 else GOLD)
    if t < t_c2_02:
        draw_text(cv, "UNA SOLA ANTENA GIGANTE", 240, 52, "press", 8, GOLD, align="center")
        # Torre central grande emitiendo ondas para toda la ciudad
        d.line([(240, 76), (226, 134)], fill=(188, 196, 214, 255), width=2)
        d.line([(240, 76), (254, 134)], fill=(188, 196, 214, 255), width=2)
        d.line([(228, 104), (252, 104)], fill=(188, 196, 214, 255), width=2)
        for r_w in (16, 28, 40):
            d.arc([240 - r_w, 76 - r_w // 2, 240 + r_w, 76 + r_w // 2], 180, 360, fill=(*TESLA_CYAN, 200), width=2)
        draw_text(cv, "PARA TODA LA CIUDAD", 240, 142, "silk", 8, CREAM, align="center")
    else:
        draw_text(cv, "2.000 ABONADOS · 12 CANALES", 240, 52, "press", 8, CHALK_RED, align="center")
        # 12 casilleros de canales llenos en rojo
        for i in range(12):
            cx = 136 + (i % 6) * 36
            cy = 74 + (i // 6) * 22
            d.rectangle([cx, cy, cx + 28, cy + 16], fill=(168, 44, 44, 255), outline=(*GOLD, 255))
            draw_text(cv, f"C{i+1}", cx + 14, cy + 4, "silk", 8, CREAM, align="center", outline=None, shadow=False)
        draw_text(cv, "OCUPADO · ESPERAR 30 MINUTOS", 240, 126, "silk", 8, GOLD, align="center")
        draw_text(cv, "FILA DE ESPERA PARA HABLAR", 240, 142, "silk", 8, CREAM, align="center")

    char(cv, "passerby_73_a", 156, 248, t, scale=2, arms="hips", look=1, mood="worried")
    char(cv, "passerby_73_b", 324, 248, t, scale=2, arms="cross", facing=-1, look=-1, mood="sad")
    return vignette(cv, 0.36)


def c2_s02_pizarra_honeycomb(t):
    """c2_03..c2_07: LA PIZARRA 1 — El Panal Celular (celdas chicas, reúso de canales y traspaso/handoff)."""
    t0 = TL.s("c2_03")
    t_c2_04 = TL.s("c2_04")
    t_c2_05 = TL.s("c2_05")
    t_c2_06 = TL.s("c2_06")
    t_c2_07 = TL.s("c2_07")

    cv = draw_pizarra_frame(
        t, t0, "EL PANAL CELULAR",
        summary_es="MUCHAS CELDAS CHICAS = MILLONES DE LLAMADAS",
        t_summary=t_c2_07,
    )
    d = ImageDraw.Draw(cv)

    if t < t_c2_04:
        # Paso 1: Una antena grande -> pocos canales -> saturado
        window(cv, 118, 46, 244, 142, fill=BOARD_DARK, border=CHALK_WHITE, alpha=0.92)
        draw_text(cv, "1 ANTENA GRANDE = POCOS CANALES", 240, 56, "silk", 8, CHALK_YELLOW, align="center")
        d.ellipse([186, 76, 294, 164], outline=(*CHALK_RED, 255), width=2)
        d.line([(240, 102), (232, 134)], fill=(*CHALK_WHITE, 255), width=2)
        d.line([(240, 102), (248, 134)], fill=(*CHALK_WHITE, 255), width=2)
        draw_text(cv, "12 / 12 OCUPADOS", 240, 144, "press", 8, CHALK_RED, align="center")
        draw_text(cv, "NADIE MÁS HABLA", 240, 166, "silk", 8, CHALK_WHITE, align="center")
        draw_chalk_hand(cv, 288, 128, t)
    elif t < t_c2_05:
        # Paso 2: Dividir la ciudad en celdas hexagonales como un panal de abejas
        window(cv, 118, 46, 244, 142, fill=BOARD_DARK, border=CHALK_YELLOW, alpha=0.92)
        draw_text(cv, "PARTIR LA CIUDAD EN CELDAS CHICAS", 240, 54, "silk", 8, CHALK_YELLOW, align="center")
        draw_honeycomb_grid(cv, 240, 118, r_cell=18, ring=1, t=t, color=CHALK_CYAN,
                            fill_col=BOARD_GREEN, highlight_idx=int((t - t_c2_04) * 3) % 7)
        draw_text(cv, "CADA CELDA TIENE SU ANTENA CHICA", 240, 168, "silk", 8, CHALK_WHITE, align="center")
        draw_chalk_hand(cv, 272, 124, t)
    elif t < t_c2_06:
        # Paso 3: Dos celdas separadas reúsan el mismo canal sin pisarse
        window(cv, 118, 46, 244, 142, fill=BOARD_DARK, border=CHALK_GREEN, alpha=0.92)
        draw_text(cv, "REÚSO DE CANALES SIN PISARSE", 240, 54, "silk", 8, CHALK_GREEN, align="center")
        labels = ["C2", "C1", "C3", "C4", "C1", "C5", "C6"]
        draw_honeycomb_grid(cv, 240, 118, r_cell=18, ring=1, t=t, color=CHALK_WHITE,
                            fill_col=BOARD_GREEN, highlight_idx=(1, 4), channel_labels=labels)
        draw_text(cv, "EL CANAL C1 SIRVE MUCHAS VECES", 240, 168, "silk", 8, CHALK_YELLOW, align="center")
    else:
        # Paso 4 (c2_06..c2_07): Cuando te mueves, la llamada pasa de una celda a la siguiente
        window(cv, 118, 42, 244, 152, fill=BOARD_DARK, border=CHALK_CYAN, alpha=0.92)
        draw_text(cv, "PASO DE UNA ANTENA A LA SIGUIENTE", 240, 50, "silk", 8, CHALK_CYAN, align="center")
        u_move = clamp01((t - t_c2_06) / 3.2)
        active_c = 1 if u_move < 0.35 else (0 if u_move < 0.7 else 4)
        draw_honeycomb_grid(cv, 240, 112, r_cell=18, ring=1, t=t, color=CHALK_WHITE,
                            fill_col=BOARD_GREEN, highlight_idx=active_c)
        # Punto móvil cruzando las celdas sin cortarse
        px = int(round(208 + 64 * u_move))
        draw_phosphor_dot(cv, px, 112, r=3, color=CHALK_YELLOW)
        draw_text(cv, "POR ESO SE LLAMA CELULAR: POR LAS CELDAS", 240, 164, "silk", 8, CHALK_YELLOW, align="center")

    return cv


def c2_s03_bell_labs_engel(t):
    """c2_08..c2_09: Bell Labs (1947) y el equipo de Joel Engel diseñando la red celular del rival."""
    t0 = TL.s("c2_08")
    t_c2_09 = TL.s("c2_09")

    cv = bg("bell_labs_honeycomb_1970").copy()
    draw_place_only(cv, "BELL LABS · 1947 – 1973", t, t0, border=TESLA_CYAN)

    # Escritorio con teléfono de disco y planos celulares
    draw_rotary_phone_table(cv, 210, 248, t, ringing=False, off_hook=False)
    char(cv, "engel_bell", 276, 248, t, scale=2,
         arms="point" if t < t_c2_09 else "cross",
         facing=-1, look=-1, mood="neutral")
    char(cv, "motorola_eng", 142, 248, t, scale=2, arms="note", look=1)

    window(cv, 118, 44, 244, 96, fill=(16, 26, 44), border=GOLD if t >= t_c2_09 else TESLA_CYAN)
    if t < t_c2_09 - 0.1:
        draw_text(cv, "IDEA NACIDA EN BELL LABS (1947)", 240, 54, "silk", 8, TESLA_CYAN, align="center")
        draw_honeycomb_grid(cv, 240, 92, r_cell=11, ring=1, t=t, color=TESLA_CYAN, highlight_idx=0)
        draw_text(cv, "EQUIPO DE JOEL ENGEL", 240, 122, "press", 8, GOLD, align="center")
    else:
        draw_text(cv, "LA PARADOJA DE 1973:", 240, 54, "silk", 8, GOLD, align="center")
        draw_text(cv, "COOPER HIZO EL TELÉFONO", 240, 74, "press", 8, CREAM, align="center")
        draw_text(cv, "SU RIVAL DISEÑABA LA RED", 240, 96, "press", 8, TESLA_CYAN, align="center")
        draw_text(cv, "SE NECESITABAN EL UNO AL OTRO", 240, 118, "silk", 8, CHALK_GREEN, align="center")

    return vignette(cv, 0.36)


def scenes():
    return [
        (TL.s("c2_00") - 0.15, make_card(2, ["EL PANAL"], "1947 – 1973 · BELL LABS Y NUEVA YORK"),
         None, "ch02"),
        (TL.s("c2_01") - 0.15, c2_s01_single_antenna_bottleneck,
         lambda t: cam_push(t, TL.s("c2_01"), TL.s("c2_03"), 1.0, 1.03, (240, 135)), "ch02"),
        (TL.s("c2_03") - 0.15, c2_s02_pizarra_honeycomb,
         None, "ch02"),
        (TL.s("c2_08") - 0.15, c2_s03_bell_labs_engel,
         lambda t: cam_push(t, TL.s("c2_08"), TL.s("c3_00"), 1.0, 1.03, (240, 135)), "ch02"),
    ]


def music(A):
    t0 = TL.s("c2_00")
    t_end = TL.s("c3_00")
    A.add_pad(t0, t_end - t0, [130.81, 196.0, 246.94], amp=0.036)


def sfx(A):
    A.fx_pop(TL.s("c2_02"), 0.08)
    A.fx_sweep(TL.s("c2_03"), 0.4, 200, 420, 0.06)
    A.fx_sparkle(TL.s("c2_07"), 0.09)
    A.fx_chime(TL.s("c2_09"), 0.10)
