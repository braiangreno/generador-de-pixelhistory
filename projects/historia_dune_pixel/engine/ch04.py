"""Capítulo 4: La mejor película que nunca se hizo (c4_00..c4_06)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa

JODOROWSKY = {
    "skin": (232, 188, 150), "hair": (44, 34, 48), "hair_style": "long",
    "beard": (44, 34, 48),
    "shirt": (184, 54, 146), "jacket": (92, 38, 118),
    "pants": (48, 32, 64),
}
MOEBIUS = {
    "skin": (238, 196, 160), "hair": (96, 72, 52), "hair_style": "parted",
    "glasses": True,
    "shirt": (242, 232, 210), "jacket": (64, 112, 148),
    "pants": (52, 68, 88),
}
DALI = {
    "skin": (236, 192, 154), "hair": (32, 28, 34), "hair_style": "parted",
    "beard": (32, 28, 34),
    "shirt": (248, 240, 210), "jacket": (168, 42, 64),
    "tie": (238, 188, 56), "pants": (44, 36, 48),
}


# ===========================================================================
# ESCENA 13 (c4_01, c4_02, c4_03): El equipo soñado de Jodorowsky en París (1975)
# ===========================================================================
def scene_jodorowsky_team(t):
    t1 = TL.s("c4_01")
    t2 = TL.s("c4_02")
    t3 = TL.s("c4_03")
    cv = bg("bg_paris_studio_1975").copy()

    window(cv, 16, 10, 448, 36, fill=(32, 14, 42), border=(238, 112, 214), alpha=0.95)
    if t < t2:
        draw_text(cv, "MEDIADOS DE LOS 70 · PARÍS", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "ALEJANDRO JODOROWSKY QUIERE HACER DUNE A LO GRANDE", 240, 30, "press", 8, GOLD, align="center")
    elif t < t3:
        draw_text(cv, "EL STORYBOARD LEGENDARIO DE MOEBIUS", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "3.000 DIBUJOS PARA PLANIFICAR CADA ESCENA", 240, 30, "press", 8, GOLD, align="center")
    else:
        draw_text(cv, "UN EQUIPO ARTÍSTICO IRREPETIBLE", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "GIGER · PINK FLOYD · DALÍ (US$ 100.000 POR HORA)", 240, 30, "press", 8, GOLD, align="center")

    # Personajes en el estudio parisino (feet=260)
    char(cv, JODOROWSKY, 92, 260, t, scale=2, arms="cheer" if t >= t3 else "point", look=1, talk=talk_v(t, True))
    char(cv, MOEBIUS, 178, 260, t, scale=2, arms="note", look=1, mood="happy")
    if t >= t3:
        char(cv, DALI, 388, 260, t, scale=2, arms="hips", look=-1, mood="happy")
    robot(cv, 32, 260, t, face="excited", scale=1)

    if t < t3:
        window(cv, 224, 58, 236, 102, fill=(34, 18, 48), border=GOLD, alpha=0.96)
        portrait(cv, "jodorowsky", 234, 68, 64)
        portrait(cv, "moebius", 306, 68, 64)
        draw_text(cv, "JODOROWSKY", 266, 138, "silk", 8, GOLD, align="center")
        draw_text(cv, "MOEBIUS", 338, 138, "silk", 8, CYAN, align="center")
        if t >= t2:
            window(cv, 376, 68, 76, 64, fill=(58, 24, 72), border=CYAN, alpha=0.98)
            draw_text(cv, "3.000", 414, 82, "press", 8, GOLD, align="center")
            draw_text(cv, "DIBUJOS", 414, 100, "silk", 8, CREAM, align="center")
    else:
        # Grilla psicodélica con los 4 integrantes clave
        cards = [
            ("MOEBIUS", "3.000 DIBUJOS", CYAN),
            ("H. R. GIGER", "DISEÑO VISUAL", GREEN),
            ("PINK FLOYD", "BANDA SONORA", (245, 120, 220)),
            ("SALVADOR DALÍ", "US$ 100.000 / HORA", GOLD),
        ]
        for idx, (who, role, col) in enumerate(cards):
            cx = 212 + (idx % 2) * 124
            cy = 58 + (idx // 2) * 52
            window(cv, cx, cy, 118, 44, fill=(32, 16, 46), border=col, alpha=0.96)
            draw_text(cv, who, cx + 59, cy + 10, "press", 8, col, align="center")
            draw_text(cv, role, cx + 59, cy + 26, "silk", 8, CREAM, align="center")

    draw_sand_ripple(cv, t, y_base=262, x_start=40, x_end=440, color=(235, 145, 220))
    return cv


# ===========================================================================
# ESCENA 14 (c4_04, c4_05, c4_06): El libro gigante, el rechazo de Hollywood y Alien
# ===========================================================================
def scene_bible_and_alien(t):
    t4 = TL.s("c4_04")
    t5 = TL.s("c4_05")
    t6 = TL.s("c4_06")
    cv = bg("bg_storage_box_1976").copy()
    d = ImageDraw.Draw(cv)

    window(cv, 16, 10, 448, 36, fill=(20, 16, 28), border=GOLD if t < t6 else GREEN, alpha=0.95)
    if t < t5:
        draw_text(cv, "UN GUION PARA MÁS DE DIEZ HORAS DE CINE", 240, 16, "press", 8, GOLD, align="center")
        draw_text(cv, "NINGÚN ESTUDIO DE HOLLYWOOD QUISO PAGARLA", 240, 30, "silk", 8, RED, align="center")
    elif t < t6:
        draw_text(cv, "1976 · EL SUEÑO SE DERRUMBA", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "GASTARON US$ 2 MILLONES Y EL PROYECTO SE CAYÓ", 240, 30, "press", 8, RED, align="center")
    else:
        draw_text(cv, "LA SEMILLA QUE CAMBIÓ EL CINE DE CIENCIA FICCIÓN", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "PARTE DE ESE EQUIPO SE REENCONTRÓ EN ALIEN (1979)", 240, 30, "press", 8, GREEN, align="center")

    char(cv, JODOROWSKY, 88, 260, t, scale=2, arms="cross" if t < t6 else "point", look=1, mood="sad" if t < t6 else "happy")
    char(cv, MOEBIUS, 168, 260, t, scale=2, arms="hips", look=1)
    robot(cv, 428, 260, t, face="sad" if t < t6 else "excited", scale=1)

    if t < t6:
        window(cv, 214, 62, 238, 108, fill=(36, 16, 24), border=RED, alpha=0.96)
        draw_text(cv, "BIBLIA DE DUNE (1975)", 333, 74, "press", 8, GOLD, align="center")
        draw_text(cv, "DURACIÓN: +10 HORAS", 333, 94, "silk", 8, CREAM, align="center")
        draw_text(cv, "HOLLYWOOD: RECHAZADO", 333, 112, "press", 8, RED, align="center")
        if t >= t5:
            window(cv, 232, 130, 202, 28, fill=(92, 18, 22), border=GOLD, alpha=0.98)
            draw_text(cv, "US$ 2.000.000 GASTADOS", 333, 140, "press", 8, CREAM, align="center")
    else:
        # Conexión luminosa entre el libro de Dune y el nacimiento de ALIEN
        window(cv, 208, 58, 248, 118, fill=(12, 28, 24), border=GREEN, alpha=0.96)
        draw_text(cv, "DEL DUNE DE JODOROWSKY", 332, 70, "silk", 8, GOLD, align="center")
        draw_text(cv, "O'BANNON · GIGER · MOEBIUS", 332, 86, "silk", 8, CREAM, align="center")
        d.line([(332, 98), (332, 114)], fill=(*GREEN, 255), width=2)
        window(cv, 224, 116, 216, 46, fill=(8, 46, 32), border=GREEN, alpha=0.98)
        draw_text(cv, "ALIEN (1979)", 332, 126, "press", 16, GREEN, align="center", outline_w=2)
        draw_text(cv, "EL EQUIPO SIGUIÓ JUNTO", 332, 148, "silk", 8, CREAM, align="center")

    draw_sand_ripple(cv, t, y_base=262, x_start=40, x_end=440)
    return cv


def scenes():
    return [
        (TL.chapter_start(4) - 0.3, make_card(4, ["LA MEJOR PELÍCULA", "QUE NUNCA SE HIZO"], "1974 - 1976 · JODOROWSKY")),
        (TL.s("c4_01") - 0.15, scene_jodorowsky_team),
        (TL.s("c4_04") - 0.15, scene_bible_and_alien),
    ]
