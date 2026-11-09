"""Piloto en pixel art: Apertura + Capítulo 1 de "Le dieron un verano. Tardó 70 años".

Uso:
  python engine/pilot.py preview 3.0 12.5 40      -> PNGs de esos instantes en frames/preview
  python engine/pilot.py sheet                     -> hoja de contacto con 1 frame por escena
  python engine/pilot.py render                    -> renders/video_mudo.mp4 (1920x1080, 30 fps)
"""
import math
import os
import subprocess
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


def char(cv, key, x, feet, t, alpha=1.0, shadow=True, **pose):
    arr = S.render(S.CAST[key], t, **pose)
    if shadow and alpha > 0.3:
        shadow_ellipse(cv, int(x), int(feet), 18, 4, 80)
    paste_arr(cv, arr, int(x) - S.SW // 2, int(feet) - FEET_OFFSET, alpha)


def silhouette(cv, key, x, feet, t, color=(12, 10, 22), **pose):
    arr = S.render(S.CAST[key], t, **pose).copy()
    m = arr[..., 3] > 0
    arr[m, :3] = color
    paste_arr(cv, arr, int(x) - S.SW // 2, int(feet) - FEET_OFFSET)


def robot(cv, x, feet, t, face="happy", frozen=False, alpha=1.0, sil=False):
    blink = (t % 3.1) < 0.12
    arr = S.render_robot(face, int(t * 30) % 90, frozen, blink)
    if sil:
        arr = arr.copy(); m = arr[..., 3] > 0; arr[m, :3] = (12, 10, 22)
    shadow_ellipse(cv, int(x), int(feet), 26, 4, 80)
    paste_arr(cv, arr, int(x) - 15, int(feet) - 39, alpha)


def walk(t, t0, t1, x0, x1):
    p = prog(t, t0, t1)
    x = x0 + (x1 - x0) * ease_in_out(p) if False else x0 + (x1 - x0) * p
    return x, ((t * 2.6) % 1.0 if 0 < p < 1 else None)


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
    off = int((1 - ease_out(prog(t, t0, t0 + 0.5))) * -30)
    tw, _ = text_size(title, "press", 16)
    sw, _ = text_size(sub, "silk", 8)
    window(cv, x - 8 + off, y - 8, max(tw, sw) + 22, 48, alpha=0.85)
    ImageDraw.Draw(cv).rectangle([x + off, y - 2, x + off + int(24 * ease_out(prog(t, t0, t0 + 0.6))), y - 1],
                                 fill=(*GOLD, 255))
    draw_text(cv, title, x + off, y + 4, "press", 16, CREAM, alpha=a)
    draw_text(cv, sub, x + off + 1, y + 24, "silk", 8, GREY, alpha=a)


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


def bulb(cv, cx, cy, t, on=1.0):
    d = ImageDraw.Draw(cv)
    glow = int(200 * on)
    if on > 0:
        for r, a in ((13, 40), (10, 70)):
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 240, 140, int(a * on)))
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


# =========================================================================== escenas
# Cada escena: función (t_global) -> Image RGBA 480x270

FOUR = ["mccarthy", "minsky", "shannon", "rochester"]


def sc_office(t):
    """En 1955, cuatro científicos pidieron dinero para un plan audaz."""
    cv = bg("bg_office_1955").copy()
    # lámpara titilando
    if int(t * 7) % 23 == 0:
        cv = grade(cv, mul=(0.93, 0.93, 0.93))
    bigyear(cv, "1955", 240, 30, t, TL.s("s01") + 0.05)
    t_cuatro = TL.word("s01", "cuatro")
    t_dinero = TL.word("s01", "dinero")
    t_audaz = TL.word("s01", "audaz")
    xs = [70, 112, 154, 196]
    for i, k in enumerate(FOUR):
        t0 = t_cuatro - 0.9 + i * 0.22
        x, ph = walk(t, t0, t0 + 1.5, -20 - i * 10, xs[i])
        speaking = (ph is None and t > t0 + 1.5 and int((t - t0) / 0.9) % 4 == i and t < t_audaz)
        arms = "down"
        mood = "neutral"
        if t > t_audaz:
            arms, mood = ("cheer" if i % 2 == 0 else "point"), "happy"
        char(cv, k, x, 258, t, walk=ph, talk=talk_v(t, speaking), arms=arms, mood=mood)
        if t > t_audaz + i * 0.07:
            a, dy = pop(t, t_audaz + i * 0.07)
            draw_text(cv, "!", int(x) - 3, 196 + dy, "press", 16, GOLD, alpha=a)
    # solicitud de fondos
    if t > t_dinero - 0.1:
        a, dy = pop(t, t_dinero - 0.1, 0.4)
        x0, y0 = 248, 96 + dy
        window(cv, x0, y0, 220, 50)
        draw_text(cv, "SOLICITUD DE FONDOS", x0 + 10, y0 + 10, "press", 8, GOLD, alpha=a)
        draw_text(cv, "FUNDACIÓN ROCKEFELLER", x0 + 10, y0 + 24, "silk", 8, CREAM, alpha=a)
        # monedas
        for j in range(3):
            cx = x0 + 186 + (j % 2) * 8
            cy = y0 + 34 - j * 5 - int(abs(math.sin(t * 5 + j)) * 2)
            d = ImageDraw.Draw(cv)
            d.ellipse([cx - 5, cy - 3, cx + 5, cy + 3], fill=(240, 200, 80, 255), outline=(120, 70, 20, 255))
            d.line([(cx - 2, cy), (cx + 2, cy)], fill=(180, 120, 40, 255))
    return vignette(cv, 0.4)


def sc_ten(t):
    """Dos meses de verano, y diez personas, para enseñarle a una máquina a pensar."""
    cv = vgradient((8, 10, 26), (34, 40, 78), 14)
    d = ImageDraw.Draw(cv)
    # piso del escenario
    d.rectangle([0, 206, W, H], fill=(20, 22, 44, 255))
    for i, y in enumerate((206, 214, 226, 242, 262)):
        d.line([(0, y), (W, y)], fill=(40, 46, 86, 255))
    for x in range(-200, W + 200, 40):
        d.line([(W // 2 + (x - W // 2) * 0.35, 206), (x, H)], fill=(30, 34, 66, 255))
    t_dos = TL.s("s02")
    t_diez = TL.word("s02", "diez")
    t_maq = TL.word("s02", "maquina")
    t_pensar = TL.word("s02", "pensar")
    # títulos
    draw_text(cv, "DOS MESES", 240 - 100, 18, "press", 16, CREAM, align="center",
              reveal=(t - t_dos) * 22)
    if t > t_diez:
        draw_text(cv, "·", 240, 18, "press", 16, GOLD, align="center")
        draw_text(cv, "DIEZ PERSONAS", 240 + 118, 18, "press", 16, CREAM, align="center",
                  reveal=(t - t_diez) * 26)
    # calendario de verano
    a, dy = pop(t, t_dos + 0.2, 0.4)
    if a > 0:
        x0, y0 = 22, 46 + dy
        draw_paper(cv, x0, y0, 62, 58)
        d = ImageDraw.Draw(cv)
        d.rectangle([x0 + 1, y0 + 1, x0 + 61, y0 + 13], fill=(200, 70, 60, 255))
        draw_text(cv, "VERANO", x0 + 31, y0 + 4, "silk", 8, CREAM, align="center", outline=None, shadow=False)
        draw_text(cv, "1956", x0 + 31, y0 + 16, "silk", 8, INK, align="center", outline=None, shadow=False)
        weeks = int(prog(t, t_dos + 0.4, t_diez + 0.8) * 8)
        for wk in range(8):
            r, c = wk // 4, wk % 4
            bx, by = x0 + 8 + c * 12, y0 + 30 + r * 12
            d.rectangle([bx, by, bx + 8, by + 8], outline=(120, 110, 100, 255))
            if wk < weeks:
                d.line([(bx + 1, by + 1), (bx + 7, by + 7)], fill=(200, 60, 50, 255))
                d.line([(bx + 7, by + 1), (bx + 1, by + 7)], fill=(200, 60, 50, 255))
        draw_sun(cv, x0 + 62, y0 + 2, 6, t, face=False)
    # diez personas con sus orbes cian
    for i, k in enumerate(S.DARTMOUTH_TEN):
        t0 = t_diez + 0.05 + i * 0.11
        a, dy = pop(t, t0)
        if a <= 0:
            continue
        x = 48 + i * 43
        cv = spotlight(cv, x, 40, 206, 4, 34, strength=0.18 * a)
        char(cv, k, x, 204 + dy, t, alpha=a, mood="happy" if t > t_pensar else "neutral",
             look=(1 if x < 240 else -1) if t > t_maq + 0.3 else 0)
        orb(cv, x, 132 + dy, t, a)
    # la máquina
    if t > t_maq - 0.6:
        x, _ = walk(t, t_maq - 0.6, t_maq + 0.5, W + 30, 240)
        face = "question" if t > t_pensar - 0.1 else "happy"
        robot(cv, x, 256, t, face=face)
        if t > t_pensar + 0.2:
            on = prog(t, t_pensar + 0.2, t_pensar + 0.5)
            bulb(cv, int(x), 196 - int(abs(math.sin(t * 3)) * 2), t, on)
    return vignette(cv, 0.3)


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


def sc_summer(t):
    """Creían que un verano alcanzaba. Ya pasaron setenta años. Y la historia todavía no terminó."""
    t3 = TL.s("s03")
    t4 = TL.s("s04")
    t_end = TL.word("s04", "termino", end=True)
    p = ease_in_out(prog(t, t4 + 0.2, TL.word("s04", "historia")))
    years = p * 70
    night = sky_cycle(years / 14.0) if p > 0 else 0.0
    base = bg("bg_dartmouth_summer").copy()
    if night > 0.01:
        base = grade(base, mul=(0.35, 0.4, 0.75), add=(4, 6, 24), sat=0.6, k=night)
    cv = base
    # sol / luna en arco
    if p <= 0:
        draw_sun(cv, 62, 44, 14, t)
    else:
        ang = (years / 14.0) % 1.0
        sx = int(-20 + ang * (W + 40))
        sy = int(110 - math.sin(ang * math.pi) * 90)
        if night < 0.6:
            draw_sun(cv, sx, sy, 12, t, face=False)
        else:
            draw_moon(cv, (sx + W // 2) % W, sy)
    # los diez sentados en el pasto
    seat = [(54, 0), (84, 1), (114, 0), (150, 1), (180, 0), (296, 1), (326, 0), (360, 1), (392, 0), (424, 1)]
    for i, k in enumerate(S.DARTMOUTH_TEN):
        fade = 1 - prog(t, t4 + 0.3 + i * 0.12, t4 + 0.8 + i * 0.12)
        if fade <= 0:
            continue
        x, row = seat[i]
        speaking = int(t / 0.7) % 10 == i and t < t4
        char(cv, k, x, 236 + row * 4, t, alpha=fade, sit=True, talk=talk_v(t, speaking), mood="happy",
             arms="think" if i == 3 else "down")
    # misión
    if t < t4 + 0.2:
        quest_window(cv, [("MISIÓN:", GOLD), ("ENSEÑAR A PENSAR", CREAM), ("A UNA MÁQUINA", CREAM),
                          ("PLAZO: 1 VERANO", CYAN)], 250, 22, t, t3 + 0.1, w=196)
    else:
        quest_window(cv, [("MISIÓN:", GOLD), ("ENSEÑAR A PENSAR", CREAM), ("A UNA MÁQUINA", CREAM),
                          ("PLAZO: " + ("70 AÑOS..." if p > 0.98 else f"{int(years) + 1} VERANOS"), CYAN)],
                     250, 22, t, t3 + 0.1, w=196)
        if p < 0.15:
            d = ImageDraw.Draw(cv)
            d.line([(258, 66), (380, 66)], fill=(230, 70, 60, 255), width=2)
    # contador de años
    if p > 0:
        year = 1956 + int(round(years))
        draw_text(cv, str(year), 240, 104, "press", 32, align="center", gradient=GOLD_RAMP, outline_w=2)
        bars70(cv, years, t)
    if t > t_end - 0.4:
        a = prog(t, t_end - 0.4, t_end)
        draw_text(cv, "SETENTA AÑOS DESPUÉS", 240, 148, "press", 8, GOLD, align="center", alpha=a)
    return vignette(cv, 0.35)


STARS = Stars(140, seed=11, region=(0, 0, W, 210))


def sc_title(t):
    """Esta es la historia de la inteligencia artificial."""
    cv = vgradient((4, 4, 12), (22, 26, 58), 12)
    STARS.draw(cv, t)
    bars70(cv, 70, t, y=246, cur_glow=False, alpha=0.8)
    # resplandor del horizonte
    d = ImageDraw.Draw(cv)
    t_hist = TL.word("s05", "historia")
    t_ia = TL.word("s05", "inteligencia")
    t_art = TL.word("s05", "artificial")
    t_end = TL.e("s05")
    draw_text(cv, "LA HISTORIA DE LA", 240, 62, "press", 16, CREAM, align="center",
              reveal=(t - t_hist + 0.2) * 24)
    dx, dy = 0, 0
    if t > t_ia:
        p = prog(t, t_ia, t_ia + 0.25)
        draw_text(cv, "INTELIGENCIA", 240, int(92 - (1 - p) * 30), "press", 32, align="center",
                  gradient=GOLD_RAMP, outline_w=2, alpha=p)
    if t > t_art:
        p = prog(t, t_art, t_art + 0.25)
        draw_text(cv, "ARTIFICIAL", 240, int(134 + (1 - p) * 30), "press", 32, align="center",
                  gradient=GOLD_RAMP, outline_w=2, alpha=p)
        for i in range(6):
            sparkle(cv, 70 + i * 68, 100 + (i % 2) * 52, t + i, 3)
    draw_text(cv, "UN VERANO QUE DURÓ 70 AÑOS", 240, 186, "press", 8, CYAN, align="center",
              reveal=(t - t_end - 0.2) * 30)
    if t > t_end + 0.5:
        robot(cv, 448, 238, t, face="happy", alpha=prog(t, t_end + 0.5, t_end + 0.8))
    for t0 in (t_ia, t_art):
        sx, sy = shake(t, t0 + 0.22)
        dx += sx; dy += sy
    cv = offset_canvas(cv, dx, dy)
    # destello
    for t0 in (t_ia + 0.22, t_art + 0.22):
        if t0 <= t < t0 + 0.15:
            cv = fade_to(cv, (255, 250, 230), 0.35 * (1 - (t - t0) / 0.15))
    return cv


def chapter_card(cv, t, t0, num, lines, years, ramp_title=CREAM_RAMP):
    open_p = ease_out(prog(t, t0, t0 + 0.35))
    if open_p <= 0:
        return
    w = int(340 * open_p)
    h = 120
    window(cv, 240 - w // 2, 70, max(8, w), h)
    if open_p < 1:
        return
    tt = t - t0 - 0.35
    d = ImageDraw.Draw(cv)
    lab = f"CAPÍTULO {num}"
    lw, _ = text_size(lab, "press", 8)
    draw_text(cv, lab, 240, 86, "press", 8, GOLD, align="center", reveal=tt * 30)
    ln = int(min(1, tt * 2) * 50)
    d.line([(240 - lw // 2 - 8 - ln, 89), (240 - lw // 2 - 8, 89)], fill=(*GOLD, 255))
    d.line([(240 + lw // 2 + 8, 89), (240 + lw // 2 + 8 + ln, 89)], fill=(*GOLD, 255))
    size = 24 if len(lines) == 1 else 16
    for i, line in enumerate(lines):
        yy = 112 if len(lines) == 1 else 106 + i * 22
        draw_text(cv, line, 240, yy, "press", size, align="center", gradient=ramp_title,
                  reveal=(tt - 0.25 - i * 0.4) * 26)
    draw_text(cv, years, 240, 170, "press", 8, CYAN, align="center", reveal=(tt - 1.0) * 30)


def sc_ch1(t):
    cv = vgradient((2, 2, 8), (14, 16, 36), 10)
    STARS.draw(cv, t * 0.5, alpha=0.6)
    t0 = TL.s("s06") - 0.35
    chapter_card(cv, t, t0, 1, ["LA PREGUNTA"], "1950 – 1956")
    # signo de pregunta flotante
    if t > t0 + 0.6:
        a = prog(t, t0 + 0.6, t0 + 0.9)
        draw_text(cv, "?", 240, 34 + int(math.sin(t * 3) * 3), "press", 24, align="center", gradient=CYAN_RAMP,
                  alpha=a)
    return cv


RAIN = Rain(110, seed=4, region=(192, 8, 428, 142), color=(196, 210, 226), speed=210)


def sc_turing(t):
    """Turing y la pregunta."""
    cv = bg("bg_turing_study").copy()
    RAIN.draw(cv, t, 200)
    t0 = TL.s("s07")
    t_alan = TL.word("s07", "Alan")
    t_art = TL.word("s07", "articulo")
    t_preg = TL.word("s07", "pregunta")
    t_pue = TL.word("s07", "pueden")
    t_maq = TL.word("s07", "maquinas")
    # 1950 gigante (sale antes de la pregunta)
    if t < t_preg:
        a_out = 1 - prog(t, t_preg - 0.5, t_preg)
        if a_out > 0:
            p = prog(t, t0, t0 + 0.55)
            yy = 26 - (1 - ease_out_back(p, 2.2)) * 50
            draw_text(cv, "1950", 310, int(yy), "press", 48, align="center", gradient=GOLD_RAMP, outline_w=2,
                      alpha=min(p * 3, a_out))
    # Turing
    pose = dict(arms="think", mood="neutral")
    if t > t_art:
        pose = dict(arms="hold", mood="neutral")
    if t > t_preg:
        pose = dict(arms="think", mood="neutral", look=0)
    if t > t_pue:
        pose = dict(arms="point_l", mood="happy")
    char(cv, "turing", 446, 256, t, **pose)
    # hoja de papel en la mano
    if t_art < t < t_preg:
        draw_paper(cv, 440, 220, 12, 15)
        for i in range(4):
            ImageDraw.Draw(cv).line([(442, 223 + i * 3), (449, 223 + i * 3)], fill=(120, 120, 140, 255))
    # pregunta en cian
    if t > t_preg + 0.2:
        a, dy = pop(t, t_preg + 0.2)
        bubble(cv, "?", 446, 196 + dy, size=16)
    if t > t_pue - 0.1:
        rv = (t - t_pue + 0.1) * 18
        draw_text(cv, "¿PUEDEN PENSAR", 300, 40, "press", 16, align="center", gradient=CYAN_RAMP, reveal=rv)
        draw_text(cv, "LAS MÁQUINAS?", 300, 64, "press", 16, align="center", gradient=CYAN_RAMP,
                  reveal=(t - t_maq + 0.3) * 18)
    # tarjeta con retrato
    if t > t_alan - 0.2:
        a = prog(t, t_alan - 0.2, t_alan + 0.2)
        off = int((1 - ease_out(a)) * -120)
        portrait_card(cv, "alan_turing", 14 + off, 160)
        tw = 300
        window(cv, 86 + off, 174, tw, 46)
        draw_text(cv, "ALAN TURING", 96 + off, 184, "press", 16, CREAM)
        draw_text(cv, "«COMPUTING MACHINERY AND INTELLIGENCE» · 1950", 96 + off, 204, "silk", 8, GREY)
    return vignette(cv, 0.4)


def booth_bg():
    cv = vgradient((34, 28, 52), (18, 16, 30), 10)
    d = ImageDraw.Draw(cv)
    for x in range(0, W, 16):
        d.line([(x, 0), (x, 230)], fill=(40, 34, 60, 255))
    d.rectangle([0, 230, W, H], fill=(70, 48, 34, 255))
    for y in (236, 246, 260):
        d.line([(0, y), (W, y)], fill=(54, 36, 26, 255))
    for x in range(0, W, 40):
        d.line([(x, 230), (x - 20, H)], fill=(58, 40, 28, 255))
    # muro divisor de ladrillos
    d.rectangle([166, 0, 182, 232], fill=(96, 48, 40, 255), outline=(*INK, 255))
    for y in range(0, 232, 8):
        off = 0 if (y // 8) % 2 else 4
        d.line([(167, y), (181, y)], fill=(64, 30, 26, 255))
        d.line([(167 + off + 4, y), (167 + off + 4, y + 7)], fill=(64, 30, 26, 255))
    # tabique entre cabinas
    d.rectangle([330, 60, 334, 232], fill=(60, 52, 80, 255), outline=(*INK, 255))
    return cv


def sc_imitation(t):
    """El juego de la imitación."""
    cv = booth_bg()
    t_juego = TL.word("s08", "juego")
    t_si = TL.word("s08", "conversas")
    t_maq = TL.word("s08", "maquina")
    t_dist = TL.word("s08", "distinguirla")
    t_imp = TL.word("s08", "importa")
    reveal = prog(t, t_imp, t_imp + 0.6)
    # interrogador
    judge_talk = t_si - 0.2 < t < t_si + 1.2
    look = 0
    if t > t_dist:
        look = 1 if int((t - t_dist) * 2) % 2 == 0 else -1
    char(cv, "judge", 78, 232, t, talk=talk_v(t, judge_talk), look=look,
         arms="type" if t_si - 1.0 < t < t_si - 0.2 else "down",
         mood="worried" if t > t_dist else "neutral")
    desk(cv, 36, 150, 220, 234)
    terminal(cv, 112, 193, t)
    # cabina A (persona) y B (máquina)
    for label, cx in (("A", 258), ("B", 404)):
        window(cv, cx - 12, 66, 24, 20)
        draw_text(cv, label, cx, 72, "press", 8, GOLD, align="center")
    if reveal < 1:
        silhouette(cv, "human_b", 274, 232, t)
        robot(cv, 424, 232, t, sil=True)
    if reveal > 0:
        a = reveal
        char(cv, "human_b", 274, 232, t, alpha=a, mood="happy", talk=0)
        robot(cv, 424, 232, t, face="happy", alpha=a)
    if reveal < 1:
        draw_text(cv, "?", 274, 194, "press", 8, CYAN, align="center")
        draw_text(cv, "?", 424, 200, "press", 8, CYAN, align="center")
    desk(cv, 196, 324, 220, 234)
    desk(cv, 340, 474, 220, 234)
    terminal(cv, 204, 193, t)
    terminal(cv, 350, 193, t)
    # título
    if t > t_juego - 0.1:
        a, dy = pop(t, t_juego - 0.1)
        window(cv, 40, 10 + dy, 400, 30)
        draw_text(cv, "EL JUEGO DE LA IMITACIÓN", 240, 18 + dy, "press", 16, align="center", gradient=GOLD_RAMP)
    # diálogo
    if t_si - 0.2 < t < t_imp + 0.4:
        bubble(cv, "¿ERES HUMANO?", 86, 172, reveal=(t - t_si + 0.2) * 22)
    if t_maq - 0.1 < t < t_imp + 2.5:
        r = (t - t_maq + 0.1) * 20
        bubble(cv, "SÍ, CLARO.", 258, 176, reveal=r)
        bubble(cv, "SÍ, CLARO.", 404, 176, reveal=r)
    if t > t_dist + 0.3 and t < t_imp + 0.4:
        a, dy = pop(t, t_dist + 0.3)
        draw_text(cv, "?", 78 + int(math.sin(t * 6) * 2), 124 + dy, "press", 16, CYAN, align="center")
    if t > t_imp:
        a = prog(t, t_imp, t_imp + 0.4)
        draw_text(cv, "¿HUMANO O MÁQUINA?", 240, 246, "press", 8, CREAM, align="center", alpha=a)
    return vignette(cv, 0.35)


def sc_dartmouth(t):
    """Cinco años después... firman la propuesta para un taller de verano en Dartmouth."""
    cv = bg("bg_dartmouth_summer").copy()
    draw_sun(cv, 52, 36, 12, t)
    t0 = TL.s("s09")
    names = ["McCarthy", "Minsky", "Shannon", "Rochester"]
    times = [TL.word("s09", n) for n in names]
    t_firman = TL.word("s09", "firman")
    t_dart = TL.word("s09", "Dartmouth")
    t_nombre = TL.word("s10", "nombre", end=True)
    t_doc = TL.word("s10", "documento")
    t_primera = TL.word("s10", "primera")
    bigyear(cv, "1955", 240, 8, t, t0 - 0.1, size=24) if t < times[0] - 0.2 else None
    portraits = ["john_mccarthy", "marvin_minsky", "claude_shannon", "nathaniel_rochester"]
    first = ["JOHN", "MARVIN", "CLAUDE", "NATHANIEL"]
    last = ["McCARTHY", "MINSKY", "SHANNON", "ROCHESTER"]
    xs = [108, 196, 284, 372]
    doc_p = prog(t, t_firman - 0.2, t_firman + 0.4)
    for i, k in enumerate(FOUR):
        tn = times[i]
        x, ph = walk(t, tn - 1.1, tn - 0.05, -24, xs[i])
        mood = "happy" if t > tn else "neutral"
        arms = "wave" if tn < t < tn + 0.9 else ("hold" if t > t_firman + 0.3 else "down")
        char(cv, k, x, 222, t, walk=ph, mood=mood, arms=arms)
        # tarjeta con retrato
        if t > tn - 0.1:
            a, dy = pop(t, tn - 0.1, 0.4)
            up = int(ease_in_out(doc_p) * -170)
            cx = 36 + i * 108
            portrait_card(cv, portraits[i], cx, 26 + dy + up)
            draw_text(cv, first[i], cx + 32, 98 + dy + up, "silk", 8, GREY, align="center")
            draw_text(cv, last[i], cx + 32, 108 + dy + up, "press", 8, CREAM, align="center")
    # documento de la propuesta
    if doc_p > 0:
        yoff = int((1 - ease_out(doc_p)) * 160)
        x0, y0 = 128, 18 + yoff
        draw_paper(cv, x0, y0, 224, 150)
        lines = ["A PROPOSAL FOR THE", "DARTMOUTH SUMMER", "RESEARCH PROJECT ON"]
        for i, ln in enumerate(lines):
            draw_text(cv, ln, x0 + 112, y0 + 12 + i * 12, "silk", 8, INK, align="center", outline=None, shadow=False)
        hl = prog(t, t_doc, t_doc + 0.5)
        col = INK if hl <= 0 else (200, 120, 20)
        if hl > 0:
            d = ImageDraw.Draw(cv)
            ww = int(196 * ease_out(hl))
            d.rectangle([x0 + 14, y0 + 46, x0 + 14 + ww, y0 + 60], fill=(255, 226, 120, 255))
        draw_text(cv, "ARTIFICIAL INTELLIGENCE", x0 + 112, y0 + 49, "silkb", 8, col, align="center",
                  outline=None, shadow=False)
        draw_text(cv, "AUGUST 31, 1955", x0 + 112, y0 + 68, "silk", 8, (90, 90, 100), align="center",
                  outline=None, shadow=False)
        sig_names = ["J. McCARTHY", "M. L. MINSKY", "N. ROCHESTER", "C. E. SHANNON"]
        for i in range(4):
            sx, sy = x0 + 16 + (i % 2) * 106, y0 + 94 + (i // 2) * 26
            p = prog(t, t_firman + 0.3 + i * 0.45, t_firman + 0.8 + i * 0.45)
            scribble(cv, sx, sy, 80, p, seed=i * 2.3)
            d = ImageDraw.Draw(cv)
            d.line([(sx, sy + 6), (sx + 84, sy + 6)], fill=(150, 140, 120, 255))
            draw_text(cv, sig_names[i], sx, sy + 9, "silk", 8, (110, 104, 96), outline=None, shadow=False)
        if t > t_primera:
            a, dy = pop(t, t_primera)
            window(cv, x0 + 176, y0 - 8 + dy, 80, 18, fill=(150, 40, 40), border=GOLD)
            draw_text(cv, "¡1ª VEZ!", x0 + 216, y0 - 3 + dy, "press", 8, CREAM, align="center")
            for i in range(4):
                sparkle(cv, x0 + 20 + i * 60, y0 + 44 + (i % 2) * 18, t + i, 3, GOLD)
    lower_third(cv, "DARTMOUTH COLLEGE", "PROPUESTA DE 1955 · TALLER DE VERANO DE 1956", t, t_dart - 0.3,
                t_nombre + 0.6, x=16, y=232)
    return vignette(cv, 0.3)


def sc_board(t):
    """... un nombre: inteligencia artificial."""
    cv = bg("bg_classroom_1956").copy()
    d = ImageDraw.Draw(cv)
    # banderín verde de Dartmouth sobre el escudo de la pared
    d.rectangle([434, 50, 479, 110], fill=(232, 210, 170, 255))
    d.polygon([(440, 58), (474, 58), (474, 100), (457, 108), (440, 100)], fill=(0, 105, 62, 255),
              outline=(*INK, 255))
    draw_text(cv, "D", 457, 70, "press", 16, CREAM, align="center")
    t_ia = TL.word("s10", "inteligencia")
    t_art = TL.word("s10", "artificial")
    t_end = TL.e("s10")
    # tiza
    def chalk(text, y, t0, t1):
        n = len(text)
        rv = prog(t, t0, t1) * n
        draw_text(cv, text, 309, y, "press", 16, (236, 240, 230), align="center", outline=None,
                  shadow=False, reveal=rv)
    chalk("INTELIGENCIA", 54, t_ia - 0.05, t_art - 0.05)
    chalk("ARTIFICIAL", 86, t_art - 0.05, t_end + 0.1)
    glow = prog(t, t_end + 0.15, t_end + 0.6)
    if glow > 0:
        draw_text(cv, "INTELIGENCIA", 309, 54, "press", 16, align="center", gradient=GOLD_RAMP, alpha=glow,
                  outline=None, shadow=False)
        draw_text(cv, "ARTIFICIAL", 309, 86, "press", 16, align="center", gradient=GOLD_RAMP, alpha=glow,
                  outline=None, shadow=False)
        for i in range(5):
            sparkle(cv, 220 + i * 44, 50 + (i % 2) * 52, t + i * 0.7, 3, GOLD)
    # personajes
    writing = t_ia - 0.1 < t < t_end + 0.1
    char(cv, "mccarthy", 438, 258, t, arms="point_l" if writing else ("cheer" if glow > 0.5 else "down"),
         mood="happy" if glow > 0 else "neutral")
    for i, (k, x) in enumerate((("minsky", 46), ("shannon", 92), ("rochester", 138))):
        cheer = glow > 0.3
        char(cv, k, x, 258 - (int(abs(math.sin(t * 7 + i)) * 4) if cheer else 0), t,
             arms="cheer" if cheer else "down", mood="happy" if cheer else "neutral", look=1)
    return vignette(cv, 0.35)


SNOW = Snow(260, seed=8)
CONF = Confetti(110, seed=6)


def sc_winter(t):
    """Eran optimistas. Demasiado optimistas. Y lo que vino después..."""
    t11 = TL.s("s11")
    t_dem = TL.word("s11", "Demasiado")
    t12 = TL.s("s12")
    t_ent = TL.word("s12", "enterrar")
    t_siempre = TL.word("s12", "siempre")
    w = ease_in_out(prog(t, t12 - 0.1, t12 + 2.2))  # 0 verano -> 1 invierno
    cv = bg("bg_dartmouth_summer").copy()
    if w > 0:
        cv = grade(cv, mul=(0.78, 0.9, 1.12), add=(36, 46, 70), sat=0.25, k=w)
    if w < 1:
        draw_sun(cv, 60, 40, 14, t, alpha=int(255 * (1 - w)))
    # los diez
    xs = [36 + i * 45 for i in range(10)]
    for i, k in enumerate(S.DARTMOUTH_TEN):
        leave = prog(t, t_ent - 0.6 + i * 0.08, t_ent - 0.1 + i * 0.08)
        if leave >= 1:
            continue
        hop = 0
        arms, mood = "down", "neutral"
        if t11 - 0.2 < t < t12:
            arms, mood = "cheer", "happy"
            hop = int(abs(math.sin(t * 7 + i * 0.8)) * 5)
        elif t >= t12:
            arms, mood = ("cross", "worried")
            hop = int(math.sin(t * 40 + i) > 0.6)  # tiritan
        char(cv, k, xs[i] + (hop if t >= t12 else 0), 238 - (hop if t < t12 else 0), t,
             alpha=1 - leave, arms=arms, mood=mood)
    if t11 - 0.2 < t < t12 + 0.4:
        CONF.draw(cv, t - t11 + 0.2)
    # medidor de optimismo
    fill = 0.55 + 0.45 * ease_out(prog(t, t11, t11 + 0.8))
    fill += 0.75 * ease_out(prog(t, t_dem, t_dem + 1.0))
    fill *= 1 - ease_in_out(prog(t, t12 + 0.5, t_ent))
    window(cv, 12, 12, 156, 34)
    draw_text(cv, "OPTIMISMO", 20, 18, "press", 8, CREAM if w < 0.5 else (190, 220, 245))
    d = ImageDraw.Draw(cv)
    d.rectangle([20, 30, 160, 38], fill=(10, 10, 20, 255), outline=(*INK, 255))
    bw = int(140 * fill)
    over = fill > 1.0
    col = GOLD if not over else ((255, 90, 70) if int(t * 8) % 2 else GOLD)
    if w > 0.5:
        col = (120, 180, 230)
    d.rectangle([21, 31, 21 + max(0, bw - 1), 37], fill=(*col, 255), outline=(*INK, 255) if over else None)
    if over and w < 0.5:
        draw_text(cv, "!!", 26 + bw, 26, "press", 8, (255, 90, 70))
    # la idea: texto que se congela y se hunde
    if t > t12 + 0.6:
        a = prog(t, t12 + 0.6, t12 + 1.0)
        sink = ease_in_out(prog(t, t_ent, t_siempre + 0.6)) * 70
        ice = prog(t, t12 + 1.2, t_ent)
        ramp = GOLD_RAMP if ice < 0.5 else ICE_RAMP
        draw_text(cv, "INTELIGENCIA ARTIFICIAL", 240, int(150 + sink), "press", 16, align="center",
                  gradient=ramp, alpha=a)
    # la máquina se congela
    if t > t12 + 0.3:
        a = prog(t, t12 + 0.3, t12 + 0.7)
        frozen = t > t_ent
        robot(cv, 240, 226, t, face="sad" if not frozen else "off", frozen=frozen, alpha=a)
    # nieve que cae y se acumula
    if w > 0:
        SNOW.draw(cv, t, density=w)
        acc = ease_in_out(prog(t, t12 + 0.5, t_siempre + 0.8))
        top = int(H - acc * 52)
        a = np.array(cv)
        xs_ = np.arange(W)
        edge = top + (np.sin(xs_ * 0.21) * 2 + np.sin(xs_ * 0.07 + 1) * 3).astype(int)
        for x in range(W):
            e = max(0, edge[x])
            a[e:, x, :3] = (232, 240, 250)
            if e < H:
                a[e, x, :3] = (255, 255, 255)
                if e + 3 < H:
                    a[e + 3:, x, :3] = (214, 226, 242) if (x + e) % 7 else (196, 212, 236)
        cv = Image.fromarray(a, "RGBA")
    return vignette(cv, 0.4)


def sc_ch2(t):
    cv = vgradient((4, 6, 16), (20, 30, 56), 10)
    t0 = TL.s("s13") - 0.35
    SNOW.draw(cv, t, density=0.7)
    chapter_card(cv, t, t0, 2, ["LA MÁQUINA QUE", "IBA A SER CONSCIENTE"], "1958 – 1969")
    if t > t0 + 1.2:
        robot(cv, 240, 252, t, face="question", frozen=False, alpha=prog(t, t0 + 1.2, t0 + 1.6))
    end = TL.total
    return fade_to(cv, (0, 0, 0), prog(t, end - 1.3, end - 0.1))


# =========================================================================== montaje

def build_scenes():
    c = []
    c.append((0.0, sc_office))
    c.append((TL.s("s02") - 0.25, sc_ten))
    c.append((TL.s("s03") - 0.3, sc_summer))
    c.append((TL.s("s05") - 0.3, sc_title))
    c.append((TL.s("s06") - 0.45, sc_ch1))
    c.append((TL.s("s07") - 0.3, sc_turing))
    c.append((TL.s("s08") - 0.3, sc_imitation))
    c.append((TL.s("s09") - 0.3, sc_dartmouth))
    c.append((TL.word("s10", "nombre", end=True) + 0.05, sc_board))
    c.append((TL.s("s11") - 0.35, sc_winter))
    c.append((TL.s("s13") - 0.5, sc_ch2))
    return c


SCENES = build_scenes()
XFADE = 0.33


def frame_at(t):
    idx = 0
    for i, (st, _) in enumerate(SCENES):
        if t >= st:
            idx = i
    st, fn = SCENES[idx]
    img = fn(t)
    # transición con dithering al entrar en la escena
    if idx > 0 and t < st + XFADE:
        prev = SCENES[idx - 1][1](t)
        k = (t - st) / XFADE
        img = dither_mix(prev, img, k)
    if t < 0.6:
        img = fade_to(img, (0, 0, 0), 1 - t / 0.6)
    return img


def preview(times):
    os.makedirs(os.path.join(ROOT, "frames", "preview"), exist_ok=True)
    for t in times:
        im = frame_at(t).convert("RGB").resize((960, 540), Image.NEAREST)
        im.save(os.path.join(ROOT, "frames", "preview", f"t{t:06.2f}.png"))
        print("saved", t)


def sheet(times=None, name="sheet.png", cols=3):
    if times is None:
        times = []
        for i, (st, _) in enumerate(SCENES):
            en = SCENES[i + 1][0] if i + 1 < len(SCENES) else TL.total
            times.append(st + (en - st) * 0.75)
    tiles = [frame_at(t).convert("RGB") for t in times]
    rows = (len(tiles) + cols - 1) // cols
    out = Image.new("RGB", (cols * 480, rows * 270))
    for i, im in enumerate(tiles):
        out.paste(im, ((i % cols) * 480, (i // cols) * 270))
    out = out.resize((out.size[0] * 2 // 1, out.size[1] * 2 // 1), Image.NEAREST) if cols <= 2 else out
    out.save(os.path.join(ROOT, "frames", name))
    print("sheet", [round(x, 2) for x in times])


def render(out_path=None, start=0.0, end=None):
    out_path = out_path or os.path.join(ROOT, "renders", "video_mudo.mp4")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    end = end or TL.total
    n0, n1 = int(start * FPS), int(end * FPS)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-vf", "scale=1920:1080:flags=neighbor",
           "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", out_path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    import time
    t_start = time.time()
    for i in range(n0, n1):
        t = i / FPS
        p.stdin.write(frame_at(t).convert("RGB").tobytes())
        if i % 150 == 0:
            print(f"frame {i}/{n1}  t={t:.1f}s  {time.time() - t_start:.0f}s", flush=True)
    p.stdin.close()
    p.wait()
    print("done", out_path)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "sheet"
    if cmd == "preview":
        preview([float(x) for x in sys.argv[2:]])
    elif cmd == "sheet":
        sheet()
    elif cmd == "times":
        sheet([float(x) for x in sys.argv[2:]], name="sheet_times.png")
    elif cmd == "render":
        render()
