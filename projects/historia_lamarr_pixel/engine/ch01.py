"""Apertura: Auriculares, Hollywood y el cajón (s01..s05) + Capítulo 1: La caja de música (c1_00..c1_06)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa


def s01_wireless_and_hollywood(t):
    """s01..s02: Auriculares inalámbricos saltando más de mil veces por segundo -> Actriz de Hollywood y pianista."""
    t_s01 = TL.s("s01")
    t_mil = TL.word("s01", "mil")
    t_s02 = TL.s("s02")
    t_pian = TL.word("s02", "pianista")

    if t < t_s02 - 0.15:
        cv = bg("hall_of_fame_modern").copy()
        draw_place_only(cv, "AHORA MISMO · TUS AURICULARES", t, t_s01, border=LAMARR_CYAN)

        # Panel central mostrando el salto entre canales > 1.000 veces/s
        window(cv, 118, 44, 244, 114, fill=(12, 20, 42), border=LAMARR_CYAN, alpha=0.94)
        lbl_top = "SEÑAL INALÁMBRICA · SALTO CONTINUO" if t < t_mil else "+1.000 SALTOS POR SEGUNDO"
        draw_text(cv, lbl_top, 240, 52, "silk", 8, GOLD if t >= t_mil else LAMARR_CYAN, align="center")
        draw_freq_lanes(cv, 128, 68, 224, 82, t, n_lanes=5, speed=6.5 if t >= t_mil else 3.5,
                        hopping=True, show_labels=True)

        # Mesa en el suelo con los auriculares inalámbricos y una oyente moderna
        draw_table_with_prop(cv, 288, 248, prop_kind="headphones", t=t)
        char(cv, "user", 176, 248, t, scale=2, arms="wave" if t >= t_mil else "down",
             look=1, mood="happy")
        return vignette(cv, 0.36)

    # s02: Actriz de Hollywood junto a un pianista en plena guerra
    cv = bg("hollywood_dining_patent").copy()
    draw_place_only(cv, "HOLLYWOOD · EN PLENA GUERRA (1942)", t, t_s02, border=GOLD)

    window(cv, 118, 46, 244, 62, fill=(22, 18, 36), border=GOLD, alpha=0.94)
    draw_text(cv, "PATENTE DE GUERRA · EE. UU.", 240, 54, "silk", 8, GOLD, align="center")
    draw_text(cv, "UNA ACTRIZ + UN PIANISTA", 240, 72, "press", 8,
              LAMARR_CYAN if t >= t_pian - 0.2 else CREAM, align="center")
    draw_text(cv, "EL ORIGEN DEL SALTO DE FRECUENCIA", 240, 90, "silk", 8, SOFT_GRAY, align="center")

    # Piano apoyado en el suelo + Hedy glamurosa y Antheil al piano
    draw_grand_piano_prop(cv, 326, 248, t=t, play=True)
    char(cv, "hedy_glam", 156, 248, t, scale=2, arms="point", look=1, mood="happy")
    char(cv, "antheil", 268, 248, t, scale=2, arms="type", look=1, mood="happy")
    return vignette(cv, 0.35)


def s03_navy_drawer_and_title(t):
    """s03..s05: La Marina la guarda en un cajón -> 'Mejor ayude con su cara' -> Título del episodio."""
    t_s03 = TL.s("s03")
    t_cajon = TL.word("s03", "cajón")
    t_s04 = TL.s("s04")
    t_s05 = TL.s("s05")
    t_inv = TL.word("s05", "inventora")

    if t < t_s05 - 0.15:
        cv = bg("navy_office_1942").copy()
        draw_place_only(cv, "MARINA DE EE. UU. · 1942", t, t_s03, border=AMBER)

        open_k = 1.0 - clamp01((t - t_cajon) / 0.55) if t >= t_cajon - 0.2 else 1.0
        draw_table_with_prop(cv, 240, 248, prop_kind="drawer", t=t, open_p=open_k)

        char(cv, "navy_officer", 148, 248, t, scale=2,
             arms="point" if t >= t_s04 else "work", look=1, mood="neutral",
             talk=talk_v(t, t >= t_s04))
        char(cv, "hedy_glam", 332, 248, t, scale=2,
             arms="hips" if t >= t_s04 else "offer", look=-1,
             mood="sad" if t >= t_cajon else "neutral")

        window(cv, 118, 48, 244, 58, fill=(18, 24, 38), border=CHALK_RED if t >= t_cajon else GOLD)
        if t < t_s04 - 0.1:
            draw_text(cv, "PATENTE Nº 2.292.387", 240, 58, "silk", 8, CREAM, align="center")
            draw_text(cv, "ARCHIVADA EN UN CAJÓN", 240, 76, "press", 8, CHALK_RED, align="center")
        else:
            draw_text(cv, "RESPUESTA OFICIAL:", 240, 58, "silk", 8, GOLD, align="center")
            draw_text(cv, "«MEJOR AYUDE CON SU CARA»", 240, 76, "press", 8, CREAM, align="center")
        return vignette(cv, 0.38)

    # s05: Tarjeta de título principal de «UN PIANO DENTRO DE UN TORPEDO»
    cv = bg("hollywood_dining_patent").copy()
    cv = grade(cv, mul=(0.85, 0.88, 1.05))
    draw_place_only(cv, "VIENA (1914) -> HOLLYWOOD -> HOY", t, t_s05, border=LAMARR_CYAN)

    a, dy = pop(t, t_s05 - 0.1)
    window(cv, 114, 44 + dy, 252, 112, fill=(14, 18, 38), border=GOLD, alpha=0.95)
    draw_text(cv, "UN PIANO DENTRO", 240, 54 + dy, "press", 16, align="center",
              gradient=GOLD_RAMP, outline_w=2, reveal=max(1, int((t - t_s05 + 0.2) * 24)))
    draw_text(cv, "DE UN TORPEDO", 240, 78 + dy, "press", 16, align="center",
              gradient=GOLD_RAMP, outline_w=2, reveal=max(0, int((t - t_s05 - 0.15) * 24)))
    draw_text(cv, "LA HISTORIA DE HEDY LAMARR", 240, 108 + dy, "silk", 8, LAMARR_CYAN, align="center",
              reveal=max(0, int((t - t_s05 - 0.4) * 32)))
    sub_role = "ACTRIZ · Y UNA INVENTORA" if t >= t_inv - 0.2 else "«LA MUJER MÁS LINDA DEL MUNDO»"
    draw_text(cv, sub_role, 240, 126 + dy, "press", 8,
              GOLD if t >= t_inv - 0.2 else CREAM, align="center")

    draw_table_with_prop(cv, 306, 248, prop_kind="torpedo", t=t)
    char(cv, "hedy_inventor" if t >= t_inv - 0.2 else "hedy_glam", 174, 248, t, scale=2,
         arms="cheer" if t >= t_inv - 0.1 else "hips", look=1, mood="happy")
    return vignette(cv, 0.34)


# ===========================================================================
# CAPÍTULO 1: LA CAJA DE MÚSICA (c1_00 .. c1_06)
# ===========================================================================

def c1_s01_vienna_walks(t):
    """c1_01..c1_02: Nace en Viena en 1914 como Hedwig Kiesler -> caminatas con su padre explicando cómo funcionan las cosas."""
    t0 = TL.s("c1_01")
    t_c1_02 = TL.s("c1_02")
    t_tran = TL.word("c1_02", "tranvías")
    t_imp = TL.word("c1_02", "imprenta")
    t_elec = TL.word("c1_02", "electricidad")

    cv = bg("vienna_street_1914").copy()
    draw_place_only(cv, "VIENA, AUSTRIA · 1914", t, t0, border=GOLD)

    if t < t_c1_02 - 0.15:
        window(cv, 118, 48, 244, 62, fill=(20, 22, 38), border=GOLD, alpha=0.94)
        draw_text(cv, "HEDWIG KIESLER (VIENA, 1914)", 240, 58, "press", 8, GOLD, align="center")
        draw_text(cv, "PADRE: DIRECTOR DE BANCO", 240, 76, "silk", 8, CREAM, align="center")
        draw_text(cv, "MADRE: PIANISTA DE CONCIERTO", 240, 92, "silk", 8, LAMARR_CYAN, align="center")

        char(cv, "father_kiesler", 156, 248, t, scale=2, arms="down", look=1, mood="happy")
        char(cv, "hedy_child", 240, 248, t, scale=2, arms="wave", look=1, mood="happy")
        char(cv, "mother_pianist", 324, 248, t, scale=2, arms="down", look=-1, mood="happy")
        return vignette(cv, 0.35)

    # c1_02: Caminata de padre e hija por Viena explicando tranvías, imprenta y electricidad
    x_f, w_f = walk(t, t_c1_02, t_elec + 0.6, 124, 212)
    x_h, w_h = walk(t, t_c1_02, t_elec + 0.6, 184, 276)

    char(cv, "father_kiesler", x_f, 248, t, scale=2, walk=w_f,
         arms="point", look=1, mood="happy", talk=talk_v(t, True))
    char(cv, "hedy_child", x_h, 248, t, scale=2, walk=w_h,
         arms="think" if t >= t_imp else "down", look=-1, mood="happy")

    window(cv, 118, 48, 244, 66, fill=(16, 24, 42), border=LAMARR_CYAN, alpha=0.94)
    draw_text(cv, "¿CÓMO FUNCIONAN LAS COSAS?", 240, 56, "silk", 8, GOLD, align="center")
    item_txt = "1. LOS TRANVÍAS ELÉCTRICOS"
    if t >= t_elec - 0.15:
        item_txt = "3. LA ELECTRICIDAD Y LOS CABLES"
    elif t >= t_imp - 0.15:
        item_txt = "2. LAS MÁQUINAS DE IMPRENTA"
    draw_text(cv, item_txt, 240, 76, "press", 8, LAMARR_CYAN, align="center")
    draw_text(cv, "CURIOSIDAD MECÁNICA DESDE NIÑA", 240, 94, "silk", 8, CREAM, align="center")
    return vignette(cv, 0.35)


def c1_s02_piano_and_music_box(t):
    """c1_03..c1_04: Su madre le enseña las 88 teclas del piano -> A los 5 años desarma y rearma su caja de música."""
    t_c1_03 = TL.s("c1_03")
    t_teclas = TL.word("c1_03", "ochenta")
    t_c1_04 = TL.s("c1_04")
    t_des = TL.word("c1_04", "desarmó")
    t_arm = TL.word("c1_04", "armar")

    cv = bg("vienna_parlor_piano").copy()
    draw_place_only(cv, "VIENA · SALÓN FAMILIAR", t, t_c1_03, border=GOLD)

    if t < t_c1_04 - 0.15:
        draw_grand_piano_prop(cv, 286, 248, t=t, play=True)
        char(cv, "mother_pianist", 154, 248, t, scale=2, arms="point", look=1, mood="happy",
             talk=talk_v(t, t < t_teclas))
        char(cv, "hedy_child", 224, 248, t, scale=2, arms="type", look=1, mood="happy")

        window(cv, 118, 46, 244, 62, fill=(24, 18, 32), border=GOLD, alpha=0.94)
        draw_text(cv, "CLASES DE PIANO CON SU MADRE", 240, 56, "silk", 8, CREAM, align="center")
        draw_text(cv, "88 TECLAS = 88 NOTAS", 240, 74, "press", 8,
                  LAMARR_CYAN if t >= t_teclas - 0.2 else GOLD, align="center")
        draw_text(cv, "UN NÚMERO QUE VOLVERÁ EN 1941", 240, 92, "silk", 8, SOFT_GRAY, align="center")
        return vignette(cv, 0.35)

    # c1_04: A los 5 años desarma su caja de música para entender cómo suena y la vuelve a armar
    open_k = 1.0 if (t_des - 0.2 <= t < t_arm - 0.2) else 0.35
    draw_table_with_prop(cv, 256, 248, prop_kind="music_box", t=t, open_p=open_k)
    char(cv, "hedy_child", 178, 248, t, scale=2,
         arms="cheer" if t >= t_arm - 0.15 else "work", look=1, mood="happy")

    window(cv, 118, 46, 244, 66, fill=(20, 22, 38), border=LAMARR_CYAN, alpha=0.94)
    draw_text(cv, "A LOS 5 AÑOS · CAJA DE MÚSICA", 240, 56, "silk", 8, GOLD, align="center")
    state_txt = "1. LA DESARMA PIEZA POR PIEZA" if t < t_arm - 0.2 else "2. ¡LA VUELVE A ARMAR Y FUNCIONA!"
    draw_text(cv, state_txt, 240, 74, "press", 8,
              CHALK_GREEN if t >= t_arm - 0.2 else LAMARR_CYAN, align="center")
    draw_text(cv, "CILINDRO DE PÚAS -> NOTAS MECÁNICAS", 240, 94, "silk", 8, CREAM, align="center")
    return vignette(cv, 0.35)


def c1_s03_cinema_and_punchline(t):
    """c1_05..c1_06: Película escandalosa a los 18 años -> 'Toda Europa hablaba de su cara. Nadie, de su cabeza.'"""
    t_c1_05 = TL.s("c1_05")
    t_proh = TL.word("c1_05", "prohibieron")
    t_c1_06 = TL.s("c1_06")
    t_cab = TL.word("c1_06", "cabeza")

    cv = bg("vienna_street_1914").copy()
    cv = grade(cv, mul=(0.92, 0.88, 1.05))
    draw_place_only(cv, "EUROPA · 1933 (18 AÑOS)", t, t_c1_05, border=LAMARR_MAGENTA)

    draw_table_with_prop(cv, 308, 248, prop_kind="film_cans", t=t)

    if t < t_c1_06 - 0.15:
        window(cv, 118, 46, 244, 68, fill=(28, 16, 34), border=CHALK_RED if t >= t_proh - 0.2 else GOLD)
        draw_text(cv, "CINE EUROPEO · «ÉXTASIS» (1933)", 240, 56, "silk", 8, GOLD, align="center")
        draw_text(cv, "ESCÁNDALO MUNDIAL A LOS 18 AÑOS", 240, 74, "silk", 8, CREAM, align="center")
        if t >= t_proh - 0.25:
            draw_text(cv, "¡PROHIBIDA EN VARIOS PAÍSES!", 240, 92, "press", 8, CHALK_RED, align="center")

        char(cv, "hedy_glam", 176, 248, t, scale=2, arms="down", look=1, mood="neutral")
        char(cv, "reporter", 112, 248, t, scale=2, arms="point", look=1, mood="happy")
        return vignette(cv, 0.38)

    # c1_06: Remate del Capítulo 1 ("Toda Europa hablaba de su cara. Nadie, de su cabeza.")
    window(cv, 116, 46, 248, 70, fill=(16, 18, 36), border=GOLD, alpha=0.96)
    draw_text(cv, "TODA EUROPA HABLABA DE SU CARA.", 240, 58, "silk", 8, CREAM, align="center")
    if t >= t_cab - 0.35:
        draw_text(cv, "NADIE, DE SU CABEZA.", 240, 80, "press", 8, LAMARR_CYAN, align="center")
        draw_text(cv, "PERO ELLA NO DEJABA DE PENSAR", 240, 98, "silk", 8, GOLD, align="center")

    char(cv, "hedy_glam", 214, 248, t, scale=2,
         arms="think" if t >= t_cab - 0.3 else "down", look=1, mood="neutral")
    if t >= t_cab - 0.3:
        glow(cv, 214, 152, 22, LAMARR_CYAN, 0.5)
    return vignette(cv, 0.40)


def scenes():
    return [
        (0.0, s01_wireless_and_hollywood,
         lambda t: cam_push(t, 0.0, TL.s("s03"), 1.0, 1.03, (240, 135)), "ch01"),
        (TL.s("s03") - 0.15, s03_navy_drawer_and_title,
         lambda t: cam_push(t, TL.s("s03"), TL.s("c1_00"), 1.0, 1.03, (240, 135)), "ch01"),
        (TL.s("c1_00") - 0.15, make_card(1, ["LA CAJA DE", "MÚSICA"], "1914 – 1933 · VIENA"),
         None, "ch01"),
        (TL.s("c1_01") - 0.15, c1_s01_vienna_walks,
         lambda t: cam_push(t, TL.s("c1_01"), TL.s("c1_03"), 1.0, 1.03, (240, 135)), "ch01"),
        (TL.s("c1_03") - 0.15, c1_s02_piano_and_music_box,
         lambda t: cam_push(t, TL.s("c1_03"), TL.s("c1_05"), 1.0, 1.03, (240, 135)), "ch01"),
        (TL.s("c1_05") - 0.15, c1_s03_cinema_and_punchline,
         lambda t: cam_push(t, TL.s("c1_05"), TL.s("c2_00"), 1.0, 1.035, (240, 125)), "ch01"),
    ]


def music(A):
    t0 = 0.0
    t_c1 = TL.s("c1_00")
    t_end = TL.s("c2_00")
    A.add_pad(t0, t_c1 - t0, [110.0, 164.81, 220.0], amp=0.042)
    A.add_pad(t_c1, t_end - t_c1, [110.0, 164.81, 220.0, 261.63], amp=0.038)


def sfx(A):
    A.fx_pop(TL.s("s01") + 0.15, 0.08)
    A.fx_sparkle(TL.word("s01", "mil"), 0.09)
    A.fx_chime(TL.s("s02"), 0.10)
    A.fx_thud(TL.word("s03", "cajón"), 0.11)
    A.fx_pop(TL.s("s04"), 0.08)
    A.fx_chime(TL.s("s05"), 0.12)
    A.fx_pop(TL.s("c1_01"), 0.09)
    A.fx_pop(TL.word("c1_02", "tranvías"), 0.08)
    A.fx_sparkle(TL.word("c1_02", "electricidad"), 0.09)
    A.fx_sparkle(TL.word("c1_03", "ochenta"), 0.10)
    A.fx_pop(TL.word("c1_04", "desarmó"), 0.08)
    A.fx_chime(TL.word("c1_04", "armar"), 0.10)
    A.fx_thud(TL.word("c1_05", "prohibieron"), 0.10)
    A.fx_chime(TL.word("c1_06", "cabeza"), 0.10)
