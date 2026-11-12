"""Apertura: Un palito y un poema (s01..s06) + Capítulo 1: Hijo de la tormenta (c1_01..c1_07)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa


def draw_candle(cv, x, y, t, scale=1):
    """Vela encendida con halo cálido ámbar (Acto 1: la luz de la vela)."""
    d = ImageDraw.Draw(cv)
    flick = int(round(math.sin(t * 13.0 + x) * 2))
    glow(cv, x, y - 10 * scale + flick, 26 * scale, (255, 196, 84), 0.45)
    # Palmatoria y cuerpo de cera
    d.rectangle([x - 5 * scale, y, x + 5 * scale, y + 2 * scale], fill=(184, 142, 64, 255), outline=(*INK, 255))
    d.rectangle([x - 3 * scale, y - 9 * scale, x + 3 * scale, y], fill=(244, 236, 214, 255), outline=(*INK, 255))
    # Llama
    d.polygon([
        (x, y - 16 * scale + flick),
        (x - 3 * scale, y - 10 * scale),
        (x + 3 * scale, y - 10 * scale),
    ], fill=(255, 204, 72, 255))
    d.polygon([
        (x, y - 14 * scale + flick),
        (x - 1 * scale, y - 10 * scale),
        (x + 1 * scale, y - 10 * scale),
    ], fill=(255, 248, 210, 255))


def s01_screen_and_grid(t):
    """0:00 - 0:16: Pantalla en habitación a oscuras -> alejamiento por escalones hasta la red eléctrica."""
    t_s01 = TL.s("s01")
    t_elec = TL.word("s01", "electricidad")
    t_lejos = TL.word("s01", "lejos")
    t_s02 = TL.s("s02")
    t_cien = TL.word("s02", "cien")

    if t < t_s02 - 0.15:
        # Plano 1: Habitación a oscuras con pantalla que se enciende y cable al enchufe
        cv = bg("bg_dark_room_screen").copy()
        on_p = clamp01((t - t_s01 + 0.25) / 0.45)
        cv = grade(cv, mul=(0.35 + 0.65 * on_p, 0.40 + 0.60 * on_p, 0.50 + 0.50 * on_p))
        d = ImageDraw.Draw(cv)

        # Pantalla brillante en el escritorio (x=136..256, y=64..136)
        sx, sy, sw, sh = 148, 62, 116, 72
        if on_p > 0.05:
            for r_glow, a_glow in ((36, int(38 * on_p)), (18, int(68 * on_p))):
                d.rectangle([sx - r_glow, sy - r_glow, sx + sw + r_glow, sy + sh + r_glow],
                            fill=(120, 210, 255, a_glow))
        d.rectangle([sx - 4, sy - 4, sx + sw + 4, sy + sh + 4], fill=(28, 32, 46, 255), outline=(*INK, 255))
        scr_col = (195, 234, 255, 255) if on_p > 0.2 else (14, 18, 28, 255)
        d.rectangle([sx, sy, sx + sw, sy + sh], fill=scr_col, outline=(*TESLA_CYAN, 255))
        if on_p > 0.4:
            draw_rotating_arrows(cv, sx + sw // 2, sy + sh // 2, 20, t, speed=2.4, color=(28, 56, 98),
                                 progress=clamp01((t - t_s01) * 0.9))

        # Cable que baja hasta el enchufe en la pared (x=336, y=214)
        cable_pts = [(sx + sw // 2, sy + sh + 4), (206, 168), (274, 198), (336, 214)]
        d.line(cable_pts, fill=(*INK, 255), width=4)
        d.line(cable_pts, fill=(58, 72, 96, 255), width=2)
        # Enchufe en el zócalo
        d.rectangle([328, 204, 346, 224], fill=(224, 220, 208, 255), outline=(*INK, 255))
        d.rectangle([333, 210, 341, 218], fill=(38, 42, 56, 255))

        # Pulsos de electricidad subiendo del enchufe a la pantalla
        if t >= t_elec - 0.15:
            for k_p in range(4):
                u = ((t * 1.8 + k_p * 0.25) % 1.0)
                # Interpolación sobre cable_pts de enchufe (fin) a pantalla (inicio)
                px = int(round(336 + (206 - 336) * u))
                py = int(round(214 + (138 - 214) * u))
                draw_phosphor_dot(cv, px, py, r=2, color=TESLA_CYAN)

        window(cv, 24, 10, 432, 24, fill=(12, 18, 34), border=TESLA_CYAN, alpha=0.92)
        draw_text(cv, "AHORA MISMO · TU PANTALLA", 240, 16, "press", 8, TESLA_CYAN, align="center",
                  reveal=max(1, int((t - t_s01 + 0.2) * 32)))
        return vignette(cv, 0.42)

    # Plano 2 (0:08 - 0:16): Alejamiento por escalones (enchufe -> casa -> torres -> central)
    cv = bg("bg_night_grid_city").copy()
    dt2 = t - t_s02
    step_idx = 1 if dt2 < 2.2 else (2 if dt2 < 4.4 else 3)
    d = ImageDraw.Draw(cv)

    # Línea de alta tensión cruzando de la central lejana (derecha) a la ciudad (izquierda)
    towers = [(92, 164), (196, 152), (304, 146), (402, 142)]
    for tx, ty in towers:
        d.line([(tx, ty), (tx - 10, 228)], fill=(44, 56, 78, 255), width=2)
        d.line([(tx, ty), (tx + 10, 228)], fill=(44, 56, 78, 255), width=2)
        d.line([(tx - 12, ty + 8), (tx + 12, ty + 8)], fill=(64, 80, 108, 255), width=2)

    # Cables y corriente que va y viene (100 veces por segundo)
    dir_sign = 1 if int(t * 16) % 2 == 0 else -1
    for i in range(len(towers) - 1):
        x0, y0 = towers[i]
        x1, y1 = towers[i + 1]
        d.line([(x0, y0 + 8), ((x0 + x1) // 2, max(y0, y1) + 16), (x1, y1 + 8)],
               fill=(90, 195, 255, 210), width=2)
        for p_i in range(3):
            u = ((t * 2.5 * dir_sign + p_i * 0.33) % 1.0)
            px = int(round(x0 + (x1 - x0) * u))
            py = int(round(y0 + 8 + math.sin(u * math.pi) * 8))
            draw_phosphor_dot(cv, px, py, r=2, color=AMBER if dir_sign > 0 else TESLA_CYAN)

    window(cv, 18, 10, 444, 26, fill=(12, 18, 34), border=TESLA_CYAN, alpha=0.94)
    lbl = f"ESCALÓN {step_idx}/3 · RED ELÉCTRICA" if t < t_cien else "CAMBIA DE SENTIDO 100 VECES POR SEGUNDO"
    draw_text(cv, lbl, 240, 17, "press", 8, TESLA_CYAN if t < t_cien else GOLD, align="center")

    # Indicador visual del vaivén de la corriente alterna en la parte inferior
    if t >= t_cien - 0.15:
        a, dy = pop(t, t_cien - 0.15)
        window(cv, 110, 196 + dy, 260, 38, fill=(14, 20, 38), border=GOLD)
        arrow_str = ">>> VA (50 Hz) >>>" if dir_sign > 0 else "<<< VIENE (50 Hz) <<<"
        draw_text(cv, arrow_str, 240, 204 + dy, "press", 8, TESLA_CYAN if dir_sign > 0 else AMBER, align="center")
        draw_text(cv, "100 CAMBIOS POR SEGUNDO", 240, 218 + dy, "silk", 8, CREAM, align="center")

    return vignette(cv, 0.35)


def s03_budapest_opening(t):
    """0:16 - 0:43: Parque de Budapest al atardecer -> palito en la arena -> 4 flechas -> Título."""
    cv = bg("bg_budapest_park_sunset").copy()
    cv = grade(cv, mul=(1.08, 0.96, 0.82), add=(10, 4, 0))
    t_s03 = TL.s("s03")
    t_poema = TL.word("s03", "poema")
    t_s04 = TL.s("s04")
    t_detuvo = TL.word("s04", "detuvo")
    t_palito = TL.word("s04", "palito")
    t_dibujo = TL.word("s04", "dibujo")
    t_s05 = TL.s("s05")
    t_s06 = TL.s("s06")

    # Si estamos en s05/s06 (0:30 - 0:43): primer plano del dibujo en la arena + título del episodio
    if t >= t_s05 - 0.25:
        d = ImageDraw.Draw(cv)
        if getattr(sys.modules.get("core"), "_VCTX", None) is None:
            # Suelo de arena dorada en primer plano (en 16:9)
            d.rectangle([0, 42, W, H], fill=(122, 82, 42, 235))
            for i in range(28):
                sx = (i * 53) % W
                sy = 48 + (i * 37) % (H - 54)
                d.rectangle([sx, sy, sx + 3, sy + 1], fill=(152, 106, 56, 180))

        draw_place_only(cv, "BUDAPEST", t, t_s03, border=AMBER)

        if t < t_s06 - 0.15:
            spin_spd = 2.6 if t >= t_s05 else 0.8
            draw_rotating_arrows(cv, 240, 118, 42, t, speed=spin_spd, color=GOLD, glow=AMBER,
                                 progress=1.0, sand_groove=True)
            a, dy = pop(t, t_s05)
            window(cv, 118, 178 + dy, 244, 36, fill=(24, 18, 12), border=GOLD)
            draw_text(cv, "ESE DIBUJO HACE GIRAR EL MUNDO", 240, 190 + dy, "silk", 8, GOLD, align="center",
                      reveal=max(1, int((t - t_s05 + 0.1) * 32)))
        else:
            # 0:35: Título en pixel sobre la arena con las flechas girando
            a, dy = pop(t, t_s06 - 0.1)
            window(cv, 116, 54 + dy, 248, 108, fill=(18, 14, 24), border=GOLD, alpha=0.94)
            draw_text(cv, "EL DIBUJO QUE", 240, 64 + dy, "press", 16, align="center",
                      gradient=GOLD_RAMP, outline_w=2, reveal=max(1, int((t - t_s06 + 0.2) * 24)))
            draw_text(cv, "ENCENDIÓ", 240, 88 + dy, "press", 16, align="center",
                      gradient=GOLD_RAMP, outline_w=2, reveal=max(0, int((t - t_s06 - 0.15) * 24)))
            draw_text(cv, "EL MUNDO", 240, 112 + dy, "press", 16, align="center",
                      gradient=GOLD_RAMP, outline_w=2, reveal=max(0, int((t - t_s06 - 0.35) * 24)))
            draw_text(cv, "LA HISTORIA DE NIKOLA TESLA", 240, 140 + dy, "silk", 8, TESLA_CYAN, align="center",
                      reveal=max(0, int((t - t_s06 - 0.6) * 32)))
        return vignette(cv, 0.35)

    # 0:16 - 0:30: Caminata por el parque de Budapest -> se detiene y dibuja con un palito
    draw_place_only(cv, "BUDAPEST", t, t_s03, border=AMBER)

    x_inv, w_inv = walk(t, t_s03, t_detuvo, 96, 214)
    x_fri, w_fri = walk(t, t_s03, t_detuvo, 52, 156)

    inv_arms = "down"
    if t_poema - 0.2 <= t < t_s04:
        inv_arms = "wave"
    elif t >= t_palito:
        inv_arms = "point"

    talking_poem = (t_s03 + 0.3 < t < t_s04 - 0.2)
    char(cv, "friend_budapest", x_fri, 250, t, scale=2, walk=w_fri,
         arms="down", look=1, mood="neutral")
    char(cv, "inventor", x_inv, 250, t, scale=2, walk=w_inv,
         arms=inv_arms, look=1, mood="happy" if t >= t_dibujo else "neutral",
         talk=talk_v(t, talking_poem))

    if talking_poem:
        bubble(cv, "«¡LA LUZ AVANZA!»", int(x_inv), 144)

    # Palito y círculo con cuatro flechas en la arena junto a sus pies / centro
    if t >= t_palito - 0.1:
        d = ImageDraw.Draw(cv)
        # Palito en la mano derecha del inventor
        d.line([(int(x_inv) + 18, 212), (int(x_inv) + 38, 236)], fill=(168, 118, 62, 255), width=2)
        draw_p = clamp01((t - t_dibujo + 0.2) / 1.4)
        # Ventana lupa mostrando el dibujo en la arena mientras lo traza
        a, dy = pop(t, t_palito)
        window(cv, 268, 72 + dy, 176, 118, fill=(68, 46, 24), border=AMBER)
        draw_text(cv, "ARENA · 4 FLECHAS", 356, 80 + dy, "silk", 8, CREAM, align="center")
        draw_rotating_arrows(cv, 356, 136 + dy, 34, t, speed=1.2 if draw_p >= 1.0 else 0.0,
                             color=GOLD, progress=draw_p, sand_groove=True)

    return vignette(cv, 0.35)


# ===========================================================================
# CAPÍTULO 1: HIJO DE LA TORMENTA (c1_01 .. c1_07)
# ===========================================================================

def c1_s01_smiljan_birth(t):
    """0:43 - 1:02: Pueblo de montaña bajo tormenta -> Interior con vela, partera y madre."""
    t0 = TL.s("c1_01")
    t_c1_02 = TL.s("c1_02")
    t_torm = TL.word("c1_02", "tormenta", occurrence=2)
    t_madre = TL.word("c1_02", "madre")
    t_luz = TL.word("c1_02", "luz")

    if t < t_c1_02 - 0.15:
        cv = bg("bg_smiljan_storm_1856").copy()
        RAIN.draw(cv, t)
        # Relámpago sobre la casa de montaña
        flash = 1.0 if abs(t - (t0 + 1.4)) < 0.18 or abs(t - (t0 + 3.1)) < 0.14 else 0.0
        if flash > 0:
            cv = grade(cv, mul=(1.35, 1.35, 1.55), add=(28, 32, 48))
            draw_tesla_sparks(cv, 260, 28, t, rays=3, max_len=95, color=TESLA_CYAN)
        draw_chapter_header(cv, t, t0, 1, "HIJO DE LA TORMENTA", "SMILJAN, HOY CROACIA", border=AMBER)
        return vignette(cv, 0.4)

    # Interior a la luz de una vela: partera, madre y bebé
    cv = bg("bg_candle_room_1856").copy()
    flash = 1.0 if abs(t - t_torm) < 0.22 else 0.0
    if flash > 0:
        cv = grade(cv, mul=(1.3, 1.35, 1.55), add=(24, 28, 44))

    draw_chapter_header(cv, t, t0, 1, "HIJO DE LA TORMENTA", "SMILJAN · 1856", border=AMBER)
    draw_candle(cv, 240, 168, t, scale=1)

    # Partera a la izquierda y madre a la derecha
    mother_holds = t >= t_madre - 0.1
    char(cv, "midwife", 156, 250, t, scale=2,
         arms="point" if (not mother_holds and t >= t_torm - 0.3) else "down",
         look=1, mood="worried" if t < t_madre else "neutral",
         talk=talk_v(t, t_torm - 0.3 < t < t_madre - 0.2))
    char(cv, "mother_tesla", 316, 250, t, scale=2,
         arms="hold" if mother_holds else "down",
         look=-1, mood="happy" if t >= t_luz - 0.2 else "neutral",
         talk=talk_v(t, t >= t_madre))

    # Bebé envuelto en manta clara
    bx = 296 if mother_holds else 176
    by = 204
    d = ImageDraw.Draw(cv)
    d.ellipse([bx - 10, by - 6, bx + 10, by + 6], fill=(244, 240, 228, 255), outline=(*INK, 255))
    d.ellipse([bx - 7, by - 4, bx - 1, by + 2], fill=(242, 196, 160, 255))

    if t_torm - 0.2 <= t < t_madre:
        bubble(cv, "«HIJO DE LA TORMENTA»", 156, 138)
    elif t >= t_luz - 0.25:
        bubble(cv, "«NO: DE LA LUZ»", 316, 138, fill=(255, 246, 210))
        sparkle(cv, 296, 194, t * 2, 3, GOLD)

    return vignette(cv, 0.38)


def c1_s02_cat_and_mind(t):
    """1:02 - 1:19: El chico acaricia al gato negro (chispas) -> máquina girando en su cabeza."""
    cv = bg("bg_candle_room_1856").copy()
    t_c1_03 = TL.s("c1_03")
    t_chis = TL.word("c1_03", "chispas")
    t_padre = TL.word("c1_03", "padre")
    t_c1_04 = TL.s("c1_04")
    t_imag = TL.word("c1_04", "imaginar")
    t_func = TL.word("c1_04", "funcionar")

    draw_candle(cv, 84, 172, t, scale=1)
    draw_place_only(cv, "SMILJAN · INFANCIA", t, t_c1_03, border=AMBER)

    if t < t_c1_04 - 0.15:
        # El chico acaricia al gato negro y el padre explica que es electricidad
        petting = t >= t_chis - 0.2
        char(cv, "boy_tesla", 176, 252, t, scale=2,
             arms="point" if petting else "down", look=1, mood="happy")
        draw_black_cat(cv, 222, 250, t, sparks=petting)
        if t >= t_padre - 0.3:
            a, _ = pop(t, t_padre - 0.3)
            char(cv, "father_tesla", 336, 252, t, alpha=a, scale=2,
                 arms="point_l" if t >= t_padre else "down", look=-1,
                 talk=talk_v(t, t >= t_padre))
            if t >= t_padre:
                bubble(cv, "ES ELECTRICIDAD, COMO LOS RAYOS", 316, 136)
        return vignette(cv, 0.42)

    # 1:12 - 1:19: Máquina imaginada en líneas de luz sobre su cabeza
    char(cv, "boy_tesla", 240, 252, t, scale=2,
         arms="think" if t < t_func else "cheer", look=0, mood="happy")

    if t >= t_imag - 0.25:
        a, dy = pop(t, t_imag - 0.25)
        build_p = clamp01((t - t_imag + 0.15) / 1.1)
        window(cv, 118, 52 + dy, 244, 94, fill=(14, 24, 44), border=TESLA_CYAN, alpha=0.92)
        draw_text(cv, "EN SU CABEZA · SIN CONSTRUIRLA", 240, 60 + dy, "silk", 8, TESLA_CYAN, align="center")
        spin_spd = 3.2 if t >= t_func - 0.1 else 0.4
        draw_rotating_arrows(cv, 240, 108 + dy, 28, t, speed=spin_spd,
                             color=TESLA_CYAN, glow=GOLD, progress=build_p)
        d = ImageDraw.Draw(cv)
        d.ellipse([232, 100 + dy, 248, 116 + dy], outline=(*GOLD, 255), width=2)

    return vignette(cv, 0.38)


def c1_s03_graz_imposible(t):
    """1:19 - 1:40: Aula en Graz, motor con chispas, palabra IMPOSIBLE en el pizarrón."""
    cv = bg("bg_graz_lecture_1875").copy()
    t_c1_05 = TL.s("c1_05")
    t_chis = TL.word("c1_05", "chispas")
    t_dijo = TL.word("c1_05", "Dijo")
    t_c1_06 = TL.s("c1_06")
    t_imp = TL.word("c1_06", "imposible")
    t_c1_07 = TL.s("c1_07")

    draw_place_only(cv, "GRAZ, AUSTRIA", t, t_c1_05, border=AMBER)

    # Pizarrón del aula universitaria en el centro-arriba
    window(cv, 116, 48, 248, 86, fill=BOARD_GREEN, border=WOOD_FRAME, alpha=0.96, inner=(42, 82, 58))
    if t < t_c1_06:
        draw_text(cv, "MOTOR DE CORRIENTE CONTINUA", 240, 62, "silk", 8, CHALK_WHITE, align="center")
        draw_text(cv, "ESCOBILLAS -> CHISPAS", 240, 82, "press", 8, CHALK_YELLOW, align="center")
    else:
        draw_text(cv, "MOTOR SIN CHISPAS:", 240, 60, "silk", 8, CHALK_WHITE, align="center")
        rev_imp = max(1, int((t - t_c1_06 - 0.2) * 18))
        draw_text(cv, "IMPOSIBLE", 240, 82, "press", 24, CHALK_RED, align="center",
                  outline_w=2, reveal=rev_imp)

    # Mesa con motor que larga chispas (x=218..262, y=184..216)
    d = ImageDraw.Draw(cv)
    d.rectangle([196, 206, 284, 248], fill=(92, 60, 34, 255), outline=(*INK, 255))
    d.rectangle([222, 186, 258, 206], fill=(168, 126, 58, 255), outline=(*INK, 255))
    if t < t_c1_06 + 0.5:
        draw_tesla_sparks(cv, 240, 192, t, rays=4, max_len=24, color=AMBER, core_col=CREAM)

    # Profesor a la izquierda y joven inventor a la derecha con estudiantes
    prof_arms = "write" if (t_c1_06 <= t < t_imp + 0.4) else ("point" if t < t_c1_06 else "down")
    char(cv, "prof_graz", 132, 250, t, scale=2, arms=prof_arms, look=1,
         mood="happy" if t >= t_c1_06 else "neutral",
         talk=talk_v(t, t_c1_06 <= t < t_c1_07 - 0.2))

    inv_arms = "wave" if (t_dijo - 0.15 <= t < t_c1_06) else "down"
    char(cv, "inventor", 336, 250, t, scale=2, arms=inv_arms, look=-1,
         mood="neutral", talk=talk_v(t, t_dijo - 0.1 <= t < t_c1_06 - 0.2))
    char(cv, "student_a", 398, 252, t, scale=2, arms="down", look=-1)

    if t_dijo - 0.1 <= t < t_c1_06:
        bubble(cv, "¿Y UNO SIN CHISPAS?", 336, 138)

    # En c1_07: oscurecimiento dramático dejando el rótulo IMPOSIBLE y al joven mirándolo
    if t >= t_c1_07:
        fade_k = clamp01((t - t_c1_07) / 2.2)
        cv = grade(cv, mul=(1.0 - 0.55 * fade_k, 1.0 - 0.55 * fade_k, 1.0 - 0.45 * fade_k))

    return vignette(cv, 0.38)


def scenes():
    return [
        (0.0, s01_screen_and_grid,
         lambda t: cam_push(t, 0.0, TL.s("s03"), 1.03, 1.0, (240, 135)), "ch01"),
        (TL.s("s03") - 0.15, s03_budapest_opening,
         lambda t: cam_push(t, TL.s("s03"), TL.s("c1_01"), 1.0, 1.03, (240, 135)), "ch01"),
        (TL.s("c1_01") - 0.15, c1_s01_smiljan_birth,
         lambda t: cam_push(t, TL.s("c1_01"), TL.s("c1_03"), 1.0, 1.03, (240, 135)), "ch01"),
        (TL.s("c1_03") - 0.15, c1_s02_cat_and_mind,
         lambda t: cam_push(t, TL.s("c1_03"), TL.s("c1_05"), 1.0, 1.03, (240, 135)), "ch01"),
        (TL.s("c1_05") - 0.15, c1_s03_graz_imposible,
         lambda t: cam_push(t, TL.s("c1_05"), TL.s("c2_01"), 1.0, 1.035, (240, 120)), "ch01"),
    ]


def music(A):
    """Acto 1: Zumbido grave de corriente alterna en la apertura + piano y cuerdas suaves en La menor."""
    t0 = 0.0
    t_park = TL.s("s03")
    t_end = TL.s("c2_01")
    # Zumbido firma de corriente alterna (100 Hz / 50 Hz) en la apertura
    A.add_pad(t0, t_park - t0, [55.0, 110.0], amp=0.045)
    # Piano y cuerdas suaves desde el parque de Budapest y Capítulo 1
    prog_chords = [
        [220.0, 261.63, 329.63],
        [174.61, 220.0, 261.63],
        [196.0, 246.94, 293.66],
        [164.81, 207.65, 246.94],
    ]
    melody = [440.0, 523.25, 493.88, 440.0, 392.0, 329.63, 349.23, 329.63]
    A.Wait_or_loop = None
    beat = 60.0 / 88.0
    t = t_park
    idx = 0
    while t < t_end:
        ch = prog_chords[idx % len(prog_chords)]
        dur = min(beat * 4, t_end - t)
        A.add_pad(t, dur, ch, amp=0.038)
        for b in range(4):
            nt = t + b * beat
            if nt >= t_end:
                break
            f_note = melody[(idx * 4 + b) % len(melody)]
            A.add_note(nt, beat * 0.85, f_note, wave="triangle", amp=0.055, vibrato=2.5)
            A.add_bass(nt, beat * 0.9, ch[0] * 0.5, amp=0.05)
        t += beat * 4
        idx += 1


def sfx(A):
    A.fx_Rumble(0.05, dur=1.2, amp=0.08) if hasattr(A, "fx_Rumble") else A.fx_thud(0.05, 0.08)
    A.fx_pop(TL.s("s02"), 0.08)
    A.fx_sweep(TL.s("s03"), 0.45, 220, 440, 0.06)
    A.fx_pop(TL.word("s04", "palito"), 0.09)
    A.fx_chime(TL.s("s06"), 0.12)
    A.fx_thud(TL.s("c1_01"), 0.10)
    A.fx_sparkle(TL.word("c1_02", "luz"), 0.10)
    A.fx_sparkle(TL.word("c1_03", "chispas"), 0.09)
    A.fx_pop(TL.word("c1_06", "imposible"), 0.11)
