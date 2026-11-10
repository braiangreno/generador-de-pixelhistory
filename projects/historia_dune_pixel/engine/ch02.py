"""Capítulo 2: Más de veinte rechazos (c2_00..c2_06)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa
from ch01 import HERBERT, READER_1, READER_2

LANIER = {
    "name": "Sterling Lanier",
    "skin": (235, 194, 156), "hair": (76, 56, 40), "hair_style": "parted",
    "glasses": True,
    "shirt": (240, 244, 250), "jacket": (44, 62, 92),
    "tie": (180, 48, 48), "pants": (38, 48, 70),
}
PUBLISHER_NO = {
    "name": "Publisher No",
    "skin": (226, 184, 148), "hair": (130, 130, 138), "hair_style": "bald",
    "shirt": (230, 230, 235), "jacket": (72, 72, 82),
    "tie": (90, 90, 105), "pants": (54, 54, 64),
}


# ===========================================================================
# ESCENA 7 (c2_01): Más de veinte rechazos editoriales
# ===========================================================================
def scene_twenty_rejections(t):
    t0 = TL.s("c2_01")
    dur = max(1.0, TL.e("c2_01") - t0)
    u = clamp01((t - t0) / dur)
    cv = bg("bg_chilton_office_1965").copy()
    cv = grade(cv, mul=(0.82, 0.78, 0.85), add=(8, 0, 6), sat=0.85, k=0.9)

    t_larga = TL.word("c2_01", "larga")
    t_complicada = TL.word("c2_01", "complicada")
    t_rara = TL.word("c2_01", "rara")

    # Sacudida en cada golpe de rechazo sincronizado con la palabra exacta del narrador
    dx, dy = 0, 0
    for t_beat in (t_larga, t_complicada, t_rara):
        sx, sy = shake(t, t_beat, dur=0.22, amp=3)
        dx += sx
        dy += sy

    window(cv, 16, 10, 448, 36, fill=(32, 14, 18), border=RED, alpha=0.95)
    n_rej = min(23, int(1 + u * 24))
    draw_text(cv, f"EDITORIALES QUE DIJERON NO: {n_rej}+", 240, 16, "press", 8, RED, align="center")
    draw_text(cv, "EL MANUSCRITO REBOTA DE PUERTA EN PUERTA", 240, 30, "silk", 8, CREAM, align="center",
              reveal=(t - t0) * 32)

    # Herbert se acerca con el manuscrito al principio; el editor lo rechaza en cada argumento ("larga", "complicada", "rara")
    hx, hph = walk(t, t0, t0 + 0.85, 52, 98)
    h_arms = "shrug" if t >= t_rara else "hold"
    p_arms = "point_l" if (t_larga <= t < t_complicada or t >= t_rara) else "cross"
    char(cv, HERBERT, hx, 260, t, scale=2, walk=hph, arms=h_arms, look=1, mood="sad")
    char(cv, PUBLISHER_NO, 392, 260, t, scale=2, arms=p_arms, look=-1, mood="angry",
         talk=talk_v(t, t >= t_larga))

    # Tres grandes sellos de rechazo sincronizados con "larga", "complicada" y "rara"
    reasons = [
        ("DEMASIADO LARGA", t_larga),
        ("DEMASIADO COMPLICADA", t_complicada),
        ("DEMASIADO RARA", t_rara),
    ]
    for idx, (txt, t_st) in enumerate(reasons):
        if t >= t_st:
            ast, dyst = pop(t, t_st, dur=0.25)
            ry = 60 + idx * 46 + dyst
            window(cv, 144, ry, 206, 38, fill=(76, 18, 22), border=RED, alpha=0.96 * ast)
            draw_text(cv, f"RECHAZO #{idx * 7 + 5}", 247, ry + 8, "silk", 8, GOLD, align="center")
            draw_text(cv, txt, 247, ry + 21, "press", 8, CREAM, align="center")

    return offset_canvas(cv, dx, dy)


# ===========================================================================
# ESCENA 8 (c2_02, c2_03): Chilton Books (manuales de autos) y Sterling Lanier
# ===========================================================================
def scene_chilton_lanier(t):
    t2 = TL.s("c2_02")
    t3 = TL.s("c2_03")
    cv = bg("bg_chilton_office_1965").copy()
    d = ImageDraw.Draw(cv)

    window(cv, 16, 10, 448, 36, fill=(14, 24, 38), border=GOLD, alpha=0.95)
    if t < t3:
        draw_text(cv, "EDITORIAL CHILTON · FILADELFIA", 240, 16, "press", 8, GOLD, align="center")
        draw_text(cv, "FAMOSA POR SUS MANUALES PARA ARREGLAR AUTOS", 240, 30, "silk", 8, CYAN, align="center",
                  reveal=(t - t2) * 32)
    else:
        draw_text(cv, "EL EDITOR STERLING LANIER APUESTA POR DUNE", 240, 16, "press", 8, GOLD, align="center")
        draw_text(cv, "LEYÓ LA REVISTA Y PAGÓ US$ 7.500 DE ADELANTO", 240, 30, "silk", 8, GREEN, align="center",
                  reveal=(t - t3) * 32)

    # Estante visual de manuales de mecánica automotriz a la izquierda con pop()
    a_cat, dy_cat = pop(t, t2 + 0.05)
    window(cv, 20, 56 + dy_cat, 176, 94, fill=(18, 28, 48), border=CYAN, alpha=0.94 * a_cat)
    draw_text(cv, "CATÁLOGO CHILTON", 108, 64 + dy_cat, "press", 8, CYAN, align="center")
    for idx, m_lbl in enumerate(("MOTOR V8 · 1964", "FRENOS Y CAJA", "CARBURADORES")):
        my = 80 + idx * 20 + dy_cat
        d.rectangle([30, my, 186, my + 16], fill=(34, 58, 96, 255), outline=(*GOLD, 255))
        draw_text(cv, m_lbl, 108, my + 4, "silk", 8, CREAM, align="center")

    # Retrato y contrato de Sterling Lanier a la derecha
    a_lan, dy_lan = pop(t, t2 + 0.25)
    window(cv, 212, 56 + dy_lan, 248, 94, fill=(22, 32, 24), border=GREEN if t >= t3 else GOLD, alpha=0.95 * a_lan)
    portrait(cv, "lanier", 222, 66 + dy_lan, 64)
    draw_text(cv, "STERLING LANIER", 296, 68 + dy_lan, "press", 8, GOLD)
    draw_text(cv, "EDITOR DE CHILTON", 296, 84 + dy_lan, "silk", 8, CYAN)
    if t < t3:
        draw_text(cv, "«YO PUBLICO ESTA", 296, 102 + dy_lan, "silk", 8, CREAM, reveal=(t - t2 - 0.3) * 28)
        draw_text(cv, "NOVELA.»", 296, 116 + dy_lan, "silk", 8, CREAM, reveal=(t - t2 - 0.7) * 28)
    else:
        a_dl, dy_dl = pop(t, t3 + 0.1)
        window(cv, 294, 100 + dy_dl, 154, 38, fill=(18, 68, 32), border=GREEN, alpha=0.98 * a_dl)
        draw_text(cv, "ADELANTO FIRMADO", 371, 107 + dy_dl, "silk", 8, CREAM, align="center")
        draw_text(cv, "US$ 7.500", 371, 121 + dy_dl, "press", 8, GOLD, align="center")
        sparkle(cv, 304, 110 + dy_dl, t, 3)

    # Herbert presenta el manuscrito; Lanier avanza al ser nombrado ("Sterling Lanier"), lee la revista y cierra el acuerdo en "siete mil quinientos"
    t_aposto = TL.word("c2_03", "aposto")
    lx, lph = walk(t, t3 - 0.1, t3 + 0.75, 368, 304)
    char(cv, HERBERT, 136, 260, t, scale=2,
         arms="cheer" if t >= t_aposto else ("point" if t >= t3 else "hold"),
         look=1, mood="happy")
    char(cv, LANIER, lx, 260, t, scale=2, walk=lph,
         arms="point_l" if t >= t_aposto else ("note" if t >= t3 else "hips"),
         look=-1, mood="happy", talk=talk_v(t, t >= t3))

    return cv


# ===========================================================================
# ESCENA 9 (c2_04, c2_05, c2_06): Despido de Lanier y Premios Hugo + Nébula (1966)
# ===========================================================================
def scene_release_and_awards(t):
    t4 = TL.s("c2_04")
    t5 = TL.s("c2_05")
    t6 = TL.s("c2_06")
    dx, dy = shake(t, t5 + 0.15, dur=0.25, amp=3)
    cv = bg("bg_bookstore_1965").copy()
    d = ImageDraw.Draw(cv)

    window(cv, 16, 10, 448, 36, fill=(24, 18, 14), border=GOLD, alpha=0.95)
    if t < t5:
        draw_text(cv, "AGOSTO DE 1965 · PRIMERA EDICIÓN", 240, 16, "press", 8, GOLD, align="center")
        draw_text(cv, "PRECIO: US$ 5,95 · CARO Y DE VENTAS LENTAS", 240, 30, "silk", 8, CYAN, align="center",
                  reveal=(t - t4) * 32)
    elif t < t6:
        draw_text(cv, "CONSECUENCIA EN LA EDITORIAL CHILTON", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "A STERLING LANIER LO DESPIDIERON", 240, 30, "press", 8, RED, align="center",
                  reveal=(t - t5) * 30)
    else:
        draw_text(cv, "1966 · GIRO HISTÓRICO Y BOCA EN BOCA", 240, 16, "press", 8, GOLD, align="center")
        draw_text(cv, "GANA LOS DOS PREMIOS MÁS IMPORTANTES DEL GÉNERO", 240, 30, "silk", 8, GREEN, align="center",
                  reveal=(t - t6) * 32)

    if t < t6:
        # Libro caro en vidriera y despido de Lanier
        a_w, dy_w = pop(t, t4 + 0.05)
        window(cv, 148, 58 + dy_w, 184, 86, fill=(32, 20, 18), border=RED if t >= t5 else GOLD, alpha=0.95 * a_w)
        draw_text(cv, "DUNE (1965)", 240, 68 + dy_w, "press", 8, GOLD, align="center")
        draw_text(cv, "PRECIO: US$ 5,95", 240, 86 + dy_w, "silk", 8, CREAM, align="center")
        if t < t5:
            t_caro = TL.word("c2_04", "caro")
            if t >= t_caro:
                draw_text(cv, "VENTAS INICIALES BAJAS", 240, 106 + dy_w, "silk", 8, RED, align="center")
            lx, lph = 112, None
            hx, hph = 368, None
        else:
            a_f, dy_f = pop(t, t5 + 0.05, dur=0.25)
            window(cv, 164, 102 + dy_f, 152, 28, fill=(130, 22, 22), border=RED, alpha=0.98 * a_f)
            draw_text(cv, "LANIER DESPEDIDO", 240, 112 + dy_f, "press", 8, CREAM, align="center")
            lx, lph = walk(t, t5 + 0.1, TL.e("c2_05"), 112, 38)
            hx, hph = 368, None

        char(cv, LANIER, lx, 260, t, scale=2, walk=lph,
             arms="down" if t >= t5 else ("shrug" if t >= TL.word("c2_04", "caro") else "hold"),
             look=-1 if t >= t5 else 1, mood="sad")
        char(cv, HERBERT, hx, 260, t, scale=2, walk=hph,
             arms="shrug" if t >= TL.word("c2_04", "caro") else "hold", look=-1, mood="sad")
    else:
        # 1966: Premios Nébula y Hugo ("ganó los dos premios") + lectores pasándose el libro en "pasar de mano en mano"
        t_mano = TL.word("c2_06", "mano")
        CONF.draw(cv, t)
        a_n, dy_n = pop(t, t6 + 0.05)
        window(cv, 56, 56 + dy_n, 174, 86, fill=(28, 24, 12), border=GOLD, alpha=0.96 * a_n)
        draw_text(cv, "PREMIO NÉBULA", 143, 68 + dy_n, "press", 8, GOLD, align="center")
        draw_text(cv, "1966 · MEJOR NOVELA", 143, 86 + dy_n, "silk", 8, CREAM, align="center")
        draw_text(cv, "1ª EDICIÓN DEL PREMIO", 143, 104 + dy_n, "silk", 8, CYAN, align="center")

        a_h, dy_h = pop(t, t6 + 0.35)
        window(cv, 250, 56 + dy_h, 174, 86, fill=(28, 24, 12), border=GOLD, alpha=0.96 * a_h)
        draw_text(cv, "PREMIO HUGO", 337, 68 + dy_h, "press", 8, GOLD, align="center")
        draw_text(cv, "1966 · MEJOR NOVELA", 337, 86 + dy_h, "silk", 8, CREAM, align="center")
        draw_text(cv, "CONSAGRACIÓN MUNDIAL", 337, 104 + dy_h, "silk", 8, GREEN, align="center")

        # Herbert festeja los premios; cuando el audio dice "pasar de mano en mano", el lector 1 le entrega el ejemplar al lector 2
        r1x, r1ph = walk(t, t_mano - 0.25, t_mano + 0.45, 208, 246)
        char(cv, HERBERT, 88, 260, t, scale=2, arms="cheer", look=1, mood="happy")
        char(cv, READER_1, r1x, 260, t, scale=2, walk=r1ph,
             arms="point" if t >= t_mano else "hold", look=1, mood="happy")
        char(cv, READER_2, 344, 260, t, scale=2,
             arms="hold" if t >= t_mano else "hips", look=-1, mood="happy")
        if t >= t_mano - 0.15:
            u_pass = ease_in_out(prog(t, t_mano - 0.1, TL.e("c2_06") - 0.15))
            bx = int(260 + 62 * u_pass)
            by = int(210 - math.sin(u_pass * math.pi) * 14)
            d.rectangle([bx - 10, by, bx + 10, by + 22], fill=(238, 174, 58, 255), outline=(*INK, 255))

    return offset_canvas(cv, dx, dy)


def scenes():
    return [
        (TL.chapter_start(2) - 0.3, make_card(2, ["MÁS DE VEINTE", "RECHAZOS"], "1965 - 1966 · CHILTON BOOKS Y PREMIOS"), None),
        (TL.s("c2_01") - 0.15, scene_twenty_rejections, lambda t: cam_push(t, TL.s("c2_01"), TL.s("c2_02"), 1.0, 1.09, (240, 135), (247, 130))),
        (TL.s("c2_02") - 0.15, scene_chilton_lanier, lambda t: (1.0 + cam_punch(t, [TL.s("c2_03") + 0.1], 0.07), 240, 140)),
        (TL.s("c2_04") - 0.15, scene_release_and_awards, lambda t: (1.0 + cam_punch(t, [TL.s("c2_05") + 0.1, TL.s("c2_06") + 0.1], 0.07), 240, 140)),
    ]
