"""Apertura: Línea por línea (s01..s05) + Capítulo 1: Un telescopio eléctrico (c1_00..c1_07)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa


def draw_tv_table_prop(cv, x, feet=248, t=0.0, mode="scan"):
    """Mesa de madera con patas hasta el suelo (feet=248) sosteniendo un televisor de tubo."""
    def _draw(canvas, cx, fy):
        d = ImageDraw.Draw(canvas)
        top_y = fy - 42
        shadow_ellipse(canvas, cx, fy, 34, 5, 85)
        # Patas de madera apoyadas en fy
        d.rectangle([cx - 24, top_y + 5, cx - 19, fy], fill=(78, 48, 26, 255), outline=(*INK, 255))
        d.rectangle([cx + 19, top_y + 5, cx + 24, fy], fill=(78, 48, 26, 255), outline=(*INK, 255))
        d.rectangle([cx - 28, top_y, cx + 28, top_y + 6], fill=(124, 78, 42, 255), outline=(*INK, 255))
        draw_crt_tv(canvas, cx - 22, top_y - 34, 44, 34, t, mode=mode)
    floor_prop(cv, _draw, x, feet)


def draw_plow_prop(cv, x, feet=248, t=0.0):
    """Arado de hierro y madera apoyado firmemente sobre los surcos del suelo (feet=248)."""
    def _draw(canvas, cx, fy):
        d = ImageDraw.Draw(canvas)
        shadow_ellipse(canvas, cx, fy, 36, 5, 85)
        # Rueda de hierro del arado apoyada en fy
        w_r = 11
        wx, wy = cx - 10, fy - w_r
        d.ellipse([wx - w_r, wy - w_r, wx + w_r, wy + w_r], fill=(64, 58, 54, 255), outline=(*INK, 255))
        d.ellipse([wx - 3, wy - 3, wx + 3, wy + 3], fill=(148, 134, 118, 255))
        for k in range(4):
            ang = t * 2.2 + k * (math.pi / 2)
            d.line([(wx, wy), (int(wx + math.cos(ang) * w_r), int(wy + math.sin(ang) * w_r))],
                   fill=(120, 110, 98, 255), width=1)
        # Reja de acero hundida en el surco (fy) y manceras de madera
        d.polygon([(cx - 4, fy - 14), (cx + 18, fy), (cx - 2, fy)], fill=(138, 146, 158, 255), outline=(*INK, 255))
        d.line([(cx - 18, fy - 34), (cx + 6, fy - 4)], fill=(134, 86, 44, 255), width=3)
        d.line([(cx - 10, fy - 34), (cx + 12, fy - 6)], fill=(112, 68, 34, 255), width=2)
    floor_prop(cv, _draw, x, feet)


def draw_nipkow_bench_prop(cv, x, feet=248, t=0.0, spin=True):
    """Mesa de taller berlinesa apoyada en el suelo con lámpara de aceite y el disco de Nipkow."""
    def _draw(canvas, cx, fy):
        d = ImageDraw.Draw(canvas)
        top_y = fy - 42
        shadow_ellipse(canvas, cx, fy, 38, 5, 85)
        # Patas y tapa de la mesa
        d.rectangle([cx - 28, top_y + 5, cx - 22, fy], fill=(74, 46, 26, 255), outline=(*INK, 255))
        d.rectangle([cx + 22, top_y + 5, cx + 28, fy], fill=(74, 46, 26, 255), outline=(*INK, 255))
        d.rectangle([cx - 32, top_y, cx + 32, top_y + 6], fill=(118, 76, 42, 255), outline=(*INK, 255))
        # Lámpara de aceite a la izquierda sobre la mesa
        lx = cx - 16
        glow(canvas, lx, top_y - 14, 20, AMBER, 0.45)
        d.rectangle([lx - 5, top_y - 6, lx + 5, top_y], fill=(184, 142, 64, 255), outline=(*INK, 255))
        d.ellipse([lx - 4, top_y - 16, lx + 4, top_y - 6], fill=(255, 224, 128, 255), outline=(*INK, 255))
        # Soporte y disco de Nipkow con agujeros en espiral a la derecha sobre la mesa
        dx_c, dy_c, r_d = cx + 10, top_y - 18, 14
        d.rectangle([dx_c - 3, top_y - 6, dx_c + 3, top_y], fill=(62, 66, 78, 255), outline=(*INK, 255))
        d.ellipse([dx_c - r_d, dy_c - r_d, dx_c + r_d, dy_c + r_d], fill=(42, 46, 58, 255), outline=(*GOLD, 255))
        ang0 = t * 3.2 if spin else 0.4
        for i in range(6):
            ang = ang0 + i * (2 * math.pi / 6)
            rr = 4 + i * 1.5
            hx = int(round(dx_c + math.cos(ang) * rr))
            hy = int(round(dy_c + math.sin(ang) * rr))
            d.rectangle([hx - 1, hy - 1, hx + 1, hy + 1], fill=(*CHALK_YELLOW, 255))
    floor_prop(cv, _draw, x, feet)


def s01_screen_scanlines(t):
    """s01: La imagen que estás viendo ahora se dibuja línea por línea, de arriba abajo."""
    t_s01 = TL.s("s01")
    t_rap = TL.word("s01", "rápido")

    cv = bg("living_room_1950s").copy()
    cv = grade(cv, mul=(0.42, 0.48, 0.58))

    window(cv, 20, 8, 440, 22, fill=(12, 20, 32), border=CHALK_GREEN, alpha=0.94)
    draw_text(cv, "AHORA MISMO · TU PANTALLA", 240, 14, "press", 8, CHALK_GREEN, align="center",
              reveal=max(1, int((t - t_s01 + 0.2) * 32)))

    # Panel central mostrando el barrido línea por línea de arriba abajo
    window(cv, 118, 44, 244, 122, fill=(10, 22, 18), border=CHALK_GREEN, alpha=0.95)
    draw_text(cv, "SE DIBUJA LÍNEA POR LÍNEA", 240, 52, "press", 8, CHALK_GREEN, align="center")
    spd = 2.6 if t >= t_rap - 0.1 else 0.95
    draw_scanline_beam(cv, 134, 68, 212, 72, t, rows=9, speed=spd, color=CHALK_GREEN, beam_col=CREAM)
    lbl_bot = "MÁS RÁPIDO QUE TU OJO" if t >= t_rap - 0.1 else "DE ARRIBA ABAJO · RENGLÓN POR RENGLÓN"
    draw_text(cv, lbl_bot, 240, 148, "silk", 8, GOLD if t >= t_rap - 0.1 else CREAM, align="center")

    draw_tv_table_prop(cv, 240, 248, t, mode="scan")
    return vignette(cv, 0.40)


def s02_idaho_opening(t):
    """s02..s05: Campo arado en Idaho (14 años) -> surcos = renglones -> título LÍNEA POR LÍNEA."""
    cv = bg("idaho_plow_field").copy()
    t_s02 = TL.s("s02")
    t_s03 = TL.s("s03")
    t_reng = TL.word("s03", "renglón")
    t_s04 = TL.s("s04")
    t_s05 = TL.s("s05")

    draw_place_only(cv, "IDAHO · 1920", t, t_s02, border=AMBER)

    if t >= t_s05 - 0.15:
        # Placa de título principal del episodio sobre el campo arado
        a, dy = pop(t, t_s05 - 0.1)
        window(cv, 116, 48 + dy, 248, 116, fill=(16, 20, 32), border=GOLD, alpha=0.95)
        draw_text(cv, "LÍNEA POR", 240, 58 + dy, "press", 16, align="center",
                  gradient=GOLD_RAMP, outline_w=2, reveal=max(1, int((t - t_s05 + 0.2) * 24)))
        draw_text(cv, "LÍNEA", 240, 82 + dy, "press", 16, align="center",
                  gradient=GOLD_RAMP, outline_w=2, reveal=max(0, int((t - t_s05 - 0.1) * 24)))
        draw_text(cv, "LA HISTORIA DE LA TELEVISIÓN", 240, 110 + dy, "silk", 8, CHALK_GREEN, align="center",
                  reveal=max(0, int((t - t_s05 - 0.35) * 32)))
        draw_text(cv, "EL CHICO DEL CAMPO ARADO", 240, 126 + dy, "silk", 8, CREAM, align="center",
                  reveal=max(0, int((t - t_s05 - 0.55) * 32)))
        draw_scanline_beam(cv, 146, 140 + dy, 188, 16, t, rows=3, speed=1.8, color=CHALK_GREEN)
        char(cv, "farnsworth_boy", 164, 248, t, scale=2, arms="point", look=1, mood="happy")
        draw_plow_prop(cv, 296, 248, t)
        return vignette(cv, 0.35)

    # Chico de 14 años arando el campo en Idaho y mirando los surcos
    x_boy, w_boy = walk(t, t_s02, t_s03 + 0.4, 110, 188)
    char(cv, "farnsworth_boy", x_boy, 248, t, scale=2, walk=w_boy,
         arms="point" if t >= t_s03 else "work",
         look=1, mood="happy" if t >= t_reng else "neutral")
    draw_plow_prop(cv, int(x_boy) + 74, 248, t)

    if t_s03 - 0.15 <= t < t_s04 - 0.15:
        a, dy = pop(t, t_s03 - 0.15)
        window(cv, 118, 44 + dy, 244, 96, fill=(14, 26, 22), border=CHALK_GREEN, alpha=0.94)
        draw_text(cv, "SURCOS EN LA TIERRA", 240, 52 + dy, "silk", 8, AMBER, align="center")
        draw_scanline_beam(cv, 138, 66 + dy, 204, 50, t, rows=6, speed=1.4, color=CHALK_GREEN)
        draw_text(cv, "IMAGEN POR EL AIRE: RENGLÓN POR RENGLÓN", 240, 122 + dy, "silk", 8, CREAM, align="center")
    elif t >= t_s04 - 0.15:
        cv = grade(cv, mul=(0.68, 0.68, 0.78))
        a, dy = pop(t, t_s04 - 0.1)
        window(cv, 118, 58 + dy, 244, 64, fill=(16, 18, 32), border=GOLD, alpha=0.95)
        draw_text(cv, "30 AÑOS DESPUÉS:", 240, 70 + dy, "silk", 8, GOLD, align="center")
        draw_text(cv, "CASI NADIE SABÍA SU NOMBRE", 240, 90 + dy, "press", 8, CREAM, align="center")

    return vignette(cv, 0.35)


# ===========================================================================
# CAPÍTULO 1: UN TELESCOPIO ELÉCTRICO (c1_01 .. c1_07)
# ===========================================================================

def c1_s01_nipkow_berlin(t):
    """c1_01..c1_03: Berlín, Nochebuena de 1883. Paul Nipkow y el disco en espiral."""
    t0 = TL.s("c1_01")
    t_c1_02 = TL.s("c1_02")
    t_esp = TL.word("c1_02", "espiral")
    t_c1_03 = TL.s("c1_03")
    t_nunca = TL.word("c1_03", "Nunca")

    cv = bg("berlin_room_1883").copy()
    SNOW.draw(cv, t, density=0.45)
    draw_place_only(cv, "BERLÍN · NOCHEBUENA DE 1883", t, t0, border=AMBER)

    # Ventana central mostrando el disco con agujeros en espiral y la patente
    window(cv, 118, 44, 244, 102, fill=(16, 22, 38), border=GOLD, alpha=0.94)
    d = ImageDraw.Draw(cv)
    if t < t_c1_03 - 0.1:
        draw_text(cv, "PAUL NIPKOW · DISCO EN ESPIRAL", 240, 52, "silk", 8, GOLD, align="center")
        # Disco giratorio grande a la izquierda del panel y franjas barridas a la derecha
        cx_d, cy_d, r_d = 176, 98, 28
        d.ellipse([cx_d - r_d, cy_d - r_d, cx_d + r_d, cy_d + r_d], fill=(34, 40, 58, 255), outline=(*GOLD, 255))
        ang_base = t * 3.0 if t >= t_c1_02 else 0.0
        for i in range(8):
            ang = ang_base + i * (2 * math.pi / 8)
            rr = 7 + i * 2.3
            hx = int(round(cx_d + math.cos(ang) * rr))
            hy = int(round(cy_d + math.sin(ang) * rr))
            d.ellipse([hx - 2, hy - 2, hx + 2, hy + 2], fill=(*CHALK_YELLOW, 255))
        draw_scanline_beam(cv, 224, 72, 120, 52, t, rows=6, speed=1.3, color=AMBER)
        draw_text(cv, "CADA AGUJERO BARRE UNA FRANJA", 240, 130, "silk", 8, CREAM, align="center")
    else:
        draw_text(cv, "PATENTE: TELESCOPIO ELÉCTRICO", 240, 56, "press", 8, GOLD, align="center")
        draw_text(cv, "BERLÍN · 1884", 240, 76, "silk", 8, TESLA_CYAN, align="center")
        if t >= t_nunca - 0.2:
            d.rectangle([142, 96, 338, 122], fill=(62, 22, 26, 255), outline=(*CHALK_RED, 255))
            draw_text(cv, "NUNCA LLEGÓ A CONSTRUIRLO", 240, 105, "press", 8, CHALK_RED, align="center")

    char(cv, "nipkow", 156, 248, t, scale=2,
         arms="think" if t < t_c1_02 else ("write" if t < t_c1_03 else "down"),
         look=1, mood="happy" if t < t_nunca else "neutral",
         talk=talk_v(t, t_c1_02 <= t < t_c1_03))
    draw_nipkow_bench_prop(cv, 304, 248, t, spin=(t >= t_esp - 0.2 and t < t_nunca))

    return vignette(cv, 0.36)


def c1_s02_pizarra_strips(t):
    """c1_04..c1_07: LA PIZARRA 1 — Cortar una foto en tiras y transmitir luz como electricidad."""
    t0 = TL.s("c1_04")
    t_c1_05 = TL.s("c1_05")
    t_c1_06 = TL.s("c1_06")
    t_c1_07 = TL.s("c1_07")

    cv = draw_pizarra_frame(t, t0, "CORTAR EN TIRAS",
                            summary_es="CORTAR EN TIRAS Y PINTAR RÁPIDO",
                            t_summary=t_c1_07)
    d = ImageDraw.Draw(cv)

    # Panel en la zona central (x=118..362, w=244 -> 100% compatible con 16:9 y 9:16)
    if t < t_c1_05 - 0.1:
        # Paso 1: Una foto no entra entera en un cable, pero se puede cortar en tiras
        d.rectangle([124, 48, 356, 184], fill=(16, 40, 28, 255), outline=(*CHALK_WHITE, 255))
        draw_text(cv, "1. CORTAR LA IMAGEN EN TIRAS", 240, 56, "press", 8, CHALK_YELLOW, align="center")
        for i in range(5):
            ry = 76 + i * 16
            slice_dx = int(round(math.sin(t * 3.0 + i) * 6))
            d.rectangle([156 + slice_dx, ry, 256 + slice_dx, ry + 11],
                        fill=(34, 82, 56, 255), outline=(*CHALK_GREEN, 255))
            draw_text(cv, f"TIRA {i+1}", 206 + slice_dx, ry + 2, "silk", 8, CREAM, align="center")
        # Cable a la derecha
        d.rectangle([284, 104, 344, 118], fill=(28, 58, 42, 255), outline=(*CHALK_CYAN, 255))
        draw_text(cv, "CABLE", 314, 124, "silk", 8, CHALK_CYAN, align="center")
        draw_chalk_hand(cv, 262, 112, t)
    elif t < t_c1_06 - 0.1:
        # Paso 2: Leer cada tira de izquierda a derecha (claro, oscuro, claro) -> electricidad
        d.rectangle([124, 48, 356, 184], fill=(16, 40, 28, 255), outline=(*CHALK_WHITE, 255))
        draw_text(cv, "2. LEER DE IZQUIERDA A DERECHA", 240, 56, "press", 8, CHALK_YELLOW, align="center")
        blocks = [("CLARO", (48, 108, 72)), ("OSCURO", (24, 44, 32)), ("CLARO", (48, 108, 72))]
        for idx_b, (b_lbl, b_col) in enumerate(blocks):
            bx = 136 + idx_b * 70
            d.rectangle([bx, 76, bx + 62, 108], fill=(*b_col, 255), outline=(*CHALK_WHITE, 255))
            draw_text(cv, b_lbl, bx + 31, 88, "silk", 8, CHALK_YELLOW if b_lbl == "CLARO" else CREAM, align="center")
        # Pulso eléctrico viajando por el cable
        d.line([(138, 142), (342, 142)], fill=(*CHALK_CYAN, 255), width=2)
        u_el = (t * 1.4) % 1.0
        px_el = int(138 + 204 * u_el)
        draw_phosphor_dot(cv, px_el, 142, r=3, color=CHALK_YELLOW)
        draw_text(cv, "CAMBIOS DE LUZ = ELECTRICIDAD", 240, 158, "silk", 8, CHALK_CYAN, align="center")
        draw_chalk_hand(cv, px_el, 108, t)
    else:
        # Paso 3: Del otro lado alguien pinta las tiras en el mismo orden
        d.rectangle([124, 44, 356, 194], fill=(16, 40, 28, 255), outline=(*CHALK_WHITE, 255))
        draw_text(cv, "3. PINTAR LAS TIRAS EN ORDEN", 240, 52, "press", 8, CHALK_YELLOW, align="center")
        draw_scanline_beam(cv, 152, 68, 176, 84, t, rows=7, speed=1.8, color=CHALK_GREEN)
        lbl3 = "FALTABAN 40 AÑOS (1883 -> 1926)" if t >= t_c1_07 - 0.1 else "MUY RÁPIDO = IMAGEN COMPLETA"
        draw_text(cv, lbl3, 240, 162, "silk", 8, GOLD if t >= t_c1_07 - 0.1 else CHALK_WHITE, align="center")

    return vignette(cv, 0.28)


def scenes():
    return [
        (0.0, s01_screen_scanlines,
         lambda t: cam_push(t, 0.0, TL.s("s02"), 1.03, 1.0, (240, 135)), "ch01"),
        (TL.s("s02") - 0.15, s02_idaho_opening,
         lambda t: cam_push(t, TL.s("s02"), TL.s("c1_00"), 1.0, 1.03, (240, 135)), "ch01"),
        (TL.s("c1_00") - 0.15, make_card(1, ["UN TELESCOPIO", "ELÉCTRICO"], "1883 · BERLÍN", snow=True),
         None, "ch01"),
        (TL.s("c1_01") - 0.15, c1_s01_nipkow_berlin,
         lambda t: cam_push(t, TL.s("c1_01"), TL.s("c1_04"), 1.0, 1.03, (240, 135)), "ch01"),
        (TL.s("c1_04") - 0.15, c1_s02_pizarra_strips,
         None, "ch01"),
    ]


def music(A):
    return


def sfx(A):
    A.fx_pop(TL.s("s02"), 0.08)
    A.fx_sweep(TL.s("s03"), 0.45, 220, 440, 0.06)
    A.fx_chime(TL.s("s05"), 0.11)
    A.fx_pop(TL.s("c1_02"), 0.08)
    A.fx_thud(TL.word("c1_03", "Nunca"), 0.09)
    A.fx_pop(TL.s("c1_04"), 0.08)
    A.fx_sparkle(TL.s("c1_06"), 0.09)
