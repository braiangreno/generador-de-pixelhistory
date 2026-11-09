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
OUTLINE = np.array([22, 14, 28], dtype=np.int32)


def hexc(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def shade(c, f):
    return tuple(int(max(0, min(255, v * f))) for v in c)


def tint(c, t, k):
    return tuple(int(a + (b - a) * k) for a, b in zip(c, t))


SKIN = {
    "light": hexc("f2c4a0"), "fair": hexc("eab48c"), "tan": hexc("d49a6a"),
    "olive": hexc("c98d5e"), "brown": hexc("a0673f"), "asian": hexc("efc39b"),
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
    # pierna izquierda
    L.rect(9, 32, 13, 46 - max(0, -lo), pants)
    L.rect(9 + lo, 40, 13 + lo, 46 - max(0, -lo), pants)
    # pierna derecha (sombra)
    L.rect(14, 32, 18, 46 - max(0, -ro), pd)
    L.rect(14 + ro, 40, 18 + ro, 46 - max(0, -ro), pd)
    L.rect(13, 32, 14, 37, shade(pants, 0.6))  # entrepierna
    # zapatos
    L.rect(8 + lo, 47 - max(0, -lo), 13 + lo, 49 - max(0, -lo), shoe)
    L.rect(14 + ro, 47 - max(0, -ro), 19 + ro, 49 - max(0, -ro), shoe)
    L.px(9 + lo, 47 - max(0, -lo), shade(shoe, 1.8))
    L.px(15 + ro, 47 - max(0, -ro), shade(shoe, 1.8))
    return L.outline()


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
    # --- cara
    blink = pose.get("blink", False)
    eye = hexc("1e1420")
    ey = 10
    lx, rx = 11, 16
    look = pose.get("look", 0)
    if blink:
        L.px(lx + look, ey + 1, sdd); L.px(lx + 1 + look, ey + 1, sdd)
        L.px(rx + look, ey + 1, sdd); L.px(rx + 1 + look, ey + 1, sdd)
    else:
        L.rect(lx + look, ey, lx + look, ey + 1, eye)
        L.rect(rx + look, ey, rx + look, ey + 1, eye)
        L.px(lx + 1 + look, ey, hexc("f6f2ea")) if spec.get("big_eyes") else None
    # cejas
    brow = shade(hair if style != "bald" else hexc("6a5040"), 0.85)
    mood = pose.get("mood", "neutral")
    if mood == "worried":
        L.px(lx - 1, ey - 1, brow); L.px(lx, ey - 2, brow)
        L.px(rx + 1, ey - 1, brow); L.px(rx, ey - 2, brow)
    else:
        L.rect(lx - 1, ey - 2, lx, ey - 2, brow)
        L.rect(rx, ey - 2, rx + 1, ey - 2, brow)
    # nariz
    L.px(14, 12, sdd); L.px(13, 12, sd)
    # mejillas
    if spec.get("blush", True):
        L.px(9, 13, tint(skin, (230, 110, 110), 0.25)); L.px(18, 13, tint(sd, (230, 110, 110), 0.2))
    # boca
    talk = pose.get("talk", 0)
    mouth = shade(skin, 0.45)
    if beard != "full":
        if talk == 2:
            L.rect(13, 14, 14, 15, hexc("5a2028")); L.px(13, 14, hexc("f0e8e0"))
        elif talk == 1:
            L.rect(13, 14, 14, 14, hexc("5a2028"))
        elif mood == "happy":
            L.px(12, 14, mouth); L.rect(13, 15, 14, 15, mouth); L.px(15, 14, mouth)
        elif mood == "sad":
            L.px(12, 15, mouth); L.rect(13, 14, 14, 14, mouth); L.px(15, 15, mouth)
        else:
            L.rect(13, 14, 14, 14, mouth)
    elif talk:
        L.rect(13, 14, 14, 14 + (talk == 2), hexc("3a1a1a"))
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
    elif arms == "write":
        j = round(math.sin(t * 9) * 1.5)
        hl, hr = (8, 30), (17 + j, 27)
    elif arms == "wave":
        j = round(math.sin(t * 10) * 2)
        hl, hr = (6, 31), (25 + j, 11)
    elif arms == "point":
        hl, hr = (6, 31), (27, 20)
    elif arms == "point_l":
        hl, hr = (0, 20), (21, 31)
    elif arms == "cheer":
        j = round(math.sin(t * 12) * 1.5)
        hl, hr = (3, 9 + j), (24, 9 - j)
    elif arms == "hold":
        hl, hr = (11, 26), (16, 26)
    elif arms == "think":
        hl, hr = (6, 31), (15, 16)
    elif arms == "shrug":
        hl, hr = (3, 22), (24, 22)
    elif arms == "cross":
        hl, hr = (17, 25), (10, 26)
    else:
        hl, hr = (6, 31), (21, 31)
    # brazo izquierdo (luz) y derecho (sombra)
    L.thick_line(sl[0], sl[1], hl[0], hl[1], sleeve, 3)
    L.thick_line(sr[0], sr[1], hr[0], hr[1], sd, 3)
    for (hx, hy), c in ((hl, skin), (hr, shade(skin, 0.86))):
        L.rect(hx - 1, hy, hx + 1, hy + 1, c)
    return L.outline()


@lru_cache(maxsize=4096)
def _render(spec_key, pose_key, tq):
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
    order = [draw_legs(spec, pose), draw_torso(spec, pose), draw_head(spec, pose)]
    arms = draw_arms(spec, pose, tq / 30.0)
    if pose.get("arms") in ("think", "type", "write", "hold", "cross"):
        order.append(arms)
    else:
        order.insert(1, arms) if pose.get("arms") == "down_back" else order.append(arms)
    img = composite(order)
    if pose.get("facing", 1) < 0:
        img = img[:, ::-1]
    return img


def _freeze(d):
    return tuple(sorted((k, tuple(v) if isinstance(v, list) else v) for k, v in d.items()))


def render(spec, t=0.0, **pose):
    """Devuelve un array RGBA (SH, SW, 4) del personaje en la pose pedida.
    Parpadeo automático salvo que se pase blink explícito."""
    if "blink" not in pose:
        seed = (hash(spec.get("name", "")) % 97) / 97.0
        cyc = (t + seed * 3.7) % 3.4
        pose["blink"] = cyc < 0.12
    tq = int(t * 30) if pose.get("arms") in ("type", "write", "wave", "cheer") else 0
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
}

DARTMOUTH_TEN = ["mccarthy", "minsky", "shannon", "rochester", "solomonoff",
                 "selfridge", "more", "samuel", "newell", "simon"]
