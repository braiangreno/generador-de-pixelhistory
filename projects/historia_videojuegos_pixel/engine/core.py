"""Motor de render del video en pixel art: lienzo 480x270, texto con fuentes
bitmap, ventanas estilo RPG, partículas y transiciones con dithering."""
import math
import os
import random
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from i18n import tr

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 480, 270
FPS = 30

GOLD = (233, 194, 122)
GOLD_D = (168, 112, 52)
CREAM = (245, 242, 235)
CYAN = (90, 220, 255)
NAVY = (27, 31, 59)
INK = (14, 12, 24)
GREY = (168, 174, 184)

FONTS = {
    "press": os.path.join(ROOT, "fonts", "PressStart2P-Regular.ttf"),
    "silk": os.path.join(ROOT, "fonts", "Silkscreen-Regular.ttf"),
    "silkb": os.path.join(ROOT, "fonts", "Silkscreen-Bold.ttf"),
}


def ease_out(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def ease_in_out(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def ease_out_back(t, s=1.70158):
    t = max(0.0, min(1.0, t)) - 1
    return t * t * ((s + 1) * t + s) + 1


def clamp01(x):
    return max(0.0, min(1.0, x))


def prog(t, a, b):
    """Progreso 0..1 de t entre a y b."""
    if b <= a:
        return 1.0 if t >= b else 0.0
    return clamp01((t - a) / (b - a))


@lru_cache(maxsize=64)
def font(name, size):
    return ImageFont.truetype(FONTS[name], size)


@lru_cache(maxsize=None)
def load_rgba(path):
    return Image.open(os.path.join(ROOT, path)).convert("RGBA")


def bg(name):
    return load_rgba(f"assets/bg/{name}.png")


def portrait(name):
    return load_rgba(f"assets/portraits/{name}.png")


# --------------------------------------------------------------------------- texto

ACCENT_INFO = {
    "Á": ("A", "acute"), "É": ("E", "acute"), "Í": ("I", "acute"), "Ó": ("O", "acute"), "Ú": ("U", "acute"),
    "À": ("A", "grave"),
    "Â": ("A", "circ"), "Ê": ("E", "circ"), "Ô": ("O", "circ"),
    "Ã": ("A", "tilde"), "Õ": ("O", "tilde"), "Ñ": ("N", "tilde"),
}


def top_pad(fname, size):
    return (size // 8) * 3 if fname == "press" else 0


@lru_cache(maxsize=2048)
def text_mask(text, fname, size):
    f = font(fname, size)
    # Press Start 2P dibuja las mayúsculas acentuadas como minúsculas: las componemos
    accents = []
    if fname == "press":
        chars = []
        for i, ch in enumerate(text):
            if ch in ACCENT_INFO:
                base, kind = ACCENT_INFO[ch]
                accents.append((i, kind))
                chars.append(base)
            else:
                chars.append(ch)
        text = "".join(chars)
    P = top_pad(fname, size)
    bbox = f.getbbox(text)
    w = max(1, bbox[2] - min(0, bbox[0]) + 2)
    h = max(1, size + size // 2 + 2 + P)
    img = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(img)
    d.fontmode = "1"
    ox, oy = 1 - min(0, bbox[0]), 1 + P
    d.text((ox, oy), text, font=f, fill=255)
    u = max(1, size // 8)
    for i, kind in accents:
        x = ox + i * size
        if kind == "acute":
            d.rectangle([x + 4 * u, oy - 2 * u, x + 6 * u - 1, oy - u - 1], fill=255)
            d.rectangle([x + 3 * u, oy - u, x + 5 * u - 1, oy - 1], fill=255)
        elif kind == "grave":
            d.rectangle([x + 2 * u, oy - 2 * u, x + 4 * u - 1, oy - u - 1], fill=255)
            d.rectangle([x + 3 * u, oy - u, x + 5 * u - 1, oy - 1], fill=255)
        elif kind == "circ":
            d.rectangle([x + 3 * u, oy - 2 * u, x + 5 * u - 1, oy - u - 1], fill=255)
            d.rectangle([x + 2 * u, oy - u, x + 3 * u - 1, oy - 1], fill=255)
            d.rectangle([x + 5 * u, oy - u, x + 6 * u - 1, oy - 1], fill=255)
        elif kind == "tilde":
            d.rectangle([x + 2 * u, oy - 2 * u, x + 4 * u - 1, oy - u - 1], fill=255)
            d.rectangle([x + 3 * u, oy - u, x + 5 * u - 1, oy - 1], fill=255)
            d.rectangle([x + 5 * u, oy - 2 * u, x + 6 * u - 1, oy - u - 1], fill=255)
    a = np.array(img) > 127
    ys = np.where(a.any(axis=1))[0]
    if len(ys) == 0:
        return np.zeros((size, max(1, w)), dtype=bool), 0
    return a[:ys.max() + 1, :], ys.min()


def text_size(text, fname="press", size=8):
    text = tr(text, fname)
    m, _ = text_mask(text, fname, size)
    return m.shape[1], m.shape[0] - top_pad(fname, size)


def dilate(mask, r=1, diag=True):
    out = mask.copy()
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            if not diag and abs(dx) + abs(dy) > r:
                continue
            out |= np.roll(np.roll(mask, dy, 0), dx, 1)
    return out


@lru_cache(maxsize=1024)
def render_text(text, fname="press", size=8, color=CREAM, outline=INK, shadow=True,
                gradient=None, outline_w=1):
    """Devuelve una imagen RGBA con el texto pixelado, contorno y sombra."""
    m, _ = text_mask(text, fname, size)
    pad = outline_w + 2
    h, w = m.shape
    M = np.zeros((h + pad * 2, w + pad * 2), dtype=bool)
    M[pad:pad + h, pad:pad + w] = m
    out = np.zeros(M.shape + (4,), dtype=np.uint8)
    if shadow:
        sh = dilate(M, outline_w) if outline else M
        sh = np.roll(np.roll(sh, 2 if size >= 16 else 1, 0), 2 if size >= 16 else 1, 1)
        out[sh] = (0, 0, 0, 150)
    if outline:
        ol = dilate(M, outline_w)
        out[ol] = (*outline, 255)
    if gradient:
        ys = np.arange(M.shape[0])
        rows = np.where(M.any(axis=1))[0]
        y0, y1 = rows.min(), rows.max()
        for y in range(y0, y1 + 1):
            k = (y - y0) / max(1, (y1 - y0))
            # rampa de 4 bandas (look 16 bits)
            band = min(len(gradient) - 1, int(k * len(gradient)))
            c = gradient[band]
            out[y][M[y]] = (*c, 255)
    else:
        out[M] = (*color, 255)
    return Image.fromarray(out, "RGBA")


GOLD_RAMP = [(255, 240, 190), (246, 214, 140), (233, 186, 98), (196, 136, 62), (150, 96, 44)]
ICE_RAMP = [(240, 250, 255), (200, 230, 250), (150, 200, 235), (110, 160, 210), (80, 120, 180)]
CYAN_RAMP = [(200, 250, 255), (120, 230, 255), (70, 200, 245), (40, 150, 220)]
CREAM_RAMP = [(255, 255, 250), (245, 242, 235), (220, 214, 200), (190, 180, 165)]


def draw_text(canvas, text, x, y, fname="press", size=8, color=CREAM, align="left", outline=INK,
              shadow=True, gradient=None, reveal=None, alpha=1.0, outline_w=1):
    """Dibuja texto. reveal = cantidad de caracteres visibles (efecto máquina de escribir)."""
    orig_len = len(text) if isinstance(text, str) else 0
    text = tr(text, fname)
    if reveal is not None:
        if orig_len > 0 and len(text) != orig_len:
            reveal = reveal * len(text) / orig_len
        n = int(reveal)
        if n <= 0:
            return
        shown = text[:n]
    else:
        shown = text
    img = render_text(shown, fname, size, tuple(color), tuple(outline) if outline else None, shadow,
                      tuple(map(tuple, gradient)) if gradient else None, outline_w)
    pad = outline_w + 2
    tw = img.size[0] - pad * 2
    if align == "center":
        x0 = x - tw // 2
    elif align == "right":
        x0 = x - tw
    else:
        x0 = x
    paste(canvas, img, int(x0) - pad, int(y) - pad - top_pad(fname, size), alpha)


def paste(canvas, img, x, y, alpha=1.0):
    if alpha <= 0:
        return
    if alpha < 1.0:
        img = img.copy()
        a = np.array(img)
        # alfa con dithering ordenado para mantener el look pixel
        th = bayer_tile(a.shape[1], a.shape[0])
        a[..., 3] = np.where(th < alpha, a[..., 3], 0)
        img = Image.fromarray(a, "RGBA")
    canvas.alpha_composite(img, (int(x), int(y))) if (0 <= x and 0 <= y and x + img.size[0] <= W and y + img.size[1] <= H) else _paste_clip(canvas, img, int(x), int(y))


def _paste_clip(canvas, img, x, y):
    w, h = img.size
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(canvas.size[0], x + w), min(canvas.size[1], y + h)
    if x1 <= x0 or y1 <= y0:
        return
    crop = img.crop((x0 - x, y0 - y, x1 - x, y1 - y))
    canvas.alpha_composite(crop, (x0, y0))


def paste_arr(canvas, arr, x, y, alpha=1.0):
    paste(canvas, Image.fromarray(arr, "RGBA"), x, y, alpha)


# --------------------------------------------------------------------------- dithering

BAYER4 = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]], dtype=np.float32) / 16.0 + 1 / 32


@lru_cache(maxsize=64)
def bayer_tile(w, h):
    reps = (h // 4 + 1, w // 4 + 1)
    return np.tile(BAYER4, reps)[:h, :w]


def dither_mix(a, b, k):
    """Mezcla dos imágenes RGB(A) con umbral Bayer (transición retro)."""
    if k <= 0:
        return a
    if k >= 1:
        return b
    A = np.array(a)
    B = np.array(b)
    th = bayer_tile(W, H)
    m = th < k
    A[m] = B[m]
    return Image.fromarray(A, a.mode)


def fade_to(canvas, color, k):
    if k <= 0:
        return canvas
    solid = Image.new(canvas.mode, canvas.size, (*color, 255) if canvas.mode == "RGBA" else color)
    return dither_mix(canvas, solid, k)


def grade(img, mul=(1, 1, 1), add=(0, 0, 0), sat=1.0, k=1.0):
    """Corrección de color simple (para día/noche e invierno)."""
    a = np.array(img).astype(np.float32)
    rgb = a[..., :3]
    lum = (rgb * np.array([0.299, 0.587, 0.114])).sum(-1, keepdims=True)
    g = lum + (rgb - lum) * sat
    g = g * np.array(mul) + np.array(add)
    out = rgb + (g - rgb) * k
    a[..., :3] = np.clip(out, 0, 255)
    return Image.fromarray(a.astype(np.uint8), img.mode)


def posterize_palette(img, levels=6):
    a = np.array(img).astype(np.int32)
    step = 256 // levels
    a[..., :3] = (a[..., :3] // step) * step + step // 2
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), img.mode)


# --------------------------------------------------------------------------- UI RPG

def window(canvas, x, y, w, h, fill=(20, 24, 52), border=GOLD, alpha=0.92, inner=(60, 70, 130)):
    """Ventana estilo RPG 16 bits con borde doble y esquinas recortadas."""
    if border is None:
        border = GOLD
    a = np.zeros((h, w, 4), dtype=np.uint8)
    a[..., :3] = fill
    a[..., 3] = int(255 * alpha)
    # gradiente vertical sutil por bandas
    for yy in range(h):
        band = yy * 4 // max(1, h)
        a[yy, :, :3] = np.clip(np.array(fill) + band * 4, 0, 255)
    a[0, :, :3] = INK; a[-1, :, :3] = INK; a[:, 0, :3] = INK; a[:, -1, :3] = INK
    a[0, :, 3] = a[-1, :, 3] = a[:, 0, 3] = a[:, -1, 3] = 255
    a[1, 1:-1, :3] = border; a[-2, 1:-1, :3] = shade(border, 0.6)
    a[1:-1, 1, :3] = border; a[1:-1, -2, :3] = shade(border, 0.6)
    a[2, 2:-2, :3] = inner; a[2:-2, 2, :3] = inner
    for (cy, cx) in ((0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)):
        a[cy, cx, 3] = 0
    paste(canvas, Image.fromarray(a, "RGBA"), x, y)


def shade(c, f):
    return tuple(int(max(0, min(255, v * f))) for v in c)


def portrait_card(canvas, name, x, y, alpha=1.0, frame=GOLD):
    p = portrait(name)
    window(canvas, x - 4, y - 4, p.size[0] + 8, p.size[1] + 8, border=frame)
    paste(canvas, p, x, y, alpha)


def bubble(canvas, text, x, y, size=8, fname="press", tail="down", reveal=None, color=INK,
           fill=(250, 248, 240), tail_x=None):
    """Globo de diálogo pixelado. (x, y) = punta de la cola."""
    if reveal is not None and int(reveal) <= 0:
        return
    tw, th = text_size(text, fname, size)
    bw, bh = tw + 12, th + 10
    bx = int(x - bw // 2)
    by = int(y - bh - 6) if tail == "down" else int(y + 6)
    bx = max(2, min(W - bw - 2, bx))
    a = np.zeros((bh, bw, 4), dtype=np.uint8)
    a[..., :3] = fill; a[..., 3] = 255
    a[0, :, :3] = INK; a[-1, :, :3] = INK; a[:, 0, :3] = INK; a[:, -1, :3] = INK
    for (cy, cx) in ((0, 0), (0, bw - 1), (bh - 1, 0), (bh - 1, bw - 1)):
        a[cy, cx, 3] = 0
    a[-2, 1:-1, :3] = shade(fill, 0.85)
    paste(canvas, Image.fromarray(a, "RGBA"), bx, by)
    d = ImageDraw.Draw(canvas)
    tx = int(x)
    if tail == "down":
        for i in range(5):
            d.line([(tx - 2 + i // 2, by + bh - 1 + i), (tx + 2 - i, by + bh - 1 + i)], fill=(*fill, 255))
            d.point((tx - 3 + i // 2, by + bh - 1 + i), fill=(*INK, 255))
            d.point((tx + 3 - i, by + bh - 1 + i), fill=(*INK, 255))
    draw_text(canvas, text, bx + bw // 2, by + 5, fname, size, color, align="center", outline=None, shadow=False, reveal=reveal)


# --------------------------------------------------------------------------- partículas

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
            d.line([(int(x), int(y)), (int(x - 1), int(y - 4 * s))], fill=(*self.color, alpha))


class Snow:
    def __init__(self, n=220, seed=2, speed=22):
        rnd = random.Random(seed)
        self.p = [(rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(0.5, 1.6), rnd.uniform(0, 6.28)) for _ in range(n)]
        self.speed = speed

    def draw(self, canvas, t, density=1.0, alpha=255):
        d = ImageDraw.Draw(canvas)
        n = int(len(self.p) * clamp01(density))
        for (x, y, s, ph) in self.p[:n]:
            yy = (y + t * self.speed * s) % (H + 10) - 5
            xx = (x + math.sin(t * 1.3 + ph) * 6 * s + t * 6) % W
            c = (240, 248, 255, alpha) if s > 1.0 else (200, 220, 240, alpha)
            if s > 1.3:
                d.rectangle([int(xx), int(yy), int(xx) + 1, int(yy) + 1], fill=c)
            else:
                d.point((int(xx), int(yy)), fill=c)


class Stars:
    def __init__(self, n=120, seed=3, region=(0, 0, W, H)):
        rnd = random.Random(seed)
        x0, y0, x1, y1 = region
        self.p = [(rnd.randint(x0, x1 - 1), rnd.randint(y0, y1 - 1), rnd.uniform(0, 6.28), rnd.random()) for _ in range(n)]

    def draw(self, canvas, t, alpha=1.0):
        d = ImageDraw.Draw(canvas)
        for (x, y, ph, b) in self.p:
            k = 0.5 + 0.5 * math.sin(t * (1.5 + b * 2) + ph)
            v = int((90 + 165 * k * b) * alpha)
            if b > 0.92 and k > 0.6:
                c = (v, v, min(255, v + 20), 255)
                d.point((x - 1, y), fill=c); d.point((x + 1, y), fill=c)
                d.point((x, y - 1), fill=c); d.point((x, y + 1), fill=c)
            d.point((x, y), fill=(v, v, min(255, v + 30), 255))


class Confetti:
    COLORS = [GOLD, CYAN, (255, 110, 130), (140, 255, 150), CREAM]

    def __init__(self, n=90, seed=5):
        rnd = random.Random(seed)
        self.p = [(rnd.uniform(0, W), rnd.uniform(-H, 0), rnd.uniform(30, 70), rnd.uniform(0, 6.28),
                   rnd.choice(self.COLORS)) for _ in range(n)]

    def draw(self, canvas, t):
        d = ImageDraw.Draw(canvas)
        for (x, y, sp, ph, c) in self.p:
            yy = y + t * sp
            if yy < -4 or yy > H:
                continue
            xx = x + math.sin(t * 3 + ph) * 8
            if int(t * 8 + ph) % 2:
                d.rectangle([int(xx), int(yy), int(xx) + 1, int(yy)], fill=(*c, 255))
            else:
                d.rectangle([int(xx), int(yy), int(xx), int(yy) + 1], fill=(*c, 255))


def sparkle(canvas, x, y, t, size=3, color=CREAM):
    d = ImageDraw.Draw(canvas)
    k = abs(math.sin(t * 6))
    s = max(1, int(size * k))
    c = (*color, 255)
    d.line([(x - s, y), (x + s, y)], fill=c)
    d.line([(x, y - s), (x, y + s)], fill=c)


def shadow_ellipse(canvas, cx, cy, w=16, h=3, alpha=90):
    d = ImageDraw.Draw(canvas)
    d.ellipse([cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2], fill=(0, 0, 0, alpha))


def vignette(canvas, strength=0.35):
    return _vignette(canvas, strength)


@lru_cache(maxsize=4)
def _vig_mask(strength):
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    m = np.clip((d - 0.75) / 0.6, 0, 1) * strength
    # cuantizamos con Bayer para que siga siendo pixel art
    th = bayer_tile(W, H)
    return (th < m)


def _vignette(canvas, strength):
    a = np.array(canvas)
    m = _vig_mask(strength)
    a[m, :3] = (a[m, :3] * 0.55).astype(np.uint8)
    return Image.fromarray(a, canvas.mode)


def new_canvas(color=(0, 0, 0)):
    return Image.new("RGBA", (W, H), (*color, 255))


def vgradient(top, bottom, bands=12):
    a = np.zeros((H, W, 4), dtype=np.uint8)
    for y in range(H):
        k = int(y / H * bands) / bands
        a[y, :, :3] = [int(t + (b - t) * k) for t, b in zip(top, bottom)]
    a[..., 3] = 255
    return Image.fromarray(a, "RGBA")
