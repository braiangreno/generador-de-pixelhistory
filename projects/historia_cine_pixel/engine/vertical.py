"""Motor de redibujado nativo 9:16 (270x480 -> 1080x1920) a pantalla completa.

En lugar de recortar el video 16:9 (480x270) dentro de un recuadro cuadrado,
intercepta las llamadas de dibujo de cada escena y las redibuja nativamente sobre
un lienzo vertical 270x480 a pantalla completa:
  - Fondo pixel-art extendido a pantalla completa 270x480 (cielo/techo arriba,
    vista completa en el centro y piso/suelo abajo hasta y=480).
  - Encabezados superiores redibujados en x=8..262 con ajuste de línea automático
    para que ningún texto se corte jamás.
  - Paneles centrales, retratos y diagramas reubicados en la zona media (y=82..352)
    centrados en x=135 (y apilados verticalmente cuando en 16:9 estaban lado a lado).
  - Personajes redibujados en el piso vertical (feet=452, x=34..236) con proporción
    pixel-art 1:1 sin recortes en los bordes.
"""
import math
import numpy as np
from PIL import Image, ImageDraw
from functools import lru_cache

import core
import common
import outro
from i18n import tr

VW, VH = 270, 480
OUT_VW, OUT_VH = 1080, 1920


def wrap_text_px(text, fname, size, max_w):
    """Divide `text` en líneas que no superen `max_w` píxeles en la fuente dada."""
    text = (text or "").strip()
    if not text:
        return [""]
    w, _ = core.text_size(text, fname, size)
    if w <= max_w:
        return [text]
    words = text.split()
    if len(words) <= 1:
        return [text]
    lines = []
    cur = words[0]
    for word in words[1:]:
        cand = cur + " " + word
        cw, _ = core.text_size(cand, fname, size)
        if cw <= max_w:
            cur = cand
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


@lru_cache(maxsize=64)
def build_vertical_bg(bg_name):
    """Convierte un fondo 480x270 en un escenario vertical 270x480 a pantalla completa."""
    src = core.load_rgba(f"assets/bg/{bg_name}.png")
    out = Image.new("RGBA", (VW, VH), (12, 12, 22, 255))

    # 1. Vista principal completa (x=0..480 -> 310x254 centrado en 270px, colocado en y=88..342)
    vista_w, vista_h = 310, 254
    vista_full = src.resize((vista_w, vista_h), Image.NEAREST)
    x_off = (vista_w - VW) // 2
    vista = vista_full.crop((x_off, 0, x_off + VW, vista_h))
    out.paste(vista, (0, 88))

    # 2. Extensión superior de cielo/techo (y=0..96) con transición dithered
    top_strip = vista.crop((0, 0, VW, 42)).resize((VW, 96), Image.NEAREST)
    top_arr = np.array(top_strip).astype(np.float32)
    for y in range(96):
        k = 0.72 + 0.28 * (y / 95.0)
        top_arr[y, :, :3] = np.clip(top_arr[y, :, :3] * k, 0, 255)
    out.paste(Image.fromarray(top_arr.astype(np.uint8), "RGBA"), (0, 0))

    # Dither blend en la unión superior (y=84..96)
    out_arr = np.array(out)
    vista_arr = np.array(vista)
    th = core.bayer_tile(VW, 16)
    for dy in range(12):
        y = 84 + dy
        if 0 <= y - 88 < vista_h:
            mask = th[dy] < (dy / 12.0)
            out_arr[y, mask] = vista_arr[y - 88, mask]

    # 3. Extensión inferior de piso/suelo (y=334..480) donde pisan los personajes
    bot_strip = vista.crop((0, vista_h - 48, VW, vista_h)).resize((VW, 148), Image.NEAREST)
    bot_arr = np.array(bot_strip).astype(np.float32)
    for y in range(148):
        k = 1.0 - 0.18 * (y / 147.0)
        bot_arr[y, :, :3] = np.clip(bot_arr[y, :, :3] * k, 0, 255)
        # Sutiles líneas horizontales de textura de piso pixel-art cada 18px
        if y in (28, 52, 80, 114):
            bot_arr[y, :, :3] = np.clip(bot_arr[y, :, :3] * 0.88, 0, 255)
    bot_img = np. clip(bot_arr, 0, 255).astype(np.uint8)
    for dy in range(148):
        y = 332 + dy
        if y >= VH:
            break
        if dy < 10 and (y - 88) < vista_h:
            mask = th[dy] < (dy / 10.0)
            out_arr[y, mask] = bot_img[dy, mask]
        else:
            out_arr[y] = bot_img[dy]

    return Image.fromarray(out_arr, "RGBA")


def build_vertical_vgradient(top, bottom, bands=12):
    a = np.zeros((VH, VW, 4), dtype=np.uint8)
    for y in range(VH):
        k = int(y / VH * bands) / bands
        a[y, :, :3] = [int(t + (b - t) * k) for t, b in zip(top, bottom)]
    a[..., 3] = 255
    return Image.fromarray(a, "RGBA")


class VerticalContext:
    """Contexto que captura las primitivas de una escena durante fn(t) para redibujarlas en 270x480."""

    def __init__(self, t):
        self.t = t
        self.bg_calls = []          # [("bg", name), ("vgrad", (top, bot, bands)), ("solid", color)]
        self.grades = []            # [(mul, add, sat, k)]
        self.particles = []         # [("sand_wind", ...), ("snow", ...), ("stars", ...), ("conf", ...), ("rain", ...)]
        self.spotlights = []        # [(cx, top, bottom, w_top, w_bot, color, strength)]
        self.shake_offset = (0, 0)
        self.vignette_strength = 0.0
        self.chapter_card = None    # dict si la escena es una placa de capítulo
        self.header_windows = []    # ventanas de encabezado superior (y <= 28, w >= 200)
        self.header_texts = []      # textos de encabezado superior (y <= 46)
        self.bigyears = []          # [(text, cx, y, t, t0, size, ramp)]
        self.mid_windows = []       # ventanas en la zona media/inferior
        self.chars = []             # [("char"|"sil"|"robot", ...)]
        self.bubbles = []           # [(text, x, y, size, fname, tail, reveal, color, fill, tail_x)]
        self.emotes = []            # [(text, x, y, fname, size, color, alpha)]
        self.mid_canvas = Image.new("RGBA", (core.W, core.H), (0, 0, 0, 0))
        self.active_x_shift = None  # mapeo x activo cuando una ventana ancha (w>254) se compacta

    def _in_header_zone(self, y):
        if self.header_windows:
            for hw in self.header_windows:
                if hw["y"] - 4 <= y <= hw["y"] + hw["h"] + 6:
                    return True
            return False
        return y <= 24 and not self.mid_windows


def render_chapter_card_vertical(cv, cc):
    """Redibuja una placa de capítulo a pantalla completa en 270x480."""
    t, t0, num, lines, years, ramp_title = (
        cc["t"], cc["t0"], cc["num"], cc["lines"], cc["years"], cc["ramp_title"]
    )
    open_p = core.ease_out(core.prog(t, t0, t0 + 0.35))
    if open_p <= 0:
        return
    card_w = 248
    w = int(card_w * open_p)
    h = 176
    wx = (VW - max(8, w)) // 2
    wy = (VH - h) // 2 - 10
    core._orig_window(cv, wx, wy, max(8, w), h)
    if open_p < 1:
        return
    tt = t - t0 - 0.35
    d = ImageDraw.Draw(cv)
    lab = tr(f"CAPÍTULO {num}", "press")
    lw, _ = core.text_size(lab, "press", 8)
    core._orig_draw_text(cv, f"CAPÍTULO {num}", VW // 2, wy + 20, "press", 8, core.GOLD,
                         align="center", reveal=tt * 30)
    ln = int(min(1, tt * 2) * 32)
    d.line([(VW // 2 - lw // 2 - 6 - ln, wy + 23), (VW // 2 - lw // 2 - 6, wy + 23)], fill=(*core.GOLD, 255))
    d.line([(VW // 2 + lw // 2 + 6, wy + 23), (VW // 2 + lw // 2 + 6 + ln, wy + 23)], fill=(*core.GOLD, 255))

    # Envolver líneas del título del capítulo para que entren en 228px
    wrapped = []
    for line in lines:
        tr_line = tr(line, "press")
        w16, _ = core.text_size(tr_line, "press", 16)
        if w16 <= 228:
            wrapped.append((line, 16))
        else:
            sub_lines = wrap_text_px(tr_line, "press", 16, 228)
            if all(core.text_size(s, "press", 16)[0] <= 228 for s in sub_lines) and len(sub_lines) <= 3:
                for s in sub_lines:
                    wrapped.append((s, 16))
            else:
                for s in wrap_text_px(tr_line, "press", 8, 228):
                    wrapped.append((s, 8))

    total_h = sum(22 if sz == 16 else 14 for _, sz in wrapped)
    cur_y = wy + 46 + max(0, (82 - total_h) // 2)
    for i, (line_txt, sz) in enumerate(wrapped):
        core._orig_draw_text(cv, line_txt, VW // 2, cur_y, "press", sz, align="center",
                             gradient=ramp_title, reveal=(tt - 0.25 - i * 0.35) * 26)
        cur_y += 22 if sz == 16 else 14

    # Años / subtítulo inferior envuelto a 228px
    yr_lines = wrap_text_px(tr(years, "press"), "press", 8, 228)
    for j, yl in enumerate(yr_lines[:2]):
        core._orig_draw_text(cv, yl, VW // 2, wy + h - 34 + j * 13, "press", 8, core.CYAN,
                             align="center", reveal=(tt - 0.45) * 45)


def _split_1d_runs(has_px, min_gap=3, min_chunk=24):
    """Divide un array booleano 1D en tramos ocupados separados por al menos `min_gap` ceros."""
    idx = np.where(has_px)[0]
    if len(idx) == 0:
        return []
    s0, s1 = int(idx[0]), int(idx[-1]) + 1
    segments = []
    cur_start = s0
    gap_start = None
    for i in range(s0, s1):
        if not has_px[i]:
            if gap_start is None:
                gap_start = i
        else:
            if gap_start is not None:
                gap_len = i - gap_start
                if gap_len >= min_gap and (gap_start - cur_start) >= min_chunk:
                    segments.append((cur_start, gap_start))
                    cur_start = i
                gap_start = None
    if (s1 - cur_start) >= min_chunk or not segments:
        segments.append((cur_start, s1))
    else:
        prev_s, _ = segments[-1]
        segments[-1] = (prev_s, s1)
    return segments


def _find_mid_rows(rgba_img, y_min=38, y_max=core.H):
    """Detecta filas visuales de paneles/objetos en `mid_canvas` (dividiendo por filas vacías y columnas vacías)."""
    arr = np.array(rgba_img)
    alpha = arr[y_min:y_max, :, 3] > 12
    if not alpha.any():
        return []

    # Ignorar líneas conectoras verticales muy finas (<= 3px) al separar bandas horizontales
    row_has_px = alpha.sum(axis=1) > 3
    if not row_has_px.any():
        row_has_px = alpha.any(axis=1)
    y_bands = _split_1d_runs(row_has_px, min_gap=2, min_chunk=12)
    visual_rows = []

    for by0_rel, by1_rel in y_bands:
        by0 = y_min + by0_rel
        by1 = y_min + by1_rel
        band_a = arr[by0:by1, :, 3] > 12
        if not band_a.any():
            continue
        ys, xs = np.where(band_a)
        x0, x1 = int(xs.min()), int(xs.max()) + 1
        y0, y1 = by0 + int(ys.min()), by0 + int(ys.max()) + 1
        w_span = x1 - x0
        if w_span <= 258:
            visual_rows.append([(x0, y0, x1, y1)])
            continue

        # Si el bloque supera 258px de ancho, dividir por columnas vacías o flechas conectoras finas (<= 4px)
        band_h = max(1, y1 - y0)
        col_has_px = band_a.sum(axis=0) > max(3, min(8, int(band_h * 0.07)))
        if not col_has_px.any():
            col_has_px = band_a.any(axis=0)
        x_segs = _split_1d_runs(col_has_px, min_gap=3, min_chunk=40)
        if len(x_segs) <= 1:
            visual_rows.append([(x0, y0, x1, y1)])
        else:
            row_items = []
            for cx0, cx1 in x_segs:
                sub_a = arr[by0:by1, cx0:cx1, 3] > 12
                if not sub_a.any():
                    continue
                sys_i, sxs_i = np.where(sub_a)
                rx0, rx1 = cx0 + int(sxs_i.min()), cx0 + int(sxs_i.max()) + 1
                ry0, ry1 = by0 + int(sys_i.min()), by0 + int(sys_i.max()) + 1
                row_items.append((rx0, ry0, rx1, ry1))
            # Empaquetar los items del tramo horizontal en filas de hasta 256px de ancho
            cur_row = []
            cur_w = 0
            for item in row_items:
                iw = item[2] - item[0]
                if not cur_row:
                    cur_row.append(item)
                    cur_w = iw
                elif cur_w + 6 + iw <= 256:
                    cur_row.append(item)
                    cur_w += 6 + iw
                else:
                    visual_rows.append(cur_row)
                    cur_row = [item]
                    cur_w = iw
            if cur_row:
                visual_rows.append(cur_row)

    return visual_rows


def _pixel_field_vertical(t, focus_x=135, focus_y=210, radius=195.0, boost=1.0):
    cv = Image.new("RGBA", (VW, VH), (*outro.PX_INK, 255))
    d = ImageDraw.Draw(cv)
    cell, gap = 8, 2
    step = cell + gap
    fx = focus_x + math.sin(t * 1.4) * 32
    fy = focus_y + math.cos(t * 1.1) * 38
    for gy in range(4, VH - 4, step):
        cy = gy + cell * 0.5
        for gx in range(4, VW - 4, step):
            cx = gx + cell * 0.5
            dist = math.hypot(cx - fx, cy - fy)
            wave = max(0.0, 1.0 - dist / radius) ** 1.7
            pulse = 0.5 + 0.5 * math.sin(dist * 0.055 - t * 3.2)
            k = core.clamp01(wave * (0.72 + 0.28 * pulse) * boost)
            if k < 0.04:
                col = (11, 15, 42)
            else:
                mix_cm = core.clamp01((cx - fx + radius * 0.6) / (radius * 1.3))
                r = int(11 + k * (outro.PX_CYAN[0] * (1 - mix_cm) + outro.PX_MAGENTA[0] * mix_cm - 11) * 0.65)
                g = int(15 + k * (outro.PX_CYAN[1] * (1 - mix_cm) + outro.PX_MAGENTA[1] * mix_cm - 15) * 0.55)
                b = int(42 + k * (outro.PX_CYAN[2] * (1 - mix_cm) + outro.PX_MAGENTA[2] * mix_cm - 42) * 0.72)
                col = (min(255, r), min(255, g), min(255, b))
            d.rectangle([gx, gy, gx + cell - 1, gy + cell - 1], fill=(*col, 255))
    return cv


def render_pixeloide_logo_vertical(t, t0):
    """Cierre oficial de Pixeloide Studios redibujado a pantalla completa 270x480."""
    dt = max(0.0, t - t0)
    cv = _pixel_field_vertical(t, focus_x=135 + int(math.sin(dt * 1.8) * 36), focus_y=195,
                               radius=210.0, boost=min(1.2, 0.4 + dt * 0.4))
    d = ImageDraw.Draw(cv)

    p_eye = outro.bezier_smooth(core.prog(dt, 0.35, 0.85))
    if p_eye > 0:
        core._orig_draw_text(cv, "ESTUDIO CREATIVO-TECNOLÓGICO", VW // 2, 34, "silk", 8,
                             outro.PX_CYAN, align="center", outline=None, shadow=False, alpha=p_eye)
        core._orig_draw_text(cv, "MONTEVIDEO · SÃO PAULO", VW // 2, 48, "silk", 8,
                             outro.PX_CYAN, align="center", outline=None, shadow=False, alpha=p_eye)
        d.line([(20, 66), (VW - 20, 66)], fill=(*outro.PX_BORDER, int(255 * p_eye)))

    # Isotipo + PIXELOIDE STUDIOS
    p_c = core.prog(dt, 0.18, 0.56)
    p_p = core.prog(dt, 0.28, 0.66)
    p_m = core.prog(dt, 0.40, 0.76)
    p_txt1 = outro.bezier_smooth(core.prog(dt, 0.46, 0.90))
    p_txt2 = outro.bezier_smooth(core.prog(dt, 0.56, 1.00))
    iso_sz = 64
    total_w = 222
    x_start = VW // 2 - total_w // 2
    y_iso = 140
    outro.draw_isotipo(cv, x_start, y_iso, size=iso_sz, p_cyan=p_c, p_paper=p_p, p_mag=p_m)
    tx = x_start + iso_sz + 14
    if p_txt1 > 0:
        dy1 = int((1.0 - p_txt1) * 10)
        core._orig_draw_text(cv, "PIXELOIDE", tx, y_iso + 12 + dy1, "press", 16,
                             outro.PX_PAPER, outline=outro.PX_INK, alpha=p_txt1)
    if p_txt2 > 0:
        dy2 = int((1.0 - p_txt2) * 10)
        core._orig_draw_text(cv, "STUDIOS", tx, y_iso + 34 + dy2, "press", 16,
                             outro.PX_CYAN, outline=outro.PX_INK, alpha=p_txt2)

    if 0.55 < dt < 1.35:
        common.sparkle(cv, x_start + 54, y_iso + 32, t * 2, 4, outro.PX_CYAN)
        common.sparkle(cv, x_start + 18, y_iso + 56, t * 2 + 0.5, 3, outro.PX_MAGENTA)

    # Lema «JUGAMOS EN SERIO.»
    p_tag1 = outro.bezier_smooth(core.prog(dt, 0.95, 1.45))
    p_tag2 = outro.bezier_smooth(core.prog(dt, 1.12, 1.62))
    if p_tag1 > 0:
        dy1 = int((1.0 - p_tag1) * 10)
        core._orig_draw_text(cv, "JUGAMOS", VW // 2, 248 + dy1, "press", 24,
                             outro.PX_PAPER, align="center", outline=outro.PX_INK, outline_w=2, alpha=p_tag1)
    if p_tag2 > 0:
        dy2 = int((1.0 - p_tag2) * 10)
        txt_es = tr("EN SERIO", "press")
        tw_es, _ = core.text_size(txt_es, "press", 24)
        x_es = VW // 2 - (tw_es + 20) // 2
        core._orig_draw_text(cv, "EN SERIO", x_es, 286 + dy2, "press", 24,
                             outro.PX_CYAN, align="left", outline=outro.PX_INK, outline_w=2, alpha=p_tag2)
        core._orig_draw_text(cv, ".", x_es + tw_es + 2, 286 + dy2, "press", 24,
                             outro.PX_MAGENTA, align="left", outline=outro.PX_INK, outline_w=2, alpha=p_tag2)

    p_foot = outro.bezier_smooth(core.prog(dt, 1.45, 1.95))
    if p_foot > 0:
        d.line([(20, 412), (VW - 20, 412)], fill=(*outro.PX_BORDER, int(255 * p_foot)))
        core._orig_draw_text(cv, "PIXELOIDE.COM", VW // 2, 428, "press", 8,
                             outro.PX_PAPER, align="center", alpha=p_foot)

    if dt < 0.52:
        wp = outro.bezier_wipe(dt / 0.52)
        if wp < 0.5:
            x_bar = int(VW * (wp * 2))
            d.rectangle([0, 0, x_bar, VH], fill=(*outro.PX_CYAN, 255))
        else:
            x_bar = int(VW * ((wp - 0.5) * 2))
            d.rectangle([x_bar, 0, VW, VH], fill=(*outro.PX_CYAN, 255))

    return cv


def render_credits_vertical(t, t0):
    """Pantalla de créditos redibujada en formato vertical 270x480 a pantalla completa."""
    dt = max(0.0, t - t0)
    cv = _pixel_field_vertical(t, focus_x=185, focus_y=150, radius=210.0, boost=0.85)
    d = ImageDraw.Draw(cv)

    outro.draw_isotipo(cv, 12, 14, size=24, p_cyan=1.0, p_paper=1.0, p_mag=1.0)
    core._orig_draw_text(cv, "PIXELOIDE STUDIOS", 42, 16, "press", 8, outro.PX_PAPER, outline=outro.PX_INK)
    core._orig_draw_text(cv, "01 — CRÉDITOS DE PRODUCCIÓN", 42, 28, "silk", 8,
                         outro.PX_CYAN, outline=None, shadow=False)
    d.line([(12, 44), (VW - 12, 44)], fill=(*outro.PX_BORDER, 255))

    p_c1 = outro.bezier_smooth(core.prog(dt, 0.15, 0.65))
    p_c2 = outro.bezier_smooth(core.prog(dt, 0.28, 0.78))
    if p_c1 > 0:
        dy = int((1.0 - p_c1) * 10)
        d.rectangle([12, 54 + dy, VW - 12, 102 + dy], fill=(*outro.PX_SURFACE, 242), outline=(*outro.PX_BORDER, 255))
        d.rectangle([12, 54 + dy, 14, 102 + dy], fill=(*outro.PX_CYAN, 255))
        core._orig_draw_text(cv, "IDEA ORIGINAL", 22, 60 + dy, "silk", 8,
                             outro.PX_CYAN, outline=None, shadow=False, alpha=p_c1)
        core._orig_draw_text(cv, "BRAIAN GRENO", 22, 74 + dy, "press", 16,
                             outro.PX_PAPER, outline=outro.PX_INK, alpha=p_c1)
    if p_c2 > 0:
        dy = int((1.0 - p_c2) * 10)
        d.rectangle([12, 110 + dy, VW - 12, 158 + dy], fill=(*outro.PX_SURFACE, 242), outline=(*outro.PX_BORDER, 255))
        d.rectangle([12, 110 + dy, 14, 158 + dy], fill=(*outro.PX_CYAN, 255))
        core._orig_draw_text(cv, "PRODUCCIÓN Y DIRECCIÓN", 22, 116 + dy, "silk", 8,
                             outro.PX_CYAN, outline=None, shadow=False, alpha=p_c2)
        core._orig_draw_text(cv, "BRAIAN GRENO", 22, 130 + dy, "press", 16,
                             outro.PX_PAPER, outline=outro.PX_INK, alpha=p_c2)

    p_ai = outro.bezier_smooth(core.prog(dt, 0.48, 1.0))
    if p_ai > 0:
        dy = int((1.0 - p_ai) * 12)
        y_box = 168 + dy
        d.rectangle([12, y_box, VW - 12, y_box + 264], fill=(*outro.PX_SURFACE, 242), outline=(*outro.PX_BORDER, 255))
        d.rectangle([20, y_box + 8, 78, y_box + 20], fill=(*outro.PX_MAGENTA, 255))
        core._orig_draw_text(cv, "IA + CODE", 25, y_box + 10, "silk", 8,
                             outro.PX_PAPER, outline=None, shadow=False)
        core._orig_draw_text(cv, "02 — HERRAMIENTAS IA", 84, y_box + 10, "silk", 8,
                             outro.PX_CYAN, outline=None, shadow=False)
        d.line([(20, y_box + 25), (VW - 20, y_box + 25)], fill=(*outro.PX_BORDER, 255))

        tools_grid = [
            ("CLAUDE & GEMINI", "DIRECCIÓN TÉCNICA · CÓDIGO Y ANIMACIÓN"),
            ("ELEVENLABS", "LOCUCIÓN NEURONAL · CARLOS AGUILAR"),
            ("OPENAI WHISPER", "ALINEACIÓN FONÉTICA Y SUBTÍTULOS"),
            ("IMAGEN / NANOBANANA", "ARTE PIXEL BASE · FONDOS Y RETRATOS"),
            ("PYTHON · PIL · NUMPY", "MOTOR PIXEL ART 16-BIT Y CHIPTUNE"),
            ("FFMPEG", "MASTERIZACIÓN 1080P · AUDIO -14 LUFS"),
        ]
        for idx, (t_name, t_role) in enumerate(tools_grid):
            p_item = outro.bezier_smooth(core.prog(dt, 0.60 + idx * 0.08, 1.05 + idx * 0.08))
            if p_item <= 0:
                continue
            ty = y_box + 32 + idx * 37
            d.rectangle([20, ty + 2, 23, ty + 22],
                        fill=(*(outro.PX_CYAN if idx % 2 == 0 else outro.PX_MAGENTA), 255))
            core._orig_draw_text(cv, t_name, 28, ty + 2, "press", 8,
                                 outro.PX_PAPER, outline=outro.PX_INK, alpha=p_item)
            core._orig_draw_text(cv, t_role, 28, ty + 14, "silk", 8,
                                 outro.PX_MUTED, outline=None, shadow=False, alpha=p_item)

    p_ft = outro.bezier_smooth(core.prog(dt, 1.1, 1.6))
    if p_ft > 0:
        core._orig_draw_text(cv, "PIXELOIDE STUDIOS · PIXELOIDE.COM · 2026", VW // 2, 448, "silk", 8,
                             outro.PX_CYAN, align="center", outline=None, shadow=False, alpha=p_ft)

    return cv


def draw_bubble_vertical(canvas, text, x, y, size=8, fname="press", tail="down", reveal=None,
                         color=core.INK, fill=(250, 248, 240)):
    """Dibuja un globo de diálogo pixel-art dentro de los límites de 270x480 sin cortarse en los bordes."""
    if reveal is not None and int(reveal) <= 0:
        return
    tr_t = tr(text, fname)
    lines = wrap_text_px(tr_t, fname, size, 232)
    line_sizes = [core.text_size(l, fname, size) for l in lines[:2]]
    tw = max((s[0] for s in line_sizes), default=16)
    lh = max((s[1] for s in line_sizes), default=8)
    bw = min(VW - 8, tw + 12)
    bh = len(lines[:2]) * (lh + 2) + 8
    bx = max(4, min(VW - bw - 4, int(x - bw // 2)))
    by = int(y - bh - 6) if tail == "down" else int(y + 6)
    by = max(4, min(VH - bh - 8, by))
    a = np.zeros((bh, bw, 4), dtype=np.uint8)
    a[..., :3] = fill
    a[..., 3] = 255
    a[0, :, :3] = core.INK
    a[-1, :, :3] = core.INK
    a[:, 0, :3] = core.INK
    a[:, -1, :3] = core.INK
    for (cy, cx) in ((0, 0), (0, bw - 1), (bh - 1, 0), (bh - 1, bw - 1)):
        a[cy, cx, 3] = 0
    a[-2, 1:-1, :3] = core.shade(fill, 0.85)
    core.paste(canvas, Image.fromarray(a, "RGBA"), bx, by)
    d = ImageDraw.Draw(canvas)
    tx = max(bx + 8, min(bx + bw - 8, int(x)))
    if tail == "down":
        for i in range(5):
            d.line([(tx - 2 + i // 2, by + bh - 1 + i), (tx + 2 - i, by + bh - 1 + i)], fill=(*fill, 255))
            d.point((tx - 3 + i // 2, by + bh - 1 + i), fill=(*core.INK, 255))
            d.point((tx + 3 - i, by + bh - 1 + i), fill=(*core.INK, 255))
    for li, lstr in enumerate(lines[:2]):
        core._orig_draw_text(
            canvas, lstr, bx + bw // 2, by + 5 + li * (lh + 2), fname, size, color,
            align="center", outline=None, shadow=False, reveal=reveal,
        )


def compose_vertical_scene(vctx):
    """Construye el fotograma 270x480 a pantalla completa a partir del VerticalContext capturado."""
    t = vctx.t
    cv = Image.new("RGBA", (VW, VH), (*core.INK, 255))
    d = ImageDraw.Draw(cv)

    # 1. FONDO A PANTALLA COMPLETA 270x480
    bg_calls = vctx.bg_calls
    if len(bg_calls) >= 2 and bg_calls[0][0] == "bg" and bg_calls[1][0] == "bg":
        # Pantalla dividida (ej. s06 Oregón 1957 / IMAX 2026)
        b_left = build_vertical_bg(bg_calls[0][1])
        b_right = build_vertical_bg(bg_calls[1][1])
        cv.paste(b_left.crop((0, 0, VW // 2, VH)), (0, 0))
        cv.paste(b_right.crop((VW // 2, 0, VW, VH)), (VW // 2, 0))
        d = ImageDraw.Draw(cv)
        d.line([(VW // 2, 0), (VW // 2, VH)], fill=(*core.GOLD, 255), width=2)
        mc_arr = np.array(vctx.mid_canvas)
        mc_arr[:, 238:243, 3] = 0
        vctx.mid_canvas = Image.fromarray(mc_arr, "RGBA")
    elif bg_calls:
        kind, val = bg_calls[-1]
        if kind == "bg":
            cv = build_vertical_bg(val).copy()
        elif kind == "vgrad":
            cv = build_vertical_vgradient(*val)
        elif kind == "solid":
            cv = Image.new("RGBA", (VW, VH), (*val, 255))
    else:
        cv = build_vertical_vgradient((12, 14, 28), (28, 34, 62), 12)

    for mul, add, sat, k in vctx.grades:
        cv = core._orig_grade(cv, mul=mul, add=add, sat=sat, k=k)

    # Partículas a pantalla completa 270x480
    d = ImageDraw.Draw(cv)
    for p_item in vctx.particles:
        pk = p_item[0]
        if pk == "sand_wind":
            _, pt, density, color = p_item
            for i in range(int(density * 1.2)):
                speed = 42 + (i % 5) * 14
                px = int((i * 37 + pt * speed) % VW)
                py = 16 + int((i * 41 + math.sin(pt * 2.5 + i) * 6) % (VH - 32))
                pa = 110 + (i % 4) * 30
                d.rectangle([px, py, px + (1 if i % 3 else 2), py], fill=(*color, pa))
        elif pk == "snow":
            _, pt, density = p_item
            for i in range(int(120 * density)):
                py = int((i * 19 + pt * (22 + (i % 4) * 6)) % VH)
                px = int((i * 31 + math.sin(pt * 1.4 + i) * 7 + pt * 5) % VW)
                d.rectangle([px, py, px + 1, py + 1], fill=(235, 245, 255, 230))
        elif pk == "stars":
            _, pt, alpha = p_item
            for i in range(95):
                px = (i * 53 + 17) % VW
                py = (i * 71 + 11) % (VH - 120)
                k_s = 0.5 + 0.5 * math.sin(pt * 2.1 + i)
                v_s = int((95 + 155 * k_s) * alpha)
                d.point((px, py), fill=(v_s, v_s, min(255, v_s + 25), 255))
        elif pk == "conf":
            _, pt = p_item
            cols = core.Confetti.COLORS
            for i in range(75):
                py = int((i * 23 + pt * (38 + (i % 5) * 9)) % VH)
                px = int((i * 43 + math.sin(pt * 3 + i) * 8) % VW)
                ccol = cols[i % len(cols)]
                d.rectangle([px, py, px + 1, py + 1], fill=(*ccol, 255))

    # Si es una escena de placa de capítulo, dibujarla a pantalla completa y retornar
    if vctx.chapter_card is not None:
        root_low = getattr(core, "ROOT", "").lower()
        is_dune = "dune" in root_low
        is_tesla = "tesla" in root_low
        is_cine = "cine" in root_low
        if is_dune and not vctx.chapter_card.get("snow"):
            d.ellipse([36, 38, 56, 58], fill=(244, 218, 162, 210))
            d.ellipse([216, 54, 230, 68], fill=(225, 232, 245, 190))
            pts1, pts2 = [(0, VH)], [(0, VH)]
            for x in range(0, VW + 12, 12):
                y1 = 392 + int(round(math.sin(x * 0.025 + t * 0.6) * 8))
                y2 = 414 + int(round(math.cos(x * 0.03 - t * 0.9) * 6))
                pts1.append((x, y1))
                pts2.append((x, y2))
            pts1.append((VW, VH))
            pts2.append((VW, VH))
            d.polygon(pts1, fill=(76, 46, 22, 230))
            d.polygon(pts2, fill=(104, 64, 30, 245))
        elif is_tesla:
            d.rectangle([0, 424, VW, VH], fill=(10, 14, 28, 245))
            for tx in (44, 135, 226):
                d.line([(tx, 386), (tx - 9, 426)], fill=(38, 54, 86, 220), width=2)
                d.line([(tx, 386), (tx + 9, 426)], fill=(38, 54, 86, 220), width=2)
                d.line([(tx - 11, 394), (tx + 11, 394)], fill=(52, 74, 114, 220), width=2)
            d.line([(0, 394), (VW, 394)], fill=(72, 168, 224, 120), width=1)
            if hasattr(common, "draw_rotating_arrows"):
                common.draw_rotating_arrows(cv, VW // 2, 78, 24, t, speed=2.0,
                                            color=common.TESLA_CYAN, glow=core.GOLD, alpha=0.75)
        elif is_cine:
            if hasattr(common, "draw_filmstrip"):
                common.draw_filmstrip(cv, 0, 28, VW, 36, t, speed=42.0, sepia=True, alpha=0.85)
                common.draw_filmstrip(cv, 0, 412, VW, 36, t, speed=-42.0, sepia=True, alpha=0.85)
            if hasattr(common, "draw_galloping_horse"):
                common.draw_galloping_horse(cv, VW // 2, 98, t * 0.9, scale=1, silhouette_col=core.GOLD, rider=True)
                common.draw_galloping_horse(cv, VW // 2, 378, t * 0.9 + 0.25, scale=1, silhouette_col=core.GOLD, rider=True)
        render_chapter_card_vertical(cv, vctx.chapter_card)
        return cv

    # 2. ENCABEZADO SUPERIOR REDIBUJADO EN x=8..262 (CERO TEXTO CORTADO)
    top_y_cursor = 10
    if vctx.header_windows or vctx.header_texts:
        hw = vctx.header_windows[0] if vctx.header_windows else {
            "fill": (20, 20, 34), "border": core.GOLD, "alpha": 0.95, "inner": (60, 70, 130)
        }
        wrapped_hdr = []
        for ht in vctx.header_texts:
            if ht["text"].strip() in ("·", "•", "-"):
                continue
            txt_tr = tr(ht["text"], ht["fname"])
            sz = 8 if ht["size"] >= 8 else ht["size"]
            lines = wrap_text_px(txt_tr, ht["fname"], sz, 238)
            for l_idx, line_str in enumerate(lines[:3]):
                rev = None
                if ht["reveal"] is not None:
                    prev_chars = sum(len(x) + 1 for x in lines[:l_idx])
                    rev = max(0, ht["reveal"] - prev_chars)
                wrapped_hdr.append({
                    **ht,
                    "text_raw": line_str,
                    "size": sz,
                    "reveal": rev,
                })
        if wrapped_hdr:
            hdr_h = max(36, 12 + len(wrapped_hdr) * 13)
            core._orig_window(cv, 8, 10, VW - 16, hdr_h, fill=hw["fill"], border=hw["border"],
                              alpha=hw["alpha"], inner=hw["inner"])
            for idx_l, hl in enumerate(wrapped_hdr):
                ly = 16 + idx_l * 13
                core._orig_draw_text(
                    cv, hl["text_raw"], VW // 2, ly, hl["fname"], hl["size"],
                    color=hl["color"], align="center", outline=hl["outline"],
                    shadow=hl["shadow"], gradient=hl["gradient"], reveal=hl["reveal"],
                    alpha=hl["alpha"], outline_w=hl["outline_w"],
                )
            top_y_cursor = 10 + hdr_h + 8

    # Bigyears (ej. "1955", "1958") centrados debajo del encabezado
    for by_item in vctx.bigyears:
        b_txt, _, b_y, b_t, b_t0, b_sz, b_ramp = by_item
        p = core.prog(b_t, b_t0, b_t0 + 0.55)
        if p > 0:
            yy = top_y_cursor + 4 - (1 - core.ease_out_back(p, 2.2)) * 24
            core._orig_draw_text(cv, b_txt, VW // 2, int(yy), "press", min(32, b_sz),
                                 align="center", gradient=b_ramp, outline_w=2, alpha=min(1.0, p * 3))
            top_y_cursor = max(top_y_cursor, int(yy) + min(32, b_sz) + 10)

    # 3. ZONA MEDIA: PANELES, RETRATOS, DIAGRAMAS Y OBJETOS DE ESCENA (y = top_y_cursor .. 354)
    has_chars = len(vctx.chars) > 0
    mid_y_min = max(72, top_y_cursor)
    mid_y_max = 352 if has_chars else 454
    avail_h = max(80, mid_y_max - mid_y_min)

    # Extraer pisos procedurales de ancho completo (x=0..480 en y >= 150) y trasladarlos al piso vertical (y=350..480)
    mc_arr = np.array(vctx.mid_canvas)
    full_bleed_rows = [
        y for y in range(150, core.H)
        if (mc_arr[y, :4, 3] > 180).any() and (mc_arr[y, core.W - 4:, 3] > 180).any()
        and (mc_arr[y, :, 3] > 180).sum() >= core.W - 12
    ]
    if full_bleed_rows:
        fb_y0 = min(full_bleed_rows)
        win_mask = np.zeros((core.H, core.W), dtype=bool)
        for (wx, wy, ww, wh) in vctx.mid_windows:
            win_mask[max(0, wy):min(core.H, wy + wh), max(0, wx):min(core.W, wx + ww)] = True
        sub_arr = mc_arr[fb_y0:, :, :]
        # Color base de cada fila del piso tomado de los márgenes laterales (x < 16 y x >= 464)
        margins = np.concatenate([sub_arr[:, :16, :3], sub_arr[:, core.W - 16:, :3]], axis=1)
        row_bg = np.median(margins, axis=1).astype(np.int16)  # (H_sub, 3)
        diff = np.abs(sub_arr[:, :, :3].astype(np.int16) - row_bg[:, None, :]).sum(axis=2)
        is_floor_px = (diff <= 65) & (~win_mask[fb_y0:, :])

        # Construir el piso limpio (rellenando cualquier texto superpuesto con el color del piso de esa fila)
        clean_floor = sub_arr.copy()
        for ry in range(clean_floor.shape[0]):
            fg_m = ~is_floor_px[ry]
            if fg_m.any():
                clean_floor[ry, fg_m, :3] = row_bg[ry].astype(np.uint8)
                clean_floor[ry, fg_m, 3] = 255
        pf_img = Image.fromarray(clean_floor, "RGBA").resize((VW, 480 - 348), Image.NEAREST)
        core.paste(cv, pf_img, 0, 348)

        # Limpiar únicamente los píxeles del piso en mid_canvas, preservando textos/tarjetas dibujados encima
        sub_arr[is_floor_px] = 0
        mc_arr[fb_y0:, :, :] = sub_arr
        vctx.mid_canvas = Image.fromarray(mc_arr, "RGBA")

    # Separar decoraciones de piso (y >= 236 fuera de ventanas, ej. pasto plantado a los pies)
    max_win_y1 = max([wy + wh for (_, wy, _, wh) in vctx.mid_windows], default=0)
    floor_y_cut = max(236, max_win_y1 + 2)
    floor_strip = None
    if floor_y_cut < core.H:
        mc_arr = np.array(vctx.mid_canvas)
        if (mc_arr[floor_y_cut:, :, 3] > 12).any():
            floor_strip = vctx.mid_canvas.crop((0, floor_y_cut, core.W, core.H))
            mc_arr[floor_y_cut:, :, :] = 0
            vctx.mid_canvas = Image.fromarray(mc_arr, "RGBA")

    scan_y_min = 38 if (vctx.header_windows or vctx.header_texts) else 4
    visual_rows = _find_mid_rows(vctx.mid_canvas, y_min=scan_y_min, y_max=core.H)
    if visual_rows:
        # Preparar crops de cada fila visual
        prepared_rows = []
        for row_items in visual_rows:
            crops = []
            for (x0, y0, x1, y1) in row_items:
                c_im = vctx.mid_canvas.crop((x0, y0, x1, y1))
                cw, ch = c_im.size
                if cw > 256:
                    sf = 256.0 / float(cw)
                    c_im = c_im.resize((256, max(1, int(round(ch * sf)))), Image.NEAREST)
                crops.append(c_im)
            row_h = max(c.size[1] for c in crops)
            prepared_rows.append((crops, row_h))

        row_gap = 6
        total_rows_h = sum(rh for _, rh in prepared_rows) + row_gap * max(0, len(prepared_rows) - 1)
        if total_rows_h > avail_h:
            sf = max(0.55, (avail_h - row_gap * max(0, len(prepared_rows) - 1)) / float(max(1, sum(rh for _, rh in prepared_rows))))
            scaled_rows = []
            for crops, _ in prepared_rows:
                sc_crops = [
                    c.resize((max(1, int(round(c.size[0] * sf))), max(1, int(round(c.size[1] * sf)))), Image.NEAREST)
                    for c in crops
                ]
                scaled_rows.append((sc_crops, max(c.size[1] for c in sc_crops)))
            prepared_rows = scaled_rows
            total_rows_h = sum(rh for _, rh in prepared_rows) + row_gap * max(0, len(prepared_rows) - 1)

        cur_y = mid_y_min + max(0, (avail_h - total_rows_h) // 2)
        for crops, row_h in prepared_rows:
            tot_w = sum(c.size[0] for c in crops) + 6 * max(0, len(crops) - 1)
            cur_x = (VW - tot_w) // 2
            for c_im in crops:
                cw, ch = c_im.size
                core.paste(cv, c_im, cur_x, cur_y + (row_h - ch) // 2)
                cur_x += cw + 6
            cur_y += row_h + row_gap

    # Si había decoración de piso (ej. matas de pasto en Oregón), dibujarla en el piso vertical (y ~ 434..460)
    if floor_strip is not None:
        fs_w = int(round(core.W * (202.0 / 408.0)))
        fs_resized = floor_strip.resize((fs_w, floor_strip.size[1]), Image.NEAREST)
        core.paste(cv, fs_resized, (VW - fs_w) // 2, 452 - (258 - floor_y_cut))

    # 4. SPOTLIGHTS Y PERSONAJES EN EL PISO VERTICAL (feet ~ 452, x en 34..236)
    def map_char_x(x_orig):
        return int(round(34 + (x_orig - 36) * (202.0 / 408.0)))

    for sp in vctx.spotlights:
        cx, top, bottom, w_top, w_bot, col, strength = sp
        vcx = map_char_x(cx)
        a = np.array(cv)
        th = core.bayer_tile(VW, VH)
        v_top, v_bot = 260, 460
        for y in range(v_top, v_bot):
            k_sp = (y - v_top) / max(1, v_bot - v_top)
            half = (w_top * 0.65 + (w_bot * 0.65 - w_top * 0.65) * k_sp) / 2
            x0, x1 = int(max(0, vcx - half)), int(min(VW, vcx + half))
            if x1 <= x0:
                continue
            m = th[y, x0:x1] < strength * (1 - 0.3 * k_sp)
            row = a[y, x0:x1, :3].astype(np.int32)
            row[m] = (row[m] * 0.4 + np.array(col) * 0.6).astype(np.int32)
            a[y, x0:x1, :3] = row
        cv = Image.fromarray(a, "RGBA")

    has_scale3 = any(c.get("scale", 1) >= 3 for c in vctx.chars)
    for ch_item in vctx.chars:
        ckind = ch_item["kind"]
        vx = map_char_x(ch_item["x"])
        orig_feet = ch_item["feet"]
        vfeet = 452 - max(0, int(round((262 - orig_feet) * 0.9)))
        vfeet = max(360, min(466, vfeet))
        orig_scale = ch_item.get("scale", 2)
        vscale = 2 if orig_scale >= 2 else 1

        if ckind == "char":
            spec = common.S.CAST[ch_item["key"]] if isinstance(ch_item["key"], str) else ch_item["key"]
            arr = common.upscale(common.S.render(spec, ch_item["t"], **ch_item["pose"]), vscale)
            if has_scale3 and orig_scale == 2:
                im_ch = Image.fromarray(arr, "RGBA")
                nw, nh = int(im_ch.size[0] * 0.75), int(im_ch.size[1] * 0.75)
                arr = np.array(im_ch.resize((nw, nh), Image.NEAREST))
                feet_off = int(common.FEET_OFFSET * vscale * 0.75)
                sh_w = int(18 * vscale * 0.75)
            else:
                feet_off = common.FEET_OFFSET * vscale
                sh_w = 18 * vscale
            if ch_item["shadow"] and ch_item["alpha"] > 0.3:
                core.shadow_ellipse(cv, vx, vfeet, sh_w, 4 * vscale, 80)
            core.paste_arr(cv, arr, vx - arr.shape[1] // 2, vfeet - feet_off, ch_item["alpha"])
        elif ckind == "sil":
            common._orig_silhouette(cv, ch_item["key"], vx, vfeet, ch_item["t"],
                                    color=ch_item["color"], scale=vscale, **ch_item["pose"])
        elif ckind == "robot":
            common._orig_robot(cv, vx, vfeet, ch_item["t"], face=ch_item["face"],
                               frozen=ch_item["frozen"], alpha=ch_item["alpha"],
                               sil=ch_item["sil"], scale=vscale)
        elif ckind == "prop":
            ch_item["fn"](cv, vx, vfeet)

    # Emotes ("!", "?") encima de las cabezas de los personajes
    for em in vctx.emotes:
        e_txt, ex_orig, ey_orig, e_fn, e_sz, e_col, e_a = em
        vex = max(12, min(VW - 12, map_char_x(ex_orig)))
        core._orig_draw_text(cv, e_txt, vex, 344, e_fn, min(16, e_sz), e_col, align="center", alpha=e_a)

    # Globos de diálogo encima de los personajes en el piso vertical (con ajuste de bordes a VW=270)
    for b_item in vctx.bubbles:
        b_txt, bx_orig, by_orig, b_sz, b_fn, b_tail, b_rev, b_col, b_fill, b_tx = b_item
        vbx = map_char_x(bx_orig)
        vby = 346
        draw_bubble_vertical(cv, b_txt, vbx, vby, size=b_sz, fname=b_fn, tail=b_tail,
                             reveal=b_rev, color=b_col, fill=b_fill)

    if vctx.vignette_strength > 0:
        yy, xx = np.mgrid[0:VH, 0:VW]
        dist = np.sqrt(((xx - VW / 2) / (VW / 2)) ** 2 + ((yy - VH / 2) / (VH / 2)) ** 2)
        m = np.clip((dist - 0.80) / 0.6, 0, 1) * vctx.vignette_strength
        th = core.bayer_tile(VW, VH)
        a = np.array(cv)
        a[th < m, :3] = (a[th < m, :3] * 0.6).astype(np.uint8)
        cv = Image.fromarray(a, "RGBA")

    dx, dy = vctx.shake_offset
    if dx != 0 or dy != 0:
        cv = common._orig_offset_canvas(cv, dx, dy)

    return cv


# ===========================================================================
# INSTALACIÓN DE HOOKS NO INTRUSIVOS EN CORE Y COMMON
# ===========================================================================

def _is_scene_cv(canvas):
    return isinstance(canvas, Image.Image) and canvas.size == (core.W, core.H)


def _install_hooks():
    if hasattr(core, "_orig_window"):
        return

    core._orig_bg = core.bg
    core._orig_vgradient = core.vgradient
    core._orig_new_canvas = core.new_canvas
    core._orig_grade = core.grade
    core._orig_vignette = core.vignette
    core._orig_window = core.window
    core._orig_draw_text = core.draw_text
    core._orig_portrait = core.portrait
    core._orig_portrait_card = core.portrait_card
    core._orig_bubble = core.bubble

    common._orig_char = common.char
    common._orig_silhouette = common.silhouette
    common._orig_robot = common.robot
    common._orig_chapter_card = common.chapter_card
    common._orig_bigyear = common.bigyear
    common._orig_spotlight = common.spotlight
    common._orig_offset_canvas = common.offset_canvas
    common._orig_draw_sand_wind = getattr(common, "draw_sand_wind", None)
    common._orig_bars70 = getattr(common, "bars70", None)

    def v_bars70(cv, lit, t, y=252, x0=30, alpha=1.0, cur_glow=True):
        vctx = getattr(core, "_VCTX", None)
        if vctx is not None and _is_scene_cv(cv):
            vy = min(214, y)
            vx0 = 240 - (70 * 3) // 2
            d = ImageDraw.Draw(cv)
            d.rectangle([vx0 - 6, vy - 5, vx0 + 70 * 3 + 4, vy + 15], fill=(10, 10, 20, int(190 * alpha)))
            for i in range(70):
                xx = vx0 + i * 3
                if i < lit:
                    c = (255, 250, 220) if (i == int(lit) - 1 and cur_glow) else core.GOLD
                    hgt = 10
                else:
                    c = (60, 56, 70)
                    hgt = 6
                d.rectangle([xx, vy + 10 - hgt, xx + 1, vy + 10], fill=(*c, 255))
            return
        if common._orig_bars70:
            return common._orig_bars70(cv, lit, t, y=y, x0=x0, alpha=alpha, cur_glow=cur_glow)

    def v_bg(name):
        vctx = getattr(core, "_VCTX", None)
        if vctx is not None:
            vctx.bg_calls.append(("bg", name))
            return Image.new("RGBA", (core.W, core.H), (0, 0, 0, 0))
        return core._orig_bg(name)

    def v_vgradient(top, bottom, bands=12):
        vctx = getattr(core, "_VCTX", None)
        if vctx is not None:
            vctx.bg_calls.append(("vgrad", (top, bottom, bands)))
            return Image.new("RGBA", (core.W, core.H), (0, 0, 0, 0))
        return core._orig_vgradient(top, bottom, bands)

    def v_new_canvas(color=(0, 0, 0)):
        vctx = getattr(core, "_VCTX", None)
        if vctx is not None:
            vctx.bg_calls.append(("solid", color))
            return Image.new("RGBA", (core.W, core.H), (0, 0, 0, 0))
        return core._orig_new_canvas(color)

    def v_grade(img, mul=(1, 1, 1), add=(0, 0, 0), sat=1.0, k=1.0):
        vctx = getattr(core, "_VCTX", None)
        if vctx is not None and _is_scene_cv(img):
            vctx.grades.append((mul, add, sat, k))
            return img
        return core._orig_grade(img, mul=mul, add=add, sat=sat, k=k)

    def v_vignette(canvas, strength=0.35):
        vctx = getattr(core, "_VCTX", None)
        if vctx is not None and _is_scene_cv(canvas):
            vctx.vignette_strength = strength
            return canvas
        return core._orig_vignette(canvas, strength)

    def v_window(canvas, x, y, w, h, fill=(20, 24, 52), border=core.GOLD, alpha=0.92, inner=(60, 70, 130)):
        vctx = getattr(core, "_VCTX", None)
        if vctx is not None:
            if _is_scene_cv(canvas):
                # Si es la ventana de encabezado superior (y <= 24 y w >= 200)
                if y <= 24 and w >= 200 and not vctx.mid_windows:
                    vctx.header_windows.append({
                        "x": x, "y": y, "w": w, "h": h,
                        "fill": fill, "border": border, "alpha": alpha, "inner": inner,
                    })
                    return
                if x + w <= 0 or x >= core.W or y + h <= 0 or y >= core.H:
                    vctx.active_x_shift = None
                    return
                if w > 254 and x >= 0:
                    # Si es un marco contenedor gigante (h >= 145) para varios sub-paneles, omitir su fondo
                    # para que los sub-paneles internos queden independientes y a escala 1:1
                    if h >= 145:
                        vctx.active_x_shift = None
                        return
                    # Limpiar líneas decorativas previas que la ventana ancha cubría en 16:9
                    if w >= 300 and y >= 50 and not vctx.mid_windows:
                        rx0, ry0 = max(0, x - 60), max(38, y - 20)
                        rx1, ry1 = min(core.W, x + w + 60), min(core.H, y + h + 10)
                        if rx1 > rx0 and ry1 > ry0:
                            d_clr = ImageDraw.Draw(canvas)
                            d_clr.rectangle([rx0, ry0, rx1, ry1], fill=(0, 0, 0, 0))
                    cx = x + w // 2
                    nw = 250
                    nx = max(8, min(core.W - nw - 8, cx - nw // 2))
                    vctx.active_x_shift = (id(canvas), x, w, nx, nw, y, y + h)
                    x, w = nx, nw
                else:
                    vctx.active_x_shift = None
                    # Si es una tarjeta inferior (y >= 165), limpiar puntas de flechas decorativas a sus lados
                    if y >= 165 and not vctx.mid_windows:
                        ry0, ry1 = max(160, y - 4), min(core.H, y + h + 4)
                        if ry1 > ry0:
                            d_clr = ImageDraw.Draw(canvas)
                            d_clr.rectangle([0, ry0, core.W, ry1], fill=(0, 0, 0, 0))
                vctx.mid_windows.append((x, y, w, h))
                core._orig_window(canvas, x, y, w, h, fill=fill, border=border, alpha=alpha, inner=inner)
                return
            else:
                # Sub-lienzo (ej. pop card): si la ventana supera 254px de ancho, compactarla a 250px
                if w > 254:
                    cx = x + w // 2
                    nw = 250
                    nx = max(0, cx - nw // 2)
                    vctx.active_x_shift = (id(canvas), x, w, nx, nw, y, y + h)
                    x, w = nx, nw
                else:
                    vctx.active_x_shift = None
                core._orig_window(canvas, x, y, w, h, fill=fill, border=border, alpha=alpha, inner=inner)
                return
        return core._orig_window(canvas, x, y, w, h, fill=fill, border=border, alpha=alpha, inner=inner)

    def v_draw_text(canvas, text, x, y, fname="press", size=8, color=core.CREAM, align="left",
                    outline=core.INK, shadow=True, gradient=None, reveal=None, alpha=1.0, outline_w=1):
        vctx = getattr(core, "_VCTX", None)
        if vctx is not None:
            t_str = (text or "").strip()
            # Si es un signo de exclamación/interrogación suelto sobre un personaje ("!", "?")
            if _is_scene_cv(canvas) and t_str in ("!", "?", "!!", "!?") and y >= 48:
                vctx.emotes.append((t_str, x, y, fname, size, color, alpha))
                return
            if _is_scene_cv(canvas) and vctx._in_header_zone(y) and size <= 16:
                vctx.header_texts.append({
                    "text": text, "x": x, "y": y, "fname": fname, "size": size,
                    "color": color, "align": align, "outline": outline, "shadow": shadow,
                    "gradient": gradient, "reveal": reveal, "alpha": alpha, "outline_w": outline_w,
                })
                return
            # Si cae dentro de una ventana ancha compactada a 250px (en cv o en un sub-lienzo pop), ajustar texto
            if vctx.active_x_shift is not None:
                cid, ox, ow, nx, nw, wy0, wy1 = vctx.active_x_shift
                if id(canvas) == cid and wy0 - 6 <= y <= wy1 + 10 and ox - 12 <= x <= ox + ow + 12:
                    if align == "center" and abs(x - (ox + ow // 2)) <= 32:
                        x = nx + nw // 2
                    elif align == "right":
                        x = nx + nw - max(6, (ox + ow - x))
                    elif align == "left":
                        x = int(round(nx + (x - ox) * (nw / float(max(1, ow)))))
                    tr_t = tr(text, fname)
                    tw, _ = core.text_size(tr_t, fname, size)
                    max_tw = nw - 14
                    if tw > max_tw:
                        if size >= 16:
                            size = 8
                            tw, _ = core.text_size(tr_t, fname, size)
                        if tw > max_tw:
                            lines = wrap_text_px(tr_t, fname, size, max_tw)
                            for li, lstr in enumerate(lines[:2]):
                                core._orig_draw_text(
                                    canvas, lstr, nx + nw // 2, y + li * 10,
                                    fname, size, color=color, align="center", outline=outline,
                                    shadow=shadow, gradient=gradient, reveal=reveal,
                                    alpha=alpha, outline_w=outline_w,
                                )
                            return
            # Si es un texto suelto en el lienzo principal (sin ventana) y supera 244px de ancho, ajustarlo
            if _is_scene_cv(canvas):
                tr_t = tr(text, fname)
                tw, _ = core.text_size(tr_t, fname, size)
                if tw > 244:
                    if size > 16:
                        size = 16
                        tw, _ = core.text_size(tr_t, fname, size)
                    if tw > 244 and size == 16:
                        size = 8
                    if core.text_size(tr_t, fname, size)[0] > 244:
                        lines8 = wrap_text_px(tr_t, fname, size, 244)
                        for li, lstr in enumerate(lines8[:3]):
                            core._orig_draw_text(
                                canvas, lstr, x if align == "center" else 240, y + li * 11,
                                fname, size, color=color, align="center", outline=outline,
                                shadow=shadow, gradient=gradient, reveal=reveal,
                                alpha=alpha, outline_w=outline_w,
                            )
                        return
            core._orig_draw_text(
                canvas, text, x, y, fname=fname, size=size, color=color,
                align=align, outline=outline, shadow=shadow, gradient=gradient,
                reveal=reveal, alpha=alpha, outline_w=outline_w,
            )
            return
        return core._orig_draw_text(
            canvas, text, x, y, fname=fname, size=size, color=color, align=align,
            outline=outline, shadow=shadow, gradient=gradient, reveal=reveal,
            alpha=alpha, outline_w=outline_w,
        )

    def v_bubble(canvas, text, x, y, size=8, fname="press", tail="down", reveal=None,
                 color=core.INK, fill=(250, 248, 240), tail_x=None):
        vctx = getattr(core, "_VCTX", None)
        if vctx is not None and _is_scene_cv(canvas):
            vctx.bubbles.append((text, x, y, size, fname, tail, reveal, color, fill, tail_x))
            return
        return core._orig_bubble(canvas, text, x, y, size=size, fname=fname, tail=tail,
                                 reveal=reveal, color=color, fill=fill, tail_x=tail_x)

    def v_char(cv, key, x, feet, t, alpha=1.0, shadow=True, scale=1, **pose):
        vctx = getattr(core, "_VCTX", None)
        if vctx is not None and _is_scene_cv(cv):
            vctx.chars.append({
                "kind": "char", "key": key, "x": x, "feet": feet, "t": t,
                "alpha": alpha, "shadow": shadow, "scale": scale, "pose": pose,
            })
            return
        return common._orig_char(cv, key, x, feet, t, alpha=alpha, shadow=shadow, scale=scale, **pose)

    def v_silhouette(cv, key, x, feet, t, color=(12, 10, 22), scale=1, **pose):
        vctx = getattr(core, "_VCTX", None)
        if vctx is not None and _is_scene_cv(cv):
            vctx.chars.append({
                "kind": "sil", "key": key, "x": x, "feet": feet, "t": t,
                "color": color, "scale": scale, "pose": pose,
            })
            return
        return common._orig_silhouette(cv, key, x, feet, t, color=color, scale=scale, **pose)

    def v_robot(cv, x, feet, t, face="happy", frozen=False, alpha=1.0, sil=False, scale=1):
        if "historia_ia" not in getattr(core, "ROOT", "").lower():
            return
        vctx = getattr(core, "_VCTX", None)
        if vctx is not None and _is_scene_cv(cv):
            vctx.chars.append({
                "kind": "robot", "x": x, "feet": feet, "t": t,
                "face": face, "frozen": frozen, "alpha": alpha, "sil": sil, "scale": scale,
            })
            return
        return common._orig_robot(cv, x, feet, t, face=face, frozen=frozen, alpha=alpha, sil=sil, scale=scale)

    def v_chapter_card(cv, t, t0, num, lines, years, ramp_title=core.CREAM_RAMP):
        vctx = getattr(core, "_VCTX", None)
        if vctx is not None and _is_scene_cv(cv):
            has_snow = any(p[0] == "snow" for p in vctx.particles)
            vctx.chapter_card = {
                "t": t, "t0": t0, "num": num, "lines": lines,
                "years": years, "ramp_title": ramp_title, "snow": has_snow,
            }
            return
        return common._orig_chapter_card(cv, t, t0, num, lines, years, ramp_title=ramp_title)

    def v_bigyear(cv, text, cx, y, t, t0, size=48, ramp=core.GOLD_RAMP):
        vctx = getattr(core, "_VCTX", None)
        if vctx is not None and _is_scene_cv(cv):
            vctx.bigyears.append((text, cx, y, t, t0, size, ramp))
            return
        return common._orig_bigyear(cv, text, cx, y, t, t0, size=size, ramp=ramp)

    def v_spotlight(cv, cx, top, bottom, w_top, w_bot, color=(120, 220, 255), strength=0.22):
        vctx = getattr(core, "_VCTX", None)
        if vctx is not None and _is_scene_cv(cv):
            vctx.spotlights.append((cx, top, bottom, w_top, w_bot, color, strength))
            return cv
        return common._orig_spotlight(cv, cx, top, bottom, w_top, w_bot, color=color, strength=strength)

    def v_offset_canvas(cv, dx, dy, fill=(0, 0, 0)):
        vctx = getattr(core, "_VCTX", None)
        if vctx is not None and _is_scene_cv(cv):
            vctx.shake_offset = (dx, dy)
            return cv
        return common._orig_offset_canvas(cv, dx, dy, fill=fill)

    def v_draw_sand_wind(cv, t, density=42, color=(238, 202, 132), y_min=20, y_max=265):
        vctx = getattr(core, "_VCTX", None)
        if vctx is not None and _is_scene_cv(cv):
            vctx.particles.append(("sand_wind", t, density, color))
            return
        if common._orig_draw_sand_wind:
            return common._orig_draw_sand_wind(cv, t, density=density, color=color, y_min=y_min, y_max=y_max)

    # Parchear partículas (SNOW, STARS, CONF)
    common._orig_snow_draw = common.SNOW.draw
    common._orig_stars_draw = common.STARS.draw
    common._orig_conf_draw = common.CONF.draw

    def v_snow_draw(canvas, t, density=1.0, alpha=255):
        vctx = getattr(core, "_VCTX", None)
        if vctx is not None and _is_scene_cv(canvas):
            vctx.particles.append(("snow", t, density))
            return
        return common._orig_snow_draw(canvas, t, density=density, alpha=alpha)

    def v_stars_draw(canvas, t, alpha=1.0):
        vctx = getattr(core, "_VCTX", None)
        if vctx is not None and _is_scene_cv(canvas):
            vctx.particles.append(("stars", t, alpha))
            return
        return common._orig_stars_draw(canvas, t, alpha=alpha)

    def v_conf_draw(canvas, t):
        vctx = getattr(core, "_VCTX", None)
        if vctx is not None and _is_scene_cv(canvas):
            vctx.particles.append(("conf", t))
            return
        return common._orig_conf_draw(canvas, t)

    common.SNOW.draw = v_snow_draw
    common.STARS.draw = v_stars_draw
    common.CONF.draw = v_conf_draw

    # Propagar hooks a core, common y todos los módulos de capítulos cargados
    import sys
    rep = {
        "bg": v_bg,
        "vgradient": v_vgradient,
        "new_canvas": v_new_canvas,
        "grade": v_grade,
        "vignette": v_vignette,
        "window": v_window,
        "draw_text": v_draw_text,
        "bubble": v_bubble,
        "char": v_char,
        "silhouette": v_silhouette,
        "robot": v_robot,
        "chapter_card": v_chapter_card,
        "bigyear": v_bigyear,
        "spotlight": v_spotlight,
        "offset_canvas": v_offset_canvas,
    }
    if common._orig_draw_sand_wind is not None:
        rep["draw_sand_wind"] = v_draw_sand_wind
    if common._orig_bars70 is not None:
        rep["bars70"] = v_bars70

    for mod in list(sys.modules.values()):
        if mod is None:
            continue
        for k_fn, fn_val in rep.items():
            if hasattr(mod, k_fn):
                setattr(mod, k_fn, fn_val)


def render_scene_vertical(fn, t):
    """Ejecuta `fn(t)` interceptando sus capas y devuelve un Image RGBA 270x480 a pantalla completa."""
    _install_hooks()
    # Escenas de cierre (logo y créditos de Pixeloide Studios) tienen su diseño vertical dedicado
    if hasattr(outro, "T_CRED") and t >= outro.T_CRED - 0.01:
        return render_credits_vertical(t, outro.T_CRED)
    if hasattr(outro, "T_LOGO") and t >= outro.T_LOGO - 0.01:
        return render_pixeloide_logo_vertical(t, outro.T_LOGO)

    vctx = VerticalContext(t)
    core._VCTX = vctx
    try:
        res = fn(t)
    finally:
        core._VCTX = None

    if isinstance(res, Image.Image) and res.size == (core.W, core.H):
        vctx.mid_canvas = res

    return compose_vertical_scene(vctx)


_VERT_BAYER = None


def dither_mix_vertical(a, b, k):
    """Mezcla dos fotogramas 270x480 con dithering Bayer 4x4."""
    global _VERT_BAYER
    if _VERT_BAYER is None:
        _VERT_BAYER = core.bayer_tile(VW, VH)
    A = np.array(a)
    B = np.array(b)
    m = _VERT_BAYER < k
    A[m] = B[m]
    return Image.fromarray(A, a.mode)


def frame_at_vertical(t, scenes_list, xfade=0.22, final=True):
    """Renderiza el instante `t` en formato 9:16 nativo (270x480 o 1080x1920 si `final=True`)."""
    idx = 0
    for i, s in enumerate(scenes_list):
        if t >= s[0]:
            idx = i
    st, fn, _, _ = scenes_list[idx]
    img = render_scene_vertical(fn, t)
    if idx > 0 and t < st + xfade:
        pst, pfn, _, _ = scenes_list[idx - 1]
        prev = render_scene_vertical(pfn, t)
        k = (t - st) / xfade
        img = dither_mix_vertical(prev, img, k)
    if final:
        return img.resize((OUT_VW, OUT_VH), Image.NEAREST)
    return img
