"""Helpers compartidos por todas las escenas (personajes, UI, efectos, camara)."""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import *  # noqa
import sprites as S
from timeline import TL

FEET_OFFSET = 50  # fila de los pies dentro del sprite

# =========================================================================== helpers

def talk_v(t, on=True):
    return [0, 1, 2, 1][int(t * 11) % 4] if on else 0


def upscale(arr, k):
    k = int(k)
    if k <= 1:
        return arr
    return np.repeat(np.repeat(arr, k, axis=0), k, axis=1)


def char(cv, key, x, feet, t, alpha=1.0, shadow=True, scale=1, **pose):
    """Dibuja un personaje con los pies en (x, feet). scale = 1, 2 o 3 (píxeles enteros)."""
    spec = S.CAST[key] if isinstance(key, str) else key  # clave del reparto o dict propio
    arr = upscale(S.render(spec, t, **pose), scale)
    if shadow and alpha > 0.3:
        shadow_ellipse(cv, int(x), int(feet), 18 * scale, 4 * scale, 80)
    paste_arr(cv, arr, int(x) - S.SW * scale // 2, int(feet) - FEET_OFFSET * scale, alpha)


def floor_prop(cv, fn_draw, x, feet=250):
    """Dibuja un objeto apoyado sobre el piso (mesas con velas, mascotas, maletas, podios)
    en (x, feet) en 16:9 y sobre el suelo vertical (vfeet=452) en 9:16 para que jamás flote."""
    vctx = getattr(sys.modules.get("core"), "_VCTX", None)
    if vctx is not None and isinstance(cv, Image.Image) and cv.size == (W, H):
        vctx.chars.append({
            "kind": "prop",
            "fn": fn_draw,
            "x": x,
            "feet": feet,
            "scale": 1,
        })
        return
    fn_draw(cv, int(x), int(feet))


def pace(t, t0, x_a, x_b, period=3.6, pause=0.28):
    """Hace que un personaje camine con ritmo entre x_a y x_b, deteniéndose brevemente en cada extremo.
    Devuelve (x, walk_phase, look_dir)."""
    if t <= t0:
        return x_a, None, (1 if x_b >= x_a else -1)
    dt = t - t0
    leg = (dt / period) % 2.0
    going_b = leg < 1.0
    u_raw = leg if going_b else (leg - 1.0)
    move_frac = max(0.2, 1.0 - pause)
    if u_raw < move_frac:
        p = ease_in_out(u_raw / move_frac)
        x = (x_a + (x_b - x_a) * p) if going_b else (x_b + (x_a - x_b) * p)
        wph = (t * 3.4) % 1.0
        look = (1 if x_b >= x_a else -1) if going_b else (-1 if x_b >= x_a else 1)
        return x, wph, look
    else:
        x = x_b if going_b else x_a
        # Al detenerse en el extremo, mira hacia el centro de la escena (x=240)
        look = 1 if x < 240 else -1
        return x, None, look


def silhouette(cv, key, x, feet, t, color=(12, 10, 22), scale=1, **pose):
    spec = S.CAST[key] if isinstance(key, str) else key
    arr = S.render(spec, t, **pose).copy()
    m = arr[..., 3] > 0
    arr[m, :3] = color
    arr = upscale(arr, scale)
    paste_arr(cv, arr, int(x) - S.SW * scale // 2, int(feet) - FEET_OFFSET * scale)


def robot(cv, x, feet, t, face="happy", frozen=False, alpha=1.0, sil=False, scale=1):
    """Desactivado en Dune: el robot retro pertenece únicamente al documental de IA."""
    return


# --------------------------------------------------------------------------- cámara
# Cada escena puede definir una cámara: (zoom, cx, cy) en coordenadas del lienzo 480x270.
# El zoom se aplica al escalar a 1080p, por eso es suave y no rompe el pixel art.

def cam_push(t, t0, t1, z0=1.0, z1=1.12, c0=(240, 135), c1=None):
    """Acercamiento lento (Ken Burns) entre t0 y t1."""
    p = ease_in_out(prog(t, t0, t1))
    c1 = c1 or c0
    return (z0 + (z1 - z0) * p, c0[0] + (c1[0] - c0[0]) * p, c0[1] + (c1[1] - c0[1]) * p)


def cam_punch(t, beats, amp=0.06, dur=0.35):
    """Pequeño golpe de zoom en cada instante de `beats` (para dar ritmo). Devuelve zoom extra."""
    z = 0.0
    for b in beats:
        if b <= t < b + dur:
            z = max(z, amp * (1 - (t - b) / dur) ** 2)
    return z


def apply_cam(img, cam):
    """Devuelve el fotograma final 1920x1080 aplicando la cámara (zoom, cx, cy) sin cortar los carteles superiores."""
    if not cam or abs(cam[0] - 1.0) < 1e-3:
        return img.resize((1920, 1080), Image.NEAREST)
    z, cx, cy = cam
    z = min(1.035, max(1.0, z))
    w, h = W / z, H / z
    x0 = min(max(0, cx - w / 2), W - w)
    y0 = min(4.0, max(0, cy - h / 2), H - h)
    return img.resize((1920, 1080), Image.NEAREST, box=(x0, y0, x0 + w, y0 + h))


def walk(t, t0, t1, x0, x1):
    p = prog(t, t0, t1)
    x = x0 + (x1 - x0) * ease_in_out(p)
    return x, ((t * 3.2) % 1.0 if 0 < p < 1 else None)


def pop(t, t0, dur=0.35):
    """Devuelve (alpha, dy) para una aparición con rebote."""
    p = prog(t, t0, t0 + dur)
    if p <= 0:
        return 0.0, 0
    return min(1.0, p * 2), int(round((1 - ease_out_back(p)) * -10))


def bigyear(cv, text, cx, y, t, t0, size=48, ramp=GOLD_RAMP):
    p = prog(t, t0, t0 + 0.55)
    if p <= 0:
        return
    yy = y - (1 - ease_out_back(p, 2.2)) * 50
    draw_text(cv, text, cx, int(yy), "press", size, align="center", gradient=ramp, outline_w=2,
              alpha=min(1, p * 3))
    if p >= 1:
        tw, _ = text_size(text, "press", size)
        for i, ph in enumerate((0.0, 1.7, 3.1)):
            sx = cx - tw // 2 + int((i + 0.5) * tw / 3)
            sparkle(cv, sx + (i * 7) % 11, y + 4 + (i * 13) % size, t + ph, 3)


def lower_third(cv, title, sub, t, t0, t1, x=16, y=222):
    a = prog(t, t0, t0 + 0.4) * (1 - prog(t, t1 - 0.4, t1))
    if a <= 0:
        return
    p_in = ease_out(prog(t, t0, t0 + 0.45))
    dy = int(round((1 - p_in) * 10))
    x = max(24, x)
    y = min(214, y)
    tw, _ = text_size(title, "press", 16)
    sw, _ = text_size(sub, "silk", 8)
    ww = max(tw, sw) + 22
    if x - 8 + ww > W - 16:
        x = max(16, W - 16 - ww + 8)
    window(cv, x - 8, y - 8 + dy, ww, 48, alpha=0.88 * a)
    ImageDraw.Draw(cv).rectangle([x, y - 2 + dy, x + int(24 * ease_out(prog(t, t0, t0 + 0.6))), y - 1 + dy],
                                 fill=(*GOLD, int(255 * a)))
    draw_text(cv, title, x, y + 4 + dy, "press", 16, CREAM, alpha=a)
    draw_text(cv, sub, x + 1, y + 24 + dy, "silk", 8, GREY, alpha=a)


def draw_sun(cv, cx, cy, r, t, face=True, alpha=255):
    d = ImageDraw.Draw(cv)
    for i in range(12):
        ang = i * math.pi / 6 + t * 0.4
        l0, l1 = r + 3, r + 6 + (2 if i % 2 else 0)
        x0, y0 = cx + math.cos(ang) * l0, cy + math.sin(ang) * l0
        x1, y1 = cx + math.cos(ang) * l1, cy + math.sin(ang) * l1
        d.line([(int(x0), int(y0)), (int(x1), int(y1))], fill=(255, 214, 90, alpha), width=2)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 226, 110, alpha), outline=(214, 140, 40, alpha))
    d.ellipse([cx - r + 3, cy - r + 3, cx - r // 3, cy - r // 3], fill=(255, 246, 190, alpha))
    if face:
        d.rectangle([cx - 5, cy - 3, cx - 4, cy - 1], fill=(120, 60, 20, alpha))
        d.rectangle([cx + 4, cy - 3, cx + 5, cy - 1], fill=(120, 60, 20, alpha))
        d.line([(cx - 4, cy + 4), (cx - 2, cy + 6), (cx + 2, cy + 6), (cx + 4, cy + 4)], fill=(120, 60, 20, alpha))


def draw_moon(cv, cx, cy, r=9, alpha=255):
    d = ImageDraw.Draw(cv)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(236, 240, 255, alpha))
    d.ellipse([cx - r + 5, cy - r - 2, cx + r + 5, cy + r - 2], fill=(0, 0, 0, 0))


def draw_paper(cv, x, y, w, h, color=(246, 240, 222)):
    d = ImageDraw.Draw(cv)
    d.rectangle([x + 3, y + 3, x + w + 3, y + h + 3], fill=(0, 0, 0, 110))
    d.rectangle([x, y, x + w, y + h], fill=(*color, 255), outline=(*INK, 255))
    d.line([(x + w - 1, y + 1), (x + w - 1, y + h - 1)], fill=(*shade(color, 0.85), 255))
    d.line([(x + 1, y + h - 1), (x + w - 1, y + h - 1)], fill=(*shade(color, 0.85), 255))


def scribble(cv, x, y, w, p, seed, color=(30, 40, 110)):
    """Firma manuscrita que se dibuja progresivamente (p 0..1)."""
    d = ImageDraw.Draw(cv)
    n = int(w * p)
    prev = None
    for i in range(n):
        yy = y + math.sin(i * 0.9 + seed) * 2.5 + math.sin(i * 0.37 + seed * 2) * 1.5
        pt = (x + i, int(yy))
        if prev:
            d.line([prev, pt], fill=(*color, 255))
        prev = pt


def bulb(cv, cx, cy, t, on=1.0, cord_top=None):
    d = ImageDraw.Draw(cv)
    if cord_top is not None and cy - 9 > cord_top:
        d.line([(cx, int(cord_top)), (cx, cy - 9)], fill=(*INK, 255), width=2)
        d.rectangle([cx - 3, cy - 10, cx + 3, cy - 6], fill=(140, 140, 152, 255), outline=(*INK, 255))
    if on > 0:
        glow(cv, cx, cy, 14, (255, 240, 140), 0.45 * on)
    d.ellipse([cx - 6, cy - 7, cx + 6, cy + 5], fill=(255, 240, 150, 255) if on > 0.5 else (200, 200, 190, 255),
              outline=(*INK, 255))
    d.rectangle([cx - 3, cy + 5, cx + 3, cy + 9], fill=(160, 160, 170, 255), outline=(*INK, 255))
    d.point((cx - 3, cy - 4), fill=(255, 255, 255, 255))


def spotlight(cv, cx, top, bottom, w_top, w_bot, color=(120, 220, 255), strength=0.22):
    a = np.array(cv)
    th = bayer_tile(W, H)
    for y in range(max(0, top), min(H, bottom)):
        k = (y - top) / max(1, bottom - top)
        half = (w_top + (w_bot - w_top) * k) / 2
        x0, x1 = int(max(0, cx - half)), int(min(W, cx + half))
        if x1 <= x0:
            continue
        m = th[y, x0:x1] < strength * (1 - 0.3 * k)
        row = a[y, x0:x1, :3].astype(np.int32)
        row[m] = (row[m] * 0.4 + np.array(color) * 0.6).astype(np.int32)
        a[y, x0:x1, :3] = row
    return Image.fromarray(a, "RGBA")


def orb(cv, cx, cy, t, on):
    if on <= 0:
        return
    d = ImageDraw.Draw(cv)
    r = 3 + int(on * 1)
    pulse = 0.5 + 0.5 * math.sin(t * 4 + cx)
    d.ellipse([cx - r - 3, cy - r - 3, cx + r + 3, cy + r + 3], fill=(90, 220, 255, int(60 * on * pulse)))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 230, 255, 255), outline=(30, 110, 160, 255))
    d.point((cx - 1, cy - 1), fill=(240, 255, 255, 255))


def terminal(cv, x, y, t, on=True):
    """Terminal CRT de 30x24."""
    d = ImageDraw.Draw(cv)
    d.rectangle([x, y, x + 30, y + 22], fill=(214, 204, 178, 255), outline=(*INK, 255))
    d.rectangle([x + 3, y + 3, x + 27, y + 17], fill=(14, 40, 26, 255))
    if on:
        for i in range(3):
            ll = 6 + ((i * 7 + int(t * 3)) % 14)
            d.line([(x + 5, y + 6 + i * 4), (x + 5 + ll, y + 6 + i * 4)], fill=(100, 250, 150, 255))
        if int(t * 3) % 2:
            d.rectangle([x + 5, y + 14, x + 7, y + 15], fill=(100, 250, 150, 255))
    d.rectangle([x + 10, y + 23, x + 20, y + 26], fill=(150, 140, 120, 255), outline=(*INK, 255))


def desk(cv, x0, x1, top, bottom, color=(110, 72, 44)):
    d = ImageDraw.Draw(cv)
    d.rectangle([x0, top, x1, bottom], fill=(*color, 255), outline=(*INK, 255))
    d.line([(x0 + 1, top + 1), (x1 - 1, top + 1)], fill=(*shade(color, 1.35), 255))
    d.line([(x0 + 1, top + 4), (x1 - 1, top + 4)], fill=(*shade(color, 0.7), 255))
    for xx in range(x0 + 12, x1 - 6, 24):
        d.rectangle([xx, top + 8, xx + 10, top + 12], fill=(*shade(color, 0.8), 255), outline=(*shade(color, 0.5), 255))


def quest_window(cv, lines, x, y, t, t0, w=210):
    a = prog(t, t0, t0 + 0.3)
    if a <= 0:
        return
    if lines:
        max_tw = max(text_size(txt, "press", 8)[0] for txt, _ in lines)
        w = max(w, max_tw + 18)
        x = min(x, W - w - 6)
    h = 14 + 12 * len(lines)
    window(cv, x, y, w, h)
    for i, (txt, col) in enumerate(lines):
        draw_text(cv, txt, x + 8, y + 8 + i * 12, "press", 8, col)


def shake(t, t0, dur=0.25, amp=3):
    if t0 <= t < t0 + dur:
        k = 1 - (t - t0) / dur
        return int(round(math.sin(t * 90) * amp * k)), int(round(math.cos(t * 77) * amp * k))
    return 0, 0


def offset_canvas(cv, dx, dy, fill=(0, 0, 0)):
    if dx == 0 and dy == 0:
        return cv
    out = Image.new("RGBA", cv.size, (*fill, 255))
    out.paste(cv, (dx, dy))
    return out


def sky_cycle(phase):
    """phase 0..1 -> nivel de noche 0..1 (0 = mediodía)."""
    return 0.5 - 0.5 * math.cos(phase * 2 * math.pi)


def bars70(cv, lit, t, y=252, x0=30, alpha=1.0, cur_glow=True):
    d = ImageDraw.Draw(cv)
    d.rectangle([x0 - 6, y - 5, x0 + 70 * 6 + 2, y + 15], fill=(10, 10, 20, int(190 * alpha)))
    for i in range(70):
        x = x0 + i * 6
        if i < lit:
            c = (255, 250, 220) if (i == int(lit) - 1 and cur_glow) else GOLD
            hgt = 10
        else:
            c = (60, 56, 70)
            hgt = 6
        d.rectangle([x, y + 10 - hgt, x + 3, y + 10], fill=(*c, 255))


def chapter_card(cv, t, t0, num, lines, years, ramp_title=CREAM_RAMP):
    open_p = ease_out(prog(t, t0, t0 + 0.35))
    if open_p <= 0:
        return
    # tamaño adaptable para evitar que el texto desborde la caja
    w24 = max(text_size(l, "press", 24)[0] for l in lines) if lines else 0
    size = 24 if (len(lines) == 1 and w24 <= 320) else 16
    max_w = max(text_size(l, "press", size)[0] for l in lines) if lines else 200
    card_w = min(440, max(360, max_w + 48))
    w = int(card_w * open_p)
    h = 124
    window(cv, 240 - w // 2, 68, max(8, w), h)
    if open_p < 1:
        return
    tt = t - t0 - 0.35
    d = ImageDraw.Draw(cv)
    lab = f"CAPÍTULO {num}"
    lw, _ = text_size(lab, "press", 8)
    draw_text(cv, lab, 240, 84, "press", 8, GOLD, align="center", reveal=tt * 30)
    ln = int(min(1, tt * 2) * 50)
    d.line([(240 - lw // 2 - 8 - ln, 87), (240 - lw // 2 - 8, 87)], fill=(*GOLD, 255))
    d.line([(240 + lw // 2 + 8, 87), (240 + lw // 2 + 8 + ln, 87)], fill=(*GOLD, 255))
    for i, line in enumerate(lines):
        yy = 112 if len(lines) == 1 else 104 + i * 22
        draw_text(cv, line, 240, yy, "press", size, align="center", gradient=ramp_title,
                  reveal=(tt - 0.25 - i * 0.4) * 26)
    draw_text(cv, years, 240, 172, "press", 8, CYAN, align="center", reveal=(tt - 0.45) * 45)


STARS = Stars(140, seed=11, region=(0, 0, W, 210))
RAIN = Rain(110, seed=4, region=(192, 8, 428, 142), color=(196, 210, 226), speed=210)
SNOW = Snow(260, seed=8)
CONF = Confetti(110, seed=6)
FOUR = ["mccarthy", "minsky", "shannon", "rochester"]


def scaled(cv, fn, w, h, x, y, k=2):
    """Dibuja con fn(img) en un lienzo chico (w x h) y lo pega ampliado x k (pixel art)."""
    tmp = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    fn(tmp)
    a = upscale(np.array(tmp), k)
    paste_arr(cv, a, x, y)


# --------------------------------------------------------------------------- placas de capítulo

CARD_YEARS = {}


def draw_sand_ripple(cv, t, y_base=248, x_start=10, x_end=470, progress=None,
                     color=(238, 194, 110), highlight=(255, 232, 168), shadow=(138, 96, 42)):
    """Brisa de arena suave al ras del suelo (sin forma de gusano), usada solo en desierto."""
    d = ImageDraw.Draw(cv)
    span = max(1, x_end - x_start)
    for i in range(18):
        speed = 54 + (i % 4) * 18
        gx = x_start + int((i * 37 + t * speed) % span)
        gy = y_base - 6 + int(round(math.sin(t * 3.5 + i * 0.9) * 4))
        col_g = highlight if i % 3 == 0 else color
        d.line([(gx, gy), (min(x_end, gx + 5 + (i % 3) * 2), gy)], fill=(*col_g, 165), width=1)


def draw_sand_wind(cv, t, density=42, color=(238, 202, 132), y_min=20, y_max=265):
    """Granos de arena llevados por el viento de izquierda a derecha."""
    d = ImageDraw.Draw(cv)
    for i in range(density):
        speed = 46 + (i % 5) * 16
        x = int((i * 47 + t * speed) % W)
        y = y_min + int((i * 29 + math.sin(t * 2.5 + i) * 5) % max(1, (y_max - y_min)))
        a = 115 + (i % 4) * 32
        d.rectangle([x, y, x + (1 if i % 3 else 2), y], fill=(*color, a))


def draw_phosphor_dot(cv, x, y, r=3, trail=None, color=(245, 200, 110)):
    """Punto luminoso cálido (ámbar/arena) para indicadores y destellos."""
    d = ImageDraw.Draw(cv)
    if trail:
        for i, (tx, ty) in enumerate(trail):
            tr = max(1, r - 1)
            d.rectangle([int(tx) - tr, int(ty) - tr, int(tx) + tr, int(ty) + tr], fill=(*color, 255))
    glow(cv, int(x), int(y), r + 6, color, 0.45)
    d.rectangle([int(x) - r, int(y) - r, int(x) + r, int(y) + r], fill=(255, 245, 215, 255))


def make_card(num, lines, years, snow=False, robot_face="question"):
    """Escena de placa de capítulo clásica de Pixeloide (estilo RPG a pantalla completa)
    con el motivo visual de NVIDIA: el calendario de 30 días arrancando una hoja + placa GPU verde."""
    def sc(t):
        t0 = TL.chapter_start(num) - 0.15
        dt = max(0.0, t - t0)
        # Paleta por acto: Acto 1 (1..2) cálida noventa; Acto 2 (3..5) penumbra verde GPU; Acto 3 (6..7) dorado, (8..9) rojo bolsa
        if num <= 2:
            cv = vgradient((18, 16, 28), (38, 32, 48), 10)
        elif num <= 5:
            cv = vgradient((8, 18, 14), (16, 38, 28), 10)
        elif num <= 7:
            cv = vgradient((22, 16, 10), (46, 34, 18), 10)
        else:
            cv = vgradient((24, 10, 14), (48, 16, 24), 10)
        STARS.draw(cv, t, alpha=0.65)
        d = ImageDraw.Draw(cv)
        d.rectangle([0, 242, W, H], fill=(10, 12, 22, 245))
        # Pistas de circuito verde/dorado/rojo en la parte inferior
        trace_col = STOCK_RED if num >= 8 else (GOLD if num in (6, 7) else GPU_GREEN)
        for i in range(6):
            ty = 208 + i * 5
            d.line([(24, ty), (W - 24, ty)], fill=(*trace_col, 65))
            px = 24 + int(((t * (48 + i * 9) + i * 67) % (W - 48)))
            d.rectangle([px - 3, ty - 1, px + 3, ty + 1], fill=(*trace_col, 220))
        # Calendario de 30 días en los flancos arrancando una hoja en la transición
        tear_p = clamp01((dt - 0.05) / 0.85)
        draw_calendar_30(cv, 38, 62, t, scale=1, tear_p=tear_p, highlight_30=(num in (1, 2, 8, 9)))
        draw_gpu_card(cv, 442, 114, t, scale=1, fan_speed=(0.0 if num == 8 else 12.0), led_col=trace_col)
        chapter_card(cv, t, t0, num, lines, years, ramp_title=GOLD_RAMP)
        return vignette(cv, 0.32)
    return sc


def chapter_end(num):
    """Inicio del capítulo siguiente (o fin del video)."""
    max_ch = max(TL.chapters) if hasattr(TL, "chapters") and TL.chapters else 8
    return TL.chapter_start(num + 1) if num < max_ch else TL.total


# ===========================================================================
# MOTIVOS VISUALES DE «EL DIBUJO QUE ENCENDIÓ EL MUNDO» (NIKOLA TESLA)
# ===========================================================================

AMBER = (255, 196, 92)
AMBER_DIM = (186, 124, 48)
TESLA_VIOLET = (188, 126, 255)
TESLA_CYAN = (108, 236, 255)
TESLA_SPARK = (210, 248, 255)
SOFT_GRAY = (176, 186, 206)
CHALK_WHITE = (242, 244, 236)
CHALK_YELLOW = (252, 224, 126)
CHALK_CYAN = (138, 234, 245)
CHALK_GREEN = (128, 238, 158)
CHALK_RED = (248, 112, 98)
BOARD_GREEN = (20, 48, 34)
BOARD_DARK = (12, 32, 22)
WOOD_FRAME = (112, 72, 38)


def glow(cv, cx, cy, r, color=GOLD, alpha=0.5):
    """Dibuja un resplandor suave concéntrico mezclando RGB con alpha real sobre cv."""
    if r <= 0 or alpha <= 0:
        return
    ov = Image.new("RGBA", cv.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for k, frac in ((1.0, 0.16), (0.68, 0.30), (0.38, 0.48)):
        rk = max(1, int(round(r * k)))
        ak = int(255 * clamp01(alpha * frac))
        d.ellipse([int(cx) - rk, int(cy) - rk, int(cx) + rk, int(cy) + rk], fill=(*color[:3], ak))
    comp = Image.alpha_composite(cv.convert("RGBA"), ov)
    cv.paste(comp, (0, 0))


def tint(cv, color=(10, 14, 24), strength=0.5):
    """Tiñe el lienzo cv hacia color con intensidad strength (0..1)."""
    return fade_to(cv, color, clamp01(strength))


def draw_rotating_arrows(cv, cx, cy, r, t, speed=2.2, color=GOLD, glow=None,
                         progress=1.0, sand_groove=False, alpha=1.0, pulse=None):
    """Dibuja el motivo central del documental: el círculo con cuatro flechas curvas
    (el campo magnético giratorio dibujado en la arena de Budapest)."""
    if progress <= 0 or alpha <= 0:
        return
    if pulse is not None and glow is None:
        glow = color
    d = ImageDraw.Draw(cv)
    ang_base = t * speed
    a_int = int(255 * clamp01(alpha))

    if sand_groove:
        d.ellipse([cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6],
                  fill=(82, 56, 30, int(130 * alpha)), outline=(58, 38, 18, int(190 * alpha)))

    if glow is not None:
        d.ellipse([cx - r - 4, cy - r - 4, cx + r + 4, cy + r + 4],
                  outline=(*glow, int(95 * alpha)), width=3)

    n_arrows = 4
    total_arcs = clamp01(progress) * n_arrows
    for k in range(n_arrows):
        arc_p = clamp01(total_arcs - k)
        if arc_p <= 0:
            continue
        a0 = ang_base + k * (math.pi / 2.0) + 0.16
        a1 = a0 + (math.pi / 2.0 - 0.34) * arc_p
        steps = max(4, int(14 * arc_p))
        pts = []
        for s_i in range(steps + 1):
            aa = a0 + (a1 - a0) * (s_i / float(steps))
            px = int(round(cx + math.cos(aa) * r))
            py = int(round(cy + math.sin(aa) * r))
            pts.append((px, py))
        if len(pts) >= 2:
            # Sombra / surco
            pts_sh = [(px + 1, py + 1) for (px, py) in pts]
            d.line(pts_sh, fill=(*INK, a_int), width=3)
            d.line(pts, fill=(*color, a_int), width=2)
            # Punta de flecha tangencial en el extremo a1
            if arc_p > 0.65:
                tx, ty = pts[-1]
                # Vector tangente en sentido horario (donde aumenta el ángulo)
                tang_x = -math.sin(a1)
                tang_y = math.cos(a1)
                norm_x = -math.cos(a1)
                norm_y = -math.sin(a1)
                head_len = max(4, int(r * 0.24))
                wing = max(3, int(r * 0.16))
                p_tip = (int(round(tx + tang_x * 2)), int(round(ty + tang_y * 2)))
                p_l = (int(round(tx - tang_x * head_len + norm_x * wing)),
                       int(round(ty - tang_y * head_len + norm_y * wing)))
                p_r = (int(round(tx - tang_x * head_len - norm_x * wing)),
                       int(round(ty - tang_y * head_len - norm_y * wing)))
                d.polygon([p_tip, p_l, p_r], fill=(*color, a_int), outline=(*INK, a_int))


def draw_chapter_header(cv, t, t0, ch_num, title_es, place_es=None, border=GOLD):
    """Encabezado superior de capítulo y lugar tipeado con cursor ('Lugares tipeados con cursor')."""
    dt = t - t0
    if dt < -0.35:
        return
    # Ventana superior de capítulo + lugar (compatible 100% con vertical.py y 16:9)
    full_title = f"{ch_num} · {title_es}"
    window(cv, 14, 8, 452, 34 if place_es else 24, fill=(16, 18, 34), border=border, alpha=0.94)
    draw_text(cv, full_title, 240, 12, "press", 8, border, align="center",
              reveal=max(1, int((dt + 0.15) * 38)))
    if place_es:
        rev_p = max(0, int((dt - 0.15) * 28))
        draw_text(cv, place_es, 240, 26, "silk", 8, CREAM, align="center", reveal=rev_p)


def draw_place_only(cv, place_es, t, t0, border=AMBER):
    """Muestra un rótulo de lugar tipeado con cursor en el encabezado superior."""
    if t < t0 - 0.1:
        return
    dt = max(0.0, t - t0)
    window(cv, 20, 8, 440, 22, fill=(16, 18, 34), border=border, alpha=0.92)
    draw_text(cv, place_es, 240, 14, "press", 8, CREAM, align="center", reveal=max(1, int(dt * 26)))


def draw_pizarra_frame(arg1, arg2, arg3=None, arg4=None, summary_es=None, t_summary=None):
    """Crea o dibuja en el lienzo el marco de 'LA PIZARRA': pizarra verde con marco de madera,
    encabezado 'LA PIZARRA · TEMA' y placa final opcional 'EN UNA FRASE'.
    Soporta tanto draw_pizarra_frame(t, t0, topic_es, ...) como draw_pizarra_frame(cv, full_title, t, t0)."""
    is_vert = getattr(sys.modules.get("core"), "_VCTX", None) is not None
    if isinstance(arg1, Image.Image):
        target_cv = arg1
        full_hdr = str(arg2)
        t = float(arg3) if arg3 is not None else 0.0
        t0 = float(arg4) if arg4 is not None else 0.0
        base_cv = vgradient(BOARD_GREEN, BOARD_DARK, 8)
        target_cv.paste(base_cv, (0, 0))
        cv = target_cv
    else:
        t = float(arg1)
        t0 = float(arg2)
        topic_es = str(arg3)
        full_hdr = topic_es if topic_es.startswith("LA PIZARRA") else f"LA PIZARRA · {topic_es}"
        cv = vgradient(BOARD_GREEN, BOARD_DARK, 8)

    if not is_vert:
        d = ImageDraw.Draw(cv)
        # Textura de polvo de tiza sutil y cuadrícula tenue (solo en 16:9; en 9:16 el fondo se genera limpio)
        for gx in range(24, W - 24, 24):
            d.line([(gx, 36), (gx, H - 22)], fill=(28, 62, 44, 90))
        for gy in range(44, H - 22, 24):
            d.line([(24, gy), (W - 24, gy)], fill=(28, 62, 44, 90))
        # Marco de madera alrededor
        d.rectangle([0, 0, W - 1, H - 1], outline=(*WOOD_FRAME, 255), width=4)
        d.rectangle([4, 4, W - 5, H - 5], outline=(*shade(WOOD_FRAME, 0.7), 255), width=2)
        # Bandeja inferior con tizas blancas y amarillas
        d.rectangle([16, H - 12, W - 16, H - 5], fill=(*WOOD_FRAME, 255), outline=(*INK, 255))
        d.rectangle([68, H - 14, 82, H - 12], fill=(*CHALK_WHITE, 255))
        d.rectangle([112, H - 14, 124, H - 12], fill=(*CHALK_YELLOW, 255))

    # Encabezado de La Pizarra
    window(cv, 24, 8, 432, 24, fill=(14, 36, 26), border=CHALK_YELLOW, alpha=0.96, inner=(42, 86, 62))
    draw_text(cv, full_hdr, 240, 15, "press", 8, CHALK_YELLOW, align="center",
              reveal=max(1, int((t - t0 + 0.2) * 36)))

    # Si llegó el momento de 'EN UNA FRASE', dibujar la placa resumen abajo (dentro de x=116..364)
    if summary_es and t_summary is not None and t >= t_summary - 0.1:
        a, dy = pop(t, t_summary - 0.1)
        window(cv, 116, 206 + dy, 248, 44, fill=(16, 40, 28), border=CHALK_WHITE, alpha=0.96, inner=CHALK_YELLOW)
        draw_text(cv, "EN UNA FRASE:", 240, 213 + dy, "silk", 8, CHALK_CYAN, align="center")
        draw_text(cv, summary_es, 240, 229 + dy, "silk", 8, CHALK_YELLOW, align="center",
                  reveal=max(1, int((t - t_summary + 0.15) * 32)))
    return cv


def draw_chalk_hand(cv, x, y, t):
    """Mano genérica en pixel art sosteniendo una tiza blanca que dibuja en la pizarra."""
    d = ImageDraw.Draw(cv)
    jx = int(round(math.sin(t * 14.0) * 2))
    jy = int(round(math.cos(t * 11.0) * 1.5))
    hx, hy = int(x) + jx, int(y) + jy
    # Tiza blanca
    d.rectangle([hx - 6, hy - 2, hx + 2, hy + 1], fill=(*CHALK_WHITE, 255), outline=(*INK, 255))
    # Dedos y dorso de la mano
    skin = (234, 184, 142, 255)
    skin_sh = (196, 144, 104, 255)
    d.rectangle([hx + 1, hy - 4, hx + 11, hy + 5], fill=skin, outline=(*INK, 255))
    d.rectangle([hx + 8, hy - 3, hx + 11, hy + 4], fill=skin_sh)
    # Puño de camisa y manga oscura
    d.rectangle([hx + 11, hy - 4, hx + 15, hy + 5], fill=(240, 238, 230, 255), outline=(*INK, 255))
    d.rectangle([hx + 15, hy - 5, hx + 26, hy + 6], fill=(32, 36, 52, 255), outline=(*INK, 255))


def draw_copper_egg(cv, cx, cy, t, spin_speed=0.0, upright=0.0, stand_p=None, scale=1):
    """Dibuja el huevo de cobre de Tesla sobre una mesa/pedestal.
    upright: 0.0 (acostado) -> 1.0 (parado sobre su punta bailando)."""
    if stand_p is not None:
        upright = stand_p
    d = ImageDraw.Draw(cv)
    rx = int(round((11 * (1 - upright) + 7 * upright) * scale))
    ry = int(round((7 * (1 - upright) + 12 * upright) * scale))
    wobble = int(round(math.sin(t * max(4.0, spin_speed)) * 2 * scale)) if spin_speed > 0 else 0
    ey = int(round(cy - ry))
    ex = int(round(cx + (wobble if upright < 0.85 else int(wobble * 0.4))))
    # Sombra en la mesa
    shadow_ellipse(cv, int(cx), int(cy) + 2, rx + 3, max(2, int(round(3 * scale))), 110)
    # Cuerpo de cobre en 3 tonos
    c_dark = (142, 68, 28, 255)
    c_mid = (212, 118, 54, 255)
    c_hi = (252, 198, 128, 255)
    d.ellipse([ex - rx, ey - ry, ex + rx, ey + ry], fill=c_mid, outline=(*INK, 255))
    d.ellipse([ex - rx + 2, ey - ry + 2, ex + rx - 2, ey + ry - 2], fill=c_dark)
    d.ellipse([ex - rx + 2, ey - ry + 2, ex + int(rx * 0.5), ey + int(ry * 0.6)], fill=c_mid)
    # Brillo especular que gira con spin_speed
    hx_off = int(round(math.cos(t * max(1.0, spin_speed)) * (rx * 0.45))) if spin_speed > 0 else -rx // 3
    hs = max(1, int(round(2 * scale)))
    d.ellipse([ex + hx_off - hs, ey - ry // 2, ex + hx_off + hs, ey], fill=c_hi)
    if spin_speed > 6.0:
        # Líneas de velocidad alrededor del huevo
        for dy_s in (-ry // 2, 0, ry // 2):
            d.line([(ex - rx - 5, ey + dy_s), (ex - rx - 2, ey + dy_s)], fill=(*AMBER, 190))
            d.line([(ex + rx + 2, ey + dy_s), (ex + rx + 5, ey + dy_s)], fill=(*AMBER, 190))


def draw_tesla_sparks(cv, x0, y0, t, rays=5, max_len=75, color=TESLA_VIOLET, core_col=(238, 252, 255),
                      seed=0, radius=None, count=None):
    """Dibuja rayos y descargas de alta frecuencia en pixel art desde (x0, y0)."""
    if radius is not None:
        max_len = radius
    if count is not None:
        rays = count
    d = ImageDraw.Draw(cv)
    step_t = int(t * 14) + seed
    for r_i in range(rays):
        base_ang = -math.pi * 0.85 + (r_i / float(max(1, rays - 1))) * (math.pi * 0.70) if rays > 1 else -math.pi / 2
        ang = base_ang + math.sin(step_t * 1.7 + r_i * 2.3) * 0.28
        segs = 6
        px, py = float(x0), float(y0)
        pts = [(int(px), int(py))]
        seg_len = max_len / float(segs)
        for s_i in range(1, segs + 1):
            jit = math.sin(step_t * 3.1 + r_i * 5.7 + s_i * 1.9) * 0.55
            px += math.cos(ang + jit) * seg_len
            py += math.sin(ang + jit) * seg_len
            pts.append((int(round(px)), int(round(py))))
        d.line(pts, fill=(*color, 215), width=3)
        d.line(pts, fill=(*core_col, 255), width=1)


def draw_pigeon(cv, x, y, t, white=False, flying=False, peck=False, flip=False, scale=1):
    """Dibuja una paloma en pixel art (gris urbana o la paloma blanca de Tesla)."""
    d = ImageDraw.Draw(cv)
    body_c = (244, 246, 252, 255) if white else (126, 136, 156, 255)
    wing_c = (216, 226, 242, 255) if white else (88, 96, 116, 255)
    neck_c = (188, 232, 245, 255) if white else (92, 168, 148, 255)
    dir_x = -1 if flip else 1

    if flying:
        flap = int(round(math.sin(t * 18.0 + x * 0.1) * 4))
        d.ellipse([x - 5 * scale, y - 2 * scale, x + 5 * scale, y + 2 * scale], fill=body_c, outline=(*INK, 255))
        d.polygon([(x - 2 * scale, y), (x - 6 * scale, y - (5 + flap) * scale), (x + 2 * scale, y - 1 * scale)],
                  fill=wing_c, outline=(*INK, 255))
        d.polygon([(x + 1 * scale, y), (x + 5 * scale, y - (4 - flap) * scale), (x + 4 * scale, y + 1 * scale)],
                  fill=wing_c, outline=(*INK, 255))
        hx = x + dir_x * 5 * scale
        d.ellipse([hx - 2 * scale, y - 3 * scale, hx + 2 * scale, y + 1 * scale], fill=body_c, outline=(*INK, 255))
        d.point((hx + dir_x * 3 * scale, y - 1 * scale), fill=(242, 174, 72, 255))
    else:
        head_dy = 3 * scale if (peck and int(t * 5 + x) % 3 == 0) else 0
        # Patitas
        d.line([(x - 1 * scale, y - 2 * scale), (x - 1 * scale, y)], fill=(218, 112, 74, 255))
        d.line([(x + 2 * scale, y - 2 * scale), (x + 2 * scale, y)], fill=(218, 112, 74, 255))
        # Cuerpo y ala
        d.ellipse([x - 5 * scale, y - 7 * scale, x + 4 * scale, y - 2 * scale], fill=body_c, outline=(*INK, 255))
        d.ellipse([x - 3 * scale, y - 6 * scale, x + 2 * scale, y - 3 * scale], fill=wing_c)
        # Cabeza y cuello tornasolado
        hx = x + dir_x * 4 * scale
        hy = y - 8 * scale + head_dy
        d.rectangle([hx - 1 * scale, hy + 1 * scale, hx + 1 * scale, hy + 3 * scale], fill=neck_c)
        d.ellipse([hx - 2 * scale, hy - 2 * scale, hx + 2 * scale, hy + 2 * scale], fill=body_c, outline=(*INK, 255))
        d.rectangle([hx + dir_x * 2 * scale, hy, hx + dir_x * 3 * scale, hy + 1 * scale], fill=(242, 174, 72, 255))


def draw_black_cat(cv, x, y, t, sparks=False):
    """Dibuja el gato negro del capítulo 1 con chispitas de estática en el lomo."""
    d = ImageDraw.Draw(cv)
    c_cat = (24, 22, 34, 255)
    c_hi = (52, 48, 72, 255)
    # Cuerpo arqueado
    d.ellipse([x - 14, y - 14, x + 12, y - 2], fill=c_cat, outline=(*INK, 255))
    d.arc([x - 12, y - 13, x + 10, y - 4], 200, 340, fill=c_hi, width=2)
    # Patas
    for lx in (x - 10, x - 6, x + 4, x + 8):
        d.rectangle([lx, y - 4, lx + 2, y], fill=c_cat)
    # Cabeza y orejas
    hx, hy = x + 12, y - 14
    d.ellipse([hx - 6, hy - 5, hx + 6, hy + 5], fill=c_cat, outline=(*INK, 255))
    d.polygon([(hx - 5, hy - 4), (hx - 3, hy - 9), (hx, hy - 4)], fill=c_cat)
    d.polygon([(hx + 1, hy - 4), (hx + 4, hy - 9), (hx + 6, hy - 4)], fill=c_cat)
    # Ojos amarillos brillantes
    d.point((hx + 1, hy - 1), fill=(255, 228, 84, 255))
    d.point((hx + 4, hy - 1), fill=(255, 228, 84, 255))
    # Cola ondulante
    tw = int(round(math.sin(t * 4.5) * 4))
    d.line([(x - 13, y - 9), (x - 19, y - 16), (x - 17 + tw, y - 24)], fill=c_cat, width=3)
    if sparks:
        for i in range(4):
            sx = x - 8 + ((i * 7 + int(t * 15)) % 18)
            sy = y - 16 - ((i * 5 + int(t * 19)) % 8)
            sparkle(cv, sx, sy, t * 4 + i, 2, TESLA_CYAN)


# ===========================================================================
# MOTIVOS VISUALES DE «UN PIANO DENTRO DE UN TORPEDO» (HEDY LAMARR)
# ===========================================================================

LAMARR_CYAN = (40, 220, 224)
LAMARR_MAGENTA = (231, 50, 182)
PAPER_ROLL = (242, 232, 204)
PAPER_SHADOW = (198, 182, 148)
BRASS_GOLD = (212, 168, 76)


def draw_piano_roll(cv, x, y, w, h, t, speed=24.0, alpha=1.0, active_row=None):
    """Dibuja un rollo de papel perforado de pianola (motivo central del documental).
    Las perforaciones avanzan verticalmente y la fila de lectura se enciende en Cian y Magenta."""
    if alpha <= 0 or w < 12 or h < 16:
        return
    d = ImageDraw.Draw(cv)
    a = int(255 * clamp01(alpha))
    # Carretes de bronce/madera arriba y abajo
    spool_h = max(4, min(7, h // 12))
    d.rectangle([x - 2, y, x + w + 2, y + spool_h], fill=(*BRASS_GOLD, a), outline=(*INK, a))
    d.rectangle([x - 2, y + h - spool_h, x + w + 2, y + h], fill=(*BRASS_GOLD, a), outline=(*INK, a))
    # Cuerpo de papel crema con sombreado lateral
    ry0, ry1 = y + spool_h, y + h - spool_h
    d.rectangle([x, ry0, x + w, ry1], fill=(*PAPER_ROLL, a), outline=(*INK, a))
    d.rectangle([x + w - max(2, w // 7), ry0 + 1, x + w - 1, ry1 - 1], fill=(*PAPER_SHADOW, a))

    # Línea lectora central (cabezal neumático/óptico)
    read_y = active_row if active_row is not None else (ry0 + (ry1 - ry0) // 2)
    d.line([(x + 1, read_y), (x + w - 1, read_y)], fill=(*LAMARR_CYAN, int(190 * clamp01(alpha))), width=1)

    # Columnas de perforaciones que avanzan con t * speed
    n_cols = max(3, min(8, (w - 6) // 5))
    col_step = (w - 6) / float(max(1, n_cols))
    scroll = int(t * speed)
    row_step = 7
    for r_y in range(ry0 + 3 - (scroll % row_step), ry1 - 3, row_step):
        if r_y < ry0 + 2 or r_y > ry1 - 4:
            continue
        row_idx = (r_y + scroll) // row_step
        # Dos o tres perforaciones activas por fila según patrón pseudoaleatorio determinista
        for c_i in range(n_cols):
            if ((row_idx * 7 + c_i * 13) % 5) in (0, 2):
                hx = int(round(x + 3 + c_i * col_step))
                is_active = abs(r_y - read_y) <= 4
                if is_active:
                    h_col = LAMARR_CYAN if (c_i % 2 == 0) else LAMARR_MAGENTA
                    glow(cv, hx + 1, r_y + 1, 5, h_col, 0.55 * alpha)
                    d.rectangle([hx, r_y, hx + 3, r_y + 3], fill=(*h_col, a))
                else:
                    d.rectangle([hx, r_y, hx + 2, r_y + 2], fill=(32, 28, 42, a))


def draw_freq_lanes(cv, x0, y0, w, h, t, n_lanes=5, speed=3.8, jammed_lane=None,
                    hopping=True, show_labels=True):
    """Dibuja canales de frecuencia horizontales y un pulso de radio que salta entre canales
    (o queda fijo en un canal si hopping=False)."""
    d = ImageDraw.Draw(cv)
    lane_gap = h / float(max(1, n_lanes))
    seq = [0, 3, 1, 4, 2, 0, 4, 1, 3, 2]
    cur_step = int(t * speed)
    active_lane = (seq[cur_step % len(seq)] % n_lanes) if hopping else (n_lanes // 2)

    for li in range(n_lanes):
        ly = int(round(y0 + (li + 0.5) * lane_gap))
        is_jam = (jammed_lane is not None and li == jammed_lane)
        is_act = (li == active_lane)
        l_col = CHALK_RED if is_jam else (LAMARR_CYAN if is_act else (58, 76, 108))
        # Línea punteada del canal
        for xx in range(x0, x0 + w - 4, 8):
            d.line([(xx, ly), (xx + 4, ly)], fill=(*l_col, 220 if (is_act or is_jam) else 130))
        if show_labels:
            draw_text(cv, f"CH {li + 1}", x0 + 2, ly - 5, "silk", 8,
                      CHALK_RED if is_jam else (GOLD if is_act else SOFT_GRAY))
        # Si el canal está bloqueado con ruido ("jamming"), dibujar dientes de sierra rojos
        if is_jam:
            pts_j = []
            for xx in range(x0 + 34, x0 + w - 6, 5):
                jy = ly + int(round(math.sin(xx * 0.7 + t * 22.0) * 5))
                pts_j.append((xx, jy))
            if len(pts_j) >= 2:
                d.line(pts_j, fill=(*CHALK_RED, 245), width=2)

    # Paquete de señal luminosa viajando o saltando por active_lane
    ly_act = int(round(y0 + (active_lane + 0.5) * lane_gap))
    u = (t * speed) % 1.0
    sx = int(round(x0 + 36 + (w - 44) * u))
    sig_col = CHALK_RED if (jammed_lane == active_lane) else (LAMARR_CYAN if cur_step % 2 == 0 else LAMARR_MAGENTA)
    glow(cv, sx, ly_act, 10, sig_col, 0.65)
    # Onda sinusoidal corta alrededor del pulso
    pts_w = []
    for dx in range(-14, 15, 2):
        wx = max(x0 + 34, min(x0 + w - 4, sx + dx))
        wy = ly_act + int(round(math.sin((dx * 0.55) - t * 18.0) * 4))
        pts_w.append((wx, wy))
    if len(pts_w) >= 2:
        d.line(pts_w, fill=(*sig_col, 255), width=2)
    d.ellipse([sx - 3, ly_act - 3, sx + 3, ly_act + 3], fill=(255, 250, 235, 255), outline=(*sig_col, 255))


def draw_grand_piano_prop(cv, x, feet=248, t=0.0, play=False):
    """Dibuja un piano vienés / de estudio apoyado con sus patas sobre el suelo (feet=248) vía floor_prop."""
    def _draw(canvas, cx, fy):
        d = ImageDraw.Draw(canvas)
        shadow_ellipse(canvas, cx, fy, 44, 6, 95)
        # Tres patas macizas apoyadas en fy
        for lx in (cx - 34, cx - 4, cx + 28):
            d.rectangle([lx - 3, fy - 26, lx + 3, fy], fill=(32, 20, 16, 255), outline=(*INK, 255))
            d.rectangle([lx - 4, fy - 3, lx + 4, fy], fill=(186, 146, 64, 255))
        # Pedales dorados en la base
        d.line([(cx - 8, fy - 24), (cx - 8, fy - 2)], fill=(186, 146, 64, 255), width=2)
        d.rectangle([cx - 13, fy - 3, cx - 3, fy], fill=(214, 174, 78, 255))
        # Caja armónica del piano
        d.rectangle([cx - 40, fy - 48, cx + 36, fy - 25], fill=(42, 24, 18, 255), outline=(*INK, 255))
        d.polygon([(cx - 40, fy - 48), (cx + 12, fy - 66), (cx + 36, fy - 48)],
                  fill=(56, 32, 24, 255), outline=(*INK, 255))
        # Teclado de 88 teclas (blancas y negras)
        d.rectangle([cx - 38, fy - 38, cx + 20, fy - 31], fill=(246, 242, 232, 255), outline=(*INK, 255))
        for kx in range(cx - 36, cx + 18, 4):
            d.line([(kx, fy - 38), (kx, fy - 31)], fill=(160, 154, 144, 255))
            if (kx // 4) % 7 not in (2, 6):
                d.rectangle([kx + 1, fy - 38, kx + 2, fy - 34], fill=(20, 18, 24, 255))
        if play:
            # Notas musicales luminosas saliendo del teclado
            for i in range(3):
                nx = cx - 20 + i * 16 + int(round(math.sin(t * 5.0 + i) * 4))
                ny = fy - 56 - int((t * 18 + i * 9) % 22)
                col_n = LAMARR_CYAN if i % 2 == 0 else GOLD
                d.ellipse([nx - 2, ny - 2, nx + 2, ny + 1], fill=(*col_n, 255))
                d.line([(nx + 2, ny), (nx + 2, ny - 7)], fill=(*col_n, 255))

    floor_prop(cv, _draw, x, feet)


def draw_table_with_prop(cv, x, feet=248, prop_kind="music_box", t=0.0, open_p=0.0):
    """Dibuja una mesa de madera apoyada firmemente en el suelo (feet=248) con un objeto encima
    ('music_box', 'radio', 'torpedo', 'patent', 'drawer', 'film_cans', 'soda_lamp', 'headphones', 'trophy').
    Garantiza CERO objetos flotantes en 16:9 y en 9:16."""
    def _draw(canvas, cx, fy):
        d = ImageDraw.Draw(canvas)
        top_y = fy - 36
        shadow_ellipse(canvas, cx, fy, 34, 5, 90)
        # Patas de madera hasta el suelo (fy)
        leg_c = (74, 46, 28, 255)
        d.rectangle([cx - 26, top_y + 5, cx - 21, fy], fill=leg_c, outline=(*INK, 255))
        d.rectangle([cx + 21, top_y + 5, cx + 26, fy], fill=leg_c, outline=(*INK, 255))
        # Faldón y tapa de la mesa
        d.rectangle([cx - 28, top_y + 4, cx + 28, top_y + 12], fill=(96, 60, 36, 255), outline=(*INK, 255))
        d.rectangle([cx - 32, top_y, cx + 32, top_y + 5], fill=(128, 84, 48, 255), outline=(*INK, 255))
        d.line([(cx - 30, top_y + 1), (cx + 30, top_y + 1)], fill=(164, 112, 68, 255))

        if prop_kind == "music_box":
            # Caja de música con cilindro de púas dorado y engranajes
            d.rectangle([cx - 14, top_y - 14, cx + 14, top_y], fill=(112, 42, 38, 255), outline=(*INK, 255))
            d.rectangle([cx - 10, top_y - 11, cx + 10, top_y - 3], fill=(*BRASS_GOLD, 255), outline=(*INK, 255))
            # Cilindro giratorio con púas
            pin_off = int(t * 10) % 6
            for px in range(cx - 8 + pin_off // 2, cx + 8, 3):
                d.point((px, top_y - 7), fill=(*INK, 255))
            if open_p > 0.2:
                # Piezas/engranajes apoyados sobre la mesa al desarmarla y rearmarla
                d.ellipse([cx - 24, top_y - 7, cx - 17, top_y], fill=(*BRASS_GOLD, 255), outline=(*INK, 255))
                d.ellipse([cx + 17, top_y - 7, cx + 24, top_y], fill=(*BRASS_GOLD, 255), outline=(*INK, 255))
                sparkle(canvas, cx, top_y - 18, t * 2.5, 3, LAMARR_CYAN)

        elif prop_kind == "film_cans":
            # Latas de película de celuloide apiladas sobre la mesa
            for i, dy_c in enumerate((0, -6, -12)):
                ox = (i - 1) * 3
                d.rectangle([cx - 16 + ox, top_y - 6 + dy_c, cx + 16 + ox, top_y + dy_c],
                            fill=(164, 172, 184, 255), outline=(*INK, 255))
                d.line([(cx - 14 + ox, top_y - 3 + dy_c), (cx + 14 + ox, top_y - 3 + dy_c)],
                       fill=(92, 100, 114, 255))

        elif prop_kind == "soda_lamp":
            # Vaso con pastilla efervescente a la izquierda + semáforo mejorado a la derecha
            d.rectangle([cx - 20, top_y - 15, cx - 8, top_y], fill=(168, 224, 248, 230), outline=(*INK, 255))
            d.rectangle([cx - 19, top_y - 11, cx - 9, top_y - 1], fill=(238, 128, 72, 235))
            for b_i in range(3):
                by = top_y - 4 - ((int(t * 14) + b_i * 4) % 10)
                d.point((cx - 16 + b_i * 3, by), fill=(255, 250, 220, 255))
            # Mini prototipo de semáforo apoyado en la mesa
            d.rectangle([cx + 10, top_y - 24, cx + 20, top_y], fill=(42, 46, 58, 255), outline=(*INK, 255))
            active_l = int(t * 2.2) % 3
            for l_i, l_col in enumerate((CHALK_RED, GOLD, CHALK_GREEN)):
                cc = l_col if l_i == active_l else shade(l_col, 0.35)
                d.ellipse([cx + 13, top_y - 22 + l_i * 7, cx + 17, top_y - 18 + l_i * 7], fill=(*cc, 255))

        elif prop_kind == "torpedo":
            # Maqueta de torpedo + rollo de pianola apoyados sobre la mesa del comedor
            d.ellipse([cx - 26, top_y - 11, cx + 18, top_y - 1], fill=(82, 94, 108, 255), outline=(*INK, 255))
            d.polygon([(cx + 16, top_y - 11), (cx + 25, top_y - 14), (cx + 25, top_y + 1), (cx + 16, top_y - 1)],
                      fill=(*BRASS_GOLD, 255), outline=(*INK, 255))
            # Pequeño rollo perforado brillando dentro del torpedo abierto
            d.rectangle([cx - 10, top_y - 9, cx + 4, top_y - 3], fill=(*PAPER_ROLL, 255), outline=(*INK, 255))
            glow(canvas, cx - 3, top_y - 6, 8, LAMARR_CYAN, 0.55)

        elif prop_kind == "patent":
            # Documento de patente US 2,292,387 con sello dorado apoyado sobre la mesa
            d.rectangle([cx - 18, top_y - 20, cx + 18, top_y], fill=(246, 240, 222, 255), outline=(*INK, 255))
            for ly in range(top_y - 16, top_y - 4, 4):
                d.line([(cx - 13, ly), (cx + 13, ly)], fill=(72, 82, 108, 255))
            d.ellipse([cx + 6, top_y - 9, cx + 14, top_y - 1], fill=(*GOLD, 255), outline=(*CHALK_RED, 255))
            glow(canvas, cx, top_y - 10, 14, GOLD, 0.45)

        elif prop_kind == "drawer":
            # Archivero con cajón que se abre/cierra (open_p 0..1) guardando la patente
            d.rectangle([cx - 22, top_y - 24, cx + 22, top_y], fill=(62, 76, 64, 255), outline=(*INK, 255))
            dy_dr = int(round(open_p * 7))
            d.rectangle([cx - 18, top_y - 18 + dy_dr, cx + 18, top_y - 4 + dy_dr],
                        fill=(78, 94, 80, 255), outline=(*INK, 255))
            d.rectangle([cx - 5, top_y - 12 + dy_dr, cx + 5, top_y - 9 + dy_dr], fill=(*BRASS_GOLD, 255))
            if open_p > 0.25:
                d.rectangle([cx - 12, top_y - 22 + dy_dr, cx + 12, top_y - 16 + dy_dr],
                            fill=(246, 240, 222, 255), outline=(*INK, 255))
                glow(canvas, cx, top_y - 19 + dy_dr, 12, LAMARR_CYAN, 0.55 * open_p)

        elif prop_kind == "radio":
            # Radio electrónica / transmisor con luz parpadeante sobre la mesa
            d.rectangle([cx - 18, top_y - 20, cx + 18, top_y], fill=(44, 52, 66, 255), outline=(*INK, 255))
            d.rectangle([cx - 14, top_y - 16, cx + 4, top_y - 6], fill=(22, 38, 34, 255), outline=(*LAMARR_CYAN, 255))
            d.ellipse([cx + 8, top_y - 15, cx + 14, top_y - 9], fill=(*GOLD, 255))
            d.line([(cx + 12, top_y - 20), (cx + 12, top_y - 34)], fill=(180, 192, 208, 255), width=2)
            glow(canvas, cx + 12, top_y - 34, 9, LAMARR_CYAN if int(t * 8) % 2 == 0 else LAMARR_MAGENTA, 0.65)

        elif prop_kind == "headphones":
            # Auriculares inalámbricos modernos apoyados en su soporte sobre la mesa
            d.rectangle([cx - 6, top_y - 4, cx + 6, top_y], fill=(42, 48, 64, 255), outline=(*INK, 255))
            d.line([(cx, top_y - 4), (cx, top_y - 22)], fill=(64, 72, 92, 255), width=2)
            d.arc([cx - 14, top_y - 28, cx + 14, top_y - 4], 180, 360, fill=(220, 228, 242, 255), width=3)
            d.ellipse([cx - 16, top_y - 17, cx - 9, top_y - 7], fill=(36, 42, 58, 255), outline=(*LAMARR_CYAN, 255))
            d.ellipse([cx + 9, top_y - 17, cx + 16, top_y - 7], fill=(36, 42, 58, 255), outline=(*LAMARR_MAGENTA, 255))
            glow(canvas, cx, top_y - 18, 16, LAMARR_CYAN if int(t * 10) % 2 == 0 else LAMARR_MAGENTA, 0.55)

        elif prop_kind == "trophy":
            # Trofeo EFF Pioneer / Salón de la Fama sobre la mesa
            d.rectangle([cx - 10, top_y - 5, cx + 10, top_y], fill=(42, 34, 28, 255), outline=(*INK, 255))
            d.polygon([(cx - 6, top_y - 5), (cx, top_y - 24), (cx + 6, top_y - 5)],
                      fill=(*GOLD, 255), outline=(*INK, 255))
            glow(canvas, cx, top_y - 16, 14, GOLD, 0.6)
            sparkle(canvas, cx, top_y - 24, t * 2.2, 3, LAMARR_CYAN)

    floor_prop(cv, _draw, x, feet)


# ===========================================================================
# MOTIVOS VISUALES DE «A TREINTA DÍAS DE QUEBRAR» (LA HISTORIA DE NVIDIA)
# ===========================================================================

BEIGE_90S = (218, 206, 180)
BEIGE_DARK = (164, 150, 124)
GPU_GREEN = (78, 236, 122)
GPU_DIM = (34, 118, 62)
DC_GOLD = (248, 198, 76)
STOCK_RED = (242, 74, 74)


def draw_calendar_30(cv, cx, cy, t, scale=1, tear_p=0.0, highlight_30=True, hand_write=False):
    """Dibuja el motivo central del documental: el calendario de pared con 30 casilleros
    y el número '30' arriba. Si tear_p > 0, una hoja se arranca y cae girando."""
    d = ImageDraw.Draw(cv)
    w = 34 * scale
    h = 42 * scale
    x0 = int(cx - w // 2)
    y0 = int(cy)
    # Sombra y cuerpo de papel crema
    d.rectangle([x0 + 2 * scale, y0 + 2 * scale, x0 + w + 2 * scale, y0 + h + 2 * scale], fill=(0, 0, 0, 110))
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(242, 236, 218, 255), outline=(*INK, 255))
    # Cabezal rojo de calendario con dos ganchos metálicos
    hdr_h = 11 * scale
    d.rectangle([x0, y0, x0 + w, y0 + hdr_h], fill=(208, 48, 48, 255), outline=(*INK, 255))
    for gx in (x0 + 8 * scale, x0 + w - 8 * scale):
        d.rectangle([gx - 1 * scale, y0 - 3 * scale, gx + 1 * scale, y0 + 2 * scale], fill=(180, 188, 202, 255), outline=(*INK, 255))
    # Número 30 grande en la parte superior del calendario
    draw_text(cv, "30", int(cx), y0 + 2 * scale, "press", 8 * scale,
              CHALK_YELLOW if highlight_30 else CREAM, align="center")
    # Cuadrícula de 30 casilleros (6 columnas x 5 filas)
    gx0 = x0 + 3 * scale
    gy0 = y0 + hdr_h + 3 * scale
    cell_w = max(3, (w - 6 * scale) // 6)
    cell_h = max(3, (h - hdr_h - 6 * scale) // 5)
    for r in range(5):
        for c in range(6):
            idx = r * 6 + c
            cx0 = gx0 + c * cell_w
            cy0 = gy0 + r * cell_h
            is_last = (idx == 29 and highlight_30)
            fill_c = (242, 74, 74, 255) if is_last else (228, 220, 200, 255)
            d.rectangle([cx0, cy0, cx0 + cell_w - 1, cy0 + cell_h - 1], fill=fill_c, outline=(168, 158, 138, 255))

    # Hoja que se arranca y cae cuando tear_p > 0
    if 0.02 < tear_p < 0.98:
        p = clamp01(tear_p)
        ty = int(y0 + hdr_h + p * 38 * scale)
        tx = int(x0 + math.sin(p * math.pi * 2.0) * 8 * scale)
        alpha_t = int(255 * (1.0 - p * 0.75))
        d.rectangle([tx, ty, tx + w - 2 * scale, ty + (h - hdr_h) - 4 * scale],
                    fill=(248, 242, 226, alpha_t), outline=(*INK, alpha_t))
        draw_text(cv, "30", tx + w // 2, ty + 4 * scale, "silk", 8, STOCK_RED, align="center", alpha=1.0 - p * 0.75)


def draw_gpu_card(cv, cx, cy, t, scale=1, fan_speed=14.0, led_col=GPU_GREEN, dual=False):
    """Dibuja una placa de video (GPU) en pixel art con sus dos ventiladores giratorios
    y barra LED superior (sin logos de marca)."""
    d = ImageDraw.Draw(cv)
    cards = [(-18 * scale, -10 * scale), (14 * scale, 8 * scale)] if dual else [(0, 0)]
    for ox, oy in cards:
        w = 48 * scale
        h = 22 * scale
        x0 = int(cx + ox - w // 2)
        y0 = int(cy + oy - h // 2)
        if fan_speed > 0.1:
            glow(cv, x0 + w // 2, y0 + h // 2, int(22 * scale), led_col, 0.35)
        # Carcasa gris oscuro metálico + conector PCI dorado abajo
        d.rectangle([x0 + 6 * scale, y0 + h, x0 + w - 8 * scale, y0 + h + 3 * scale],
                    fill=(218, 174, 64, 255), outline=(*INK, 255))
        for px in range(x0 + 8 * scale, x0 + w - 8 * scale, 3 * scale):
            d.line([(px, y0 + h), (px, y0 + h + 2 * scale)], fill=(*INK, 255))
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(38, 44, 54, 255), outline=(*INK, 255))
        # Barra superior verde/dorada/roja
        bar_c = led_col if fan_speed > 0.1 else (72, 78, 88)
        d.rectangle([x0 + 2 * scale, y0 + 2 * scale, x0 + w - 2 * scale, y0 + 4 * scale], fill=(*bar_c, 255))
        # Dos ventiladores circulares girando con fan_speed
        for fx in (x0 + 14 * scale, x0 + w - 14 * scale):
            fy = y0 + 12 * scale
            r = 7 * scale
            d.ellipse([fx - r, fy - r, fx + r, fy + r], fill=(22, 26, 34, 255), outline=(74, 82, 96, 255))
            ang0 = t * fan_speed
            for b_i in range(4):
                ang = ang0 + b_i * (math.pi / 2.0)
                bx = int(round(fx + math.cos(ang) * (r - 1)))
                by = int(round(fy + math.sin(ang) * (r - 1)))
                d.line([(fx, fy), (bx, by)], fill=(120, 132, 148, 255), width=max(1, scale))
            hub_c = led_col if fan_speed > 0.1 else (90, 96, 108)
            d.ellipse([fx - 2 * scale, fy - 2 * scale, fx + 2 * scale, fy + 2 * scale], fill=(*hub_c, 255))


def draw_stock_chart(cv, x, y, w, h, pts_norm, progress=1.0, col_up=GPU_GREEN, col_down=STOCK_RED,
                     split_idx=None, fill_bg=True):
    """Dibuja un gráfico de bolsa en pixel art (sin logos de terceros) con subida en verde
    y caída en rojo a partir de split_idx."""
    d = ImageDraw.Draw(cv)
    if fill_bg:
        d.rectangle([x, y, x + w, y + h], fill=(12, 18, 24, 238), outline=(58, 74, 92, 255))
        for gx in range(x + 16, x + w, 20):
            d.line([(gx, y + 2), (gx, y + h - 2)], fill=(22, 34, 44, 180))
        for gy in range(y + 12, y + h, 14):
            d.line([(x + 2, gy), (x + w - 2, gy)], fill=(22, 34, 44, 180))
    n = len(pts_norm)
    if n < 2:
        return
    max_i = max(1, int(round(clamp01(progress) * (n - 1))))
    coords = []
    for i in range(max_i + 1):
        px = int(round(x + 6 + (w - 12) * (i / float(n - 1))))
        py = int(round(y + h - 6 - (h - 14) * clamp01(pts_norm[i])))
        coords.append((px, py))
    sp = split_idx if split_idx is not None else n
    for i in range(len(coords) - 1):
        c_seg = col_down if i >= sp else col_up
        d.line([coords[i], coords[i + 1]], fill=(*c_seg, 255), width=2)
    if coords:
        lx, ly = coords[-1]
        c_last = col_down if (len(coords) - 1) > sp else col_up
        glow(cv, lx, ly, 7, c_last, 0.55)
        d.rectangle([lx - 2, ly - 2, lx + 2, ly + 2], fill=(255, 250, 235, 255), outline=(*c_last, 255))


def draw_nvidia_prop(cv, x, feet=248, kind="diner_table", t=0.0, state=0.0):
    """Dibuja todos los objetos de escena apoyados sobre el suelo (feet=248) mediante floor_prop
    para que NINGÚN objeto flote en 16:9 ni en 9:16."""
    def _draw(canvas, cx, fy):
        d = ImageDraw.Draw(canvas)
        top_y = fy - 34
        shadow_ellipse(canvas, cx, fy, 38, 5, 95)

        if kind == "diner_table":
            # Mesa de restaurante de ruta de 1993 con 3 tazas de café, servilleta con triángulo y fajo de US$40.000
            d.rectangle([cx - 4, top_y + 4, cx + 4, fy], fill=(140, 148, 162, 255), outline=(*INK, 255))
            d.rectangle([cx - 18, fy - 4, cx + 18, fy], fill=(96, 104, 118, 255), outline=(*INK, 255))
            d.rectangle([cx - 42, top_y, cx + 42, top_y + 5], fill=(218, 198, 168, 255), outline=(*INK, 255))
            d.line([(cx - 42, top_y + 2), (cx + 42, top_y + 2)], fill=(198, 54, 54, 255))
            # Tres tazas de café humeantes
            for mx in (cx - 28, cx - 10, cx + 24):
                d.rectangle([mx - 4, top_y - 8, mx + 4, top_y], fill=(244, 240, 230, 255), outline=(*INK, 255))
                d.line([(mx, top_y - 11 - int(t * 6) % 4), (mx, top_y - 14 - int(t * 6) % 4)], fill=(220, 226, 236, 175))
            # Servilleta blanca con el dibujo de un triángulo
            d.rectangle([cx + 2, top_y - 5, cx + 16, top_y], fill=(250, 248, 242, 255), outline=(*INK, 255))
            d.polygon([(cx + 6, top_y - 1), (cx + 9, top_y - 4), (cx + 12, top_y - 1)], outline=(38, 168, 92, 255))
            if state >= 1.0:
                # Fajo de billetes de US$40.000 sobre la mesa
                d.rectangle([cx - 22, top_y - 7, cx - 6, top_y - 1], fill=(84, 178, 96, 255), outline=(*INK, 255))
                d.rectangle([cx - 16, top_y - 7, cx - 12, top_y - 1], fill=(238, 214, 128, 255))
            if state >= 2.0:
                # Al final (Cap 9): chip brillando suavemente sobre la servilleta
                glow(canvas, cx + 9, top_y - 4, 10, GPU_GREEN, 0.65)
                d.rectangle([cx + 7, top_y - 5, cx + 11, top_y - 2], fill=(*GPU_GREEN, 255))

        elif kind == "crt_pair":
            # Escritorio beige de 1995 con dos monitores de tubo: izquierda curvas (NV1), derecha triángulos
            d.rectangle([cx - 46, top_y + 5, cx - 40, fy], fill=(132, 120, 98, 255), outline=(*INK, 255))
            d.rectangle([cx + 40, top_y + 5, cx + 46, fy], fill=(132, 120, 98, 255), outline=(*INK, 255))
            d.rectangle([cx - 50, top_y, cx + 50, top_y + 5], fill=(184, 170, 144, 255), outline=(*INK, 255))
            # Monitor izquierdo (curvas NV1)
            for side, m_col in ((-26, STOCK_RED), (26, GPU_GREEN)):
                mx = cx + side
                d.rectangle([mx - 18, top_y - 28, mx + 18, top_y - 3], fill=(*BEIGE_90S, 255), outline=(*INK, 255))
                d.rectangle([mx - 14, top_y - 24, mx + 14, top_y - 7], fill=(16, 28, 24, 255), outline=(*INK, 255))
                d.rectangle([mx - 8, top_y - 3, mx + 8, top_y], fill=(*BEIGE_DARK, 255), outline=(*INK, 255))
                if side < 0:
                    # Superficie curva en el monitor izquierdo
                    d.ellipse([mx - 8, top_y - 21, mx + 8, top_y - 10], outline=(*m_col, 255))
                    d.arc([mx - 10, top_y - 19, mx + 10, top_y - 12], 0, 180, fill=(*m_col, 255))
                else:
                    # Malla de triángulos en el monitor derecho
                    d.polygon([(mx, top_y - 22), (mx - 9, top_y - 9), (mx + 9, top_y - 9)], outline=(*m_col, 255))
                    d.line([(mx, top_y - 22), (mx, top_y - 9)], fill=(*m_col, 255))

        elif kind == "fax_desk":
            # Escritorio con fax llegando desde Japón (contrato Sega) y caja de software con triángulos
            d.rectangle([cx - 32, top_y + 5, cx - 27, fy], fill=(124, 112, 92, 255), outline=(*INK, 255))
            d.rectangle([cx + 27, top_y + 5, cx + 32, fy], fill=(124, 112, 92, 255), outline=(*INK, 255))
            d.rectangle([cx - 36, top_y, cx + 36, top_y + 5], fill=(176, 162, 136, 255), outline=(*INK, 255))
            # Caja de estándar con triángulo a la izquierda
            d.rectangle([cx - 28, top_y - 22, cx - 8, top_y], fill=(42, 88, 158, 255), outline=(*INK, 255))
            d.polygon([(cx - 18, top_y - 18), (cx - 24, top_y - 6), (cx - 12, top_y - 6)], outline=(*GOLD, 255))
            # Máquina de fax a la derecha sacando hoja de papel
            d.rectangle([cx + 4, top_y - 12, cx + 28, top_y], fill=(*BEIGE_90S, 255), outline=(*INK, 255))
            paper_h = int(6 + (state * 12))
            d.rectangle([cx + 8, top_y - 12 - paper_h, cx + 24, top_y - 11], fill=(248, 246, 238, 255), outline=(*INK, 255))

        elif kind == "tokyo_tea_table":
            # Mesa baja japonesa con dos tazas de té verde y carpeta de US$5M / sobre de acciones
            d.rectangle([cx - 34, top_y + 10, cx - 28, fy], fill=(72, 44, 28, 255), outline=(*INK, 255))
            d.rectangle([cx + 28, top_y + 10, cx + 34, fy], fill=(72, 44, 28, 255), outline=(*INK, 255))
            d.rectangle([cx - 38, top_y + 6, cx + 38, top_y + 11], fill=(108, 66, 40, 255), outline=(*INK, 255))
            for tx in (cx - 20, cx + 20):
                d.rectangle([tx - 4, top_y, tx + 4, top_y + 6], fill=(168, 212, 158, 255), outline=(*INK, 255))
            # Sobre / carpeta en el centro
            d.rectangle([cx - 10, top_y + 1, cx + 10, top_y + 6], fill=(242, 224, 168, 255), outline=(*INK, 255))
            if state >= 1.0:
                glow(canvas, cx, top_y + 3, 12, GOLD, 0.55)

        elif kind == "gpu_pedestal":
            # Mesa de laboratorio / escenario con una placa de video o supercomputadora apoyada
            d.rectangle([cx - 28, top_y + 5, cx - 23, fy], fill=(48, 56, 72, 255), outline=(*INK, 255))
            d.rectangle([cx + 23, top_y + 5, cx + 28, fy], fill=(48, 56, 72, 255), outline=(*INK, 255))
            d.rectangle([cx - 32, top_y, cx + 32, top_y + 5], fill=(72, 82, 104, 255), outline=(*INK, 255))
            draw_gpu_card(canvas, cx, top_y - 12, t, scale=1, fan_speed=(0.0 if state < 0 else 16.0),
                          led_col=(GOLD if state >= 2.0 else GPU_GREEN), dual=(state == 1.5))

        elif kind == "ceo_desk":
            # Escritorio ejecutivo en Cap 8 y 9: carta de renuncia, diarios apilados, silla vacía y saco colgado
            # Silla vacía detrás del escritorio + perchero con saco a la derecha
            d.rectangle([cx - 12, top_y - 26, cx + 12, top_y], fill=(36, 38, 48, 255), outline=(*INK, 255))
            d.rectangle([cx - 34, top_y + 4, cx + 34, fy], fill=(68, 38, 28, 255), outline=(*INK, 255))
            d.rectangle([cx - 38, top_y, cx + 38, top_y + 5], fill=(98, 54, 38, 255), outline=(*INK, 255))
            # Carta blanca sobre el escritorio
            d.rectangle([cx - 10, top_y - 5, cx + 10, top_y], fill=(246, 242, 232, 255), outline=(*INK, 255))
            if state >= 1.0:
                # Pila de diarios genéricos a la izquierda del escritorio
                for i in range(int(min(3, state))):
                    dy_n = i * 4
                    d.rectangle([cx - 32, top_y - 5 - dy_n, cx - 14, top_y - 1 - dy_n],
                                fill=(226, 222, 212, 255), outline=(*INK, 255))
            # Perchero de pie apoyado en fy a la derecha con un saco oscuro colgado
            rx = cx + 52
            d.line([(rx, fy - 48), (rx, fy)], fill=(92, 64, 42, 255), width=2)
            d.rectangle([rx - 8, fy - 3, rx + 8, fy], fill=(72, 48, 32, 255), outline=(*INK, 255))
            d.polygon([(rx - 8, fy - 42), (rx + 8, fy - 42), (rx + 10, fy - 18), (rx - 10, fy - 18)],
                      fill=(28, 32, 44, 255), outline=(*INK, 255))

    floor_prop(cv, _draw, x, feet)



