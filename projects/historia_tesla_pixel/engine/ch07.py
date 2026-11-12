"""Capítulo 7: La torre (Colorado Springs, la foto de doble exposición, Wardenclyffe, Marconi y LA PIZARRA: Energía sin cables)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa


def c7_s01_colorado_springs(t):
    """7:45 - 8:11: Colorado Springs (rayos de 30m, apagón en la ciudad y el truco de la foto de doble exposición)."""
    cv = bg("bg_colorado_springs_1899").copy()
    t0 = TL.s("c7_01")
    t_ray = TL.word("c7_01", "rayos")
    t_c7_02 = TL.s("c7_02")
    t_osc = TL.word("c7_02", "oscuras")
    t_c7_03 = TL.s("c7_03")
    t_truco = TL.word("c7_03", "truco")

    draw_chapter_header(cv, t, t0, 7, "LA TORRE", "COLORADO SPRINGS · 1899", border=TESLA_VIOLET)
    d = ImageDraw.Draw(cv)

    if t < t_c7_02:
        # Rayos gigantes de 30 metros saliendo del mástil de Colorado Springs
        glow(cv, 240, 96, 78, TESLA_VIOLET, 0.55)
        draw_tesla_sparks(cv, 240, 98, t, radius=76, count=7, color=TESLA_SPARK)
        window(cv, 122, 52, 236, 42, fill=(18, 22, 38), border=TESLA_CYAN)
        draw_text(cv, "RAYOS ARTIFICIALES DE +30 METROS", 240, 60, "silk", 8, TESLA_CYAN, align="center")
        draw_text(cv, "RÉCORD EN COLORADO SPRINGS", 240, 76, "silk", 8, CREAM, align="center")
        char(cv, "inventor", 156, 248, t, scale=2, arms="up", look=1, mood="happy")
    elif t < t_c7_03:
        # Apagón en la ciudad: el fondo se oscurece cuando dice "a oscuras" y Tesla paga la reparación
        if t >= t_osc - 0.25:
            cv = tint(cv, (6, 8, 16), 0.72)
            glow(cv, 198, 212, 26, GOLD, 0.65)  # Linterna de mano
        # Generador humeante a la derecha
        d.rectangle([286, 202, 336, 244], fill=(56, 52, 58, 255), outline=(*CHALK_RED, 255))
        for k in range(3):
            hy = 192 - int((t * 18 + k * 7) % 20)
            d.ellipse([304 + k * 5, hy - 4, 314 + k * 5, hy + 4], fill=(140, 144, 152, 200))
        window(cv, 122, 54, 236, 48, fill=(32, 16, 22), border=CHALK_RED)
        draw_text(cv, "¡GENERADOR MUNICIPAL QUEMADO!", 240, 62, "silk", 8, CHALK_RED, align="center")
        draw_text(cv, "CIUDAD A OSCURAS · TUVO QUE PAGAR", 240, 80, "silk", 8, GOLD, align="center")
        char(cv, "inventor", 184, 248, t, scale=2, arms="offer", look=1, mood="sad")
    else:
        # La foto más famosa: leyendo sentado junto a rayos -> se separa en DOS FOTOS SUPERPUESTAS
        split_p = clamp01((t - (t_truco - 0.1)) / 0.8) if t >= t_truco - 0.1 else 0.0
        sep = int(52 * ease_out(split_p))

        window(cv, 118, 44, 244, 162, fill=(20, 22, 32), border=GOLD)
        draw_text(cv, "LA FOTO MÁS FAMOSA (1899)", 240, 52, "silk", 8, GOLD, align="center")

        # Capa 1 (izquierda al separarse): Tesla sentado leyendo con calma en el laboratorio apagado
        c1_x = 240 - sep
        d.rectangle([c1_x - 56, 72, c1_x + 56, 168], fill=(32, 30, 38, 255), outline=(*CREAM, 255))
        char(cv, "inventor", c1_x, 162, t, scale=1, arms="hold", look=1)
        draw_text(cv, "FOTO 1: LEYENDO", c1_x, 154, "silk", 8, CREAM, align="center")

        # Capa 2 (derecha al separarse): Los rayos gigantes disparados en la oscuridad sin nadie en la silla
        c2_x = 240 + sep
        if sep > 4:
            d.rectangle([c2_x - 56, 72, c2_x + 56, 168], fill=(18, 22, 42, 255), outline=(*TESLA_CYAN, 255))
            draw_text(cv, "FOTO 2: RAYOS", c2_x, 154, "silk", 8, TESLA_CYAN, align="center")
        draw_tesla_sparks(cv, c2_x, 112, t, radius=38, count=5, color=TESLA_CYAN)

        draw_text(cv, "DOBLE EXPOSICIÓN" if split_p > 0.2 else "LEYENDO JUNTO A RAYOS GIGANTES",
                  240, 182, "press", 8, TESLA_CYAN if split_p > 0.2 else CREAM, align="center")

    return vignette(cv, 0.34)


def c7_s02_wardenclyffe_and_marconi(t):
    """8:11 - 8:37: Torre Wardenclyffe en Long Island (J. P. Morgan US$150.000) vs la señal transatlántica de Marconi."""
    t0 = TL.s("c7_04")
    t_c7_05 = TL.s("c7_05")
    t_c7_06 = TL.s("c7_06")
    t_mar = TL.word("c7_06", "Marconi")
    t_mor = TL.word("c7_06", "Morgan")

    if t < t_c7_06:
        cv = bg("bg_wardenclyffe_1901").copy()
        draw_place_only(cv, "WARDENCLYFFE · LONG ISLAND", t, t0, border=GOLD)

        if t < t_c7_05:
            # J. P. Morgan entrega US$150.000 para construir la torre
            window(cv, 122, 54, 236, 52, fill=(18, 24, 38), border=GOLD)
            draw_text(cv, "INVERSOR: J. P. MORGAN", 240, 62, "silk", 8, GOLD, align="center")
            draw_text(cv, "APORTE: US$150.000", 240, 80, "press", 8, CHALK_GREEN, align="center")
            char(cv, "banker_morgan", 160, 248, t, scale=2, arms="offer", look=1)
            char(cv, "inventor", 320, 248, t, scale=2, arms="hold", look=-1, mood="happy")
        else:
            # Cúpula de la torre emitiendo ondas para todo el planeta
            glow(cv, 240, 88, 64, TESLA_CYAN, 0.55)
            for k in range(3):
                r_w = int(((t * 36 + k * 24) % 72)) + 16
                d = ImageDraw.Draw(cv)
                d.ellipse([240 - r_w, 88 - r_w // 2, 240 + r_w, 88 + r_w // 2], outline=(*TESLA_CYAN, 200))
            window(cv, 118, 52, 244, 52, fill=(16, 24, 42), border=TESLA_CYAN)
            draw_text(cv, "EL SUEÑO DE TESLA:", 240, 60, "silk", 8, TESLA_CYAN, align="center")
            draw_text(cv, "ENERGÍA SIN CABLES MUNDIAL", 240, 78, "silk", 8, CREAM, align="center")
            char(cv, "inventor", 240, 248, t, scale=2, arms="up", look=1, mood="happy")
        return vignette(cv, 0.32)

    # c7_06: Marconi cruza el Atlántico con 3 pitidos ("S" = · · ·) y Morgan cierra la billetera
    cv = bg("bg_marconi_station_1901").copy()
    draw_place_only(cv, "MARCONI · SEÑAL TRANSATLÁNTICA (1901)", t, t_c7_06, border=AMBER)

    window(cv, 118, 52, 244, 68, fill=(18, 26, 38), border=GOLD)
    draw_text(cv, "MARCONI CRUZA EL ATLÁNTICO:", 240, 60, "silk", 8, GOLD, align="center")
    dots = "·  " * (1 + (int(t * 4) % 3))
    draw_text(cv, f"SEÑAL DE RADIO: {dots}", 240, 78, "press", 8, TESLA_CYAN, align="center")
    if t >= t_mor - 0.25:
        draw_text(cv, "MORGAN CORTA EL FINANCIAMIENTO", 240, 98, "silk", 8, CHALK_RED, align="center")

    char(cv, "marconi_op", 156, 248, t, scale=2, arms="work", look=1, mood="happy")
    char(cv, "banker_morgan", 332, 248, t, scale=2, arms="down", look=-1, mood="angry")
    return vignette(cv, 0.36)


def c7_s03_pizarra_wireless(t):
    """8:37 - 9:02: LA PIZARRA · ENERGÍA SIN CABLES (la luz que se dispersa vs carga inalámbrica del teléfono a centímetros)."""
    cv = Image.new("RGBA", (W, H), (14, 28, 22, 255))
    t0 = TL.s("c7_07")
    t_lam = TL.word("c7_07", "lámpara")
    t_c7_08 = TL.s("c7_08")
    t_cm = TL.word("c7_08", "centímetros")
    t_c7_09 = TL.s("c7_09")

    draw_pizarra_frame(cv, "LA PIZARRA · ENERGÍA SIN CABLES", t, t0)
    d = ImageDraw.Draw(cv)

    if t < t_c7_08:
        # Paso 1 (c7_07): Lámpara en el centro cuyos rayos se abren para todos lados y se debilitan con la distancia
        window(cv, 118, 44, 244, 156, fill=(18, 36, 28), border=CHALK_YELLOW)
        draw_text(cv, "COMO LA LUZ DE UNA LÁMPARA:", 240, 52, "silk", 8, CHALK_YELLOW, align="center")

        bulb(cv, 240, 122, t, on=1.0)
        for k in range(3):
            rr = 22 + k * 20 + int((t * 18) % 16)
            alpha_c = max(50, 230 - rr * 3)
            d.ellipse([240 - rr, 122 - rr // 2, 240 + rr, 122 + rr // 2],
                      outline=(*CHALK_YELLOW, alpha_c))
        draw_text(cv, "SE REPARTE PARA TODOS LADOS", 240, 164, "silk", 8, CHALK_WHITE, align="center")
        draw_text(cv, "LEJOS LLEGA MUY POCA ENERGÍA", 240, 180, "silk", 8, CHALK_RED, align="center")
    else:
        # Paso 2 (c7_08..c7_09): A pocos centímetros funciona muy bien -> Base cargando un teléfono + Sello
        window(cv, 118, 42, 244, 114, fill=(18, 36, 28), border=CHALK_CYAN)
        draw_text(cv, "A POCOS CENTÍMETROS: ¡FUNCIONA!", 240, 50, "silk", 8, CHALK_GREEN, align="center")

        # Base de carga con bobina inferior (tiza amarilla)
        d.rectangle([184, 122, 296, 134], fill=(32, 58, 48, 255), outline=(*CHALK_YELLOW, 255))
        draw_text(cv, "BASE (BOBINA 1)", 240, 138, "silk", 8, CHALK_YELLOW, align="center")

        # Teléfono apoyado a milímetros encima con bobina receptora y batería cargando
        d.rectangle([196, 86, 284, 116], fill=(20, 34, 46, 255), outline=(*CHALK_CYAN, 255))
        # Icono de batería llenándose en la pantalla del teléfono
        bat_w = int(32 * clamp01((t - t_c7_08) / 2.2))
        d.rectangle([222, 95, 258, 107], outline=(*CHALK_WHITE, 255))
        d.rectangle([258, 98, 261, 104], fill=(*CHALK_WHITE, 255))
        if bat_w > 0:
            d.rectangle([224, 97, 224 + bat_w, 105], fill=(*CHALK_GREEN, 255))
        # Ondas cortas verdes entre base y teléfono
        for lx in (212, 240, 268):
            d.line([(lx, 121), (lx, 116)], fill=(*CHALK_GREEN, 255), width=2)
        draw_text(cv, "CARGA TU TELÉFONO", 240, 70, "silk", 8, CHALK_WHITE, align="center")

        # Sello en una frase
        a, dy = pop(t, t_c7_08 + 0.4)
        window(cv, 118, 162 + dy, 244, 46, fill=(22, 48, 36), border=CHALK_GREEN)
        draw_text(cv, "EN UNA FRASE:", 240, 169 + dy, "silk", 8, CHALK_GREEN, align="center")
        draw_text(cv, "LA DISTANCIA SE COME LA ENERGÍA", 240, 185 + dy, "silk", 8, CHALK_WHITE, align="center")

    return vignette(cv, 0.24)


SCENES = [
    (TL.s("c7_01"), TL.s("c7_04"), c7_s01_colorado_springs),
    (TL.s("c7_04"), TL.s("c7_07"), c7_s02_wardenclyffe_and_marconi),
    (TL.s("c7_07"), TL.s("c8_01"), c7_s03_pizarra_wireless),
]


def scenes():
    return [(s[0], s[2], None) for s in SCENES]


def music(A):
    """Acto 3: Colorado Springs, Wardenclyffe y La Pizarra 4 (Energía sin cables)."""
    t0 = TL.s("c7_01")
    t_piz = TL.s("c7_07")
    t_end = TL.s("c8_01")
    A.add_pad(t0, t_piz - t0, [110.0, 164.81, 220.0, 261.63], amp=0.04)
    piz_beat = 60.0 / 112.0
    piz_arp = [523.25, 659.25, 783.99, 659.25, 587.33, 698.46, 880.0, 698.46]
    t = t_piz
    step = 0
    while t < t_end:
        f_n = piz_arp[step % len(piz_arp)]
        A.add_note(t, piz_beat * 0.42, f_n, wave="pulse25", amp=0.042)
        t += piz_beat * 0.5
        step += 1


def sfx(A):
    A.fx_sparkle(TL.word("c7_01", "rayos"), 0.12)
    A.fx_thud(TL.word("c7_02", "oscuras"), 0.11)
    A.fx_pop(TL.word("c7_03", "truco"), 0.09)
    A.fx_pop(TL.s("c7_04"), 0.09)
    A.fx_chime(TL.word("c7_06", "Marconi"), 0.10)
    A.fx_chime(TL.s("c7_09"), 0.11)

