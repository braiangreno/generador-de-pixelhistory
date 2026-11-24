"""Personajes en pixel art 16-bit, generados proceduralmente.

Cada personaje se define con un diccionario de rasgos (pelo, anteojos, ropa, colores)
y se dibuja en un sprite de 28x52 px con capas (piernas, torso, cabeza, brazos),
cada una con sombreado de 3 tonos y contorno propio ("selout"), para poder animarlo:
caminar, tipear, escribir, saludar, señalar, festejar, hablar y parpadear.
"""
import math
from functools import lru_cache

import numpy as np

SW, SH = 28, 52  # tamaño del sprite
OUTLINE = np.array([12, 12, 16], dtype=np.int32)


def hexc(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def shade(c, f):
    return tuple(int(max(0, min(255, v * f))) for v in c)


def tint(c, t, k):
    return tuple(int(a + (b - a) * k) for a, b in zip(c, t))


# Stickman Histórico 2D (estilo OverSimplified): cabezas y manos blancas puras con contorno negro
SKIN = {
    "light": hexc("f8f8fc"), "fair": hexc("f8f8fc"), "tan": hexc("f4f4f8"),
    "olive": hexc("f4f4f8"), "brown": hexc("f0f0f6"), "asian": hexc("f8f8fc"),
}


class Layer:
    """Capa RGBA pequeña con utilidades de dibujo por píxel."""

    def __init__(self):
        self.a = np.zeros((SH, SW, 4), dtype=np.int32)

    def px(self, x, y, c):
        if 0 <= x < SW and 0 <= y < SH:
            self.a[y, x, :3] = c
            self.a[y, x, 3] = 255

    def rect(self, x0, y0, x1, y1, c):  # inclusivo
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.px(x, y, c)

    def clear(self, x, y):
        if 0 <= x < SW and 0 <= y < SH:
            self.a[y, x, 3] = 0

    def get(self, x, y):
        if 0 <= x < SW and 0 <= y < SH and self.a[y, x, 3]:
            return tuple(self.a[y, x, :3])
        return None

    def thick_line(self, x0, y0, x1, y1, c, w=3, shadow=None):
        n = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
        r = w // 2
        for i in range(n + 1):
            t = i / max(1, n)
            x = round(x0 + (x1 - x0) * t)
            y = round(y0 + (y1 - y0) * t)
            for dy in range(-r, w - r):
                for dx in range(-r, w - r):
                    cc = shadow if (shadow and dx == w - r - 1) else c
                    self.px(x + dx, y + dy, cc)

    def outline(self, color=None):
        """Agrega contorno exterior de 1 px (oscuro del color vecino)."""
        alpha = self.a[:, :, 3] > 0
        out = self.a.copy()
        for y in range(SH):
            for x in range(SW):
                if alpha[y, x]:
                    continue
                nb = None
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    xx, yy = x + dx, y + dy
                    if 0 <= xx < SW and 0 <= yy < SH and alpha[yy, xx]:
                        nb = self.a[yy, xx, :3]
                        break
                if nb is not None:
                    c = color if color is not None else (nb * 0.28 + OUTLINE * 0.72)
                    out[y, x, :3] = np.array(c, dtype=np.int32)
                    out[y, x, 3] = 255
        self.a = out
        return self


def composite(layers):
    base = np.zeros((SH, SW, 4), dtype=np.int32)
    for L in layers:
        m = L.a[:, :, 3] > 0
        base[m] = L.a[m]
    return base.astype(np.uint8)


# --------------------------------------------------------------------------- partes

def draw_legs(spec, pose):
    L = Layer()
    pants = spec["pants"]
    pd = shade(pants, 0.72)
    shoe = spec.get("shoes", hexc("2b1d1a"))
    phase = pose.get("walk")
    sit = pose.get("sit", False)
    if sit:
        # sentado de frente: piernas cortas hacia adelante
        L.rect(8, 33, 19, 37, pants)
        L.rect(16, 33, 19, 37, pd)
        L.rect(9, 38, 12, 44, pants)
        L.rect(15, 38, 18, 44, pd)
        L.rect(8, 45, 12, 47, shoe)
        L.rect(15, 45, 19, 47, shoe)
        return L.outline()
    lo = ro = 0
    if phase is not None:
        s = math.sin(phase * 2 * math.pi)
        lo = round(s * 2)
        ro = -lo
    if spec.get("skirt"):
        sk = spec.get("skirt_color", pants)
        for i, y in enumerate(range(32, 41)):
            L.rect(8 - i // 3, y, 19 + i // 3, y, sk)
            L.rect(16 + i // 4, y, 19 + i // 3, y, shade(sk, 0.75))
        legc = spec["skin"]
        L.rect(10, 41, 12, 46 + min(0, lo), legc)
        L.rect(15, 41, 17, 46 + min(0, ro), shade(legc, 0.85))
        L.rect(9, 47 + min(0, lo) , 12, 49 + min(0, lo), shoe)
        L.rect(15, 47 + min(0, ro), 18, 49 + min(0, ro), shoe)
        return L.outline()
    # Piernas estilo Stickman Histórico 2D (palitos negros articulados con zapatos redondeados)
    stick_col = hexc("14141a")
    L.rect(10 + lo // 2, 32, 11 + lo // 2, 46 - max(0, -lo), stick_col)
    L.rect(16 + ro // 2, 32, 17 + ro // 2, 46 - max(0, -ro), stick_col)
    # Zapatos negros redondeados
    L.rect(8 + lo, 47 - max(0, -lo), 12 + lo, 49 - max(0, -lo), stick_col)
    L.rect(15 + ro, 47 - max(0, -ro), 19 + ro, 49 - max(0, -ro), stick_col)
    return L


def draw_torso(spec, pose):
    L = Layer()
    top = spec["top"]
    tc = spec["top_color"]
    td = shade(tc, 0.72)
    th = tint(tc, (255, 255, 255), 0.18)
    shirt = spec.get("shirt", hexc("eeeae0"))
    tie = spec.get("tie")
    skin = spec["skin"]
    # cuello
    L.rect(12, 17, 15, 19, shade(skin, 0.8))
    # tronco (hombros 7..20, cintura 8..19)
    for y in range(19, 33):
        x0, x1 = (7, 20) if y < 24 else (8, 19)
        L.rect(x0, y, x1, y, tc)
        L.rect(x1 - 3, y, x1, y, td)
        L.px(x0, y, th) if y < 28 else None
    L.rect(8, 19, 19, 19, th)
    if top in ("suit", "labcoat", "blazer", "trench"):
        # camisa en V y solapas
        for i, y in enumerate(range(19, 26)):
            w = max(0, 3 - i // 2)
            L.rect(13 - w, y, 14 + w, y, shirt)
        if tie:
            L.rect(13, 20, 14, 28, tie)
            L.px(14, 21, shade(tie, 0.7)); L.px(14, 24, shade(tie, 0.7)); L.px(14, 27, shade(tie, 0.7))
            L.rect(13, 20, 14, 20, shade(tie, 1.25))
        # solapas
        for i, y in enumerate(range(19, 27)):
            L.px(12 - min(i, 3) + (i // 4), y, td)
            L.px(15 + min(i, 3) - (i // 4), y, shade(tc, 0.6))
        # botones
        L.px(13, 29, shade(tc, 0.5)); L.px(14, 29, shade(tc, 0.5))
        if top == "labcoat":
            L.rect(13, 26, 14, 32, shade(tc, 0.85))
    elif top == "vest":
        # camisa de color con chaleco
        L.rect(7, 19, 20, 23, shirt)
        L.rect(17, 19, 20, 23, shade(shirt, 0.8))
        for i, y in enumerate(range(21, 33)):
            L.rect(9, y, 18, y, tc)
            L.rect(15, y, 18, y, td)
        for i, y in enumerate(range(21, 26)):
            w = max(0, 2 - i // 2)
            L.rect(13 - w, y, 14 + w, y, shirt)
        if tie:
            L.rect(13, 20, 14, 26, tie)
        L.rect(12, 19, 15, 19, shade(shirt, 0.85))
    elif top == "shirt":
        L.rect(12, 19, 15, 20, shade(tc, 0.85))
        L.px(12, 20, shade(tc, 0.6)); L.px(15, 20, shade(tc, 0.6))
        if tie:
            L.rect(13, 20, 14, 28, tie)
            L.px(14, 23, shade(tie, 0.7)); L.px(14, 26, shade(tie, 0.7))
        else:
            for y in range(22, 32, 3):
                L.px(13, y, shade(tc, 0.7))
        L.rect(16, 23, 18, 24, shade(tc, 0.85))  # bolsillo
    elif top in ("sweater", "tshirt", "hoodie", "turtleneck"):
        if top == "sweater":
            L.rect(12, 19, 15, 20, spec.get("shirt", hexc("eeeae0")))
        if top == "turtleneck":
            L.rect(11, 17, 16, 20, tc); L.rect(14, 17, 16, 20, td)
        if top == "hoodie":
            L.rect(10, 19, 17, 21, shade(tc, 0.85))
            L.px(12, 22, shade(tc, 1.3)); L.px(12, 23, shade(tc, 1.3))
            L.px(15, 22, shade(tc, 1.3)); L.px(15, 23, shade(tc, 1.3))
            L.rect(10, 28, 17, 30, shade(tc, 0.85))
        L.rect(8, 31, 19, 32, shade(tc, 0.8))
    elif top == "uniform":
        L.rect(12, 19, 15, 22, shirt)
        if tie:
            L.rect(13, 20, 14, 25, tie)
        for y in (24, 27, 30):
            L.px(11, y, hexc("e8c25a")); L.px(16, y, hexc("e8c25a"))
        L.rect(7, 19, 9, 19, hexc("e8c25a")); L.rect(18, 19, 20, 19, hexc("e8c25a"))
    if spec.get("belt", top in ("shirt",)):
        L.rect(8, 31, 19, 31, shade(spec["pants"], 0.5))
        L.px(13, 31, hexc("c9a24a"))
    return L.outline()


def draw_head(spec, pose):
    L = Layer()
    skin = spec["skin"]
    sd = shade(skin, 0.82)
    sdd = shade(skin, 0.68)
    hair = spec.get("hair", hexc("3a2a20"))
    hd = shade(hair, 0.7)
    hh = tint(hair, (255, 255, 255), 0.22)
    style = spec.get("hair_style", "side")
    bob = 0
    # cara: x 8..19, y 3..16 con esquinas redondeadas
    for y in range(3, 17):
        x0, x1 = 8, 19
        if y in (3, 16):
            x0, x1 = 10, 17
        elif y in (4, 15):
            x0, x1 = 9, 18
        L.rect(x0, y, x1, y, skin)
        L.rect(x1 - 2, y, x1, y, sd)
    # orejas
    L.rect(7, 9, 7, 12, skin); L.rect(20, 9, 20, 12, sd)
    L.px(7, 10, sd); L.px(20, 10, sdd)
    # mentón/sombra
    L.rect(11, 16, 16, 16, sd)
    # --- pelo
    if style != "bald":
        top_y = 0 if style in ("wavy", "curly", "bouffant", "long", "bun") else 1
        for y in range(top_y, 6):
            w = {0: (10, 17), 1: (9, 18), 2: (8, 19), 3: (7, 20), 4: (7, 20), 5: (7, 20)}[y]
            L.rect(w[0], y, w[1], y, hair)
        L.rect(15, 1, 20, 5, hd)
        L.rect(9, 1, 12, 1, hh)
        L.rect(8, 2, 10, 2, hh)
    if style == "side":
        L.rect(7, 6, 8, 9, hair); L.rect(19, 6, 20, 9, hd)
        L.rect(8, 6, 13, 6, hair)  # flequillo con raya
        L.px(14, 5, skin); L.px(13, 4, skin) if False else None
        L.px(15, 6, hair); L.px(16, 6, hd)
    elif style == "slick":
        L.rect(7, 6, 7, 8, hair); L.rect(20, 6, 20, 8, hd)
        for x in range(9, 19, 3):
            L.px(x, 2, hh); L.px(x + 1, 3, hh)
    elif style == "wavy":
        L.rect(7, 6, 8, 10, hair); L.rect(19, 6, 20, 10, hd)
        L.rect(8, 6, 12, 6, hair); L.px(9, 7, hair)
        for x in (9, 12, 15, 18):
            L.px(x, 0, hh if x < 14 else hd)
        L.px(11, 3, hh); L.px(12, 3, hd); L.px(16, 3, hh)
    elif style == "curly":
        L.rect(6, 4, 8, 11, hair); L.rect(19, 4, 21, 11, hd)
        for x in range(7, 21, 2):
            L.px(x, 0, hair); L.px(x, 6, hair if x < 14 else hd)
            L.px(x + 1, 2, hh if x < 14 else hd)
    elif style == "recede":
        L.rect(7, 6, 7, 10, hair); L.rect(20, 6, 20, 10, hd)
        for x in range(10, 18):  # entradas
            L.px(x, 4, skin if x < 17 else sd); L.px(x, 5, skin if x < 17 else sd)
        L.rect(11, 3, 16, 3, skin)
    elif style == "bald":
        L.rect(7, 5, 7, 10, hair); L.rect(20, 5, 20, 10, hd)
        L.rect(10, 2, 17, 2, skin); L.rect(9, 3, 18, 3, skin)
        L.px(11, 3, tint(skin, (255, 255, 255), 0.35))
    elif style == "crew":
        L.rect(7, 4, 7, 7, hair); L.rect(20, 4, 20, 7, hd)
        L.rect(9, 1, 18, 1, hh)
    elif style == "long":
        L.rect(6, 4, 8, 22, hair); L.rect(19, 4, 21, 22, hd)
        L.rect(8, 6, 14, 7, hair); L.px(8, 8, hair)
    elif style == "bun":
        L.rect(11, -1 + 1, 16, 0, hair)
        L.rect(6, 4, 8, 13, hair); L.rect(19, 4, 21, 13, hd)
        L.rect(8, 6, 12, 6, hair)
    elif style == "bangs":
        L.rect(6, 4, 8, 20, hair); L.rect(19, 4, 21, 20, hd)
        L.rect(8, 6, 19, 7, hair); L.rect(16, 6, 19, 7, hd)
    elif style == "fringe":
        L.rect(7, 6, 8, 9, hair); L.rect(19, 6, 20, 9, hd)
        L.rect(8, 6, 19, 7, hair); L.rect(16, 6, 19, 7, hd)
        L.px(11, 7, hh)
    elif style == "short":
        L.rect(7, 6, 7, 8, hair); L.rect(20, 6, 20, 8, hd)
        L.rect(8, 6, 10, 6, hair)
    # --- barba / bigote
    beard = spec.get("beard")
    bc = spec.get("beard_color", hair)
    if beard == "full":
        L.rect(8, 11, 19, 15, bc); L.rect(10, 16, 17, 17, bc)
        L.rect(16, 11, 19, 16, shade(bc, 0.7))
        L.rect(12, 13, 15, 13, shade(skin, 0.6))  # boca
    elif beard == "short":
        L.rect(9, 13, 18, 15, shade(bc, 0.95)); L.rect(11, 16, 16, 16, bc)
        L.rect(12, 13, 15, 13, bc)
    elif beard == "stubble":
        for x in range(9, 19, 2):
            L.px(x, 15, shade(skin, 0.7)); L.px(x + 1, 14, shade(skin, 0.75))
    if beard in ("mustache", "short") or spec.get("mustache"):
        L.rect(12, 13, 15, 13, spec.get("mustache_color", bc))
    # --- cara Stickman Histórico 2D (ojos grandes redondos estilo OverSimplified)
    blink = pose.get("blink", False)
    eye = hexc("121216")
    white_eye = hexc("ffffff")
    ey = 10
    lx, rx = 11, 16
    look = pose.get("look", 0)
    if blink:
        L.rect(lx - 1, ey, lx + 1, ey, eye)
        L.rect(rx - 1, ey, rx + 1, ey, eye)
    else:
        for cx in (lx, rx):
            L.rect(cx - 1, ey - 1, cx + 1, ey + 1, white_eye)
            px_p = max(cx - 1, min(cx + 1, cx + look))
            L.rect(px_p, ey, px_p, ey + 1, eye)
    # cejas expresivas negras
    brow = hexc("14141a")
    mood = pose.get("mood", "neutral")
    if mood == "worried":
        L.px(lx - 1, ey - 2, brow); L.px(lx, ey - 3, brow)
        L.px(rx + 1, ey - 2, brow); L.px(rx, ey - 3, brow)
    else:
        L.rect(lx - 1, ey - 3, lx + 1, ey - 3, brow)
        L.rect(rx - 1, ey - 3, rx + 1, ey - 3, brow)
    # boca expresiva cartoon
    talk = pose.get("talk", 0)
    mouth = hexc("14141a")
    if beard != "full":
        if talk == 2:
            L.rect(12, 14, 15, 15, mouth)
            L.rect(13, 15, 14, 15, hexc("e85858"))
        elif talk == 1:
            L.rect(12, 14, 15, 14, mouth)
        elif mood == "happy":
            L.px(11, 14, mouth); L.rect(12, 15, 15, 15, mouth); L.px(16, 14, mouth)
        elif mood == "sad":
            L.px(11, 15, mouth); L.rect(12, 14, 15, 14, mouth); L.px(16, 15, mouth)
        else:
            L.rect(12, 14, 15, 14, mouth)
    elif talk:
        L.rect(12, 14, 15, 14 + (talk == 2), hexc("18141a"))
    # anteojos
    g = spec.get("glasses")
    if g:
        gc = {"black": hexc("141018"), "wire": hexc("b8b0a0"), "round": hexc("8a7a60"),
              "gold": hexc("c9a24a")}[g]
        lens = tint(skin, (225, 240, 255), 0.35)
        for cx in (lx, rx):
            # cristal claro con el ojo adentro
            for yy in (ey, ey + 1):
                for xx in (cx - 1, cx + 1):
                    L.px(xx, yy, lens)
            L.rect(cx - 1, ey - 1, cx + 1, ey - 1, gc)
            L.px(cx - 2, ey, gc); L.px(cx - 2, ey + 1, gc)
            L.px(cx + 2, ey, gc); L.px(cx + 2, ey + 1, gc)
            if g != "round":
                L.rect(cx - 1, ey + 2, cx + 1, ey + 2, gc)
            else:
                L.px(cx, ey + 2, gc)
            if not blink:
                L.rect(cx + look, ey, cx + look, ey + 1, eye)
        L.px(14, ey, gc)
        L.px(8, ey, gc); L.px(19, ey, gc)
    # sombreros
    hat = spec.get("hat")
    if hat == "fedora":
        hc = spec.get("hat_color", hexc("6a4a30"))
        L.rect(5, 5, 22, 6, hc); L.rect(8, 0, 19, 4, hc)
        L.rect(16, 0, 19, 4, shade(hc, 0.75)); L.rect(8, 4, 19, 4, hexc("2a1a14"))
        L.rect(9, 3, 11, 3, hexc("f0ead8"))
        for y in range(7, 9):
            L.rect(8, y, 19, y, skin)
    elif hat == "navy":
        L.rect(7, 0, 20, 3, hexc("f4f2ec")); L.rect(17, 0, 20, 3, hexc("cfcac0"))
        L.rect(7, 4, 20, 5, hexc("1a2236")); L.rect(6, 6, 16, 6, hexc("101420"))
        L.rect(12, 1, 15, 3, hexc("e8c25a"))
    elif hat == "helmet":
        L.rect(6, 1, 21, 16, hexc("f0f2f6"))
        L.rect(17, 1, 21, 16, hexc("cfd6e2"))
        L.rect(8, 5, 19, 13, hexc("d8a238"))
        L.rect(9, 6, 13, 8, hexc("ffe082"))
    L.outline()
    return L


def draw_arms(spec, pose, t=0.0):
    L = Layer()
    tc = spec["top_color"]
    sleeve = spec.get("sleeve", tc)
    if spec["top"] == "vest":
        sleeve = spec.get("shirt", hexc("eeeae0"))
    sd = shade(sleeve, 0.72)
    skin = spec["skin"]
    arms = pose.get("arms", "down")
    sl, sr = (7, 21), (20, 21)
    phase = pose.get("walk")
    sw = 0
    if phase is not None:
        sw = round(math.sin(phase * 2 * math.pi) * 2)

    if arms == "down":
        hl, hr = (6 - sw // 2, 31), (21 + sw // 2, 31)
    elif arms == "type":
        j = int(t * 14) % 2
        hl, hr = (10, 27 + j), (17, 28 - j)
    elif arms in ("write", "note"):
        j = round(math.sin(t * 9) * 1.5)
        hl, hr = (9, 27), (18 + j, 26)
    elif arms == "work":
        j = round(math.sin(t * 7.5) * 2)
        hl, hr = (9, 28 + j), (18, 29 + j)
    elif arms == "hips":
        hl, hr = (5, 27), (22, 27)
    elif arms == "wave":
        j = round(math.sin(t * 9) * 2)
        hl, hr = (6, 31), (25 + j, 11)
    elif arms == "point":
        hl, hr = (6, 31), (27, 20)
    elif arms == "point_l":
        hl, hr = (0, 20), (21, 31)
    elif arms in ("cheer", "up"):
        j = round(math.sin(t * 10) * 1.5)
        hl, hr = (3, 9 + j), (24, 9 - j)
    elif arms == "offer":
        hl, hr = (8, 25), (23, 22)
    elif arms == "hold":
        hl, hr = (10, 26), (17, 26)
    elif arms == "think":
        hl, hr = (6, 31), (15, 16)
    elif arms == "shrug":
        hl, hr = (3, 22), (24, 22)
    elif arms == "cross":
        hl, hr = (17, 25), (10, 26)
    else:
        hl, hr = (6, 31), (21, 31)

    # Brazos estilo Stickman Histórico 2D: palitos negros articulados + manos blancas redondas
    stick_col = hexc("14141a")
    hand_col = hexc("f8f8fc")
    L.thick_line(sl[0], sl[1], hl[0], hl[1], stick_col, 2)
    L.thick_line(sr[0], sr[1], hr[0], hr[1], stick_col, 2)
    for (hx, hy) in (hl, hr):
        L.rect(hx - 1, hy - 1, hx + 1, hy + 1, stick_col)
        L.rect(hx - 1, hy, hx, hy + 1, hand_col)

    if arms == "note":
        L.rect(7, 24, 12, 28, hexc("f4ecd2"))
        L.rect(7, 24, 12, 24, hexc("c84a32"))
    return L


@lru_cache(maxsize=8192)
def _render(spec_key, pose_key, tq):
    """Renderizador Stickman Histórico 2D (estilo OverSimplified / Sam O'Nella):
    Cabeza blanca redonda grande con contorno negro grueso, ojos circulares grandes expresivos,
    boca cartoon con lengua roja al hablar, torso trapezoidal con vestimenta histórica,
    brazos y piernas de palito negro articulados y manos blancas redondas."""
    from PIL import Image, ImageDraw
    spec = dict(spec_key)
    if "top" not in spec:
        spec["top"] = "suit" if "jacket" in spec else "shirt"
    if "top_color" not in spec:
        spec["top_color"] = spec.get("jacket", spec.get("shirt", (80, 90, 120)))
    if isinstance(spec.get("beard"), tuple):
        spec["beard_color"] = spec["beard"]
        spec["beard"] = "full"
    if spec.get("glasses") is True:
        spec["glasses"] = "black"
    pose = dict(pose_key)
    scale = max(1, int(pose.pop("scale", 1)))
    t_sec = tq / 30.0

    # Renderizado 2D Cartoon Vectorial anti-aliased (supersampling 2x sobre 1080p -> LANCZOS)
    K = 8 * scale
    W_HI, H_HI = SW * K, SH * K
    im = Image.new("RGBA", (W_HI, H_HI), (0, 0, 0, 0))
    d = ImageDraw._orig_imagedraw_draw(im) if hasattr(ImageDraw, "_orig_imagedraw_draw") else ImageDraw.ImageDraw(im)

    INK_C = (16, 16, 22, 255)
    WHITE_C = (250, 250, 252, 255)
    tc = (*spec["top_color"][:3], 255)
    shirt_c = (*spec.get("shirt", (238, 234, 224))[:3], 255)
    hair_c = (*spec.get("hair", (58, 42, 32))[:3], 255)
    tie_c = (*spec["tie"][:3], 255) if spec.get("tie") else None
    style = spec.get("hair_style", "side")
    ow = max(2, K)

    phase = pose.get("walk")
    lo = ro = sw = 0
    if phase is not None:
        s = math.sin(phase * 2 * math.pi)
        lo = int(round(s * 2 * K))
        ro = -lo
        sw = int(round(s * 2 * K))

    # 1. PIERNAS DE PALITO NEGRO + ZAPATOS REDONDEADOS (pies en y = 50 * K)
    leg_y0 = 35 * K
    foot_y = 49 * K
    lx_foot = 11 * K + lo
    rx_foot = 17 * K + ro
    d.line([(11 * K, leg_y0), (lx_foot, foot_y)], fill=INK_C, width=max(2, int(1.6 * K)))
    d.line([(17 * K, leg_y0), (rx_foot, foot_y)], fill=INK_C, width=max(2, int(1.6 * K)))
    d.ellipse([lx_foot - 2 * K, foot_y - K, lx_foot + 2 * K, foot_y + K], fill=INK_C)
    d.ellipse([rx_foot - 2 * K, foot_y - K, rx_foot + 2 * K, foot_y + K], fill=INK_C)

    # 2. TORSO TRAPEZOIDAL CON CONTORNO NEGRO GRUESO (y = 22*K .. 36*K)
    t_poly = [(8 * K, 22 * K), (20 * K, 22 * K), (21 * K, 36 * K), (7 * K, 36 * K)]
    d.polygon(t_poly, fill=tc, outline=INK_C)
    d.line(t_poly + [t_poly[0]], fill=INK_C, width=ow)
    if spec["top"] in ("suit", "blazer", "labcoat", "vest"):
        d.polygon([(11 * K, 22 * K), (17 * K, 22 * K), (14 * K, 29 * K)], fill=shirt_c, outline=INK_C)
        if tie_c:
            d.line([(14 * K, 23 * K), (14 * K, 32 * K)], fill=tie_c, width=max(2, K))
    elif spec["top"] == "turtleneck":
        d.rectangle([11 * K, 20 * K, 17 * K, 23 * K], fill=tc, outline=INK_C, width=ow)

    # 3. BRAZOS DE PALITO NEGRO ARTICULADOS + MANOS BLANCAS REDONDAS
    arms_mode = pose.get("arms", "down")
    l_arm = pose.get("l_arm")
    r_arm = pose.get("r_arm")
    sl = (8 * K, 24 * K)
    sr = (20 * K, 24 * K)
    hl = (3 * K - sw // 2, 34 * K)
    hr = (25 * K + sw // 2, 34 * K)
    if arms_mode in ("cheer", "up") or (l_arm == "up" and r_arm == "up"):
        hl, hr = (2 * K, 13 * K), (26 * K, 13 * K)
    else:
        if l_arm == "up":
            hl = (2 * K, 14 * K)
        elif l_arm == "point":
            hl = (1 * K, 22 * K)
        if r_arm == "up" or arms_mode == "wave":
            hr = (26 * K, 14 * K)
        elif r_arm == "point" or arms_mode == "point":
            hr = (27 * K, 22 * K)

    for (sx, sy), (hx, hy), side_k in ((sl, hl, -1), (sr, hr, 1)):
        mx = (sx + hx) // 2 + side_k * K
        my = (sy + hy) // 2 + K
        d.line([(sx, sy), (mx, my), (hx, hy)], fill=INK_C, width=max(2, int(1.6 * K)))
        hr_hand = int(1.8 * K)
        d.ellipse([hx - hr_hand, hy - hr_hand, hx + hr_hand, hy + hr_hand],
                  fill=WHITE_C, outline=INK_C, width=ow)

    # 4. CABEZA BLANCA REDONDA GRANDE (centro en 14*K, 12*K, radio 8.5*K)
    cx, cy, hr_x, hr_y = 14 * K, 12 * K, int(8.5 * K), int(8.5 * K)
    d.ellipse([cx - hr_x, cy - hr_y, cx + hr_x, cy + hr_y], fill=WHITE_C, outline=INK_C, width=ow)

    # Cabello superior (solo en el tercio superior de la cabeza para dejar libre toda la cara blanca)
    if style != "bald":
        d.chord([cx - hr_x, cy - hr_y, cx + hr_x, cy + hr_y],
                205, 335, fill=hair_c, outline=INK_C, width=ow)
        if style in ("curly", "wavy", "long"):
            for ang_deg in (205, 235, 270, 305, 335):
                rad = math.radians(ang_deg)
                bx = int(cx + math.cos(rad) * (hr_x - K))
                by = int(cy + math.sin(rad) * (hr_y - K))
                d.ellipse([bx - 2 * K, by - 2 * K, bx + 2 * K, by + 2 * K],
                          fill=hair_c, outline=INK_C, width=max(1, ow - 1))

    # Barba cartoon (solo en el borde inferior del mentón)
    beard = spec.get("beard")
    if beard in ("full", "short"):
        bc = (*spec.get("beard_color", hair_c[:3])[:3], 255)
        d.chord([cx - hr_x + K, cy - hr_y + K, cx + hr_x - K, cy + hr_y],
                25, 155, fill=bc, outline=INK_C, width=ow)

    # Ojos circulares grandes expresivos estilo OverSimplified (siempre encima del pelo)
    look = int(pose.get("look", 0))
    blink = pose.get("blink", False)
    ey = cy - int(0.5 * K)
    elx, erx = cx - int(3.0 * K), cx + int(3.0 * K)
    er = int(2.6 * K)
    if blink:
        d.line([(elx - er, ey), (elx + er, ey)], fill=INK_C, width=ow)
        d.line([(erx - er, ey), (erx + er, ey)], fill=INK_C, width=ow)
    else:
        for ex in (elx, erx):
            d.ellipse([ex - er, ey - er, ex + er, ey + er], fill=WHITE_C, outline=INK_C, width=ow)
            px_off = look * K
            pr = max(2, int(1.1 * K))
            d.ellipse([ex + px_off - pr, ey - pr, ex + px_off + pr, ey + pr], fill=INK_C)

    # Anteojos (si tiene)
    if spec.get("glasses"):
        d.ellipse([elx - er - 1, ey - er - 1, elx + er + 1, ey + er + 1], outline=INK_C, width=ow)
        d.ellipse([erx - er - 1, ey - er - 1, erx + er + 1, ey + er + 1], outline=INK_C, width=ow)
        d.line([(elx + er, ey), (erx - er, ey)], fill=INK_C, width=ow)

    # Cejas expresivas
    brows_m = pose.get("brows") or pose.get("mood", "neutral")
    by_top = ey - er - K
    if brows_m == "angry":
        d.line([(elx - 2 * K, by_top - K), (elx + 2 * K, by_top)], fill=INK_C, width=ow)
        d.line([(erx + 2 * K, by_top - K), (erx - 2 * K, by_top)], fill=INK_C, width=ow)
    elif brows_m in ("sad", "worried"):
        d.line([(elx - 2 * K, by_top), (elx + 2 * K, by_top - K)], fill=INK_C, width=ow)
        d.line([(erx + 2 * K, by_top), (erx - 2 * K, by_top - K)], fill=INK_C, width=ow)
    else:
        d.line([(elx - 2 * K, by_top), (elx + 2 * K, by_top)], fill=INK_C, width=ow)
        d.line([(erx - 2 * K, by_top), (erx + 2 * K, by_top)], fill=INK_C, width=ow)

    # Boca cartoon expresiva (con lengua roja al hablar)
    talk = int(pose.get("talk", 0))
    my = cy + int(3.6 * K)
    if talk >= 1:
        mh = int((2.2 if talk == 1 else 3.2) * K)
        d.chord([cx - int(2.6 * K), my - K, cx + int(2.6 * K), my + mh], 0, 180,
                fill=INK_C, outline=INK_C, width=max(1, ow - 1))
        d.ellipse([cx - int(1.3 * K), my + mh - int(1.6 * K), cx + int(1.3 * K), my + mh - 1],
                  fill=(236, 84, 84, 255))
    elif pose.get("frown") or brows_m in ("sad", "angry"):
        d.arc([cx - 2 * K, my, cx + 2 * K, my + 2 * K], 195, 345, fill=INK_C, width=ow)
    else:
        d.arc([cx - 2 * K, my - K, cx + 2 * K, my + 2 * K], 15, 165, fill=INK_C, width=ow)

    im_out = im.resize((SW * scale * 4, SH * scale * 4), Image.LANCZOS)
    arr = np.array(im_out, dtype=np.uint8)
    if pose.get("facing", 1) < 0:
        arr = arr[:, ::-1]
    return arr


def _freeze(d):
    return tuple(sorted((k, tuple(v) if isinstance(v, list) else v) for k, v in d.items()))


def render(spec, t=0.0, **pose):
    """Devuelve un array RGBA (SH, SW, 4) del personaje en la pose pedida.
    Parpadeo automático salvo que se pase blink explícito."""
    seed = (hash(str(spec.get("name", spec.get("jacket", "")))) % 97) / 97.0
    if "blink" not in pose:
        cyc = (t + seed * 3.7) % 3.4
        pose["blink"] = cyc < 0.12
    tq = int(t * 30) if pose.get("arms") in ("type", "write", "note", "work", "wave", "cheer", "up") else 0
    return _render(_freeze(spec), _freeze(pose), tq)


# --------------------------------------------------------------------------- robot

@lru_cache(maxsize=512)
def render_robot(face="happy", tq=0, frozen=False, blink=False, scale_note=0):
    """La Máquina: robot retro de los 50, crema con pantalla CRT verde."""
    W2, H2 = 30, 40
    a = np.zeros((H2, W2, 4), dtype=np.int32)

    def px(x, y, c):
        if 0 <= x < W2 and 0 <= y < H2:
            a[y, x, :3] = c; a[y, x, 3] = 255

    def rect(x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                px(x, y, c)

    body = hexc("e9dfc4") if not frozen else hexc("cfe6f2")
    bd = shade(body, 0.75)
    metal = hexc("8f8778") if not frozen else hexc("9fb8c8")
    scr = hexc("163a26") if not frozen else hexc("4a7a9a")
    glow = hexc("6dfc9a") if not frozen else hexc("e6f6ff")
    t = tq / 30.0
    # antena
    rect(14, 1, 15, 5, metal)
    lamp = hexc("5ff4ff") if (int(t * 3) % 2 == 0 and not frozen) else hexc("2a8a9a")
    rect(13, 0, 16, 1, lamp)
    # cabeza
    rect(5, 5, 24, 18, body)
    rect(20, 5, 24, 18, bd)
    rect(5, 5, 24, 5, tint(body, (255, 255, 255), 0.4))
    rect(7, 7, 21, 16, metal)
    rect(8, 8, 20, 15, scr)
    # scanlines del CRT
    for y in range(8, 16, 2):
        rect(8, y, 20, y, shade(scr, 1.25))
    # cara en pantalla
    if face == "happy" or face == "talk":
        if blink:
            rect(10, 11, 12, 11, glow); rect(16, 11, 18, 11, glow)
        else:
            rect(11, 10, 12, 12, glow); rect(16, 10, 17, 12, glow)
        if face == "talk" and int(t * 8) % 2:
            rect(12, 13, 16, 14, glow)
        else:
            px(11, 13, glow); rect(12, 14, 16, 14, glow); px(17, 13, glow)
    elif face == "question":
        rect(12, 9, 16, 9, glow); px(17, 10, glow); px(16, 11, glow); px(15, 12, glow)
        px(14, 12, glow); px(14, 14, glow)
    elif face == "think":
        rect(10, 11, 12, 11, glow); rect(16, 11, 18, 11, glow)
        for i in range(3):
            if int(t * 4) % 3 >= i:
                px(11 + i * 3, 14, glow)
    elif face == "sad":
        rect(11, 10, 12, 11, glow); rect(16, 10, 17, 11, glow)
        rect(12, 13, 16, 13, glow); px(11, 14, glow); px(17, 14, glow)
    elif face == "off":
        pass
    elif face == "heart":
        for (x, y) in [(11, 10), (12, 10), (16, 10), (17, 10), (10, 11), (13, 11), (15, 11), (18, 11),
                       (10, 12), (14, 12), (18, 12), (11, 13), (17, 13), (12, 14), (16, 14), (13, 15), (15, 15), (14, 15)]:
            px(x, y, hexc("ff6a8a"))
    # orejas/bulones
    rect(3, 9, 4, 13, metal); rect(25, 9, 26, 13, metal)
    # cuello
    rect(12, 19, 17, 20, metal)
    # cuerpo
    rect(6, 21, 23, 33, body)
    rect(19, 21, 23, 33, bd)
    rect(6, 21, 23, 21, tint(body, (255, 255, 255), 0.4))
    # lámparas del pecho
    cols = [hexc("ff5a4a"), hexc("ffd24a"), hexc("5aff8a")]
    for i, c in enumerate(cols):
        on = (int(t * 5) + i) % 3 != 0 and not frozen
        rect(9 + i * 4, 24, 10 + i * 4, 25, c if on else shade(c, 0.4))
    rect(9, 28, 18, 29, metal)
    for x in range(9, 19, 2):
        px(x, 28, shade(metal, 0.6))
    # brazos
    rect(2, 22, 4, 30, metal); rect(25, 22, 27, 30, shade(metal, 0.8))
    rect(1, 31, 4, 32, bd); rect(25, 31, 28, 32, bd)
    # ruedas/orugas
    rect(6, 34, 23, 38, hexc("3a342e"))
    for x in range(7, 23, 3):
        px(x + (tq // 3) % 3, 36, hexc("6a625a"))
    # contorno
    alpha = a[:, :, 3] > 0
    out = a.copy()
    for y in range(H2):
        for x in range(W2):
            if alpha[y, x]:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                xx, yy = x + dx, y + dy
                if 0 <= xx < W2 and 0 <= yy < H2 and alpha[yy, xx]:
                    out[y, x, :3] = OUTLINE; out[y, x, 3] = 255
                    break
    if frozen:  # bloque de hielo
        ice = out.copy()
        for y in range(H2):
            for x in range(W2):
                if 0 < x < W2 - 1 and 1 < y < H2 - 1:
                    base = ice[y, x, :3] if ice[y, x, 3] else np.array([160, 210, 240])
                    ice[y, x, :3] = (base * 0.55 + np.array([190, 230, 255]) * 0.45).astype(np.int32)
                    ice[y, x, 3] = 255 if out[y, x, 3] else 150
        for i in range(0, 30, 6):
            ice[2 + i // 3, 2 + i // 2, :3] = (255, 255, 255)
        out = ice
    return out.astype(np.uint8)


# --------------------------------------------------------------------------- reparto

C = hexc
CAST = {
    # ---- Apertura / Capítulo 1
    "turing": dict(name="Alan Turing", skin=SKIN["fair"], hair=C("4a2e1c"), hair_style="wavy",
                   top="suit", top_color=C("7a5a3a"), shirt=C("efeadc"), tie=C("2a2420"), pants=C("4e3e30")),
    "mccarthy": dict(name="John McCarthy", skin=SKIN["fair"], hair=C("2a2226"), hair_style="slick",
                     glasses="black", top="shirt", top_color=C("eeeae2"), tie=C("1e2a44"), pants=C("4a4a52")),
    "minsky": dict(name="Marvin Minsky", skin=SKIN["light"], hair=C("8a5a34"), hair_style="recede",
                   glasses="round", top="vest", top_color=C("8e8a78"), shirt=C("a8c0dc"), pants=C("4a4440")),
    "shannon": dict(name="Claude Shannon", skin=SKIN["fair"], hair=C("3a2c24"), hair_style="slick",
                    top="suit", top_color=C("8a8c90"), shirt=C("f0eee8"), tie=C("22386a"), pants=C("6a6c70")),
    "rochester": dict(name="Nathaniel Rochester", skin=SKIN["fair"], hair=C("2a2024"), hair_style="recede",
                      glasses="black", top="suit", top_color=C("26304e"), shirt=C("f0eee8"), tie=C("7a2030"),
                      pants=C("1e2640")),
    # los otros seis asistentes de Dartmouth (completan las "diez personas")
    "solomonoff": dict(name="Ray Solomonoff", skin=SKIN["light"], hair=C("2e2a28"), hair_style="short",
                       glasses="black", top="shirt", top_color=C("d8cba8"), pants=C("5a5040")),
    "selfridge": dict(name="Oliver Selfridge", skin=SKIN["light"], hair=C("6a4a2a"), hair_style="side",
                      top="suit", top_color=C("5a6a5a"), tie=C("8a6a2a"), pants=C("3a4a3a")),
    "more": dict(name="Trenchard More", skin=SKIN["fair"], hair=C("b08a52"), hair_style="crew",
                 top="sweater", top_color=C("7a3a3a"), pants=C("4a4440")),
    "samuel": dict(name="Arthur Samuel", skin=SKIN["light"], hair=C("b8b4ac"), hair_style="recede",
                   glasses="wire", top="suit", top_color=C("4a4a5a"), tie=C("6a2a2a"), pants=C("3a3a46")),
    "newell": dict(name="Allen Newell", skin=SKIN["fair"], hair=C("3a2a1e"), hair_style="side",
                   top="shirt", top_color=C("9ab4c8"), tie=C("2a2a3a"), pants=C("5a5248")),
    "simon": dict(name="Herbert Simon", skin=SKIN["light"], hair=C("4a3a30"), hair_style="recede",
                  glasses="black", top="suit", top_color=C("6a5a48"), tie=C("2a3a5a"), pants=C("4a3e34")),
    # jurado del juego de la imitación
    "judge": dict(name="Interrogador", skin=SKIN["tan"], hair=C("1e1a1a"), hair_style="side",
                  top="sweater", top_color=C("3a5a7a"), pants=C("3a3a40")),
    "human_b": dict(name="Persona", skin=SKIN["fair"], hair=C("6a3a1e"), hair_style="bun",
                    top="shirt", top_color=C("c87a6a"), skirt=True, skirt_color=C("4a4a6a"), pants=C("4a4a6a")),
    # ---- Capítulo 2
    "rosenblatt": dict(name="Frank Rosenblatt", skin=SKIN["fair"], hair=C("2a2020"), hair_style="wavy",
                       top="suit", top_color=C("4a4a50"), tie=C("141418"), pants=C("3a3a40")),
    "navy": dict(name="Oficial de la Marina", skin=SKIN["fair"], hair=C("3a3030"), hair_style="short",
                 top="uniform", top_color=C("1e2a4a"), shirt=C("f0eee8"), tie=C("141418"), pants=C("1a2440"),
                 hat="navy"),
    "reporter": dict(name="Periodista (NYT)", skin=SKIN["fair"], hair=C("4a3020"), hair_style="short",
                     mustache=True, top="trench", top_color=C("bca77e"), shirt=C("f0eee8"), tie=C("6a2a2a"),
                     pants=C("5a5040"), hat="fedora"),
    "papert": dict(name="Seymour Papert", skin=SKIN["fair"], hair=C("2a2020"), hair_style="wavy",
                   beard="full", top="blazer", top_color=C("7a5a3a"), shirt=C("e8e0c8"), pants=C("4a4038")),
    # ---- Capítulo 3
    "minsky70": dict(name="Marvin Minsky (1970)", skin=SKIN["light"], hair=C("8a6a4a"), hair_style="bald",
                     glasses="black", top="turtleneck", top_color=C("5a4030"), pants=C("3a3430")),
    "lighthill": dict(name="James Lighthill", skin=SKIN["light"], hair=C("8a7a6a"), hair_style="recede",
                      top="suit", top_color=C("2e2e36"), tie=C("6a2a3a"), pants=C("26262e")),
    "darpa": dict(name="Funcionario DARPA", skin=SKIN["fair"], hair=C("9a9a9a"), hair_style="crew",
                  glasses="black", top="suit", top_color=C("4a4c52"), tie=C("1e2030"), pants=C("3a3c42")),
    # ---- Capítulo 4
    "kengineer": dict(name="Ingeniero del conocimiento", skin=SKIN["fair"], hair=C("6a4428"), hair_style="side",
                      glasses="black", mustache=True, top="shirt", top_color=C("a8c4e0"), tie=C("6a3a2a"),
                      pants=C("6a5a40")),
    "rumelhart": dict(name="David Rumelhart", skin=SKIN["fair"], hair=C("6a4a2a"), hair_style="recede",
                      beard="short", top="shirt", top_color=C("8a3a2a"), pants=C("3a3a4a")),
    "hinton86": dict(name="Geoffrey Hinton (1986)", skin=SKIN["light"], hair=C("4a3424"), hair_style="side",
                     top="sweater", top_color=C("22305a"), shirt=C("e8e4dc"), pants=C("4a4440")),
    "williams": dict(name="Ronald Williams", skin=SKIN["fair"], hair=C("2e2620"), hair_style="short",
                     mustache=True, glasses="wire", top="blazer", top_color=C("a88a5a"), shirt=C("e8e0c8"),
                     pants=C("4a3e30")),
    # ---- Capítulo 5
    "kasparov": dict(name="Garry Kasparov", skin=SKIN["fair"], hair=C("1e1818"), hair_style="curly",
                     top="suit", top_color=C("1e1e26"), tie=C("3a2a4a"), pants=C("18181e")),
    "ibm_op": dict(name="Operador de Deep Blue", skin=SKIN["asian"], hair=C("141418"), hair_style="side",
                   glasses="black", top="blazer", top_color=C("1f4fa0"), shirt=C("e8eef8"), pants=C("2a2a34")),
    "feifei": dict(name="Fei-Fei Li", skin=SKIN["asian"], hair=C("141016"), hair_style="bangs",
                   top="blazer", top_color=C("2a2a36"), shirt=C("e8e4f0"), skirt=False, pants=C("26262e")),
    "krizhevsky": dict(name="Alex Krizhevsky", skin=SKIN["light"], hair=C("2a2020"), hair_style="short",
                       beard="stubble", top="hoodie", top_color=C("6a6c72"), pants=C("2a3a5a")),
    "sutskever": dict(name="Ilya Sutskever", skin=SKIN["light"], hair=C("2a2020"), hair_style="recede",
                      top="tshirt", top_color=C("1e1e22"), pants=C("2a3a5a")),
    "hinton12": dict(name="Geoffrey Hinton (2012)", skin=SKIN["light"], hair=C("c8c4bc"), hair_style="side",
                     top="sweater", top_color=C("2a2a3a"), shirt=C("dcd8d0"), pants=C("3a3a40")),
    # ---- Capítulo 6
    "leesedol": dict(name="Lee Sedol", skin=SKIN["asian"], hair=C("141016"), hair_style="fringe",
                     top="suit", top_color=C("1e1e26"), shirt=C("f0f0f0"), pants=C("18181e")),
    "ajahuang": dict(name="Aja Huang", skin=SKIN["asian"], hair=C("141016"), hair_style="short",
                     glasses="black", top="suit", top_color=C("22222a"), shirt=C("f0f0f0"), pants=C("1a1a22")),
    # ---- Capítulo 7
    "googler": dict(name="Investigador/a de Google", skin=SKIN["tan"], hair=C("1a1414"), hair_style="short", beard="short",
                    top="tshirt", top_color=C("3a7ad8"), pants=C("2a3a5a")),
    "altman": dict(name="Sam Altman", skin=SKIN["fair"], hair=C("8a6a3e"), hair_style="side",
                   top="sweater", top_color=C("3a3c44"), shirt=C("f0f0f0"), pants=C("262a36")),
    "user": dict(name="Usuaria de ChatGPT", skin=SKIN["brown"], hair=C("1a1414"), hair_style="curly", skirt=False,
                 top="hoodie", top_color=C("10a37f"), pants=C("2a2a34")),
    # ---- Capítulo 8
    "hopfield": dict(name="John Hopfield", skin=SKIN["light"], hair=C("eeeae4"), hair_style="bald",
                     mustache=True, mustache_color=C("eeeae4"), glasses="wire", top="suit",
                     top_color=C("7a6a50"), tie=C("3a2a2a"), pants=C("4a4034")),
    "hinton24": dict(name="Geoffrey Hinton (2024)", skin=SKIN["light"], hair=C("eeece8"), hair_style="side",
                     top="suit", top_color=C("1e2230"), shirt=C("f4f4f4"), pants=C("1a1e2a")),
    "hassabis": dict(name="Demis Hassabis", skin=SKIN["olive"], hair=C("2a2220"), hair_style="crew",
                     top="blazer", top_color=C("1e2440"), shirt=C("141418"), pants=C("1a1e30")),
    "jumper": dict(name="John Jumper", skin=SKIN["light"], hair=C("6a4a2a"), hair_style="short",
                   beard="short", glasses="black", top="shirt", top_color=C("9ab8dc"), pants=C("3a3a46")),
    "baker": dict(name="David Baker", skin=SKIN["light"], hair=C("a8a49c"), hair_style="short",
                  glasses="black", top="blazer", top_color=C("2a2a34"), shirt=C("6a8aa8"), pants=C("26262e")),
    # ---- El dibujo que encendió el mundo (Nikola Tesla)
    "inventor": dict(name="Inventor", skin=SKIN["light"], hair=C("1c1820"), hair_style="slick",
                     mustache=True, top="suit", top_color=C("1c2030"), shirt=C("f2f0e8"), tie=C("283454"),
                     pants=C("161824")),
    "inventor_hat": dict(name="Inventor (sombrero)", skin=SKIN["light"], hair=C("1c1820"), hair_style="slick",
                         mustache=True, top="suit", top_color=C("1c2030"), shirt=C("f2f0e8"), tie=C("283454"),
                         pants=C("161824"), hat="fedora"),
    "inventor_ditch": dict(name="Inventor (zanja)", skin=SKIN["light"], hair=C("1c1820"), hair_style="slick",
                           mustache=True, top="trench", top_color=C("4e463e"), shirt=C("d8d2c4"), tie=C("2a2622"),
                           pants=C("34302c")),
    "inventor_old": dict(name="Inventor mayor", skin=SKIN["light"], hair=C("d8dce4"), hair_style="recede",
                         top="suit", top_color=C("222636"), shirt=C("eceae2"), tie=C("384464"),
                         pants=C("1a1d2a")),
    "boy_tesla": dict(name="Chico", skin=SKIN["light"], hair=C("241c18"), hair_style="short",
                      top="vest", top_color=C("52688a"), shirt=C("efeadd"), pants=C("323846")),
    "mother_tesla": dict(name="Madre", skin=SKIN["fair"], hair=C("4e3222"), hair_style="bun",
                         top="shirt", top_color=C("9e4e64"), skirt=True, skirt_color=C("583448"), pants=C("583448")),
    "midwife": dict(name="Partera", skin=SKIN["light"], hair=C("98948c"), hair_style="bun",
                    top="shirt", top_color=C("dfd9cc"), skirt=True, skirt_color=C("646c7c"), pants=C("646c7c")),
    "father_tesla": dict(name="Padre", skin=SKIN["fair"], hair=C("3c2e24"), hair_style="recede",
                         beard="full", top="suit", top_color=C("2c2c38"), shirt=C("e8e4da"), pants=C("22222c")),
    "prof_graz": dict(name="Profesor", skin=SKIN["light"], hair=C("8c867e"), hair_style="recede",
                      glasses="wire", beard="short", top="suit", top_color=C("463c34"), shirt=C("efeadd"),
                      tie=C("5a2626"), pants=C("342c26")),
    "student_a": dict(name="Estudiante", skin=SKIN["fair"], hair=C("5a3c26"), hair_style="side",
                      top="blazer", top_color=C("445268"), shirt=C("ece8dc"), pants=C("323844")),
    "student_b": dict(name="Estudiante", skin=SKIN["light"], hair=C("2e241e"), hair_style="short",
                      top="vest", top_color=C("685442"), shirt=C("ece8dc"), pants=C("3c342e")),
    "friend_budapest": dict(name="Amigo", skin=SKIN["fair"], hair=C("5c3e26"), hair_style="side",
                            mustache=True, top="suit", top_color=C("68503c"), shirt=C("efeadd"), tie=C("782c2c"),
                            pants=C("48382a")),
    "edison_gen": dict(name="Empresario continua", skin=SKIN["fair"], hair=C("786c60"), hair_style="side",
                       top="vest", top_color=C("46423e"), shirt=C("f0ece2"), tie=C("282422"), pants=C("32302e")),
    "worker_a": dict(name="Obrero", skin=SKIN["tan"], hair=C("3a2a1e"), hair_style="crew",
                     mustache=True, top="shirt", top_color=C("6e7e90"), pants=C("42464e")),
    "worker_b": dict(name="Obrero", skin=SKIN["fair"], hair=C("543824"), hair_style="short",
                     top="vest", top_color=C("745c46"), shirt=C("d8d0c0"), pants=C("463e36")),
    "foreman": dict(name="Jefe de obra", skin=SKIN["tan"], hair=C("463222"), hair_style="short",
                    mustache=True, top="blazer", top_color=C("7e5a38"), shirt=C("e8e0d0"), pants=C("4a3c30"),
                    hat="fedora"),
    "investor_a": dict(name="Inversor", skin=SKIN["light"], hair=C("64605c"), hair_style="recede",
                       mustache=True, top="suit", top_color=C("2c3242"), shirt=C("f0eee6"), tie=C("6a242c"),
                       pants=C("222634")),
    "investor_b": dict(name="Inversor", skin=SKIN["fair"], hair=C("8a847c"), hair_style="side",
                       glasses="wire", top="suit", top_color=C("3c3632"), shirt=C("f0eee6"), tie=C("283c58"),
                       pants=C("2c2826")),
    "investor_c": dict(name="Inversor", skin=SKIN["light"], hair=C("4e4238"), hair_style="slick",
                       beard="short", top="suit", top_color=C("2e3c38"), shirt=C("f0eee6"), tie=C("584426"),
                       pants=C("222c2a")),
    "westinghouse_gen": dict(name="Empresario alterna", skin=SKIN["fair"], hair=C("584638"), hair_style="side",
                             beard="short", mustache=True, top="suit", top_color=C("2c384e"), shirt=C("f2f0e8"),
                             tie=C("742830"), pants=C("202838")),
    "president_1893": dict(name="Presidente", skin=SKIN["fair"], hair=C("6e665e"), hair_style="recede",
                           mustache=True, top="suit", top_color=C("1e202a"), shirt=C("f4f2ec"), tie=C("2a2c38"),
                           pants=C("181a22")),
    "writer_twain": dict(name="Escritor", skin=SKIN["light"], hair=C("e4e2dc"), hair_style="wavy",
                         mustache=True, mustache_color=C("e4e2dc"), top="suit", top_color=C("b8b0a0"),
                         shirt=C("f4f2ec"), tie=C("3a342e"), pants=C("9e9688")),
    "banker_morgan": dict(name="Banquero", skin=SKIN["fair"], hair=C("a8a49e"), hair_style="bald",
                          mustache=True, top="suit", top_color=C("20222e"), shirt=C("f4f2ec"), tie=C("5e2228"),
                          pants=C("181a24")),
    "marconi_op": dict(name="Operador", skin=SKIN["fair"], hair=C("342820"), hair_style="side",
                       top="vest", top_color=C("3e4e62"), shirt=C("eae6dc"), tie=C("242c38"), pants=C("2c3644")),
    "organizer": dict(name="Organizador", skin=SKIN["light"], hair=C("423832"), hair_style="slick",
                      glasses="wire", top="suit", top_color=C("202432"), shirt=C("f4f2ec"), tie=C("685224"),
                      pants=C("181c26")),
    "tech_modern": dict(name="Técnico", skin=SKIN["fair"], hair=C("2c2420"), hair_style="short",
                        top="shirt", top_color=C("4a88b8"), pants=C("2e3846")),
    # ---- Línea por línea (La historia de la televisión)
    "farnsworth_boy": dict(name="Philo Farnsworth (14)", skin=SKIN["fair"], hair=C("6e4c2e"), hair_style="side",
                           top="vest", top_color=C("466284"), shirt=C("efeadd"), pants=C("384c68")),
    "farnsworth_young": dict(name="Philo Farnsworth", skin=SKIN["fair"], hair=C("6e4c2e"), hair_style="side",
                             top="vest", top_color=C("54463a"), shirt=C("f4f0e6"), tie=C("2c4870"), pants=C("38322e")),
    "farnsworth_older": dict(name="Philo Farnsworth (1957)", skin=SKIN["fair"], hair=C("9e9890"), hair_style="recede",
                             top="suit", top_color=C("383e4e"), shirt=C("f4f2ec"), tie=C("782c32"), pants=C("282c38")),
    "pem": dict(name="Pem Farnsworth", skin=SKIN["fair"], hair=C("5c3824"), hair_style="wavy",
                top="shirt", top_color=C("d86e62"), skirt=True, skirt_color=C("3e4864"), pants=C("3e4864")),
    "nipkow": dict(name="Paul Nipkow", skin=SKIN["light"], hair=C("4e3824"), hair_style="side",
                   glasses="wire", mustache=True, top="suit", top_color=C("363242"), shirt=C("efeadd"),
                   tie=C("6a2c2c"), pants=C("262430")),
    "baird": dict(name="John Logie Baird", skin=SKIN["light"], hair=C("785232"), hair_style="wavy",
                  glasses="round", top="vest", top_color=C("68523e"), shirt=C("f0ece0"), tie=C("2c4258"),
                  pants=C("42362c")),
    "taynton": dict(name="William Taynton", skin=SKIN["fair"], hair=C("543a24"), hair_style="short",
                    top="shirt", top_color=C("e8e4d8"), tie=C("3a5274"), pants=C("383c48")),
    "tolman": dict(name="Profesor Justin Tolman", skin=SKIN["light"], hair=C("7c746c"), hair_style="recede",
                   glasses="wire", top="suit", top_color=C("484038"), shirt=C("f2eee4"), tie=C("5c2828"),
                   pants=C("342e28")),
    "sarnoff": dict(name="David Sarnoff (RCA)", skin=SKIN["fair"], hair=C("221e24"), hair_style="slick",
                    top="suit", top_color=C("1c2234"), shirt=C("f4f2ec"), tie=C("8c242c"), pants=C("161a28")),
    "zworykin": dict(name="Vladimir Zworykin", skin=SKIN["light"], hair=C("7e766e"), hair_style="recede",
                     glasses="round", top="suit", top_color=C("464a56"), shirt=C("f2f0e8"), tie=C("284064"),
                     pants=C("323640")),
    "tv_host": dict(name="Conductor TV (1957)", skin=SKIN["fair"], hair=C("322822"), hair_style="crew",
                    glasses="black", top="suit", top_color=C("282c38"), shirt=C("f6f4f0"), tie=C("c43c3c"),
                    pants=C("1e222c")),
    "panelist": dict(name="Panelista Famosa", skin=SKIN["fair"], hair=C("d8b25c"), hair_style="wavy",
                     top="shirt", top_color=C("4688a8"), skirt=True, skirt_color=C("2c4862"), pants=C("2c4862")),
    "astronaut": dict(name="Astronauta (Apolo 11)", skin=SKIN["fair"], hair=C("3a2e24"), hair_style="short",
                      top="suit", top_color=C("e8ecf2"), shirt=C("cfd6e2"), pants=C("dcdce4"), hat="helmet"),
    # ---- El empleado número cero (La historia de Apple)
    "mike_scott": dict(name="Mike Scott", skin=SKIN["light"], hair=C("5a3c26"), hair_style="side",
                       glasses="wire", beard="short", top="suit", top_color=C("9e8868"), shirt=C("f4f0e4"),
                       tie=C("8c382c"), pants=C("685842")),
    "jobs_1977": dict(name="Socio #0 (1977)", skin=SKIN["fair"], hair=C("281e1a"), hair_style="long",
                      beard="stubble", top="vest", top_color=C("785238"), shirt=C("e8dec8"), pants=C("324664")),
    "wozniak_1977": dict(name="Ingeniero #1 (1977)", skin=SKIN["light"], hair=C("4a3222"), hair_style="wavy",
                         beard="full", top="shirt", top_color=C("5482a8"), pants=C("384454")),
    "jobs_teen": dict(name="Joven Socio (1971)", skin=SKIN["fair"], hair=C("281e1a"), hair_style="long",
                      top="tshirt", top_color=C("c86838"), pants=C("344a6c")),
    "wozniak_teen": dict(name="Joven Ingeniero (1971)", skin=SKIN["light"], hair=C("4a3222"), hair_style="wavy",
                         top="shirt", top_color=C("4678a2"), pants=C("3a4252")),
    "vatican_guard": dict(name="Asistente Vaticano", skin=SKIN["light"], hair=C("68625c"), hair_style="recede",
                          top="suit", top_color=C("5a222c"), shirt=C("f4f0e6"), tie=C("d4a84c"), pants=C("381820")),
    "atari_tech": dict(name="Técnico Atari", skin=SKIN["fair"], hair=C("6a4a2e"), hair_style="side",
                       glasses="black", top="shirt", top_color=C("d8a448"), pants=C("4a3c30")),
    "bushnell": dict(name="Nolan Bushnell", skin=SKIN["fair"], hair=C("5c3e26"), hair_style="wavy",
                     beard="full", top="shirt", top_color=C("c45c32"), pants=C("3c342c")),
    "ronald_wayne": dict(name="Ronald Wayne", skin=SKIN["light"], hair=C("8a847c"), hair_style="recede",
                         glasses="wire", mustache=True, top="suit", top_color=C("4e4842"), shirt=C("f2eee4"),
                         tie=C("68322c"), pants=C("383430")),
    "clerk_1976": dict(name="Empleado Oficina", skin=SKIN["light"], hair=C("423832"), hair_style="side",
                       glasses="wire", top="vest", top_color=C("465468"), shirt=C("f0ece0"), tie=C("782c2c"),
                       pants=C("323a46")),
    "fair_visitor": dict(name="Visitante Feria", skin=SKIN["tan"], hair=C("32241c"), hair_style="short",
                         top="blazer", top_color=C("466854"), shirt=C("efeadd"), pants=C("343c38")),
    "mac_coder": dict(name="Programador Mac", skin=SKIN["fair"], hair=C("4e3624"), hair_style="wavy",
                      glasses="black", top="sweater", top_color=C("385a88"), shirt=C("f0eee6"), pants=C("2e3846")),
    "susan_kare": dict(name="Susan Kare", skin=SKIN["fair"], hair=C("34241e"), hair_style="wavy",
                       top="sweater", top_color=C("b84a62"), shirt=C("f4f0e8"), skirt=True, skirt_color=C("323a50"),
                       pants=C("323a50")),
    "lawyer_london": dict(name="Abogado", skin=SKIN["light"], hair=C("78746e"), hair_style="slick",
                          glasses="wire", top="suit", top_color=C("262a36"), shirt=C("f4f4f0"), tie=C("7a242c"),
                          pants=C("1c202a")),
    "jim_reekes": dict(name="Jim Reekes", skin=SKIN["fair"], hair=C("6e4e32"), hair_style="wavy",
                       top="shirt", top_color=C("3e7a8c"), pants=C("2e3644")),
    "jobs_1997": dict(name="Presentador (1997-2007)", skin=SKIN["fair"], hair=C("585450"), hair_style="short",
                      beard="short", top="blazer", top_color=C("24344e"), shirt=C("dce4f0"), pants=C("2a3852")),
    "security_chief": dict(name="Jefe de Seguridad", skin=SKIN["tan"], hair=C("38322e"), hair_style="crew",
                           top="uniform", top_color=C("283448"), shirt=C("e8ecf2"), tie=C("1c2434"), pants=C("1e2636")),
    "iphone_eng": dict(name="Ingeniero 2007", skin=SKIN["light"], hair=C("3a2c22"), hair_style="short",
                       glasses="black", top="shirt", top_color=C("4a6e94"), pants=C("2c3442")),
    "tim_cook": dict(name="Tim Cook", skin=SKIN["light"], hair=C("dcdce2"), hair_style="side",
                     glasses="wire", top="sweater", top_color=C("222c42"), shirt=C("e8ecf4"), pants=C("282c36")),
    "mccartney_2026": dict(name="Músico Mayor (2026)", skin=SKIN["light"], hair=C("c8c6c0"), hair_style="wavy",
                           top="blazer", top_color=C("1e2436"), shirt=C("f2f0ec"), pants=C("181c2a")),
    "john_ternus": dict(name="John Ternus", skin=SKIN["fair"], hair=C("2c2828"), hair_style="short",
                        top="shirt", top_color=C("28588c"), pants=C("262c38")),
    # ---- Un chico llamado Baron Trump (Stickman Histórico 2D)
    "lockwood": dict(name="Ingersoll Lockwood", skin=SKIN["light"], hair=C("5a3e28"), hair_style="side",
                     mustache=True, top="suit", top_color=C("2c2420"), shirt=C("f4f0e4"),
                     tie=C("7a2626"), pants=C("201a18")),
    "baron_boy": dict(name="Baron Trump (libro)", skin=SKIN["light"], hair=C("9a7238"), hair_style="wavy",
                      top="vest", top_color=C("7a2632"), shirt=C("f6f2e8"), tie=C("22385c"),
                      pants=C("2a2630")),
    "don_fum": dict(name="Don Fum (sabio)", skin=SKIN["light"], hair=C("dcd8d0"), hair_style="long",
                    beard="full", top="trench", top_color=C("3a3248"), shirt=C("ece6d8"),
                    pants=C("282234")),
    "passerby_a": dict(name="Transeúnte 1893", skin=SKIN["fair"], hair=C("3e2e24"), hair_style="short",
                       mustache=True, top="trench", top_color=C("6a5a48"), shirt=C("efeadd"),
                       tie=C("3a2a24"), pants=C("443a30"), hat="fedora"),
    "passerby_b": dict(name="Transeúnte 1893", skin=SKIN["fair"], hair=C("4a2e20"), hair_style="bun",
                       top="shirt", top_color=C("8a5a64"), skirt=True, skirt_color=C("3a3444"),
                       pants=C("3a3444")),
    "mob_a": dict(name="Manifestante 1896", skin=SKIN["fair"], hair=C("3a2a20"), hair_style="crew",
                  mustache=True, top="vest", top_color=C("5a4434"), shirt=C("e8dfd0"), pants=C("382e26")),
    "mob_b": dict(name="Manifestante 1896", skin=SKIN["tan"], hair=C("2a2220"), hair_style="short",
                  top="shirt", top_color=C("786a5a"), pants=C("3a3430"), hat="fedora"),
    "agent_a": dict(name="Agente 1943", skin=SKIN["light"], hair=C("262224"), hair_style="slick",
                    top="trench", top_color=C("262c3a"), shirt=C("f0eee8"), tie=C("181c26"),
                    pants=C("1e222e"), hat="fedora"),
    "agent_b": dict(name="Agente 1943", skin=SKIN["fair"], hair=C("3a322e"), hair_style="short",
                    top="suit", top_color=C("2e3442"), shirt=C("f0eee8"), tie=C("5a2228"),
                    pants=C("222632"), hat="fedora"),
    "engineer_mit": dict(name="Ingeniero MIT", skin=SKIN["light"], hair=C("4a4440"), hair_style="side",
                         glasses="wire", top="suit", top_color=C("323c4e"), shirt=C("f2f0e8"),
                         tie=C("263a5a"), pants=C("242c3a")),
    "einstein": dict(name="Albert Einstein", skin=SKIN["light"], hair=C("eceae4"), hair_style="wavy",
                     mustache=True, mustache_color=C("eceae4"), top="sweater", top_color=C("3a3c44"),
                     shirt=C("f2f0e8"), pants=C("2c2e36")),
    "astronaut_a": dict(name="Astronauta A", skin=SKIN["light"], hair=C("4a3828"), hair_style="crew",
                        top="suit", top_color=C("eef2f8"), shirt=C("cfd8e6"), pants=C("dce2ec"), hat="helmet"),
    "astronaut_b": dict(name="Astronauta B", skin=SKIN["light"], hair=C("4a3828"), hair_style="crew",
                        top="suit", top_color=C("426898"), shirt=C("eef2f8"), pants=C("2a4262")),
    "traveler_past": dict(name="Viajero del tiempo", skin=SKIN["light"], hair=C("2e2836"), hair_style="side",
                          glasses="round", top="blazer", top_color=C("2c6e8a"), shirt=C("f4f2ec"),
                          pants=C("223a4a")),
    "grandpa_past": dict(name="Abuelo joven", skin=SKIN["fair"], hair=C("5c422c"), hair_style="side",
                         top="vest", top_color=C("6a523c"), shirt=C("efeadd"), tie=C("7a2c2c"), pants=C("42362c")),
    "grandma_past": dict(name="Abuela joven", skin=SKIN["fair"], hair=C("6e4428"), hair_style="bun",
                         top="shirt", top_color=C("c46e74"), skirt=True, skirt_color=C("3c4864"), pants=C("3c4864")),
}

DARTMOUTH_TEN = ["mccarthy", "minsky", "shannon", "rochester", "solomonoff",
                 "selfridge", "more", "samuel", "newell", "simon"]
