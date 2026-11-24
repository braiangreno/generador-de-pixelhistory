"""Motor gráfico 2D Cartoon HD (1920x1080 nativo, CERO pixel art) para Stickman Histórico 2D.

Mantiene el sistema de coordenadas lógicas 480x270 (W=480, H=270) para compatibilidad total
con las escenas y las 5 reglas de oro, pero renderiza absolutamente todo (fondos, personajes
Stickman, tipografías vectoriales, paneles redondeados, sombras y transiciones) en alta definición
1920x1080 (escala interna HD_K = 4) con anti-aliasing suave (LANCZOS / curvas vectoriales)
y CERO pixelado o dithering."""
from functools import lru_cache
import math
import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 480, 270
HD_K = 4
W_HD, H_HD = W * HD_K, H * HD_K
FPS = 30

GOLD = (246, 198, 76)
GOLD_D = (188, 132, 38)
CREAM = (252, 248, 236)
WHITE = (255, 255, 255)
INK = (18, 18, 24)
CYAN = (72, 218, 248)
CYAN_D = (28, 128, 168)
PINK = (242, 92, 98)
GREEN = (88, 218, 118)
VIOLET = (176, 128, 248)
GREY = (184, 192, 212)
DARK_GREY = (92, 98, 118)

GOLD_RAMP = [(255, 244, 176), (248, 202, 84), (218, 148, 42)]
CREAM_RAMP = [(255, 255, 255), (248, 242, 224), (218, 210, 192)]
CYAN_RAMP = [(208, 248, 255), (88, 218, 248), (38, 148, 196)]
PINK_RAMP = [(255, 204, 204), (242, 96, 96), (178, 42, 48)]
ICE_RAMP = [(236, 248, 255), (168, 214, 242), (104, 152, 196)]

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Tipografías vectoriales limpias estilo documental 2D (OverSimplified) — CERO fuentes pixeladas
WIN_FONTS = r"C:\Windows\Fonts"
FONTS = {
    "press": os.path.join(WIN_FONTS, "arialbd.ttf") if os.path.exists(os.path.join(WIN_FONTS, "arialbd.ttf")) else os.path.join(ROOT, "fonts", "PixelifySans.ttf"),
    "silk": os.path.join(WIN_FONTS, "seguisb.ttf") if os.path.exists(os.path.join(WIN_FONTS, "seguisb.ttf")) else os.path.join(WIN_FONTS, "arialbd.ttf"),
    " silk_b": os.path.join(WIN_FONTS, "arialbd.ttf"),
    "vt": os.path.join(WIN_FONTS, "arialbd.ttf"),
}


def clamp01(x):
    return 0.0 if x < 0.0 else (1.0 if x > 1.0 else float(x))


def ease_out(t):
    t = clamp01(t)
    return 1.0 - (1.0 - t) ** 3


def ease_in(t):
    t = clamp01(t)
    return t * t * t


def ease_in_out(t):
    t = clamp01(t)
    return 3 * t * t - 2 * t * t * t


def ease_out_back(t, s=1.70158):
    t = clamp01(t) - 1.0
    return t * t * ((s + 1) * t + s) + 1.0


def prog(t, a, b):
    if b <= a:
        return 1.0 if t >= b else 0.0
    return clamp01((t - a) / (b - a))


def shade(c, f):
    return tuple(int(max(0, min(255, v * f))) for v in c[:3])


# --------------------------------------------------------------------------- Escalador Vectorial HD para ImageDraw
_orig_imagedraw_draw = ImageDraw.Draw


def _scale_xy(xy, k):
    if isinstance(xy, (list, tuple)):
        if len(xy) == 4 and all(isinstance(v, (int, float)) for v in xy):
            x0, y0, x1, y1 = xy
            if x1 < x0:
                x0, x1 = x1, x0
            if y1 < y0:
                y0, y1 = y1, y0
            return [int(round(x0 * k)), int(round(y0 * k)), int(round(x1 * k)), int(round(y1 * k))]
        return [
            (int(round(pt[0] * k)), int(round(pt[1] * k))) if isinstance(pt, (list, tuple)) else int(round(pt * k))
            for pt in xy
        ]
    return xy


class _HDImageDrawProxy:
    """Escala automáticamente todas las primitivas de dibujo 480x270 a 1920x1080 con trazos vectoriales suaves."""
    def __init__(self, im, mode=None):
        self._im = im
        self._d = _orig_imagedraw_draw(im, mode)
        self._k = HD_K if getattr(im, "size", None) == (W_HD, H_HD) else 1

    def rectangle(self, xy, fill=None, outline=None, width=1):
        if isinstance(xy, (list, tuple)) and len(xy) == 4 and all(isinstance(v, (int, float)) for v in xy):
            x0, y0, x1, y1 = xy
            if x1 < x0:
                x0, x1 = x1, x0
            if y1 < y0:
                y0, y1 = y1, y0
            xy = [x0, y0, x1, y1]
            if self._k == HD_K and outline is not None:
                rw, rh = int(x1 - x0), int(y1 - y0)
                if 64 <= rw <= 460 and 16 <= rh <= 220:
                    cx = int(x0 + rw // 2)
                    if globals().get("_VCTX") is None and abs(cx - 240) <= 10 and 174 <= rw <= 248:
                        rw = max(rw, 268 if rw >= 218 else 224)
                        x0 = cx - rw // 2
                        x1 = x0 + rw
                        xy = [x0, y0, x1, y1]
                    wins = getattr(self._im, "_windows", None)
                    if wins is None:
                        wins = []
                        self._im._windows = wins
                    wins.append((int(x0), int(y0), int(rw), int(rh)))
        s_xy = _scale_xy(xy, self._k)
        s_w = max(1, int(round(width * self._k))) if outline is not None else 1
        if self._k == HD_K and outline is not None and (s_xy[2] - s_xy[0]) >= 32 and (s_xy[3] - s_xy[1]) >= 24:
            return self._d.rounded_rectangle(s_xy, radius=8, fill=fill, outline=outline, width=s_w)
        return self._d.rectangle(s_xy, fill=fill, outline=outline, width=s_w)

    def rounded_rectangle(self, xy, radius=0, fill=None, outline=None, width=1):
        return self._d.rounded_rectangle(_scale_xy(xy, self._k), radius=int(radius * self._k),
                                         fill=fill, outline=outline, width=max(1, int(width * self._k)))

    def line(self, xy, fill=None, width=1, joint=None):
        return self._d.line(_scale_xy(xy, self._k), fill=fill, width=max(1, int(round(width * self._k))), joint="curve")

    def ellipse(self, xy, fill=None, outline=None, width=1):
        return self._d.ellipse(_scale_xy(xy, self._k), fill=fill, outline=outline, width=max(1, int(round(width * self._k))))

    def arc(self, xy, start, end, fill=None, width=1):
        return self._d.arc(_scale_xy(xy, self._k), start, end, fill=fill, width=max(1, int(round(width * self._k))))

    def chord(self, xy, start, end, fill=None, outline=None, width=1):
        return self._d.chord(_scale_xy(xy, self._k), start, end, fill=fill, outline=outline, width=max(1, int(round(width * self._k))))

    def pieslice(self, xy, start, end, fill=None, outline=None, width=1):
        return self._d.pieslice(_scale_xy(xy, self._k), start, end, fill=fill, outline=outline, width=max(1, int(round(width * self._k))))

    def polygon(self, xy, fill=None, outline=None, width=1):
        return self._d.polygon(_scale_xy(xy, self._k), fill=fill, outline=outline, width=max(1, int(round(width * self._k))))

    def point(self, xy, fill=None):
        if isinstance(xy, (list, tuple)) and len(xy) == 2 and isinstance(xy[0], (int, float)):
            px, py = int(round(xy[0] * self._k)), int(round(xy[1] * self._k))
            r = max(1, self._k // 2)
            return self._d.ellipse([px - r, py - r, px + r, py + r], fill=fill)
        return self._d.point(_scale_xy(xy, self._k), fill=fill)

    def __getattr__(self, name):
        return getattr(self._d, name)


def _hooked_draw(im, mode=None):
    return _HDImageDrawProxy(im, mode)


ImageDraw.Draw = _hooked_draw


# --------------------------------------------------------------------------- Lienzos, Fondos y Retratos 2D HD

def new_canvas(color=(16, 18, 28)):
    return Image.new("RGBA", (W_HD, H_HD), (*color[:3], 255))


def vgradient(top, bottom, bands=None):
    """Degradado vertical suave continuo en 1920x1080 (sin bandas pixeladas)."""
    y = np.linspace(0.0, 1.0, H_HD, dtype=np.float32)[:, None, None]
    t_arr = np.array(top[:3], dtype=np.float32)[None, None, :]
    b_arr = np.array(bottom[:3], dtype=np.float32)[None, None, :]
    rgb = np.clip(t_arr + (b_arr - t_arr) * y, 0, 255).astype(np.uint8)
    rgb = np.broadcast_to(rgb, (H_HD, W_HD, 3)).copy()
    a = np.full((H_HD, W_HD, 1), 255, dtype=np.uint8)
    return Image.fromarray(np.concatenate([rgb, a], axis=2), "RGBA")


@lru_cache(maxsize=64)
def load_rgba_hd(path, target_size=None):
    im = Image.open(os.path.join(ROOT, path)).convert("RGBA")
    if target_size and im.size != target_size:
        im = im.resize(target_size, Image.LANCZOS)
    return im


def load_rgba(path):
    return load_rgba_hd(path)


def bg(name):
    return load_rgba_hd(f"assets/bg/{name}.png", (W_HD, H_HD)).copy()


def portrait(arg1, name=None, x=0, y=0, size=64):
    if isinstance(arg1, str):
        return load_rgba_hd(f"assets/portraits/{arg1}.png", (256, 256))
    cv = arg1
    k = HD_K if cv.size == (W_HD, H_HD) else 1
    im = load_rgba_hd(f"assets/portraits/{name}.png", (size * k, size * k))
    cv.paste(im, (int(x * k), int(y * k)), im)
    _orig_imagedraw_draw(cv).rounded_rectangle(
        [int(x * k) - 2, int(y * k) - 2, int((x + size) * k) + 2, int((y + size) * k) + 2],
        radius=8, outline=(*INK, 255), width=max(2, k)
    )
    return im


# --------------------------------------------------------------------------- Tipografía Vectorial 2D Cartoon

@lru_cache(maxsize=64)
def font_hd(name, size_logical):
    path = FONTS.get(name, FONTS["press"])
    # Escalar tamaño lógico (8, 16, 24) a píxeles 1080p con proporción limpia
    px_size = max(14, int(round(size_logical * 3.15))) if name == "press" else max(14, int(round(size_logical * 3.35)))
    return ImageFont.truetype(path, px_size)


@lru_cache(maxsize=2048)
def text_size(text, fname="press", size=8):
    if not text:
        return (0, size)
    f = font_hd(fname, size)
    bbox = f.getbbox(str(text))
    w_hd = max(1, bbox[2] - bbox[0])
    h_hd = max(1, bbox[3] - bbox[1])
    return (int(math.ceil(w_hd / float(HD_K))), int(math.ceil(h_hd / float(HD_K))))


def draw_text(canvas, text, x, y, fname="press", size=8, color=WHITE, align="left",
              outline=INK, shadow=True, gradient=None, alpha=1.0, reveal=None, outline_w=1):
    """Dibuja texto vectorial anti-aliased en 1080p con contorno cartoon negro suave
    y ajuste automático dentro de la ventana contenedora."""
    if alpha <= 0 or not text:
        return
    try:
        from i18n import tr
    except Exception:
        tr = lambda s, f="press": s

    if outline is not None and tuple(color[:3]) == tuple(outline[:3]):
        outline = None
        shadow = False

    orig_len = len(text) if isinstance(text, str) else 0
    raw_text = str(text)

    wins = getattr(canvas, "_windows", None)
    containing_win = None
    if wins:
        for (wx, wy, ww, wh) in wins:
            if (wx - 6 <= x <= wx + ww + 6) and (wy - 2 <= y <= wy + wh - 3):
                if containing_win is None or ww < containing_win[2]:
                    containing_win = (wx, wy, ww, wh)

    if containing_win is not None:
        wx, wy, ww, wh = containing_win
        bound_x0, bound_x1 = wx + 8, wx + ww - 8
        if align == "center" and abs(x - (wx + ww // 2)) <= 18:
            x = wx + ww // 2
    else:
        bound_x0, bound_x1 = 8, W - 8

    if align == "center":
        max_tw = min(bound_x1 - bound_x0, 2 * min(x - bound_x0, bound_x1 - x))
    elif align == "right":
        max_tw = x - bound_x0
    else:
        max_tw = bound_x1 - x

    full_text = tr(raw_text, fname)
    full_tw, _ = text_size(full_text, fname, size)

    if max_tw >= 36 and full_tw > max_tw:
        if size > 16:
            size = 16
            full_text = tr(raw_text, fname)
            full_tw, _ = text_size(full_text, fname, size)
        if full_tw > max_tw and size > 8:
            size = 8
            full_text = tr(raw_text, fname)
            full_tw, _ = text_size(full_text, fname, size)

    shown = full_text
    if reveal is not None:
        if orig_len > 0 and len(full_text) != orig_len:
            reveal = reveal * len(full_text) / orig_len
        n = int(reveal)
        if n <= 0:
            return
        shown = full_text[:n]

    k = HD_K if canvas.size == (W_HD, H_HD) else 1
    f = font_hd(fname, size) if k == HD_K else ImageFont.truetype(FONTS.get(fname, FONTS["press"]), max(8, size))
    bbox = f.getbbox(shown)
    tw_px = max(1, bbox[2] - bbox[0])
    th_px = max(1, bbox[3] - bbox[1])
    full_bbox = f.getbbox(full_text)
    full_tw_px = max(1, full_bbox[2] - full_bbox[0])
    max_tw_px = max(36 * k, int(max_tw * k))

    stroke_w = (max(3, outline_w * 3) if k == HD_K else 1) if outline is not None else 0
    pad_px = stroke_w + 6
    tmp = Image.new("RGBA", (tw_px + pad_px * 2, th_px + pad_px * 2), (0, 0, 0, 0))
    dtmp = _orig_imagedraw_draw(tmp)

    fill_col = (*gradient[0][:3], int(255 * alpha)) if gradient else (*color[:3], int(255 * alpha))
    tx0, ty0 = pad_px - bbox[0], pad_px - bbox[1]

    if shadow and outline is not None:
        sh_off = 3 if k == HD_K else 1
        dtmp.text((tx0 + sh_off, ty0 + sh_off), shown, font=f, fill=(10, 10, 16, int(190 * alpha)),
                  stroke_width=stroke_w, stroke_fill=(10, 10, 16, int(190 * alpha)))

    if outline is not None:
        dtmp.text((tx0, ty0), shown, font=f, fill=fill_col,
                  stroke_width=stroke_w, stroke_fill=(*outline[:3], int(255 * alpha)))
    else:
        dtmp.text((tx0, ty0), shown, font=f, fill=fill_col)

    if full_tw_px > max_tw_px and tw_px > 0:
        scale_f = max_tw_px / float(full_tw_px)
        new_w = max(1, int(round(tmp.size[0] * scale_f)))
        tmp = tmp.resize((new_w, tmp.size[1]), Image.LANCZOS)
        tw_px = max(1, int(round(tw_px * scale_f)))

    x_px = int(round(x * k))
    y_px = int(round(y * k))
    if align == "center":
        x0_px = x_px - tw_px // 2
    elif align == "right":
        x0_px = x_px - tw_px
    else:
        x0_px = x_px

    b0_px, b1_px = int(bound_x0 * k), int(bound_x1 * k)
    if x0_px + tw_px > b1_px:
        x0_px = b1_px - tw_px
    if x0_px < b0_px:
        x0_px = b0_px

    _paste_raw(canvas, tmp, x0_px - pad_px, y_px - pad_px // 2)


# --------------------------------------------------------------------------- Composición y Efectos 2D Suaves

def _paste_raw(canvas, img, x_px, y_px):
    w, h = img.size
    cw, ch = canvas.size
    x0, y0 = max(0, int(x_px)), max(0, int(y_px))
    x1, y1 = min(cw, int(x_px) + w), min(ch, int(y_px) + h)
    if x1 <= x0 or y1 <= y0:
        return
    crop = img.crop((x0 - int(x_px), y0 - int(y_px), x1 - int(x_px), y1 - int(y_px)))
    canvas.alpha_composite(crop, (x0, y0))


def paste(canvas, img, x, y, alpha=1.0):
    if alpha <= 0:
        return
    k = HD_K if canvas.size == (W_HD, H_HD) else 1
    if k == HD_K and img.size[0] <= W and img.size[1] <= H and not getattr(img, "_is_hd", False):
        img = img.resize((img.size[0] * HD_K, img.size[1] * HD_K), Image.LANCZOS)
    if alpha < 1.0:
        img = img.copy()
        a = np.array(img)
        a[..., 3] = (a[..., 3].astype(np.float32) * clamp01(alpha)).astype(np.uint8)
        img = Image.fromarray(a, "RGBA")
    _paste_raw(canvas, img, int(round(x * k)), int(round(y * k)))


def paste_arr(canvas, arr, x, y, alpha=1.0):
    im = Image.fromarray(arr, "RGBA")
    im._is_hd = (arr.shape[0] > H or arr.shape[1] > W)
    if canvas.size == (W_HD, H_HD) and im._is_hd:
        if alpha < 1.0:
            a = arr.copy()
            a[..., 3] = (a[..., 3].astype(np.float32) * clamp01(alpha)).astype(np.uint8)
            im = Image.fromarray(a, "RGBA")
        _paste_raw(canvas, im, int(round(x * HD_K)), int(round(y * HD_K)))
    else:
        paste(canvas, im, x, y, alpha)


@lru_cache(maxsize=16)
def bayer_tile(w, h):
    return np.full((h, w), 0.5, dtype=np.float32)


def dither_mix(a, b, k):
    """Transición suave crossfade 2D (reemplaza el dithering pixelado Bayer)."""
    k = clamp01(k)
    if k <= 0:
        return a
    if k >= 1:
        return b
    if a.size != b.size:
        b = b.resize(a.size, Image.LANCZOS)
    return Image.blend(a.convert("RGBA"), b.convert("RGBA"), k)


def fade_to(canvas, color, k):
    k = clamp01(k)
    if k <= 0:
        return canvas
    solid = Image.new(canvas.mode, canvas.size, (*color[:3], 255) if canvas.mode == "RGBA" else color[:3])
    return Image.blend(canvas, solid, k)


def grade(img, mul=(1, 1, 1), add=(0, 0, 0), sat=1.0, k=1.0, tint=None, dark=0.0):
    if tint is not None:
        mul = tuple(float(c) * (1.0 - float(dark)) for c in tint)
    elif dark:
        mul = tuple(float(c) * (1.0 - float(dark)) for c in mul)
    a = np.array(img).astype(np.float32)
    rgb = a[..., :3]
    lum = (rgb * np.array([0.299, 0.587, 0.114])).sum(-1, keepdims=True)
    g = lum + (rgb - lum) * sat
    g = g * np.array(mul) + np.array(add)
    out = rgb + (g - rgb) * k
    a[..., :3] = np.clip(out, 0, 255)
    res = Image.fromarray(a.astype(np.uint8), img.mode)
    try:
        img.paste(res, (0, 0))
        return img
    except Exception:
        return res


# --------------------------------------------------------------------------- Tarjetas, Globos y Sombras 2D Cartoon

def window(canvas, x, y, w, h, fill=(24, 30, 52), border=GOLD, alpha=0.95, inner=(64, 78, 128)):
    """Tarjeta documental 2D Cartoon con bordes redondeados, contorno negro grueso y sombra suave."""
    if border is None:
        border = GOLD
    if globals().get("_VCTX") is None and getattr(canvas, "size", None) in ((W, H), (W_HD, H_HD)):
        cx = x + w // 2
        if 232 <= w <= 296 and 24 <= y <= 62 and 36 <= h <= 176 and abs(cx - 240) <= 12:
            w = 328
            x = cx - w // 2
    wins = getattr(canvas, "_windows", None)
    if wins is None:
        wins = []
        try:
            canvas._windows = wins
        except Exception:
            pass
    wins.append((int(x), int(y), int(w), int(h)))

    k = HD_K if canvas.size == (W_HD, H_HD) else 1
    x0, y0, x1, y1 = int(x * k), int(y * k), int((x + w) * k), int((y + h) * k)
    rad = 14 if k == HD_K else 3
    ov = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = _orig_imagedraw_draw(ov)
    # Sombra suave
    sh_off = 6 if k == HD_K else 2
    d.rounded_rectangle([x0 + sh_off, y0 + sh_off, x1 + sh_off, y1 + sh_off],
                        radius=rad, fill=(0, 0, 0, int(130 * alpha)))
    # Cuerpo de la tarjeta con contorno exterior negro cartoon y filete interior de color
    d.rounded_rectangle([x0, y0, x1, y1], radius=rad,
                        fill=(*fill[:3], int(246 * alpha)), outline=(*INK, 255), width=max(2, 5 if k == HD_K else 1))
    in_pad = 5 if k == HD_K else 1
    if (x1 - x0) > in_pad * 4 and (y1 - y0) > in_pad * 4:
        d.rounded_rectangle([x0 + in_pad, y0 + in_pad, x1 - in_pad, y1 - in_pad],
                            radius=max(2, rad - 3), outline=(*border[:3], int(235 * alpha)),
                            width=max(1, 3 if k == HD_K else 1))
    canvas.alpha_composite(ov)


def portrait_card(canvas, name, x, y, alpha=1.0, frame=GOLD):
    p = portrait(name)
    window(canvas, x - 4, y - 4, 64 + 8, 64 + 8, border=frame)
    k = HD_K if canvas.size == (W_HD, H_HD) else 1
    im = p.resize((64 * k, 64 * k), Image.LANCZOS)
    _paste_raw(canvas, im, int(x * k), int(y * k))


def bubble(canvas, text, x, y, size=8, fname="press", tail="down", reveal=None, color=INK,
           fill=(252, 250, 242), tail_x=None, align=None):
    """Globo de diálogo 2D Cartoon redondeado con contorno negro grueso."""
    if reveal is not None and int(reveal) <= 0:
        return
    try:
        from i18n import tr
        text = tr(text, fname)
    except Exception:
        pass
    tw, th = text_size(text, fname, size)
    bw, bh = tw + 16, th + 12
    bx = int(x - bw // 2)
    by = int(y - bh - 6) if tail == "down" else int(y + 6)
    bx = max(4, min(W - bw - 4, bx))
    wins = getattr(canvas, "_windows", None)
    if wins:
        for (wx, wy, ww, wh) in wins:
            if not (bx + bw <= wx or bx >= wx + ww or by + bh <= wy or by >= wy + wh):
                if wy < 140:
                    by = max(by, wy + wh + 4)
    if wins is None:
        wins = []
        canvas._windows = wins
    wins.append((bx - 2, by, bw + 4, bh))

    k = HD_K if canvas.size == (W_HD, H_HD) else 1
    x0, y0, x1, y1 = bx * k, by * k, (bx + bw) * k, (by + bh) * k
    tx = int(x * k)
    d = _orig_imagedraw_draw(canvas)
    d.rounded_rectangle([x0 + 4, y0 + 4, x1 + 4, y1 + 4], radius=12 if k == HD_K else 3, fill=(0, 0, 0, 100))
    d.rounded_rectangle([x0, y0, x1, y1], radius=12 if k == HD_K else 3,
                        fill=(*fill[:3], 255), outline=(*INK, 255), width=max(2, 4 if k == HD_K else 1))
    if tail == "down":
        pts = [(tx - 8, y1 - 2), (tx + 8, y1 - 2), (tx, y1 + 14)] if k == HD_K else [(tx - 2, y1), (tx + 2, y1), (tx, y1 + 4)]
        d.polygon(pts, fill=(*fill[:3], 255), outline=(*INK, 255))
    draw_text(canvas, text, bx + bw // 2, by + 5, fname, size, color, align="center",
              outline=None, shadow=False, reveal=reveal)


def shadow_ellipse(canvas, cx, cy, rx, ry, alpha=90):
    if rx <= 0 or ry <= 0 or alpha <= 0:
        return
    k = HD_K if canvas.size == (W_HD, H_HD) else 1
    ov = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = _orig_imagedraw_draw(ov)
    d.ellipse([int((cx - rx) * k), int((cy - ry) * k), int((cx + rx) * k), int((cy + ry) * k)],
              fill=(10, 10, 18, int(alpha)))
    canvas.alpha_composite(ov)


def sparkle(canvas, cx, cy, t, r=3, color=GOLD):
    s = round((math.sin(t * 7) * 0.5 + 0.5) * r)
    if s <= 0:
        return
    d = ImageDraw.Draw(canvas)
    d.line([(cx - s, cy), (cx + s, cy)], fill=(*color[:3], 255), width=2)
    d.line([(cx, cy - s), (cx, cy + s)], fill=(*color[:3], 255), width=2)


class Rain:
    def __init__(self, n=140, seed=1, region=(0, 0, W, H), color=(170, 190, 215), speed=260, slant=0.25):
        rnd = random.Random(seed)
        self.p = [(rnd.uniform(0, 1), rnd.uniform(0, 1), rnd.uniform(0.7, 1.3)) for _ in range(n)]
        self.region, self.color, self.speed, self.slant = region, color, speed, slant

    def draw(self, canvas, t, alpha=255):
        x0, y0, x1, y1 = self.region
        d = ImageDraw.Draw(canvas)
        hgt = y1 - y0
        for (u, v, s) in self.p:
            y = y0 + ((v * hgt + t * self.speed * s) % hgt)
            x = x0 + ((u * (x1 - x0) + (y - y0) * self.slant) % (x1 - x0))
            d.line([(int(x), int(y)), (int(x - 1), int(y - 4 * s))], fill=(*self.color, alpha), width=1)


class Snow:
    def __init__(self, n=220, seed=2, region=(0, 0, W, H)):
        rnd = random.Random(seed)
        self.p = [(rnd.uniform(0, 1), rnd.uniform(0, 1), rnd.uniform(22, 55),
                   rnd.uniform(0, 6.28), rnd.choice([1, 1, 2])) for _ in range(n)]
        self.region = region

    def draw(self, canvas, t, density=1.0, alpha=255):
        x0, y0, x1, y1 = self.region
        d = ImageDraw.Draw(canvas)
        n = int(len(self.p) * clamp01(density))
        for (u, v, spd, ph, sz) in self.p[:n]:
            y = y0 + ((v * (y1 - y0) + t * spd) % (y1 - y0))
            x = x0 + ((u * (x1 - x0) + math.sin(t * 1.8 + ph) * 10) % (x1 - x0))
            d.ellipse([int(x), int(y), int(x) + sz, int(y) + sz], fill=(240, 246, 255, alpha))


class Stars:
    def __init__(self, n=120, seed=3, region=(0, 0, W, H)):
        rnd = random.Random(seed)
        self.p = [(rnd.randint(region[0], region[2] - 1), rnd.randint(region[1], region[3] - 1),
                   rnd.uniform(0, 6.28), rnd.choice([1, 1, 1, 2])) for _ in range(n)]

    def draw(self, canvas, t, alpha=1.0):
        d = ImageDraw.Draw(canvas)
        for (x, y, ph, sz) in self.p:
            tw = 0.55 + 0.45 * math.sin(t * 2.4 + ph)
            a = int(255 * alpha * tw)
            d.ellipse([x, y, x + sz, y + sz], fill=(245, 242, 220, a))


class Confetti:
    COLORS = [GOLD, CYAN, PINK, GREEN, VIOLET, CREAM]

    def __init__(self, n=90, seed=5):
        rnd = random.Random(seed)
        self.p = [(rnd.uniform(0, W), rnd.uniform(-H, 0), rnd.uniform(35, 75),
                   rnd.uniform(0, 6.28), rnd.choice(self.COLORS)) for _ in range(n)]

    def draw(self, canvas, t):
        d = ImageDraw.Draw(canvas)
        for (x0, y0, spd, ph, col) in self.p:
            y = (y0 + t * spd) % (H + 20) - 10
            x = (x0 + math.sin(t * 3 + ph) * 14) % W
            d.ellipse([int(x), int(y), int(x) + 3, int(y) + 2], fill=(*col, 255))


def flush_person_cards(canvas):
    q = getattr(canvas, "_deferred_person_cards", None)
    if q:
        canvas._deferred_person_cards = []
        for fn_pc in q:
            fn_pc(canvas)
    return canvas


@lru_cache(maxsize=4)
def _build_smooth_vignette(w, h, strength):
    y = np.linspace(-1.0, 1.0, h, dtype=np.float32)[:, None]
    x = np.linspace(-1.0, 1.0, w, dtype=np.float32)[None, :]
    r2 = x * x * 0.75 + y * y * 1.05
    alpha = np.clip((r2 - 0.35) * strength * 240.0, 0, 185).astype(np.uint8)
    z = np.zeros((h, w, 4), dtype=np.uint8)
    z[..., 3] = alpha
    return Image.fromarray(z, "RGBA")


def vignette(canvas, strength=0.32):
    flush_person_cards(canvas)
    if strength <= 0:
        return canvas
    ov = _build_smooth_vignette(canvas.size[0], canvas.size[1], round(float(strength), 2))
    canvas.alpha_composite(ov)
    return canvas
