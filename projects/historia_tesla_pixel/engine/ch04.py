"""Capítulo 4: La guerra de las corrientes (Westinghouse, LA PIZARRA: El Transformador y los tubos de luz)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa


def c4_s01_westinghouse(t):
    """3:55 - 4:10: Oficina de George Westinghouse; firma de contrato y contador US$2,50 por caballo de fuerza."""
    cv = bg("bg_westinghouse_office_1888").copy()
    t0 = TL.s("c4_01")
    t_west = TL.word("c4_01", "Uéstinjaus")
    t_alt = TL.word("c4_01", "alterna")
    t_c4_02 = TL.s("c4_02")
    t_dos = TL.word("c4_02", "dos")
    t_rec = TL.word("c4_02", "Recuerda")

    draw_chapter_header(cv, t, t0, 4, "LA GUERRA DE LAS CORRIENTES", "WESTINGHOUSE · 1888", border=GOLD)

    # Plano del motor de corriente alterna sobre el escritorio
    d = ImageDraw.Draw(cv)
    d.rectangle([198, 210, 282, 224], fill=(24, 52, 88, 255), outline=(*TESLA_CYAN, 255))
    draw_rotating_arrows(cv, 240, 217, 5, t * 2.2, color=TESLA_CYAN, pulse=0.8)

    # Tarjeta contador US$2,50 POR CABALLO DE FUERZA (dentro de x=120..360 para 9:16 1:1)
    if t >= t_c4_02 - 0.15:
        a, dy = pop(t, t_c4_02 - 0.15)
        glow_rec = t >= t_rec - 0.2
        border_c = TESLA_SPARK if glow_rec else GOLD
        window(cv, 120, 62 + dy, 240, 58, fill=(18, 24, 38), border=border_c)
        draw_text(cv, "REGALÍA POR PATENTE DE MOTOR:", 240, 70 + dy, "silk", 8, CREAM, align="center")
        draw_text(cv, "US$2,50 POR CABALLO DE FUERZA", 240, 86 + dy, "silk", 8, GOLD, align="center")
        draw_text(cv, "RECUERDA ESE NÚMERO", 240, 102 + dy, "silk", 8,
                  TESLA_CYAN if glow_rec else SOFT_GRAY, align="center")

    # Westinghouse a la izquierda, Tesla a la derecha estrechando / firmando
    char(cv, "westinghouse_gen", 156, 250, t, scale=2,
         arms="offer" if t >= t_c4_02 else "point", look=1, mood="happy",
         talk=talk_v(t, t_west <= t < t_rec))
    char(cv, "inventor", 324, 250, t, scale=2,
         arms="offer" if t >= t_c4_02 else "down", look=-1, mood="happy")

    return vignette(cv, 0.34)


def c4_s02_pizarra_transformador(t):
    """4:10 - 4:49: LA PIZARRA · EL TRANSFORMADOR (calor en cables, alta tensión, casita y centrales cada 1,5 km)."""
    cv = Image.new("RGBA", (W, H), (14, 28, 22, 255))
    t0 = TL.s("c4_03")
    t_c4_04 = TL.s("c4_04")
    t_calor = TL.word("c4_04", "calor")
    t_mucha = TL.word("c4_04", "mucha")
    t_poca = TL.word("c4_04", "poca")
    t_c4_05 = TL.s("c4_05")
    t_sube = TL.word("c4_05", "sube")
    t_baja = TL.word("c4_05", "baja")
    t_c4_06 = TL.s("c4_06")
    t_km = TL.word("c4_06", "kilómetro")

    draw_pizarra_frame(cv, "LA PIZARRA · EL TRANSFORMADOR", t, t0)
    d = ImageDraw.Draw(cv)

    if t < t_c4_05:
        # Paso 1 (c4_03..c4_04): Cable que pierde calor vs. poca corriente a alta tensión
        window(cv, 118, 42, 244, 78, fill=(18, 36, 28), border=CHALK_RED)
        draw_text(cv, "MUCHA CORRIENTE = MUCHO CALOR", 240, 48, "silk", 8, CHALK_RED, align="center")
        # Cable grueso al rojo vivo con ondas de calor
        heat_on = t >= t_calor - 0.3
        wire_c = (255, 96, 82, 255) if heat_on else (190, 200, 194, 255)
        d.rectangle([136, 74, 344, 84], fill=wire_c, outline=(*CHALK_WHITE, 255))
        for k in range(6):
            px = int((142 + k * 34 + t * 28) % 200) + 138
            d.ellipse([px - 2, 76, px + 2, 82], fill=(*CHALK_YELLOW, 255))
            if heat_on:
                wy = 66 - int(3 * abs(math.sin(t * 8 + k)))
                d.line([(px, 72), (px - 3, wy), (px + 2, wy - 5)], fill=(*CHALK_RED, 220), width=1)
        draw_text(cv, "LA ENERGÍA SE PIERDE EN EL CABLE", 240, 96, "silk", 8, CHALK_WHITE, align="center")

        # Abajo: Poca corriente a mucha tensión (manguera fina a presión)
        if t >= t_poca - 0.5:
            a, dy = pop(t, t_poca - 0.5)
            window(cv, 118, 126 + dy, 244, 84, fill=(18, 36, 28), border=CHALK_CYAN)
            draw_text(cv, "POCA CORRIENTE + ALTA TENSIÓN", 240, 132 + dy, "silk", 8, CHALK_CYAN, align="center")
            d.rectangle([136, 156 + dy, 312, 160 + dy], fill=(80, 210, 245, 255))
            for k in range(4):
                px = int((140 + k * 44 + t * 95) % 170) + 138
                d.ellipse([px - 2, 155 + dy, px + 2, 161 + dy], fill=(*CHALK_WHITE, 255))
            # Rueda/turbina girando al final del chorro de alta presión
            draw_rotating_arrows(cv, 328, 158 + dy, 12, t * 4.5, color=CHALK_YELLOW, pulse=0.9)
            draw_text(cv, "VIAJA LEJOS CASI SIN CALENTAR", 240, 184 + dy, "silk", 8, CHALK_GREEN, align="center")
            draw_chalk_hand(cv, 306, 166 + dy, t)
    elif t < t_c4_06:
        # Paso 2 (c4_05): Diagrama del transformador (Central -> Sube ↑ -> Cable largo -> Baja ↓ -> Casa)
        window(cv, 118, 44, 244, 118, fill=(18, 36, 28), border=CHALK_CYAN)
        draw_text(cv, "EL VIAJE DE LA CORRIENTE ALTERNA", 240, 52, "silk", 8, CHALK_YELLOW, align="center")

        # 1. Central (izq)
        d.rectangle([128, 92, 156, 124], fill=(32, 54, 44, 255), outline=(*CHALK_WHITE, 255))
        draw_text(cv, "CENTRAL", 142, 128, "silk", 8, CHALK_WHITE, align="center")

        # 2. Transformador SUBE
        up_glow = t >= t_sube - 0.3
        d.rectangle([168, 86, 198, 124], fill=(28, 68, 56, 255),
                    outline=(*(CHALK_YELLOW if up_glow else CHALK_WHITE), 255))
        d.polygon([(183, 94), (177, 102), (189, 102)], fill=(*CHALK_YELLOW, 255))
        d.rectangle([181, 102, 185, 114], fill=(*CHALK_YELLOW, 255))
        draw_text(cv, "SUBE", 183, 128, "silk", 8, CHALK_YELLOW, align="center")

        # 3. Línea de alta tensión larga
        d.line([(198, 96), (278, 96)], fill=(*CHALK_CYAN, 255), width=2)
        px = 202 + int(((t * 72) % 72))
        d.ellipse([px - 2, 94, px + 2, 98], fill=(*CHALK_WHITE, 255))
        draw_text(cv, "ALTA TENSIÓN", 238, 78, "silk", 8, CHALK_CYAN, align="center")

        # 4. Transformador BAJA
        dn_glow = t >= t_baja - 0.3
        d.rectangle([278, 86, 308, 124], fill=(28, 68, 56, 255),
                    outline=(*(CHALK_GREEN if dn_glow else CHALK_WHITE), 255))
        d.rectangle([291, 94, 295, 106], fill=(*CHALK_GREEN, 255))
        d.polygon([(293, 114), (287, 106), (299, 106)], fill=(*CHALK_GREEN, 255))
        draw_text(cv, "BAJA", 293, 128, "silk", 8, CHALK_GREEN, align="center")

        # 5. Casita con ventana iluminada
        d.polygon([(322, 96), (338, 82), (354, 96)], fill=(44, 68, 54, 255), outline=(*CHALK_WHITE, 255))
        d.rectangle([324, 96, 352, 124], fill=(32, 54, 44, 255), outline=(*CHALK_WHITE, 255))
        win_c = CHALK_YELLOW if dn_glow else (60, 74, 68)
        d.rectangle([333, 103, 343, 113], fill=(*win_c, 255))
        draw_text(cv, "CASA", 338, 128, "silk", 8, CHALK_YELLOW, align="center")
        draw_chalk_hand(cv, 294 if dn_glow else 184, 114, t)
    else:
        # Paso 3 (c4_06): Continua (una central cada 1,5 km) + Sello final
        window(cv, 118, 42, 244, 112, fill=(18, 36, 28), border=CHALK_RED)
        draw_text(cv, "CORRIENTE CONTINUA (1888):", 240, 50, "silk", 8, CHALK_RED, align="center")
        draw_text(cv, "1 CENTRAL CADA 1,5 KM", 240, 66, "press", 8, CHALK_YELLOW, align="center")
        for i, sx in enumerate((142, 192, 242, 292, 334)):
            d.rectangle([sx - 12, 98, sx + 12, 124], fill=(56, 42, 42, 255), outline=(*CHALK_RED, 255))
            d.rectangle([sx - 4, 84, sx + 2, 98], fill=(72, 56, 56, 255))
            # Humo de cada central
            hy = 78 - int((t * 14 + i * 5) % 10)
            d.ellipse([sx - 5, hy - 3, sx + 3, hy + 3], fill=(140, 148, 144, 190))
        draw_text(cv, "BARRIOS LLENOS DE HUMO Y CABLES", 240, 134, "silk", 8, CHALK_WHITE, align="center")

        # Sello en una frase
        a, dy = pop(t, t_km - 0.2)
        window(cv, 118, 164 + dy, 244, 44, fill=(22, 48, 36), border=CHALK_GREEN)
        draw_text(cv, "EN UNA FRASE:", 240, 171 + dy, "silk", 8, CHALK_GREEN, align="center")
        draw_text(cv, "LA ALTERNA VIAJA LEJOS", 240, 187 + dy, "press", 8, CHALK_WHITE, align="center")

    return vignette(cv, 0.24)


def c4_s03_fear_and_tubes(t):
    """4:49 - 5:19: Titulares de miedo ('¡PELIGRO: CORRIENTE ALTERNA!') vs. Tesla iluminando tubos con las manos."""
    t0 = TL.s("c4_07")
    t_c4_08 = TL.s("c4_08")
    t_manos = TL.word("c4_08", "manos")
    t_pel = TL.word("c4_08", "peligroso")
    t_c4_09 = TL.s("c4_09")

    if t < t_c4_08:
        # Diarios cayendo con titulares alarmistas (sin animales ni silla eléctrica)
        cv = bg("bg_westinghouse_office_1888").copy()
        cv = tint(cv, (24, 14, 22), 0.55)
        for i in range(3):
            ti = t0 + i * 0.65
            if t >= ti:
                a, dy = pop(t, ti)
                ny = 42 + i * 52 + dy
                window(cv, 118, ny, 244, 44, fill=(236, 226, 202), border=RED)
                draw_text(cv, "EXTRA · DIARIO DE NUEVA YORK", 240, ny + 7, "silk", 8, INK, align="center")
                draw_text(cv, "¡PELIGRO: CORRIENTE ALTERNA!", 240, ny + 22, "silk", 8, RED, align="center")
        char(cv, "edison_gen", 136, 250, t, scale=2, arms="point", look=1, mood="angry", talk=talk_v(t, True))
        return vignette(cv, 0.45)

    # Escenario oscuro: Tesla iluminando dos tubos de vidrio con sus propias manos
    cv = bg("bg_stage_tubes_1891").copy()
    d = ImageDraw.Draw(cv)

    # Halo eléctrico detrás del inventor
    glow_r = 68 + int(8 * math.sin(t * 10))
    glow(cv, 240, 188, glow_r, TESLA_CYAN, 0.45 if t < t_c4_09 else 0.65)
    draw_tesla_sparks(cv, 240, 198, t, radius=48, count=5, color=TESLA_VIOLET)

    char(cv, "inventor", 240, 246, t, scale=2, arms="up", look=1, mood="happy")

    # Dos tubos fluorescentes brillantes en sus manos (izquierda y derecha)
    tube_col = TESLA_SPARK if int(t * 18) % 2 == 0 else TESLA_CYAN
    d.line([(196, 196), (222, 162)], fill=(*tube_col, 255), width=4)
    d.line([(284, 196), (258, 162)], fill=(*tube_col, 255), width=4)
    glow(cv, 208, 178, 24, TESLA_CYAN, 0.55)
    glow(cv, 272, 178, 24, TESLA_CYAN, 0.55)

    # Placa roja de advertencia obligatoria: NO LO INTENTES
    if t >= t_pel - 0.6 or t >= t_c4_09:
        a, dy = pop(t, min(t_pel - 0.6, t_c4_09))
        window(cv, 124, 44 + dy, 232, 52, fill=(38, 14, 18), border=CHALK_RED)
        draw_text(cv, "ADVERTENCIA · ALTA FRECUENCIA", 240, 52 + dy, "silk", 8, CHALK_YELLOW, align="center")
        draw_text(cv, "NO LO INTENTES", 240, 68 + dy, "press", 8, CHALK_RED, align="center")
    else:
        window(cv, 124, 44, 232, 42, fill=(16, 22, 38), border=TESLA_CYAN)
        draw_text(cv, "DEMOSTRACIÓN PÚBLICA · 1891", 240, 52, "silk", 8, TESLA_CYAN, align="center")
        draw_text(cv, "LUZ EN LAS MANOS", 240, 68, "silk", 8, CREAM, align="center")

    # Siluetas del público maravillado abajo a los lados
    char(cv, "investor_a", 104, 254, t, scale=2, arms="up" if t >= t_c4_09 else "down", look=1)
    char(cv, "investor_b", 376, 254, t, scale=2, arms="up" if t >= t_c4_09 else "down", look=-1)

    return vignette(cv, 0.36)


SCENES = [
    (TL.s("c4_01"), TL.s("c4_03"), c4_s01_westinghouse),
    (TL.s("c4_03"), TL.s("c4_07"), c4_s02_pizarra_transformador),
    (TL.s("c4_07"), TL.s("c5_01"), c4_s03_fear_and_tubes),
]


def scenes():
    return [(s[0], s[2], None) for s in SCENES]


def music(A):
    """Acto 2: La guerra de las corrientes + tema juguetón de La Pizarra 2 (El Transformador)."""
    t0 = TL.s("c4_01")
    t_piz = TL.s("c4_03")
    t_fear = TL.s("c4_07")
    t_end = TL.s("c5_01")
    A.add_pad(t0, t_piz - t0, [146.83, 220.0, 293.66], amp=0.04)
    piz_beat = 60.0 / 112.0
    piz_arp = [523.25, 659.25, 783.99, 659.25, 587.33, 698.46, 880.0, 698.46]
    t = t_piz
    step = 0
    while t < t_fear:
        f_n = piz_arp[step % len(piz_arp)]
        A.add_note(t, piz_beat * 0.42, f_n, wave="pulse25", amp=0.042)
        t += piz_beat * 0.5
        step += 1
    A.add_pad(t_fear, t_end - t_fear, [110.0, 164.81, 220.0, 329.63], amp=0.042)


def sfx(A):
    A.fx_pop(TL.s("c4_02"), 0.09)
    A.fx_pop(TL.s("c4_03"), 0.09)
    A.fx_chime(TL.word("c4_06", "kilómetro"), 0.11)
    A.fx_thud(TL.s("c4_07"), 0.09)
    A.fx_sparkle(TL.word("c4_08", "manos"), 0.12)

