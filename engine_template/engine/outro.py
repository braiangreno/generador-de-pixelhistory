"""Cierre de marca (Pixeloide Studios) y pantalla de créditos finales.

Sigue fielmente el Manual de Marca de Pixeloide Studios (Versión 1.0 - 2026):
- Colores oficiales: Ink (#070A1F), Surface (#0D1132), Paper (#F4F3EE), Cyan (#28DCE0), Magenta (#E732B6)
- Gráfica: Campo de píxeles reactivo que se enciende de cian a magenta
- Logotipo: Isotipo «Una P que es un play» (triángulo cian, banda Paper y triángulo magenta) + PIXELOIDE / STUDIOS
- Motion: Barrido de página en cian (520 ms) y curvas suaves cubic-bezier(.2,.7,.2,1)
- Créditos: Idea Original y Producción (Braian Greno) + Herramientas de IA utilizadas
"""
import json
import math
import os
import numpy as np
from PIL import Image, ImageDraw

from common import *  # noqa


def _credito_imagenes():
    """Qué IA hizo el arte: production_plan.json → "creditos": {"imagenes": "NANO BANANA / GPT IMAGE"}.
    Si el plan no lo dice, queda el texto del manual de marca."""
    try:
        plan_path = os.path.join(ROOT, "production_plan.json")
        if os.path.exists(plan_path):
            valor = (json.load(open(plan_path, encoding="utf-8")).get("creditos") or {}).get("imagenes")
            if valor:
                return str(valor).upper()
    except Exception:
        pass
    return "IMAGEN / NANOBANANA"


CREDITO_IMAGENES = _credito_imagenes()

# --------------------------------------------------------------------------- paleta oficial Pixeloide Studios
PX_INK = (7, 10, 31)         # #070A1F - Fondo principal
PX_SURFACE = (13, 17, 50)    # #0D1132 - Tarjetas y paneles
PX_PAPER = (244, 243, 238)   # #F4F3EE - Texto y fondo claro
PX_CYAN = (40, 220, 224)     # #28DCE0 - Acento y CTA
PX_MAGENTA = (231, 50, 182)  # #E732B6 - Chispa
PX_BORDER = (50, 56, 92)     # Línea divisoria 1 px (Paper al 15% sobre Surface)
PX_MUTED = (165, 172, 196)   # Texto secundario


def bezier_smooth(t):
    """Aproximación fiel a cubic-bezier(.2, .7, .2, 1): arranca decidido, frena suave."""
    t = clamp01(t)
    return 1.0 - (1.0 - t) ** 3.4


def bezier_wipe(t):
    """Aproximación a cubic-bezier(.76, 0, .24, 1) para el barrido de página en cian."""
    t = clamp01(t)
    return t * t * (3.0 - 2.0 * t) if t < 0.5 else 1.0 - ((-2.0 * t + 2.0) ** 3) / 2.0


def pixel_field_bg(t, focus_x=320, focus_y=135, radius=165.0, boost=1.0):
    """Campo de píxeles: celdas en grilla sobre Ink que se encienden de cian a magenta."""
    cv = new_canvas(PX_INK)
    d = ImageDraw.Draw(cv)
    cell, gap = 8, 2
    step = cell + gap
    # El puntero virtual se mueve suavemente dando vida al campo
    fx = focus_x + math.sin(t * 1.4) * 42
    fy = focus_y + math.cos(t * 1.1) * 26
    for gy in range(4, H - 4, step):
        cy = gy + cell * 0.5
        for gx in range(4, W - 4, step):
            cx = gx + cell * 0.5
            dist = math.hypot(cx - fx, cy - fy)
            # Onda reactiva desde el foco
            wave = max(0.0, 1.0 - dist / radius) ** 1.7
            pulse = 0.5 + 0.5 * math.sin(dist * 0.055 - t * 3.2)
            k = clamp01(wave * (0.72 + 0.28 * pulse) * boost)
            if k < 0.04:
                col = (11, 15, 42)
            else:
                # Degradado de cian -> violeta -> magenta según posición y onda
                mix_cm = clamp01((cx - fx + radius * 0.6) / (radius * 1.3))
                r = int(11 + k * (PX_CYAN[0] * (1 - mix_cm) + PX_MAGENTA[0] * mix_cm - 11) * 0.65)
                g = int(15 + k * (PX_CYAN[1] * (1 - mix_cm) + PX_MAGENTA[1] * mix_cm - 15) * 0.55)
                b = int(42 + k * (PX_CYAN[2] * (1 - mix_cm) + PX_MAGENTA[2] * mix_cm - 42) * 0.72)
                col = (min(255, r), min(255, g), min(255, b))
            d.rectangle([gx, gy, gx + cell - 1, gy + cell - 1], fill=(*col, 255))
    return cv


def draw_isotipo(cv, x0, y0, size=56, p_cyan=1.0, p_paper=1.0, p_mag=1.0):
    """Dibuja el isotipo de Pixeloide Studios ('Una P que es un play') con supersampling 2x
    convertido a grilla pixel art nítida."""
    if p_cyan <= 0 and p_paper <= 0 and p_mag <= 0:
        return
    S2 = size * 2
    im = Image.new("RGBA", (S2, S2), (0, 0, 0, 0))
    px = im.load()

    def in_poly(x, y, poly):
        inside = False
        n = len(poly)
        j = n - 1
        for i in range(n):
            xi, yi = poly[i]
            xj, yj = poly[j]
            if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi + 1e-9) + xi):
                inside = not inside
            j = i
        return inside

    # Coordenadas normalizadas (0..1) fieles a la P-Play del Manual de Marca (pág. 9)
    # 1. Triángulo Cian superior (apunta hacia arriba-derecha hacia el corte de la banda Paper)
    poly_cyan = [
        (0.08, 0.04),
        (0.58, 0.31),
        (0.32, 0.50),
        (0.08, 0.37),
    ]
    # 2. Banda Paper diagonal (forma la punta derecha del Play y baja al asta izquierda)
    poly_paper = [
        (0.61, 0.33),
        (0.88, 0.48),
        (0.08, 0.84),
        (0.08, 0.60),
    ]
    # 3. Triángulo Magenta inferior (cierra el asta vertical de la P por debajo)
    poly_mag = [
        (0.10, 0.85),
        (0.35, 0.68),
        (0.35, 0.98),
    ]

    for yy in range(S2):
        u_y = yy / S2
        for xx in range(S2):
            u_x = xx / S2
            # Triángulo Cian
            if p_cyan > 0:
                off_x = (1.0 - bezier_smooth(p_cyan)) * 0.25
                if in_poly(u_x + off_x, u_y + off_x * 0.5, poly_cyan):
                    # Sutil degradado cian -> azul petróleo en la unión inferior derecha
                    g_k = clamp01((u_x - 0.08) * 1.4 + (u_y - 0.1) * 1.1)
                    c = (
                        int(PX_CYAN[0] * (1 - 0.45 * g_k) + 14 * (0.45 * g_k)),
                        int(PX_CYAN[1] * (1 - 0.38 * g_k) + 110 * (0.38 * g_k)),
                        int(PX_CYAN[2] * (1 - 0.22 * g_k) + 165 * (0.22 * g_k)),
                        int(255 * min(1.0, p_cyan * 2)),
                    )
                    px[xx, yy] = c
            # Triángulo Magenta
            if p_mag > 0:
                off_y = (1.0 - bezier_smooth(p_mag)) * -0.22
                if in_poly(u_x, u_y + off_y, poly_mag):
                    # Sutil degradado violeta arriba -> magenta chispa abajo
                    g_k = clamp01((u_y - 0.68) / 0.28)
                    c = (
                        int(120 * (1 - g_k) + PX_MAGENTA[0] * g_k),
                        int(30 * (1 - g_k) + PX_MAGENTA[1] * g_k),
                        int(145 * (1 - g_k) + PX_MAGENTA[2] * g_k),
                        int(255 * min(1.0, p_mag * 2)),
                    )
                    px[xx, yy] = c
            # Banda Paper (encima)
            if p_paper > 0:
                off_p = (1.0 - bezier_smooth(p_paper)) * 0.3
                if in_poly(u_x + off_p, u_y - off_p * 0.55, poly_paper):
                    px[xx, yy] = (*PX_PAPER, int(255 * min(1.0, p_paper * 2)))

    # Reducimos a tamaño 1x con NEAREST para estética pixel art pura
    im_small = im.resize((size, size), Image.NEAREST)
    paste(cv, im_small, int(x0), int(y0))


def draw_pixeloide_lockup(cv, cx, cy, t, t0, scale="large"):
    """Dibuja el lockup oficial: Isotipo + PIXELOIDE (Paper) + STUDIOS (Cyan)."""
    dt = max(0.0, t - t0)
    p_c = prog(dt, 0.0, 0.38)
    p_p = prog(dt, 0.10, 0.48)
    p_m = prog(dt, 0.22, 0.58)
    p_txt1 = bezier_smooth(prog(dt, 0.28, 0.72))
    p_txt2 = bezier_smooth(prog(dt, 0.38, 0.82))

    if scale == "large":
        iso_sz = 64
        total_w = 222
        x_start = cx - total_w // 2
        y_iso = cy - iso_sz // 2
        draw_isotipo(cv, x_start, y_iso, size=iso_sz, p_cyan=p_c, p_paper=p_p, p_mag=p_m)
        tx = x_start + iso_sz + 14
        if p_txt1 > 0:
            dy1 = int((1.0 - p_txt1) * 10)
            draw_text(cv, "PIXELOIDE", tx, y_iso + 12 + dy1, "press", 16, PX_PAPER, outline=PX_INK,
                      alpha=p_txt1)
        if p_txt2 > 0:
            dy2 = int((1.0 - p_txt2) * 10)
            draw_text(cv, "STUDIOS", tx, y_iso + 34 + dy2, "press", 16, PX_CYAN, outline=PX_INK,
                      alpha=p_txt2)
    else:
        iso_sz = 26
        x_start = cx
        y_iso = cy
        draw_isotipo(cv, x_start, y_iso, size=iso_sz, p_cyan=1.0, p_paper=1.0, p_mag=1.0)
        tx = x_start + iso_sz + 6
        draw_text(cv, "PIXELOIDE", tx, y_iso + 3, "press", 8, PX_PAPER, outline=PX_INK)
        draw_text(cv, "STUDIOS", tx, y_iso + 14, "silk", 8, PX_CYAN, outline=None, shadow=False)


def px_card(cv, x, y, w, h, accent_cyan=False):
    """Tarjeta en color Surface (#0D1132) con línea divisoria de 1 px (Manual pág. 16)."""
    d = ImageDraw.Draw(cv)
    d.rectangle([x, y, x + w, y + h], fill=(*PX_SURFACE, 242), outline=(*PX_BORDER, 255))
    if accent_cyan:
        d.rectangle([x, y, x + 2, y + h], fill=(*PX_CYAN, 255))


def px_badge(cv, text, x, y, bg_col=PX_MAGENTA, fg_col=PX_PAPER):
    """Badge estilo Manual pág. 17 (fondo Magenta o borde fino en mono)."""
    tw, _ = text_size(text, "silk", 8)
    w = tw + 10
    d = ImageDraw.Draw(cv)
    d.rectangle([x, y, x + w, y + 12], fill=(*bg_col, 255))
    draw_text(cv, text, x + 5, y + 2, "silk", 8, fg_col, outline=None, shadow=False)
    return w


def px_tag(cv, text, x, y):
    """Tag técnico con borde fino en mono (Manual pág. 17)."""
    tw, _ = text_size(text, "silk", 8)
    w = tw + 10
    d = ImageDraw.Draw(cv)
    d.rectangle([x, y, x + w, y + 13], fill=(*PX_INK, 220), outline=(*PX_BORDER, 255))
    draw_text(cv, text, x + 5, y + 3, "silk", 8, PX_PAPER, outline=None, shadow=False)
    return w


# =========================================================================== escenas de cierre

def sc_pixeloide_logo(t, t0):
    """Escena 1 del cierre: Animación del logo de Pixeloide Studios («Jugamos en serio.»)."""
    dt = max(0.0, t - t0)
    # Foco del campo de píxeles sigue el ensamble del isotipo
    cv = pixel_field_bg(t, focus_x=240 + int(math.sin(dt * 1.8) * 60), focus_y=115, radius=190.0,
                        boost=min(1.2, 0.4 + dt * 0.4))
    d = ImageDraw.Draw(cv)

    # Eyebrow superior en mono cian (Manual pág. 15 y 20)
    p_eye = bezier_smooth(prog(dt, 0.35, 0.85))
    if p_eye > 0:
        draw_text(cv, "ESTUDIO CREATIVO-TECNOLÓGICO · MONTEVIDEO · SÃO PAULO", 240, 24, "silk", 8,
                  PX_CYAN, align="center", outline=None, shadow=False, alpha=p_eye)
        d.line([(64, 38), (416, 38)], fill=(*PX_BORDER, int(255 * p_eye)))

    # Lockup central: Isotipo + PIXELOIDE STUDIOS
    draw_pixeloide_lockup(cv, 240, 96, t, t0 + 0.18, scale="large")

    # Destello chispa en la punta del Play cuando termina de ensamblarse
    if 0.55 < dt < 1.35:
        sparkle(cv, 162, 96, t * 2, 4, PX_CYAN)
        sparkle(cv, 122, 122, t * 2 + 0.5, 3, PX_MAGENTA)

    # Lema «JUGAMOS EN SERIO.» con punto final en Magenta (Manual pág. 1, 3 y 14)
    p_tag1 = bezier_smooth(prog(dt, 0.95, 1.45))
    p_tag2 = bezier_smooth(prog(dt, 1.12, 1.62))
    if p_tag1 > 0:
        dy1 = int((1.0 - p_tag1) * 10)
        draw_text(cv, "JUGAMOS", 240, 152 + dy1, "press", 24, PX_PAPER, align="center", outline=PX_INK,
                  outline_w=2, alpha=p_tag1)
    if p_tag2 > 0:
        dy2 = int((1.0 - p_tag2) * 10)
        # "EN SERIO" en Cyan + "." en Magenta
        txt_es = "EN SERIO"
        tw_es, _ = text_size(txt_es, "press", 24)
        x_es = 240 - (tw_es + 20) // 2
        draw_text(cv, txt_es, x_es, 182 + dy2, "press", 24, PX_CYAN, align="left", outline=PX_INK,
                  outline_w=2, alpha=p_tag2)
        draw_text(cv, ".", x_es + tw_es + 2, 182 + dy2, "press", 24, PX_MAGENTA, align="left", outline=PX_INK,
                  outline_w=2, alpha=p_tag2)

    # Footer con dominio web y pill de marca
    p_foot = bezier_smooth(prog(dt, 1.45, 1.95))
    if p_foot > 0:
        d.line([(64, 224), (416, 224)], fill=(*PX_BORDER, int(255 * p_foot)))
        draw_text(cv, "PIXELOIDE.COM", 240, 236, "press", 8, PX_PAPER, align="center", alpha=p_foot)

    # Barrido inicial de página en cian (520 ms, Manual pág. 18)
    if dt < 0.52:
        wp = bezier_wipe(dt / 0.52)
        if wp < 0.5:
            x_bar = int(W * (wp * 2))
            d.rectangle([0, 0, x_bar, H], fill=(*PX_CYAN, 255))
        else:
            x_bar = int(W * ((wp - 0.5) * 2))
            d.rectangle([x_bar, 0, W, H], fill=(*PX_CYAN, 255))

    return vignette(cv, 0.25)


def sc_credits(t, t0, t_end):
    """Escena 2 del cierre: Créditos de Idea Original, Producción y Herramientas de IA."""
    dt = max(0.0, t - t0)
    cv = pixel_field_bg(t, focus_x=370, focus_y=80, radius=180.0, boost=0.85)
    d = ImageDraw.Draw(cv)

    # Barra superior con logo compacto y eyebrow numerado
    draw_pixeloide_lockup(cv, 18, 10, t, t0, scale="small")
    draw_text(cv, "01 — CRÉDITOS DE PRODUCCIÓN", 462, 16, "silk", 8, PX_CYAN, align="right",
              outline=None, shadow=False)
    d.line([(18, 40), (462, 40)], fill=(*PX_BORDER, 255))

    # Tarjetas principales: IDEA ORIGINAL y PRODUCCIÓN
    p_c1 = bezier_smooth(prog(dt, 0.15, 0.65))
    p_c2 = bezier_smooth(prog(dt, 0.28, 0.78))
    if p_c1 > 0:
        dy = int((1.0 - p_c1) * 12)
        px_card(cv, 18, 48 + dy, 216, 56, accent_cyan=True)
        draw_text(cv, "IDEA ORIGINAL", 30, 56 + dy, "silk", 8, PX_CYAN, outline=None, shadow=False, alpha=p_c1)
        draw_text(cv, "BRAIAN GRENO", 30, 72 + dy, "press", 16, PX_PAPER, outline=PX_INK, alpha=p_c1)
    if p_c2 > 0:
        dy = int((1.0 - p_c2) * 12)
        px_card(cv, 246, 48 + dy, 216, 56, accent_cyan=True)
        draw_text(cv, "PRODUCCIÓN Y DIRECCIÓN", 258, 56 + dy, "silk", 8, PX_CYAN, outline=None, shadow=False,
                  alpha=p_c2)
        draw_text(cv, "BRAIAN GRENO", 258, 72 + dy, "press", 16, PX_PAPER, outline=PX_INK, alpha=p_c2)

    # Panel de Herramientas de IA y Tecnología
    p_ai = bezier_smooth(prog(dt, 0.48, 1.0))
    if p_ai > 0:
        dy = int((1.0 - p_ai) * 14)
        y_box = 114 + dy
        px_card(cv, 18, y_box, 444, 114, accent_cyan=False)
        bw = px_badge(cv, "IA + CODE", 28, y_box + 8, bg_col=PX_MAGENTA, fg_col=PX_PAPER)
        draw_text(cv, "02 — HERRAMIENTAS DE IA Y TECNOLOGÍA", 28 + bw + 8, y_box + 10, "silk", 8, PX_CYAN,
                  outline=None, shadow=False)
        d.line([(28, y_box + 25), (452, y_box + 25)], fill=(*PX_BORDER, 255))

        tools_grid = [
            ("CLAUDE & GEMINI", "DIRECCIÓN TÉCNICA · CÓDIGO Y ANIMACIÓN"),
            ("ELEVENLABS", "LOCUCIÓN NEURONAL · CARLOS AGUILAR"),
            ("OPENAI WHISPER", "ALINEACIÓN FONÉTICA Y SUBTÍTULOS"),
            (CREDITO_IMAGENES, "ARTE PIXEL BASE · FONDOS Y RETRATOS"),
            ("PYTHON · PIL · NUMPY", "MOTOR PIXEL ART 16-BIT Y CHIPTUNE"),
            ("FFMPEG", "MASTERIZACIÓN 1080P · AUDIO -14 LUFS"),
        ]
        for idx, (t_name, t_role) in enumerate(tools_grid):
            p_item = bezier_smooth(prog(dt, 0.60 + idx * 0.08, 1.05 + idx * 0.08))
            if p_item <= 0:
                continue
            col_i = idx % 2
            row_i = idx // 2
            tx = 28 + col_i * 216
            ty = y_box + 32 + row_i * 26
            d.rectangle([tx, ty + 2, tx + 3, ty + 18], fill=(*(PX_CYAN if col_i == 0 else PX_MAGENTA), 255))
            draw_text(cv, t_name, tx + 8, ty + 1, "press", 8, PX_PAPER, outline=PX_INK, alpha=p_item)
            draw_text(cv, t_role, tx + 8, ty + 12, "silk", 8, PX_MUTED, outline=None, shadow=False, alpha=p_item)

    # Pie de marca
    p_ft = bezier_smooth(prog(dt, 1.1, 1.6))
    if p_ft > 0:
        draw_text(cv, "PIXELOIDE STUDIOS · JUGAMOS EN SERIO. · PIXELOIDE.COM · 2026", 240, 244, "silk", 8,
                  PX_CYAN, align="center", outline=None, shadow=False, alpha=p_ft)

    # Barrido corto en cian al pasar del logo a los créditos
    if dt < 0.36:
        wp = bezier_wipe(dt / 0.36)
        x_bar = int(W * wp)
        d.rectangle([x_bar, 0, min(W, x_bar + 48), H], fill=(*PX_CYAN, 220))

    return vignette(cv, 0.25)


T_LOGO = TL.e(TL.order[-1]) + 2.8
T_CRED = T_LOGO + 3.8


def scenes():
    return [
        (T_LOGO, lambda t: sc_pixeloide_logo(t, T_LOGO), None),
        (T_CRED, lambda t: sc_credits(t, T_CRED, TL.total), None),
    ]


def music(A):
    # Jingle de marca de Pixeloide Studios (acorde Cmaj9 brillante + pulso electrónico)
    t0 = T_LOGO + 0.18
    A.kick(A.music, t0, 0.42)
    A.sting(t0, [60, 67, 71, 74, 79, 84], vol=0.055, step=0.08, hold=1.8)
    for m in (48, 55, 60, 64, 71):
        A.note(A.music, t0 + 0.2, A.midi_hz(m), 3.4, duty=0.25, vol=0.024, a=0.1, s=0.75, r=0.8, vib=0.15)
    A.note(A.music, t0, A.midi_hz(36), 3.5, "tri", vol=0.22, a=0.02, s=0.85, r=0.8)

    # Música suave y moderna durante la placa de créditos
    tc = T_CRED
    A.kick(A.music, tc, 0.35)
    prog_chords = [("F", "maj7"), ("G", "add9"), ("A", "min7"), ("C", "maj7")]
    dur_c = (TL.total - tc - 0.6) / len(prog_chords)
    for idx, (root, kind) in enumerate(prog_chords):
        ct = tc + idx * dur_c
        notes = A.chord_notes(root, kind, octave=4)
        A.note(A.music, ct, A.midi_hz(notes[0] - 12), dur_c, "tri", vol=0.18, a=0.03, s=0.8, r=0.3)
        for j, m in enumerate(notes):
            A.note(A.music, ct + j * 0.12, A.midi_hz(m), dur_c * 0.85, duty=0.25, vol=0.025, a=0.04, s=0.6, r=0.4)


def sfx(A):
    # Barrido cian inicial + ensamble de las 3 piezas del isotipo (Cian, Paper, Magenta)
    A.whoosh(T_LOGO, 0.42, 0.055)
    A.pop_sfx(T_LOGO + 0.18, 620, 0.05)
    A.pop_sfx(T_LOGO + 0.28, 780, 0.05)
    A.pop_sfx(T_LOGO + 0.40, 960, 0.055)
    A.coin(T_LOGO + 0.62, 0.05)
    # «JUGAMOS EN SERIO.»
    A.pop_sfx(T_LOGO + 1.15, 520, 0.045)
    A.pop_sfx(T_LOGO + 1.32, 680, 0.05)
    # Transición a créditos y aparición de tarjetas
    A.whoosh(T_CRED, 0.35, 0.05)
    A.pop_sfx(T_CRED + 0.20, 540, 0.045)
    A.pop_sfx(T_CRED + 0.34, 640, 0.045)
    for k in range(6):
        A.blip(T_CRED + 0.62 + k * 0.08, 880 + k * 110, 0.035, 0.028)

