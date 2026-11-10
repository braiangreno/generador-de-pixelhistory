"""Capítulo 4: La mejor película que nunca se hizo (c4_00..c4_06)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa

JODOROWSKY = {
    "name": "Alejandro Jodorowsky",
    "skin": (232, 188, 150), "hair": (44, 34, 48), "hair_style": "long",
    "beard": (44, 34, 48),
    "shirt": (184, 54, 146), "jacket": (92, 38, 118),
    "pants": (48, 32, 64),
}
MOEBIUS = {
    "name": "Moebius",
    "skin": (238, 196, 160), "hair": (96, 72, 52), "hair_style": "parted",
    "glasses": True,
    "shirt": (242, 232, 210), "jacket": (64, 112, 148),
    "pants": (52, 68, 88),
}
DALI = {
    "name": "Salvador Dali",
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
        draw_text(cv, "ALEJANDRO JODOROWSKY QUIERE HACER DUNE A LO GRANDE", 240, 30, "press", 8, GOLD, align="center",
                  reveal=(t - t1) * 32)
    elif t < t3:
        draw_text(cv, "EL STORYBOARD LEGENDARIO DE MOEBIUS", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "3.000 DIBUJOS PARA PLANIFICAR CADA ESCENA", 240, 30, "press", 8, GOLD, align="center",
                  reveal=(t - t2) * 32)
    else:
        draw_text(cv, "UN EQUIPO ARTÍSTICO IRREPETIBLE", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "GIGER · PINK FLOYD · DALÍ (US$ 100.000 POR HORA)", 240, 30, "press", 8, GOLD, align="center",
                  reveal=(t - t3) * 32)

    # Jodorowsky entra en c4_01 y levanta los brazos en "a lo grande"; Moebius dibuja en c4_02; Dalí entra al decir "Dalí" en c4_03
    t_grande = TL.word("c4_01", "grande")
    t_dali = TL.word("c4_03", "Dali")
    jx, jph = walk(t, t1, t1 + 0.85, 38, 86)
    char(cv, JODOROWSKY, jx, 260, t, scale=2, walk=jph,
         arms="cheer" if t >= t_grande else "point", look=1, talk=talk_v(t, t < t2 or t >= t3), mood="happy")
    char(cv, MOEBIUS, 156, 260, t, scale=2,
         arms="write" if t >= t2 else "note", look=1, mood="happy")

    if t >= t_dali - 0.1:
        dx_dali, dph = walk(t, t_dali - 0.1, t_dali + 0.65, 448, 396)
        char(cv, DALI, dx_dali, 260, t, scale=2, walk=dph, arms="wave" if dph is None else "down", look=-1, mood="happy")

    if t < t3:
        a_p, dy_p = pop(t, t1 + 0.1)
        window(cv, 224, 58 + dy_p, 236, 102, fill=(34, 18, 48), border=GOLD, alpha=0.96 * a_p)
        portrait(cv, "jodorowsky", 234, 68 + dy_p, 64)
        portrait(cv, "moebius", 306, 68 + dy_p, 64)
        draw_text(cv, "JODOROWSKY", 266, 138 + dy_p, "silk", 8, GOLD, align="center")
        draw_text(cv, "MOEBIUS", 338, 138 + dy_p, "silk", 8, CYAN, align="center")
        if t >= t2:
            a_d, dy_d = pop(t, t2 + 0.05)
            u_cnt = clamp01((t - t2) / max(0.8, (t3 - t2) * 0.7))
            n_drawings = int(3000 * ease_out(u_cnt))
            window(cv, 376, 68 + dy_d, 76, 64, fill=(58, 24, 72), border=CYAN, alpha=0.98 * a_d)
            draw_text(cv, f"{n_drawings:,}".replace(",", "."), 414, 82 + dy_d, "press", 8, GOLD, align="center")
            draw_text(cv, "DIBUJOS", 414, 100 + dy_d, "silk", 8, CREAM, align="center")
    else:
        # Grilla con los 4 integrantes apareciendo en la palabra exacta del narrador
        cards = [
            ("MOEBIUS", "3.000 DIBUJOS", CYAN, t3),
            ("H. R. GIGER", "DISEÑO VISUAL", GREEN, TL.word("c4_03", "Giger")),
            ("PINK FLOYD", "BANDA SONORA", (245, 120, 220), TL.word("c4_03", "Pink")),
            ("SALVADOR DALÍ", "US$ 100.000 / HORA", GOLD, t_dali),
        ]
        for idx, (who, role, col, t_c) in enumerate(cards):
            if t >= t_c:
                ac, dyc = pop(t, t_c)
                cx = 212 + (idx % 2) * 124
                cy = 58 + (idx // 2) * 52 + dyc
                window(cv, cx, cy, 118, 44, fill=(32, 16, 46), border=col, alpha=0.96 * ac)
                draw_text(cv, who, cx + 59, cy + 10, "press", 8, col, align="center")
                draw_text(cv, role, cx + 59, cy + 26, "silk", 8, CREAM, align="center")

    return cv


# ===========================================================================
# ESCENA 14 (c4_04, c4_05, c4_06): El libro gigante, el rechazo de Hollywood y Alien
# ===========================================================================
def scene_bible_and_alien(t):
    t4 = TL.s("c4_04")
    t5 = TL.s("c4_05")
    t6 = TL.s("c4_06")
    dx, dy = shake(t, t5 + 0.1, dur=0.25, amp=3)
    cv = bg("bg_storage_box_1976").copy()
    d = ImageDraw.Draw(cv)

    window(cv, 16, 10, 448, 36, fill=(20, 16, 28), border=GOLD if t < t6 else GREEN, alpha=0.95)
    if t < t5:
        draw_text(cv, "UN GUION PARA MÁS DE DIEZ HORAS DE CINE", 240, 16, "press", 8, GOLD, align="center")
        draw_text(cv, "NINGÚN ESTUDIO DE HOLLYWOOD QUISO PAGARLA", 240, 30, "silk", 8, RED, align="center",
                  reveal=(t - t4) * 32)
    elif t < t6:
        draw_text(cv, "1976 · EL SUEÑO SE DERRUMBA", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "GASTARON US$ 2 MILLONES Y EL PROYECTO SE CAYÓ", 240, 30, "press", 8, RED, align="center",
                  reveal=(t - t5) * 32)
    else:
        draw_text(cv, "LA SEMILLA QUE CAMBIÓ EL CINE DE CIENCIA FICCIÓN", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "PARTE DE ESE EQUIPO SE REENCONTRÓ EN ALIEN (1979)", 240, 30, "press", 8, GREEN, align="center",
                  reveal=(t - t6) * 32)

    t_ningun = TL.word("c4_04", "Ningun")
    t_alien = TL.word("c4_06", "Alien")
    char(cv, JODOROWSKY, 84, 260, t, scale=2,
         arms="point" if t >= t_alien else ("shrug" if t >= t_ningun else "hold"),
         look=1, mood="sad" if (t_ningun <= t < t6) else "happy")
    char(cv, MOEBIUS, 152, 260, t, scale=2,
         arms="cheer" if t >= t_alien else ("cross" if t >= t5 else "note"),
         look=1, mood="sad" if (t_ningun <= t < t6) else "happy")

    if t < t6:
        a_b, dy_b = pop(t, t4 + 0.05)
        window(cv, 214, 62 + dy_b, 238, 108, fill=(36, 16, 24), border=RED, alpha=0.96 * a_b)
        draw_text(cv, "BIBLIA DE DUNE (1975)", 333, 74 + dy_b, "press", 8, GOLD, align="center")
        draw_text(cv, "DURACIÓN: +10 HORAS", 333, 94 + dy_b, "silk", 8, CREAM, align="center")
        draw_text(cv, "HOLLYWOOD: RECHAZADO", 333, 112 + dy_b, "press", 8, RED, align="center")
        if t >= t5:
            a_c, dy_c = pop(t, t5 + 0.05, dur=0.25)
            window(cv, 232, 130 + dy_c, 202, 28, fill=(92, 18, 22), border=GOLD, alpha=0.98 * a_c)
            draw_text(cv, "US$ 2.000.000 GASTADOS", 333, 140 + dy_c, "press", 8, CREAM, align="center")
    else:
        # Conexión luminosa entre el libro de Dune y el nacimiento de ALIEN
        a_a, dy_a = pop(t, t6 + 0.05)
        window(cv, 208, 58 + dy_a, 248, 118, fill=(12, 28, 24), border=GREEN, alpha=0.96 * a_a)
        draw_text(cv, "DEL DUNE DE JODOROWSKY", 332, 70 + dy_a, "silk", 8, GOLD, align="center")
        draw_text(cv, "O'BANNON · GIGER · MOEBIUS", 332, 86 + dy_a, "silk", 8, CREAM, align="center")
        d.line([(332, 98 + dy_a), (332, 114 + dy_a)], fill=(*GREEN, 255), width=2)
        window(cv, 224, 116 + dy_a, 216, 46, fill=(8, 46, 32), border=GREEN, alpha=0.98 * a_a)
        draw_text(cv, "ALIEN (1979)", 332, 126 + dy_a, "press", 16, GREEN, align="center", outline_w=2)
        draw_text(cv, "EL EQUIPO SIGUIÓ JUNTO", 332, 148 + dy_a, "silk", 8, CREAM, align="center")
        sparkle(cv, 236, 128 + dy_a, t, 3)
        sparkle(cv, 428, 132 + dy_a, t + 1.2, 3)

    return offset_canvas(cv, dx, dy)


def scenes():
    return [
        (TL.chapter_start(4) - 0.3, make_card(4, ["LA MEJOR PELÍCULA", "QUE NUNCA SE HIZO"], "1974 - 1976 · JODOROWSKY"), None),
        (TL.s("c4_01") - 0.15, scene_jodorowsky_team, lambda t: (1.0 + cam_punch(t, [TL.s("c4_02"), TL.s("c4_03")], 0.06), 240, 140)),
        (TL.s("c4_04") - 0.15, scene_bible_and_alien, lambda t: cam_push(t, TL.s("c4_04"), TL.e("c4_06"), 1.0, 1.10, (240, 140), (265, 135))),
    ]
