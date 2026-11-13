"""Generador procedural de fondos pixel-art 16-bit (480x270, paleta indexada de 56 colores)
para LÍNEA POR LÍNEA — La historia de la televisión (historia_tv_pixel).
Garantiza línea de piso consistente (y=216..270) para que ningún objeto o personaje flote en 16:9 ni en 9:16.
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


def dither_gradient(w, h, y0, y1, c_top, c_bot, bands=16):
    arr = np.zeros((h, w, 3), dtype=np.uint8)
    th = np.tile(BAYER4, (h // 4 + 1, w // 4 + 1))[:h, :w]
    for y in range(y0, min(h, y1)):
        t = (y - y0) / max(1, (y1 - y0 - 1))
        tb = np.floor(t * bands + th[y] * 0.85) / bands
        tb = np.clip(tb, 0.0, 1.0)
        for c in range(3):
            arr[y, :, c] = (c_top[c] + (c_bot[c] - c_top[c]) * tb).astype(np.uint8)
    return arr


def draw_wood_floor(im, y_top=216, c_base=(84, 54, 34), c_dark=(56, 36, 22), c_hi=(108, 72, 46)):
    d = ImageDraw.Draw(im)
    # Zócalo
    d.rectangle([0, y_top - 6, W, y_top], fill=c_dark)
    d.line([(0, y_top - 6), (W, y_top - 6)], fill=c_hi)
    d.line([(0, y_top), (W, y_top)], fill=(24, 16, 12))
    # Tablones horizontales con perspectiva
    y = y_top + 1
    row = 0
    while y < H:
        step = max(4, int(5 + (y - y_top) * 0.14))
        y_next = min(H, y + step)
        shade_k = 1.0 - 0.18 * ((y - y_top) / max(1, H - y_top))
        col = tuple(int(v * shade_k) for v in c_base)
        d.rectangle([0, y, W, y_next], fill=col)
        d.line([(0, y), (W, y)], fill=c_dark)
        # Juntas verticales entre tablones
        offset = (row * 53) % 90
        for x_joint in range(offset, W, 90):
            d.line([(x_joint, y), (x_joint - 4, y_next)], fill=c_dark)
        y = y_next
        row += 1


def save_indexed(im, name):
    os.makedirs(OUT_DIR, exist_ok=True)
    q = im.convert("RGB").quantize(colors=56, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    path = os.path.join(OUT_DIR, f"{name}.png")
    q.save(path)
    print(f"Saved {path} ({q.size})")


def build_idaho_plow_field():
    """Atardecer en un campo arado de Idaho con surcos paralelos horizontales, montañas y cabaña lejana."""
    arr = dither_gradient(W, H, 0, 148, (46, 32, 74), (242, 138, 64), bands=18)
    im = Image.fromarray(arr, "RGB")
    d = ImageDraw.Draw(im)

    # Sol poniente dorado en el horizonte
    sun_x, sun_y = 350, 118
    for r, col in ((46, (246, 152, 72)), (32, (252, 188, 92)), (20, (255, 228, 148))):
        d.ellipse([sun_x - r, sun_y - r, sun_x + r, sun_y + r], fill=col)

    # Nubes pixeladas al atardecer
    clouds = [(70, 38, 64, 10), (165, 52, 80, 12), (290, 34, 72, 10), (410, 48, 56, 8)]
    for cx, cy, cw, ch in clouds:
        d.rectangle([cx - cw // 2, cy, cx + cw // 2, cy + ch], fill=(168, 86, 92))
        d.rectangle([cx - cw // 2 + 6, cy + ch - 3, cx + cw // 2 - 4, cy + ch + 2], fill=(232, 142, 88))

    # Cordillera de Idaho en silueta violeta/azul
    mtn1 = [(0, 145), (45, 108), (95, 128), (155, 96), (220, 132), (275, 104), (340, 130), (405, 102), (455, 124), (480, 114), (480, 150), (0, 150)]
    d.polygon(mtn1, fill=(68, 44, 76))
    mtn2 = [(0, 150), (60, 130), (130, 142), (210, 124), (290, 140), (380, 128), (480, 138), (480, 156), (0, 156)]
    d.polygon(mtn2, fill=(92, 56, 62))

    # Pequeña cabaña de troncos y pinos en el horizonte izquierdo
    d.rectangle([54, 136, 86, 152], fill=(74, 44, 28), outline=(32, 18, 12))
    d.polygon([(50, 136), (70, 124), (90, 136)], fill=(52, 30, 20), outline=(32, 18, 12))
    d.rectangle([66, 141, 74, 147], fill=(252, 204, 96))  # ventanita cálida

    # Campo arado con surcos paralelos bien marcados (de izquierda a derecha, renglón por renglón)
    y = 152
    row_idx = 0
    while y < H:
        h_row = max(4, int(4 + (y - 152) * 0.08))
        c_ridge = (134, 84, 46) if row_idx % 2 == 0 else (118, 72, 38)
        c_trough = (72, 42, 24)
        c_highlight = (168, 108, 58)
        d.rectangle([0, y, W, y + h_row], fill=c_ridge)
        d.line([(0, y), (W, y)], fill=c_highlight)
        d.rectangle([0, y + h_row - 2, W, y + h_row], fill=c_trough)
        # Textura de terrones de tierra a lo largo del surco
        for tx in range((row_idx * 19) % 28, W, 28):
            d.rectangle([tx, y + 1, tx + 6, y + 2], fill=c_highlight)
            d.rectangle([tx + 10, y + h_row - 2, tx + 15, y + h_row - 1], fill=(54, 30, 16))
        y += h_row
        row_idx += 1

    # Poste de madera rústico en los bordes
    for px in (18, 462):
        d.rectangle([px - 3, 142, px + 3, 166], fill=(64, 38, 22), outline=(28, 16, 10))
    d.line([(18, 148), (462, 148)], fill=(86, 54, 34), width=1)

    save_indexed(im, "idaho_plow_field")


def build_berlin_room_1883():
    """Habitación estudiantil en Berlín, Nochebuena de 1883: ventana nevada, biblioteca, estufa y piso de madera."""
    arr = dither_gradient(W, H, 0, 216, (36, 28, 46), (62, 44, 58), bands=14)
    im = Image.fromarray(arr, "RGB")
    d = ImageDraw.Draw(im)

    # Papel tapiz alemán del siglo XIX (franjas sutiles)
    for x in range(12, W, 24):
        d.line([(x, 0), (x, 168)], fill=(48, 36, 54))
    # Revestimiento de madera inferior (wainscoting)
    d.rectangle([0, 168, W, 216], fill=(68, 44, 30), outline=(28, 18, 12))
    for x in range(16, W - 16, 48):
        d.rectangle([x, 174, x + 38, 208], fill=(58, 36, 24), outline=(88, 58, 38))

    # Ventana alta a la derecha con cielo nocturno de Berlín y nieve
    wx, wy, ww, wh = 332, 24, 104, 126
    d.rectangle([wx - 6, wy - 6, wx + ww + 6, wy + wh + 6], fill=(92, 60, 38), outline=(24, 16, 12))
    d.rectangle([wx, wy, wx + ww, wy + wh], fill=(16, 24, 48))
    # Silueta de tejados de Berlín y campanario nevado
    d.polygon([(wx, wy + 98), (wx + 28, wy + 78), (wx + 52, wy + 98)], fill=(24, 32, 58))
    d.polygon([(wx + 56, wy + 98), (wx + 72, wy + 52), (wx + 88, wy + 98)], fill=(22, 28, 52))
    d.rectangle([wx, wy + 96, wx + ww, wy + wh], fill=(28, 36, 64))
    # Copos de nieve y escarcha en los cristales
    rnd = random.Random(1883)
    for _ in range(45):
        sx = rnd.randint(wx + 3, wx + ww - 4)
        sy = rnd.randint(wy + 3, wy + wh - 4)
        d.rectangle([sx, sy, sx + 1, sy + 1], fill=(225, 238, 255))
    # Marco en cruz de la ventana
    d.rectangle([wx + ww // 2 - 2, wy, wx + ww // 2 + 2, wy + wh], fill=(92, 60, 38))
    d.rectangle([wx, wy + wh // 2 - 2, wx + ww, wy + wh // 2 + 2], fill=(92, 60, 38))
    # Guirnalda navideña de pino con cinta roja sobre la ventana (Nochebuena 1883)
    d.rectangle([wx - 4, wy - 8, wx + ww + 4, wy - 2], fill=(34, 88, 48), outline=(18, 48, 26))
    d.rectangle([wx + ww // 2 - 5, wy - 9, wx + ww // 2 + 5, wy - 1], fill=(198, 48, 48))

    # Estantería con libros de física e ingeniería a la izquierda
    bx, by, bw, bh = 28, 32, 96, 136
    d.rectangle([bx, by, bx + bw, by + bh], fill=(52, 32, 22), outline=(24, 14, 10))
    book_cols = [(168, 52, 48), (52, 98, 142), (62, 124, 72), (184, 142, 58), (124, 68, 132)]
    for shelf_y in (by + 32, by + 66, by + 100, by + 132):
        d.rectangle([bx + 3, shelf_y, bx + bw - 3, shelf_y + 4], fill=(86, 54, 34))
        cur_x = bx + 6
        while cur_x < bx + bw - 10:
            bw_i = rnd.randint(5, 9)
            bh_i = rnd.randint(18, 26)
            col = rnd.choice(book_cols)
            d.rectangle([cur_x, shelf_y - bh_i, cur_x + bw_i, shelf_y - 1], fill=col, outline=(24, 16, 12))
            cur_x += bw_i + 1

    draw_wood_floor(im, y_top=216, c_base=(88, 56, 36), c_dark=(56, 34, 22), c_hi=(116, 76, 48))
    save_indexed(im, "berlin_room_1883")


def build_london_attic_1926():
    """Altillo abarrotado de John Logie Baird en Londres (1926): vigas inclinadas, cables, lámparas y cajas."""
    arr = dither_gradient(W, H, 0, 216, (32, 34, 48), (58, 54, 68), bands=14)
    im = Image.fromarray(arr, "RGB")
    d = ImageDraw.Draw(im)

    # Paredes de ladrillo visto y madera gastada de altillo londinense
    for y in range(20, 216, 10):
        offset = 8 if (y // 10) % 2 else 0
        for x in range(-offset, W, 18):
            d.rectangle([x, y, x + 16, y + 8], fill=(64, 52, 54), outline=(42, 34, 38))

    # Vigas de madera inclinadas del techo del altillo
    for i in range(6):
        vx = i * 44
        d.polygon([(0, 96 - i * 14), (vx + 90, 0), (vx + 110, 0), (0, 112 - i * 14)], fill=(58, 38, 24))
        d.polygon([(W, 96 - i * 14), (W - vx - 90, 0), (W - vx - 110, 0), (W, 112 - i * 14)], fill=(58, 38, 24))
    d.rectangle([0, 0, W, 18], fill=(46, 30, 20))

    # Ventana abuhardillada central-derecha con niebla de Londres
    wx, wy, ww, wh = 346, 42, 84, 96
    d.rectangle([wx - 5, wy - 5, wx + ww + 5, wy + wh + 5], fill=(72, 48, 32), outline=(22, 16, 12))
    d.rectangle([wx, wy, wx + ww, wy + wh], fill=(78, 92, 112))
    # Chimeneas de Londres en silueta
    d.rectangle([wx + 12, wy + 58, wx + 28, wy + wh], fill=(44, 50, 66))
    d.rectangle([wx + 48, wy + 46, wx + 66, wy + wh], fill=(38, 44, 58))
    d.line([(wx + ww // 2, wy), (wx + ww // 2, wy + wh)], fill=(72, 48, 32), width=3)
    d.line([(wx, wy + wh // 2), (wx + ww, wy + wh // 2)], fill=(72, 48, 32), width=3)

    # Estanterías de taller con bobinas, baterías, latas de galletas y válvulas a la izquierda
    sx, sy = 24, 68
    d.rectangle([sx, sy, sx + 96, 216], fill=(54, 36, 24), outline=(24, 16, 12))
    for sh_y in (102, 140, 178):
        d.rectangle([sx + 2, sh_y, sx + 94, sh_y + 4], fill=(84, 56, 36))
        # Cajas, bobinas y frascos
        d.rectangle([sx + 8, sh_y - 20, sx + 28, sh_y - 1], fill=(168, 72, 52), outline=(24, 16, 12))
        d.ellipse([sx + 36, sh_y - 22, sx + 56, sh_y - 2], fill=(184, 148, 68), outline=(24, 16, 12))
        d.rectangle([sx + 64, sh_y - 18, sx + 86, sh_y - 1], fill=(78, 126, 148), outline=(24, 16, 12))

    # Cables colgando entre las vigas
    for cx in (140, 220, 300):
        d.arc([cx - 40, 10, cx + 40, 56], 0, 180, fill=(24, 22, 28), width=2)

    draw_wood_floor(im, y_top=216, c_base=(76, 50, 34), c_dark=(48, 30, 20), c_hi=(102, 68, 44))
    save_indexed(im, "london_attic_1926")


def build_school_chalkboard_1922():
    """Aula escolar rural de 1922 (Rigby, Idaho): gran pizarrón verde en el muro, ventanas luminosas y piso escolar."""
    arr = dither_gradient(W, H, 0, 216, (188, 178, 152), (156, 144, 118), bands=12)
    im = Image.fromarray(arr, "RGB")
    d = ImageDraw.Draw(im)

    # Revestimiento de madera inferior del aula
    d.rectangle([0, 164, W, 216], fill=(112, 74, 44), outline=(42, 26, 16))
    for x in range(8, W, 32):
        d.line([(x, 164), (x, 216)], fill=(86, 54, 32))

    # Ventana escolar soleada a la izquierda
    wx, wy, ww, wh = 20, 28, 68, 122
    d.rectangle([wx - 4, wy - 4, wx + ww + 4, wy + wh + 4], fill=(96, 62, 36), outline=(32, 20, 12))
    d.rectangle([wx, wy, wx + ww, wy + wh], fill=(148, 208, 242))
    d.polygon([(wx, wy + 88), (wx + 34, wy + 68), (wx + ww, wy + 84), (wx + ww, wy + wh), (wx, wy + wh)],
              fill=(96, 164, 92))
    d.line([(wx + ww // 2, wy), (wx + ww // 2, wy + wh)], fill=(96, 62, 36), width=3)
    d.line([(wx, wy + wh // 2), (wx + ww, wy + wh // 2)], fill=(96, 62, 36), width=3)

    # Gran pizarrón verde clásico en la pared central-derecha
    bx, by, bw, bh = 112, 34, 268, 118
    d.rectangle([bx - 6, by - 6, bx + bw + 6, by + bh + 6], fill=(104, 66, 36), outline=(32, 20, 12))
    d.rectangle([bx, by, bx + bw, by + bh], fill=(22, 52, 38), outline=(64, 40, 22))
    # Bandeja de tizas y borrador
    d.rectangle([bx - 8, by + bh + 2, bx + bw + 8, by + bh + 9], fill=(86, 52, 28), outline=(32, 20, 12))
    d.rectangle([bx + 42, by + bh - 1, bx + 54, by + bh + 2], fill=(244, 244, 236))
    d.rectangle([bx + 88, by + bh - 2, bx + 106, by + bh + 2], fill=(62, 62, 68))

    # Estante de química con matraces a la derecha
    rx, ry = 402, 58
    d.rectangle([rx, ry, rx + 58, 164], fill=(88, 56, 34), outline=(32, 20, 12))
    for sy in (92, 126, 160):
        d.rectangle([rx + 2, sy, rx + 56, sy + 4], fill=(116, 76, 46))
        d.ellipse([rx + 10, sy - 16, rx + 24, sy - 1], fill=(120, 212, 228), outline=(32, 20, 12))
        d.rectangle([rx + 32, sy - 18, rx + 44, sy - 1], fill=(228, 168, 84), outline=(32, 20, 12))

    draw_wood_floor(im, y_top=216, c_base=(118, 80, 48), c_dark=(78, 50, 28), c_hi=(148, 104, 66))
    save_indexed(im, "school_chalkboard_1922")


def build_sf_lab_1927():
    """Laboratorio de Farnsworth en San Francisco (202 Green Street, 1927): ladrillos, tubos de vacío y osciloscopios."""
    arr = dither_gradient(W, H, 0, 216, (28, 36, 48), (46, 58, 72), bands=14)
    im = Image.fromarray(arr, "RGB")
    d = ImageDraw.Draw(im)

    # Pared de ladrillo industrial pintado y cañerías
    for y in range(16, 216, 12):
        off = 10 if (y // 12) % 2 else 0
        for x in range(-off, W, 22):
            d.rectangle([x, y, x + 20, y + 10], fill=(42, 52, 66), outline=(30, 38, 50))

    # Ventana industrial esmerilada a la izquierda
    wx, wy, ww, wh = 24, 34, 82, 114
    d.rectangle([wx - 4, wy - 4, wx + ww + 4, wy + wh + 4], fill=(24, 28, 36), outline=(14, 16, 22))
    d.rectangle([wx, wy, wx + ww, wy + wh], fill=(86, 122, 148))
    for gx in range(wx + 20, wx + ww, 20):
        d.line([(gx, wy), (gx, wy + wh)], fill=(32, 38, 48), width=2)
    for gy in range(wy + 28, wy + wh, 28):
        d.line([(wx, gy), (wx + ww, gy)], fill=(32, 38, 48), width=2)

    # Estanterías de válvulas de vacío y fuentes de poder al fondo derecha
    rx, ry, rw, rh = 356, 36, 98, 178
    d.rectangle([rx, ry, rx + rw, ry + rh], fill=(32, 38, 48), outline=(16, 20, 28))
    for sy in (76, 116, 156, 196):
        d.rectangle([rx + 3, sy, rx + rw - 3, sy + 4], fill=(68, 76, 90))
        for vx in range(rx + 12, rx + rw - 14, 20):
            # Tubos de vidrio brillantes
            d.ellipse([vx, sy - 22, vx + 12, sy - 4], fill=(92, 186, 196), outline=(22, 28, 36))
            d.rectangle([vx + 3, sy - 6, vx + 9, sy - 1], fill=(142, 112, 64))
            d.rectangle([vx + 5, sy - 14, vx + 7, sy - 10], fill=(255, 214, 112))

    # Conductos eléctricos en el techo
    d.rectangle([0, 14, W, 20], fill=(64, 72, 86), outline=(20, 24, 32))
    for lx in (150, 310):
        d.line([(lx, 20), (lx, 42)], fill=(24, 28, 36), width=2)
        d.polygon([(lx - 14, 42), (lx + 14, 42), (lx + 8, 36), (lx - 8, 36)], fill=(68, 88, 76), outline=(18, 22, 28))
        d.ellipse([lx - 5, 41, lx + 5, 48], fill=(255, 236, 156))

    draw_wood_floor(im, y_top=216, c_base=(68, 58, 52), c_dark=(42, 36, 32), c_hi=(92, 80, 72))
    save_indexed(im, "sf_lab_1927")


def build_rca_skyscraper_court():
    """Rascacielos Art Déco de RCA en Nueva York / Sala de patentes de los años 30."""
    arr = dither_gradient(W, H, 0, 216, (22, 28, 48), (48, 56, 84), bands=16)
    im = Image.fromarray(arr, "RGB")
    d = ImageDraw.Draw(im)

    # Grandes ventanales Art Déco mostrando el skyline de Manhattan (Rockefeller Center)
    for wx in (44, 196, 348):
        wy, ww, wh = 26, 88, 148
        d.rectangle([wx - 4, wy - 4, wx + ww + 4, wy + wh + 4], fill=(168, 134, 68), outline=(28, 22, 16))
        d.rectangle([wx, wy, wx + ww, wy + wh], fill=(18, 26, 52))
        # Rascacielos en silueta con ventanitas iluminadas
        buildings = [(wx + 6, wy + 52, 24), (wx + 32, wy + 28, 26), (wx + 60, wy + 44, 22)]
        for bx, by_top, bw in buildings:
            d.rectangle([bx, by_top, bx + bw, wy + wh], fill=(28, 38, 68), outline=(14, 18, 36))
            for wy_i in range(by_top + 6, wy + wh - 6, 8):
                for wx_i in range(bx + 4, bx + bw - 4, 6):
                    if (wx_i + wy_i) % 3 != 0:
                        d.rectangle([wx_i, wy_i, wx_i + 2, wy_i + 3], fill=(246, 208, 112))
        # Motivo geométrico Art Déco dorado en la parte superior del ventanal
        d.line([(wx + ww // 2, wy), (wx + ww // 2, wy + wh)], fill=(168, 134, 68), width=2)
        d.polygon([(wx + ww // 2 - 16, wy), (wx + ww // 2 + 16, wy), (wx + ww // 2, wy + 18)],
                  fill=(196, 158, 82), outline=(28, 22, 16))

    # Pilares de mármol y bronce Art Déco entre ventanales
    for px in (12, 152, 304, 452):
        d.rectangle([px, 0, px + 22, 216], fill=(64, 58, 72), outline=(24, 20, 28))
        d.line([(px + 6, 0), (px + 6, 216)], fill=(184, 148, 76), width=2)
        d.line([(px + 15, 0), (px + 15, 216)], fill=(184, 148, 76), width=2)

    # Revestimiento de caoba y bronce en la parte baja del muro
    d.rectangle([0, 176, W, 216], fill=(72, 42, 34), outline=(28, 16, 14))
    d.line([(0, 178), (W, 178)], fill=(196, 158, 82), width=2)

    # Piso de mármol ajedrezado y madera lustrosa en y=216..270
    draw_wood_floor(im, y_top=216, c_base=(76, 68, 78), c_dark=(48, 42, 52), c_hi=(112, 102, 118))
    save_indexed(im, "rca_skyscraper_court")


def build_living_room_1950s():
    """Living familiar de los años 50: empapelado retro cálido, cortinas, cuadros, alfombra y piso de madera."""
    arr = dither_gradient(W, H, 0, 216, (164, 132, 98), (132, 100, 72), bands=14)
    im = Image.fromarray(arr, "RGB")
    d = ImageDraw.Draw(im)

    # Patrón de empapelado de mediados de siglo (rombos sutiles)
    for y in range(16, 172, 24):
        for x in range(16, W - 16, 28):
            d.polygon([(x, y - 5), (x + 5, y), (x, y + 5), (x - 5, y)], fill=(178, 146, 110))

    # Zócalo y moldura de madera
    d.rectangle([0, 172, W, 216], fill=(96, 62, 40), outline=(38, 24, 16))
    d.line([(0, 172), (W, 172)], fill=(214, 184, 138), width=2)

    # Ventana con cortinas de los años 50 a la izquierda
    wx, wy, ww, wh = 34, 32, 92, 116
    d.rectangle([wx - 4, wy - 4, wx + ww + 4, wy + wh + 4], fill=(224, 214, 192), outline=(48, 34, 24))
    d.rectangle([wx, wy, wx + ww, wy + wh], fill=(92, 156, 212))
    # Casas suburbanas con antenas de TV en los techos vistas por la ventana
    for hx in (wx + 8, wx + 48):
        d.rectangle([hx, wy + 84, hx + 30, wy + wh], fill=(212, 196, 176), outline=(48, 34, 24))
        d.polygon([(hx - 4, wy + 84), (hx + 15, wy + 68), (hx + 34, wy + 84)], fill=(168, 68, 56))
        # Antena de TV en el techo
        d.line([(hx + 15, wy + 50), (hx + 15, wy + 68)], fill=(42, 46, 58), width=1)
        d.line([(hx + 7, wy + 54), (hx + 23, wy + 54)], fill=(42, 46, 58), width=1)
        d.line([(hx + 10, wy + 60), (hx + 20, wy + 60)], fill=(42, 46, 58), width=1)
    # Cortinas rojas cálidas a los lados de la ventana
    d.rectangle([wx - 10, wy - 6, wx + 12, wy + wh + 8], fill=(168, 58, 52), outline=(48, 24, 22))
    d.rectangle([wx + ww - 12, wy - 6, wx + ww + 10, wy + wh + 8], fill=(168, 58, 52), outline=(48, 24, 22))

    # Cuadros enmarcados en la pared derecha
    for fx, fy, fw, fh in ((356, 44, 46, 36), (412, 52, 38, 30)):
        d.rectangle([fx, fy, fx + fw, fy + fh], fill=(88, 56, 32), outline=(28, 18, 12))
        d.rectangle([fx + 4, fy + 4, fx + fw - 4, fy + fh - 4], fill=(224, 212, 186))
        d.polygon([(fx + 6, fy + fh - 6), (fx + fw // 2, fy + 10), (fx + fw - 6, fy + fh - 6)], fill=(86, 142, 96))

    draw_wood_floor(im, y_top=216, c_base=(108, 70, 44), c_dark=(68, 42, 26), c_hi=(138, 94, 60))
    # Alfombra ovalada tejida en el centro del piso
    d.ellipse([96, 228, 384, 264], fill=(148, 54, 48), outline=(216, 176, 96))
    d.ellipse([112, 233, 368, 259], fill=(168, 68, 58), outline=(92, 32, 28))
    save_indexed(im, "living_room_1950s")


def build_tv_game_show_1957():
    """Estudio de programa de preguntas y respuestas de 1957 ('I've Got a Secret' / Doctor X)."""
    arr = dither_gradient(W, H, 0, 216, (24, 28, 44), (56, 64, 88), bands=16)
    im = Image.fromarray(arr, "RGB")
    d = ImageDraw.Draw(im)

    # Telón plisado de estudio de televisión de los años 50 (tonos plata/azul/dorado clásico)
    for x in range(0, W, 16):
        c_pleat = (46, 54, 78) if (x // 16) % 2 == 0 else (34, 40, 62)
        d.rectangle([x, 24, x + 15, 216], fill=c_pleat)
        d.line([(x + 7, 24), (x + 7, 216)], fill=(64, 74, 104))

    # Parrilla de reflectores de estudio arriba
    d.rectangle([0, 0, W, 22], fill=(18, 20, 30))
    for lx in (68, 164, 240, 316, 412):
        d.rectangle([lx - 10, 14, lx + 10, 26], fill=(42, 46, 58), outline=(12, 14, 20))
        d.ellipse([lx - 7, 22, lx + 7, 30], fill=(248, 236, 184))

    # Gran emblema circular retro en el telón central ("?” / "SECRET")
    cx, cy = 240, 96
    for r, col in ((48, (76, 86, 118)), (38, (98, 112, 148)), (28, (32, 38, 58))):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col, outline=(214, 184, 108))

    # Piso lustroso de estudio de televisión en y=216..270
    draw_wood_floor(im, y_top=216, c_base=(52, 58, 76), c_dark=(34, 38, 52), c_hi=(82, 92, 118))
    d.line([(0, 218), (W, 218)], fill=(214, 184, 108), width=2)
    save_indexed(im, "tv_game_show_1957")


def build_moon_landing_living_1969():
    """Living en la noche del 20 de julio de 1969 iluminado por la transmisión del alunizaje del Apolo 11."""
    arr = dither_gradient(W, H, 0, 216, (18, 24, 46), (34, 46, 78), bands=16)
    im = Image.fromarray(arr, "RGB")
    d = ImageDraw.Draw(im)

    # Ventana nocturna a la izquierda con la Luna llena brillando en el cielo de julio de 1969
    wx, wy, ww, wh = 28, 28, 96, 124
    d.rectangle([wx - 4, wy - 4, wx + ww + 4, wy + wh + 4], fill=(48, 36, 32), outline=(16, 12, 14))
    d.rectangle([wx, wy, wx + ww, wy + wh], fill=(10, 14, 32))
    # Luna llena en la ventana
    mx, my = wx + 64, wy + 34
    for r, col in ((22, (42, 64, 112)), (15, (148, 178, 224)), (11, (238, 244, 255))):
        d.ellipse([mx - r, my - r, mx + r, my + r], fill=col)
    d.ellipse([mx - 5, my - 4, mx - 1, my], fill=(196, 208, 232))
    d.ellipse([mx + 2, my + 1, mx + 6, my + 5], fill=(196, 208, 232))
    # Estrellas
    for sx, sy in ((wx + 16, wy + 20), (wx + 28, wy + 48), (wx + 18, wy + 78), (wx + 76, wy + 82)):
        d.point((sx, sy), fill=(220, 235, 255))
    d.line([(wx + ww // 2, wy), (wx + ww // 2, wy + wh)], fill=(48, 36, 32), width=3)
    d.line([(wx, wy + wh // 2), (wx + ww, wy + wh // 2)], fill=(48, 36, 32), width=3)

    # Revestimiento de madera de fines de los 60 y biblioteca a la derecha
    d.rectangle([0, 172, W, 216], fill=(44, 32, 28), outline=(18, 14, 14))
    bx, by, bw, bh = 368, 42, 86, 172
    d.rectangle([bx, by, bx + bw, by + bh], fill=(38, 28, 26), outline=(16, 12, 12))
    for sy in (78, 114, 150, 186):
        d.rectangle([bx + 3, sy, bx + bw - 3, sy + 4], fill=(62, 44, 36))
        for kx in range(bx + 8, bx + bw - 12, 10):
            d.rectangle([kx, sy - 20, kx + 7, sy - 1], fill=(52, 82, 116) if kx % 20 == 0 else (124, 62, 54))

    # Resplandor azul-blanco del televisor en el ambiente nocturno
    draw_wood_floor(im, y_top=216, c_base=(46, 38, 48), c_dark=(28, 22, 32), c_hi=(68, 58, 74))
    d.ellipse([88, 226, 392, 264], fill=(38, 52, 78), outline=(72, 98, 138))
    save_indexed(im, "moon_landing_living_1969")


if __name__ == "__main__":
    build_idaho_plow_field()
    build_berlin_room_1883()
    build_london_attic_1926()
    build_school_chalkboard_1922()
    build_sf_lab_1927()
    build_rca_skyscraper_court()
    build_living_room_1950s()
    build_tv_game_show_1957()
    build_moon_landing_living_1969()
    print("All 9 backgrounds generated in assets/bg/!")
