"""Generador procedural de fondos 16-bit Pixel Art (480x270) estilo SNES / Chrono Trigger
para «UN PIANO DENTRO DE UN TORPEDO — La historia de Hedy Lamarr».

Cada fondo tiene:
- Techo / cielo rico en y=0..48 (para que vertical.py extienda el cielo/techo en 9:16 con naturalidad)
- Arquitectura, ventanas y detalles de época en y=48..220 (dejando libre el plano de texto y tarjetas)
- Piso con perspectiva, tablas/baldosas y zócalo en y=220..270 donde apoyan personajes y muebles en feet=248.
"""
import math
import os
import random
import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "assets", "bg")
W, H = 480, 270

BAYER4 = np.array([
    [0, 8, 2, 10],
    [12, 4, 14, 6],
    [3, 11, 1, 9],
    [15, 7, 13, 5],
], dtype=np.float32) / 16.0


def dither_grad(w, h, c_top, c_bot, y0=0, y1=None):
    if y1 is None:
        y1 = h
    arr = np.zeros((h, w, 3), dtype=np.uint8)
    th = np.tile(BAYER4, (h // 4 + 1, w // 4 + 1))[:h, :w]
    for y in range(y0, min(h, y1)):
        t = (y - y0) / max(1, (y1 - y0 - 1))
        # Bandas de 16 bits + dithering Bayer
        tb = np.floor(t * 10.0 + th[y] * 0.95) / 10.0
        tb = np.clip(tb, 0.0, 1.0)
        for ch in range(3):
            arr[y, :, ch] = np.clip(c_top[ch] + (c_bot[ch] - c_top[ch]) * tb, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, "RGB")


def draw_wood_floor(d, y_top=220, c_base=(76, 48, 30), c_dark=(52, 32, 18), c_hi=(98, 64, 40)):
    d.rectangle([0, y_top, W, H], fill=c_base)
    # Zócalo
    d.rectangle([0, y_top - 6, W, y_top], fill=c_dark)
    d.line([(0, y_top - 6), (W, y_top - 6)], fill=c_hi)
    d.line([(0, y_top), (W, y_top)], fill=(24, 16, 12))
    # Tablas horizontales con perspectiva
    y = y_top + 4
    step = 5
    row = 0
    while y < H:
        d.line([(0, y), (W, y)], fill=c_dark)
        if y + 1 < H:
            d.line([(0, y + 1), (W, y + 1)], fill=c_hi)
        # Juntas verticales alternadas
        for x in range((row * 37) % 64, W, 64):
            d.line([(x, y - step), (x - 4, y)], fill=c_dark)
        y += step
        step = min(11, step + 1)
        row += 1


def draw_marble_floor(d, y_top=220, c1=(46, 44, 62), c2=(30, 28, 42), c_gold=(148, 116, 56)):
    d.rectangle([0, y_top, W, H], fill=c1)
    d.rectangle([0, y_top - 5, W, y_top], fill=(24, 20, 32))
    d.line([(0, y_top - 5), (W, y_top - 5)], fill=c_gold)
    rows = [220, 226, 233, 241, 250, 260, 270]
    for r_i in range(len(rows) - 1):
        ya, yb = rows[r_i], rows[r_i + 1]
        for col_i in range(-2, 14):
            xa0 = 240 + (col_i - 6) * (36 + r_i * 4)
            xa1 = 240 + (col_i - 5) * (36 + r_i * 4)
            xb0 = 240 + (col_i - 6) * (36 + (r_i + 1) * 4)
            xb1 = 240 + (col_i - 5) * (36 + (r_i + 1) * 4)
            col = c1 if (r_i + col_i) % 2 == 0 else c2
            d.polygon([(xa0, ya), (xa1, ya), (xb1, yb), (xb0, yb)], fill=col, outline=c2)


def quantize_save(im, name):
    q = im.convert("RGB").quantize(colors=56, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, f"{name}.png")
    q.convert("RGBA").save(path)
    print("Generated bg:", path)


def build_vienna_street_1914():
    im = dither_grad(W, H, (28, 38, 68), (118, 92, 78), 0, 218)
    d = ImageDraw.Draw(im)
    # Edificios clásicos vieneses al fondo
    buildings = [
        (0, 62, 112, (74, 64, 62), (96, 84, 78)),
        (112, 48, 232, (88, 76, 68), (114, 98, 86)),
        (232, 68, 356, (68, 60, 64), (88, 78, 80)),
        (356, 52, 480, (82, 70, 64), (106, 92, 82)),
    ]
    for x0, y0, x1, col, hi in buildings:
        d.rectangle([x0, y0, x1, 218], fill=col, outline=(24, 20, 26))
        d.rectangle([x0, y0, x1, y0 + 6], fill=hi, outline=(24, 20, 26))
        d.rectangle([x0, y0 + 42, x1, y0 + 45], fill=hi)
        # Ventanas arqueadas con luz cálida
        for wx in range(x0 + 14, x1 - 16, 26):
            for wy in range(y0 + 14, 192, 34):
                w_lit = ((wx + wy) % 3 == 0)
                wcol = (218, 178, 102) if w_lit else (38, 44, 58)
                d.rectangle([wx, wy, wx + 12, wy + 20], fill=wcol, outline=(28, 22, 26))
                d.line([(wx + 6, wy), (wx + 6, wy + 20)], fill=(28, 22, 26))
                d.line([(wx, wy + 9), (wx + 12, wy + 9)], fill=(28, 22, 26))

    # Cables de tranvía eléctrico arriba
    d.line([(0, 34), (W, 28)], fill=(22, 24, 34), width=1)
    d.line([(0, 42), (W, 38)], fill=(22, 24, 34), width=1)
    for tx in range(40, W, 90):
        d.line([(tx, 28), (tx, 42)], fill=(36, 40, 52))

    # Farolas vienesas
    for lx in (68, 412):
        d.rectangle([lx - 2, 128, lx + 2, 220], fill=(28, 32, 38))
        d.ellipse([lx - 7, 116, lx + 7, 130], fill=(252, 224, 136), outline=(28, 32, 38))

    # Empedrado y rieles de tranvía en el suelo (y=218..270)
    d.rectangle([0, 218, W, H], fill=(58, 54, 62))
    d.rectangle([0, 214, W, 220], fill=(78, 72, 80))
    for y in range(222, H, 6):
        d.line([(0, y), (W, y)], fill=(44, 40, 48))
        for x in range((y * 13) % 18, W, 18):
            d.line([(x, y), (x, min(H, y + 5))], fill=(44, 40, 48))
    # Rieles brillantes
    d.line([(0, 234), (W, 234)], fill=(132, 138, 152), width=2)
    d.line([(0, 254), (W, 254)], fill=(132, 138, 152), width=2)
    quantize_save(im, "vienna_street_1914")


def build_vienna_parlor_piano():
    im = dither_grad(W, H, (56, 36, 34), (88, 56, 46), 0, 220)
    d = ImageDraw.Draw(im)
    # Papel tapiz adamascado sutil
    for y in range(18, 168, 16):
        for x in range((y // 16 % 2) * 12, W, 24):
            d.rectangle([x + 10, y + 4, x + 13, y + 9], fill=(98, 64, 52))
    # Cornisa superior y revestimiento de madera (boiserie) abajo
    d.rectangle([0, 0, W, 14], fill=(44, 28, 22))
    d.line([(0, 14), (W, 14)], fill=(168, 128, 68), width=2)
    d.rectangle([0, 166, W, 220], fill=(64, 40, 26), outline=(32, 20, 14))
    for px in range(12, W - 12, 48):
        d.rectangle([px, 172, px + 38, 212], outline=(92, 58, 36))
    # Dos grandes ventanales vieneses con cortinas doradas/terracota
    for wx in (44, 356):
        d.rectangle([wx, 28, wx + 76, 166], fill=(176, 204, 226), outline=(42, 26, 18), width=2)
        d.line([(wx + 38, 28), (wx + 38, 166)], fill=(42, 26, 18), width=2)
        d.line([(wx, 86), (wx + 76, 86)], fill=(42, 26, 18), width=2)
        # Cortinas laterales
        d.polygon([(wx - 8, 24), (wx + 18, 24), (wx + 8, 168), (wx - 8, 168)], fill=(138, 38, 42))
        d.polygon([(wx + 58, 24), (wx + 84, 24), (wx + 84, 168), (wx + 68, 168)], fill=(138, 38, 42))
    # Cuadros musicales en el centro
    for fx in (176, 264):
        d.rectangle([fx, 56, fx + 40, 108], fill=(224, 212, 186), outline=(158, 118, 52), width=2)
        for ly in range(66, 100, 6):
            d.line([(fx + 6, ly), (fx + 34, ly)], fill=(90, 78, 64))
    draw_wood_floor(d, 220, (82, 52, 32), (56, 34, 20), (108, 70, 44))
    quantize_save(im, "vienna_parlor_piano")


def build_vienna_mansion_cage():
    im = dither_grad(W, H, (26, 20, 38), (52, 34, 56), 0, 220)
    d = ImageDraw.Draw(im)
    # Columnas de mármol y ventanales con barrotes dorados ("La jaula de oro")
    for wx in (52, 196, 340):
        d.rectangle([wx, 26, wx + 88, 182], fill=(16, 24, 46), outline=(176, 138, 62), width=2)
        # Rejas doradas ornamentales en cada ventanal
        for bx in range(wx + 14, wx + 80, 14):
            d.line([(bx, 26), (bx, 182)], fill=(198, 158, 74), width=2)
        for by in (64, 112, 154):
            d.line([(wx, by), (wx + 88, by)], fill=(198, 158, 74), width=2)
    # Cortinados pesados borgoña y arañas de cristal arriba
    for cx in (28, 168, 312, 452):
        d.rectangle([cx - 12, 14, cx + 12, 220], fill=(96, 24, 38), outline=(48, 12, 20))
    for chx in (140, 340):
        d.line([(chx, 0), (chx, 22)], fill=(198, 158, 74), width=2)
        d.ellipse([chx - 18, 18, chx + 18, 34], fill=(246, 214, 128), outline=(168, 128, 52))
    draw_marble_floor(d, 220, (44, 38, 56), (28, 24, 38), (186, 146, 68))
    quantize_save(im, "vienna_mansion_cage")


def build_ocean_liner_1937():
    # Cielo nocturno del Atlántico / llegada a Nueva York
    im = dither_grad(W, H, (8, 14, 32), (24, 46, 82), 0, 178)
    d = ImageDraw.Draw(im)
    rnd = random.Random(37)
    for _ in range(90):
        sx, sy = rnd.randint(4, W - 4), rnd.randint(4, 128)
        d.point((sx, sy), fill=(230, 240, 255))
    # Silueta lejana de Manhattan iluminada a la izquierda y mar en el centro
    for bx in range(12, 168, 14):
        bh = 22 + ((bx * 19) % 44)
        d.rectangle([bx, 164 - bh, bx + 12, 164], fill=(18, 26, 48), outline=(10, 14, 28))
        for wy in range(164 - bh + 4, 160, 6):
            for wx in range(bx + 2, bx + 10, 4):
                if (wx + wy) % 3 == 0:
                    d.point((wx, wy), fill=(248, 212, 118))
    # Agua del océano con reflejos de luna (y=164..218)
    d.rectangle([0, 164, W, 218], fill=(12, 26, 52))
    for wy in range(168, 216, 5):
        for wx in range((wy * 11) % 28, W, 32):
            d.line([(wx, wy), (wx + 12, wy)], fill=(54, 108, 162))
    # Superestructura blanca Art Déco del transatlántico a la derecha y baranda
    d.rectangle([308, 78, 480, 218], fill=(216, 220, 228), outline=(38, 46, 64), width=2)
    for px in range(334, 468, 34):
        d.ellipse([px - 9, 114, px + 9, 132], fill=(252, 218, 128), outline=(64, 72, 92), width=2)
    # Baranda de cubierta en y=192..220
    d.rectangle([0, 190, W, 194], fill=(168, 122, 68), outline=(28, 20, 16))
    for rx in range(12, W, 24):
        d.line([(rx, 194), (rx, 220)], fill=(182, 188, 198), width=2)
    draw_wood_floor(d, 220, (92, 64, 40), (62, 42, 24), (118, 84, 54))
    quantize_save(im, "ocean_liner_1937")


def build_hollywood_dressing_room():
    im = dither_grad(W, H, (42, 32, 48), (74, 52, 68), 0, 220)
    d = ImageDraw.Draw(im)
    # Mitad izquierda: Camarín de estrella de MGM (espejo con bombillas y cortina de terciopelo)
    d.rectangle([16, 24, 96, 218], fill=(124, 28, 46), outline=(48, 12, 22))
    d.rectangle([114, 46, 212, 152], fill=(86, 124, 156), outline=(198, 158, 72), width=3)
    for bx in range(118, 212, 16):
        d.ellipse([bx - 3, 41, bx + 3, 47], fill=(255, 242, 176))
        d.ellipse([bx - 3, 151, bx + 3, 157], fill=(255, 242, 176))
    for by in range(54, 150, 16):
        d.ellipse([109, by - 3, 115, by + 3], fill=(255, 242, 176))
        d.ellipse([211, by - 3, 217, by + 3], fill=(255, 242, 176))
    # Mitad derecha: Estantería de química, planos de alas de avión y tablero técnico
    d.rectangle([264, 42, 452, 158], fill=(28, 48, 72), outline=(142, 164, 188), width=2)
    for gx in range(276, 444, 16):
        d.line([(gx, 44), (gx, 156)], fill=(38, 66, 96))
    for gy in range(54, 154, 16):
        d.line([(266, gy), (450, gy)], fill=(38, 66, 96))
    # Silueta de ala aerodinámica en el plano de la pared
    d.arc([288, 74, 428, 134], 190, 350, fill=(120, 232, 255), width=2)
    d.line([(288, 104), (428, 104)], fill=(238, 244, 255), width=1)
    draw_wood_floor(d, 220, (86, 58, 42), (58, 38, 26), (112, 78, 56))
    quantize_save(im, "hollywood_dressing_room")


def build_atlantic_night_1940():
    im = dither_grad(W, H, (6, 12, 26), (16, 36, 62), 0, 158)
    d = ImageDraw.Draw(im)
    # Nubes de tormenta y lluvia nocturna en el Atlántico Norte
    for cx in range(20, W, 72):
        d.ellipse([cx - 44, 14, cx + 44, 48], fill=(18, 26, 44))
    # Mar embravecido nocturno (y=154..220)
    d.rectangle([0, 154, W, 220], fill=(10, 24, 44))
    for wy in range(158, 218, 6):
        for wx in range((wy * 17) % 36, W, 38):
            d.arc([wx, wy - 3, wx + 22, wy + 5], 180, 360, fill=(38, 78, 118), width=1)
    # Piso de puente naval / sala de mando en el frente (y=220..270)
    d.rectangle([0, 220, W, H], fill=(28, 36, 48))
    d.rectangle([0, 214, W, 220], fill=(46, 58, 74), outline=(14, 18, 26))
    for rx in range(16, W, 32):
        d.ellipse([rx - 1, 216, rx + 1, 218], fill=(122, 136, 154))
    for y in range(228, H, 10):
        d.line([(0, y), (W, y)], fill=(20, 26, 36))
    quantize_save(im, "atlantic_night_1940")


def build_hollywood_dining_patent():
    im = dither_grad(W, H, (34, 26, 44), (62, 44, 64), 0, 220)
    d = ImageDraw.Draw(im)
    # Ventanal nocturno con vista a las colinas de Los Ángeles iluminadas
    d.rectangle([156, 28, 324, 156], fill=(12, 18, 38), outline=(112, 78, 48), width=3)
    d.line([(240, 28), (240, 156)], fill=(112, 78, 48), width=2)
    d.line([(156, 92), (324, 92)], fill=(112, 78, 48), width=2)
    # Colinas y lucecitas de Hollywood en la ventana
    d.polygon([(158, 132), (204, 108), (266, 122), (322, 98), (322, 154), (158, 154)], fill=(20, 26, 48))
    for lx in range(164, 318, 9):
        ly = 128 + ((lx * 7) % 22)
        d.point((lx, ly), fill=(252, 214, 112) if lx % 2 == 0 else (90, 220, 255))
    # Biblioteca a la izquierda y lámpara cálida a la derecha
    d.rectangle([22, 44, 118, 216], fill=(58, 38, 26), outline=(28, 18, 12), width=2)
    cols_book = [(168, 54, 54), (54, 118, 168), (186, 146, 62), (68, 142, 96)]
    for sy in range(56, 204, 28):
        d.rectangle([26, sy + 20, 114, sy + 24], fill=(86, 56, 38))
        for bx in range(30, 108, 7):
            d.rectangle([bx, sy + 4, bx + 5, sy + 20], fill=cols_book[(bx + sy) % 4])
    draw_wood_floor(d, 220, (78, 50, 32), (52, 32, 18), (104, 68, 44))
    # Alfombra persa en el centro del piso
    d.polygon([(84, 228), (396, 228), (432, 268), (48, 268)], fill=(118, 34, 46), outline=(198, 158, 72))
    quantize_save(im, "hollywood_dining_patent")


def build_navy_office_1942():
    im = dither_grad(W, H, (32, 42, 54), (54, 68, 82), 0, 220)
    d = ImageDraw.Draw(im)
    # Revestimiento de madera institucional y mapa naval en la pared
    d.rectangle([0, 158, W, 220], fill=(66, 46, 32), outline=(28, 20, 14))
    d.rectangle([148, 34, 332, 138], fill=(24, 52, 74), outline=(168, 132, 62), width=3)
    # Líneas de latitud/longitud del mapa naval
    for gx in range(168, 324, 24):
        d.line([(gx, 36), (gx, 136)], fill=(42, 82, 108))
    for gy in range(52, 132, 22):
        d.line([(150, gy), (330, gy)], fill=(42, 82, 108))
    # Archiveros metálicos verde oliva de la Marina a la izquierda y derecha
    for fx in (28, 376):
        d.rectangle([fx, 58, fx + 74, 220], fill=(58, 72, 58), outline=(24, 32, 24), width=2)
        for dy in range(66, 210, 34):
            d.rectangle([fx + 6, dy, fx + 68, dy + 28], fill=(68, 84, 68), outline=(32, 42, 32))
            d.rectangle([fx + 28, dy + 8, fx + 46, dy + 14], fill=(186, 156, 78))
    draw_wood_floor(d, 220, (68, 54, 42), (46, 36, 28), (88, 70, 54))
    quantize_save(im, "navy_office_1942")


def build_florida_living_1970():
    im = dither_grad(W, H, (38, 34, 56), (68, 58, 82), 0, 220)
    d = ImageDraw.Draw(im)
    # Gran ventana al crepúsculo donde se ven torres de telecomunicaciones multiplicándose en el horizonte
    d.rectangle([188, 32, 436, 162], fill=(18, 24, 52), outline=(92, 68, 48), width=3)
    # Cielo de atardecer en la ventana
    for wy in range(35, 160):
        k = (wy - 35) / 125.0
        col = (int(24 + 90 * k), int(28 + 46 * k), int(68 + 30 * (1 - k)))
        d.line([(191, wy), (433, wy)], fill=col)
    # Siluetas de torres de radio/celulares en el horizonte de la ventana
    for tx in (224, 278, 336, 396):
        d.line([(tx, 84), (tx - 10, 158)], fill=(22, 20, 38), width=2)
        d.line([(tx, 84), (tx + 10, 158)], fill=(22, 20, 38), width=2)
        d.ellipse([tx - 2, 80, tx + 2, 84], fill=(40, 220, 224))
    # Cuadro enmarcado a la izquierda
    d.rectangle([42, 52, 134, 132], fill=(52, 44, 64), outline=(176, 138, 68), width=2)
    draw_wood_floor(d, 220, (64, 52, 68), (44, 34, 48), (86, 70, 92))
    quantize_save(im, "florida_living_1970")


def build_hall_of_fame_modern():
    im = dither_grad(W, H, (8, 12, 32), (20, 32, 68), 0, 220)
    d = ImageDraw.Draw(im)
    # Columnas luminosas modernas y constelación de canales digitales
    for cx in range(48, W, 96):
        d.rectangle([cx - 6, 0, cx + 6, 220], fill=(16, 28, 58), outline=(36, 72, 124))
        d.line([(cx, 0), (cx, 220)], fill=(40, 220, 224))
    for gy in range(28, 210, 22):
        d.line([(0, gy), (W, gy)], fill=(18, 34, 72))
    # Piso de escenario moderno oscuro con reflejo cian y dorado (y=220..270)
    draw_marble_floor(d, 220, (18, 24, 48), (12, 16, 34), (40, 220, 224))
    quantize_save(im, "hall_of_fame_modern")


def main():
    build_vienna_street_1914()
    build_vienna_parlor_piano()
    build_vienna_mansion_cage()
    build_ocean_liner_1937()
    build_hollywood_dressing_room()
    build_atlantic_night_1940()
    build_hollywood_dining_patent()
    build_navy_office_1942()
    build_florida_living_1970()
    build_hall_of_fame_modern()
    print("All 10 16-bit backgrounds generated successfully!")


if __name__ == "__main__":
    main()
