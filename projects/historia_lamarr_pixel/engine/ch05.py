"""Capítulo 5: Un piano dentro de un torpedo (c5_00..c5_10) — George Antheil, LA PIZARRA 2 (Salto de frecuencia y 88 teclas) y la patente de 1942."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa


def c5_s01_meeting_antheil(t):
    """c5_01..c5_04: Conoce a George Antheil ('el chico malo de la música') -> 16 pianolas -> La idea de saltar de canal."""
    t0 = TL.s("c5_01")
    t_c5_02 = TL.s("c5_02")
    t_diec = TL.word("c5_02", "dieciséis")
    t_c5_03 = TL.s("c5_03")
    t_c5_04 = TL.s("c5_04")
    t_salt = TL.word("c5_04", "saltara")

    cv = bg("hollywood_dining_patent").copy()
    draw_place_only(cv, "HOLLYWOOD · 1940–1941", t, t0, border=GOLD)

    draw_grand_piano_prop(cv, 326, 248, t=t, play=(t < t_c5_03 or t >= t_c5_04))
    char(cv, "hedy_inventor", 156, 248, t, scale=2,
         arms="point" if t >= t_c5_04 else "down",
         look=1, mood="worried" if (t_c5_03 <= t < t_c5_04) else "happy",
         talk=talk_v(t, t >= t_c5_04))
    char(cv, "antheil", 252, 248, t, scale=2,
         arms="type" if t < t_c5_03 else ("down" if t < t_c5_04 else "cheer"),
         look=-1 if t >= t_c5_03 else 1,
         mood="sad" if (t_c5_03 <= t < t_c5_04) else "happy",
         talk=talk_v(t, t < t_c5_04))

    window(cv, 114, 44, 252, 74, fill=(16, 22, 42), border=LAMARR_CYAN if t >= t_c5_04 else GOLD, alpha=0.94)
    if t < t_c5_02 - 0.1:
        draw_text(cv, "GEORGE ANTHEIL · COMPOSITOR", 240, 54, "press", 8, GOLD, align="center")
        draw_text(cv, "«EL CHICO MALO DE LA MÚSICA»", 240, 74, "silk", 8, CREAM, align="center")
        draw_text(cv, "VANGUARDIA Y MECÁNICA MUSICAL", 240, 92, "silk", 8, LAMARR_CYAN, align="center")
    elif t < t_c5_03 - 0.1:
        draw_text(cv, "SU OBRA «BALLET MÉCANIQUE»:", 240, 54, "silk", 8, GOLD, align="center")
        draw_text(cv, "16 PIANOLAS TOCANDO EN SINCRONÍA", 240, 74, "press", 8,
                  LAMARR_CYAN if t >= t_diec - 0.2 else CREAM, align="center")
        draw_text(cv, "+ SIRENAS Y HÉLICES DE AVIÓN", 240, 94, "silk", 8, SOFT_GRAY, align="center")
    elif t < t_c5_04 - 0.1:
        draw_text(cv, "ÉL TAMBIÉN QUERÍA AYUDAR:", 240, 54, "silk", 8, GOLD, align="center")
        draw_text(cv, "SU HERMANO MURIÓ EN LA GUERRA", 240, 74, "silk", 8, CHALK_RED, align="center")
        draw_text(cv, "CUANDO DERRIBARON SU AVIÓN", 240, 92, "silk", 8, CREAM, align="center")
    else:
        draw_text(cv, "LA IDEA DE HEDY LAMARR:", 240, 54, "silk", 8, GOLD, align="center")
        draw_text(cv, "QUE LA SEÑAL NO SE QUEDE QUIETA", 240, 74, "silk", 8, CREAM, align="center")
        if t >= t_salt - 0.35:
            draw_text(cv, "¡QUE SALTE DE CANAL TODO EL TIEMPO!", 240, 94, "press", 8, LAMARR_CYAN, align="center")
    return vignette(cv, 0.35)


def c5_s02_pizarra_hopping(t):
    """c5_05..c5_08: LA PIZARRA 2 — Lista secreta, el espía que solo oye un pedacito y los dos rollos perforados (88 frecuencias)."""
    t0 = TL.s("c5_05")
    t_c5_06 = TL.s("c5_06")
    t_c5_07 = TL.s("c5_07")
    t_rollos = TL.word("c5_07", "rollos")
    t_c5_08 = TL.s("c5_08")

    cv = draw_pizarra_frame(t, t0, "SALTO DE FRECUENCIA",
                            summary_es="88 CANALES QUE SALTAN EN SECRETO",
                            t_summary=t_c5_08)
    d = ImageDraw.Draw(cv)

    window(cv, 116, 40, 248, 160, fill=(16, 40, 28), border=CHALK_WHITE, alpha=0.96, inner=(38, 78, 54))

    if t < t_c5_07 - 0.1:
        # Paso 1 (c5_05 y c5_06): Dos amigos cambian de emisora con lista secreta -> Espía en un canal solo oye un pedacito
        hdr = "CAMBIAR JUNTOS CON LISTA SECRETA:" if t < t_c5_06 else "EL ESPÍA EN 1 CANAL OYE UN PEDACITO:"
        draw_text(cv, hdr, 240, 48, "silk", 8, CHALK_YELLOW, align="center")
        draw_freq_lanes(cv, 126, 66, 228, 96, t, n_lanes=4, speed=4.2,
                        jammed_lane=1 if t >= t_c5_06 else None,
                        hopping=True, show_labels=True)
        bot_txt = "LISTA: CH 1 -> CH 4 -> CH 2 -> CH 3" if t < t_c5_06 else "PARA BLOQUEAR: ¡HABRÍA QUE TAPAR TODOS!"
        draw_text(cv, bot_txt, 240, 170, "silk", 8,
                  CHALK_GREEN if t >= t_c5_06 else CHALK_CYAN, align="center")
    else:
        # Paso 2 (c5_07 y c5_08): Dos rollos perforados de pianola (uno en el barco, otro en el torpedo) -> 88 frecuencias
        hdr2 = "2 ROLLOS PERFORADOS IGUALES:" if t < t_c5_08 else "88 FRECUENCIAS = 88 TECLAS DEL PIANO"
        draw_text(cv, hdr2, 240, 48, "press" if t >= t_c5_08 else "silk", 8, CHALK_YELLOW, align="center")

        # Rollo 1 (Barco) a la izquierda y Rollo 2 (Torpedo) a la derecha girando exactamente al mismo ritmo
        draw_piano_roll(cv, 144, 66, 38, 86, t, speed=26.0, alpha=0.95)
        draw_piano_roll(cv, 298, 66, 38, 86, t, speed=26.0, alpha=0.95)
        draw_text(cv, "BARCO", 163, 156, "silk", 8, CHALK_CYAN, align="center")
        draw_text(cv, "TORPEDO", 317, 156, "silk", 8, CHALK_YELLOW, align="center")

        # Rayo sincronizado saltando entre ambos rollos
        hop_y = 78 + (int(t * 5.0) % 4) * 16
        d.line([(186, hop_y), (294, hop_y)], fill=(*LAMARR_CYAN, 245), width=2)
        glow(cv, 240, hop_y, 9, LAMARR_MAGENTA, 0.55)
        draw_text(cv, "SINCRONIZADOS", 240, 172, "silk", 8, CHALK_GREEN, align="center")

    return vignette(cv, 0.28)


def c5_s03_patent_1942(t):
    """c5_09..c5_10: Meses en la mesa del comedor con profesor de ingeniería -> Patente 1942 firmada Hedy Kiesler Markey."""
    t_c5_09 = TL.s("c5_09")
    t_pat = TL.word("c5_09", "patente")
    t_mark = TL.word("c5_09", "Markey")
    t_c5_10 = TL.s("c5_10")

    cv = bg("hollywood_dining_patent").copy()
    draw_place_only(cv, "AGOSTO DE 1942 · PATENTE DE EE. UU.", t, t_c5_09, border=GOLD)

    draw_table_with_prop(cv, 240, 248, prop_kind="patent" if t >= t_pat - 0.3 else "torpedo", t=t)

    char(cv, "hedy_inventor", 148, 248, t, scale=2,
         arms="write" if (t_pat <= t < t_c5_10) else "work",
         look=1, mood="happy" if t < t_c5_10 else "neutral")
    char(cv, "antheil", 312, 248, t, scale=2, arms="point_l", look=-1, mood="happy")
    char(cv, "engineer", 374, 248, t, scale=2, arms="note", look=-1, mood="happy")

    window(cv, 114, 44, 252, 78, fill=(18, 22, 42), border=GOLD, alpha=0.95)
    if t < t_c5_10 - 0.1:
        draw_text(cv, "PATENTE EE. UU. Nº 2.292.387 (1942)", 240, 54, "press", 8, GOLD, align="center")
        draw_text(cv, "«SISTEMA DE COMUNICACIÓN SECRETA»", 240, 72, "silk", 8, LAMARR_CYAN, align="center")
        if t >= t_mark - 0.6:
            draw_text(cv, "FIRMÓ: HEDY KIESLER MARKEY", 240, 92, "press", 8, CREAM, align="center")
            draw_text(cv, "(SU APELLIDO DE CASADA DE ENTONCES)", 240, 108, "silk", 8, SOFT_GRAY, align="center")
    else:
        draw_text(cv, "FIRMÓ COMO «H. K. MARKEY»", 240, 56, "silk", 8, GOLD, align="center")
        draw_text(cv, "POR ESO, DURANTE DÉCADAS,", 240, 76, "silk", 8, CREAM, align="center")
        draw_text(cv, "CASI NADIE SUPO QUE ERA SUYA.", 240, 96, "press", 8, CHALK_RED, align="center")
    return vignette(cv, 0.35)


SCENES = [
    (TL.s("c5_00") - 0.15, TL.s("c5_01"), make_card(5, ["UN PIANO EN", "UN TORPEDO"], "1940 – 1942 · HOLLYWOOD")),
    (TL.s("c5_01") - 0.15, TL.s("c5_05"), c5_s01_meeting_antheil),
    (TL.s("c5_05") - 0.15, TL.s("c5_09"), c5_s02_pizarra_hopping),
    (TL.s("c5_09") - 0.15, TL.s("c6_00"), c5_s03_patent_1942),
]


def scenes():
    return [(s[0], s[2], None, "ch05") for s in SCENES]


def music(A):
    t0 = TL.s("c5_00")
    t_piz = TL.s("c5_05")
    t_end = TL.s("c6_00")
    A.add_pad(t0, t_piz - t0, [130.81, 196.0, 261.63], amp=0.040)
    A.add_pad(t_piz, t_end - t_piz, [130.81, 196.0, 261.63, 329.63], amp=0.044)


def sfx(A):
    A.fx_pop(TL.s("c5_01"), 0.08)
    A.fx_sparkle(TL.word("c5_02", "dieciséis"), 0.09)
    A.fx_chime(TL.word("c5_04", "saltara"), 0.11)
    A.fx_pop(TL.s("c5_05"), 0.09)
    A.fx_pop(TL.word("c5_07", "rollos"), 0.09)
    A.fx_sparkle(TL.s("c5_08"), 0.11)
    A.fx_chime(TL.word("c5_09", "patente"), 0.11)
    A.fx_thud(TL.s("c5_10"), 0.09)
