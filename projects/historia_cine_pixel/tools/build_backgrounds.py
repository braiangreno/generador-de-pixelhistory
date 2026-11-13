"""Generador procedural de escenarios en pixel art 16-bit (480x270, paleta indexada de 56 colores)
para 'UN CABALLO EN EL AIRE — La historia del cine'."""
import math
import os
import random
import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "assets", "bg")
W, H = 480, 270

BAYER4 = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]], dtype=np.float32) / 16.0


def dither_grad(y0, y1, c_top, c_bot, w=W):
    """Genera una banda horizontal con degradado vertical y dithering Bayer 4x4 (look 16-bit SNES)."""
    h = max(1, y1 - y0)
    arr = np.zeros((h, w, 3), dtype=np.uint8)
    th = np.tile(BAYER4, (h // 4 + 1, w // 4 + 1))[:h, :w]
    for y in range(h):
        t = y / max(1, h - 1)
        # Cuantizar en 8 bandas con dithering
        t_q = np.floor(t * 7.0 + th[y]) / 7.0
        t_q = np.clip(t_q, 0.0, 1.0)
        for ch in range(3):
            arr[y, :, ch] = (c_top[ch] + (c_bot[ch] - c_top[ch]) * t_q).astype(np.uint8)
    return Image.fromarray(arr, "RGB")


def save_indexed(im, name):
    os.makedirs(OUT_DIR, exist_ok=True)
    q = im.convert("RGB").quantize(colors=56, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    path = os.path.join(OUT_DIR, f"{name}.png")
    q.save(path)
    print(f"Saved {path} ({q.size}, mode={q.mode})")


def build_palo_alto_track_1878():
    """Pista de tierra en Palo Alto (1878) con el muro blanco numerado y la casilla de las 12 cámaras."""
    im = Image.new("RGB", (W, H), (0, 0, 0))
    # Cielo californiano cálido de mañana
    im.paste(dither_grad(0, 136, (88, 152, 224), (218, 232, 245)), (0, 0))
    d = ImageDraw.Draw(im)

    # Colinas lejanas de California y robles
    pts_hills = [(0, 136)]
    for x in range(0, W + 8, 8):
        hy = 114 + int(math.sin(x * 0.015) * 10 + math.cos(x * 0.035) * 6)
        pts_hills.append((x, hy))
    pts_hills.append((W, 136))
    d.polygon(pts_hills, fill=(142, 168, 118))

    # Hilera de árboles al fondo
    rnd = random.Random(1878)
    for tx in range(18, W, 34):
        r = rnd.randint(10, 16)
        ty = 116 + rnd.randint(-4, 4)
        d.ellipse([tx - r, ty - r, tx + r, ty + r // 2], fill=(64, 108, 62))
        d.ellipse([tx - r + 3, ty - r + 2, tx + r // 2, ty], fill=(88, 138, 78))

    # Muro blanco de referencia de Muybridge con líneas verticales numeradas (y=124..186)
    d.rectangle([16, 124, 464, 186], fill=(242, 238, 226), outline=(58, 46, 36))
    d.rectangle([16, 124, 464, 130], fill=(214, 206, 190))
    for i, gx in enumerate(range(28, 456, 18)):
        d.line([(gx, 128), (gx, 185)], fill=(182, 174, 158), width=1)

    # Casilla de madera larga con las 12 lentes de cámaras en serie (arriba del muro / costado)
    d.rectangle([36, 96, 444, 124], fill=(118, 78, 44), outline=(36, 24, 16))
    d.polygon([(30, 96), (450, 96), (440, 84), (40, 84)], fill=(88, 56, 32), outline=(36, 24, 16))
    for i in range(12):
        cx = 56 + i * 33
        d.rectangle([cx - 10, 100, cx + 10, 121], fill=(74, 48, 28), outline=(36, 24, 16))
        d.ellipse([cx - 5, 105, cx + 5, 115], fill=(28, 36, 48), outline=(196, 156, 74))
        d.point((cx - 2, 108), fill=(180, 225, 255))

    # Baranda de madera de la pista
    d.rectangle([0, 186, W, 192], fill=(156, 110, 64), outline=(48, 32, 18))
    for px in range(12, W, 32):
        d.rectangle([px, 180, px + 4, 198], fill=(134, 92, 52), outline=(48, 32, 18))

    # Pista de tierra compactada donde corren el caballo y pisan los personajes (y=192..270)
    im.paste(dither_grad(192, H, (194, 152, 98), (138, 98, 56)), (0, 192))
    d = ImageDraw.Draw(im)
    # Hilos disparadores tenues cruzando la pista desde las 12 cámaras
    for i in range(12):
        cx = 56 + i * 33
        d.line([(cx, 186), (cx, 246)], fill=(224, 214, 194))
    # Textura de tierra y huellas en el suelo
    for _ in range(95):
        rx = rnd.randint(4, W - 8)
        ry = rnd.randint(198, H - 4)
        col = (168, 126, 76) if rnd.random() < 0.5 else (118, 82, 44)
        d.rectangle([rx, ry, rx + rnd.randint(2, 5), ry + 1], fill=col)

    save_indexed(im, "palo_alto_track_1878")


def build_paris_salon_indien_1895():
    """Sótano del Salon Indien du Grand Café en París (28 de diciembre de 1895)."""
    im = Image.new("RGB", (W, H), (0, 0, 0))
    # Paredes subterráneas cálidas de terciopelo bordó y madera oscura
    im.paste(dither_grad(0, 198, (32, 18, 28), (68, 28, 38)), (0, 0))
    d = ImageDraw.Draw(im)

    # Arcos abovedados del sótano parisino y columnas con molduras doradas
    for ax in (0, 120, 240, 360):
        d.arc([ax - 10, 6, ax + 130, 96], 180, 360, fill=(96, 56, 44), width=3)
    for col_x in (22, 118, 362, 458):
        d.rectangle([col_x - 8, 24, col_x + 8, 202], fill=(78, 46, 34), outline=(24, 14, 12))
        d.rectangle([col_x - 10, 24, col_x + 10, 32], fill=(168, 126, 62))
        d.rectangle([col_x - 10, 194, col_x + 10, 202], fill=(168, 126, 62))

    # Empapelado adamascado sutil y lámparas de gas en las paredes laterales
    for wy in range(48, 180, 22):
        for wx in (64, 412):
            d.ellipse([wx - 4, wy - 4, wx + 4, wy + 4], fill=(255, 208, 112))
            d.rectangle([wx - 2, wy + 4, wx + 2, wy + 10], fill=(154, 112, 52))

    # Cortinados bordó y marco de la pantalla blanca central (x=136..344, y=42..168)
    d.rectangle([126, 36, 354, 174], fill=(92, 22, 32), outline=(184, 142, 68))
    d.rectangle([140, 46, 340, 164], fill=(236, 232, 218), outline=(42, 28, 22))

    # Zócalo de madera y piso de parquet francés (y=198..270)
    d.rectangle([0, 196, W, 204], fill=(62, 38, 24), outline=(24, 14, 12))
    im.paste(dither_grad(204, H, (92, 58, 36), (54, 32, 20)), (0, 204))
    d = ImageDraw.Draw(im)
    for py in range(208, H, 10):
        d.line([(0, py), (W, py)], fill=(44, 26, 16))
        for px in range((py * 3) % 36, W, 36):
            d.line([(px, py), (px - 8, py + 10)], fill=(44, 26, 16))

    # Filas de sillas de café de madera al fondo frente a la pantalla (y=176..204)
    for row_y in (176, 190):
        for sx in range(84, 396, 26):
            d.rectangle([sx - 6, row_y, sx + 6, row_y + 10], fill=(74, 42, 24), outline=(24, 14, 12))
            d.line([(sx - 5, row_y + 10), (sx - 5, row_y + 16)], fill=(48, 26, 14))
            d.line([(sx + 5, row_y + 10), (sx + 5, row_y + 16)], fill=(48, 26, 14))

    save_indexed(im, "paris_salon_indien_1895")


def build_melies_glass_studio():
    """Estudio de vidrio de Georges Méliès en Montreuil con estructura de hierro y cielo estrellado/diurno."""
    im = Image.new("RGB", (W, H), (0, 0, 0))
    # Cielo azul-violeta mágico detrás de los ventanales de vidrio
    im.paste(dither_grad(0, 196, (28, 44, 88), (84, 128, 184)), (0, 0))
    d = ImageDraw.Draw(im)

    # Techo a dos aguas y paredes de vidrio con estructura de hierro forjado (estilo invernadero de Montreuil)
    for gx in range(0, W + 40, 40):
        d.line([(gx, 0), (gx, 196)], fill=(46, 58, 78), width=2)
    for gy in range(24, 196, 28):
        d.line([(0, gy), (W, gy)], fill=(46, 58, 78), width=2)
    # Vigas diagonales de hierro en el techo
    for gx in range(0, W, 80):
        d.line([(gx, 0), (gx + 40, 52)], fill=(34, 44, 62), width=2)
        d.line([(gx + 80, 0), (gx + 40, 52)], fill=(34, 44, 62), width=2)

    # Reflejos diagonales en los paneles de vidrio
    for gx in range(12, W - 20, 40):
        for gy in (32, 88, 144):
            d.line([(gx, gy + 14), (gx + 14, gy)], fill=(138, 182, 226), width=1)

    # Telón teatral pintado en el centro del estudio (con nubes y estrellas barrocas)
    d.rectangle([108, 42, 372, 196], fill=(38, 32, 68), outline=(188, 146, 68))
    d.rectangle([104, 38, 376, 48], fill=(148, 36, 48), outline=(188, 146, 68))
    # Bambalinas laterales rojas
    d.rectangle([108, 48, 126, 196], fill=(132, 28, 42))
    d.rectangle([354, 48, 372, 196], fill=(132, 28, 42))

    # Piso de tablas de madera de escenario (con escotilla para trucos de magia)
    im.paste(dither_grad(196, H, (124, 86, 52), (76, 48, 28)), (0, 196))
    d = ImageDraw.Draw(im)
    d.line([(0, 196), (W, 196)], fill=(188, 146, 68), width=2)
    for py in range(206, H, 12):
        d.line([(0, py), (W, py)], fill=(58, 36, 20))
    for px in range(24, W, 48):
        d.line([(px, 196), (px - 16, H)], fill=(64, 40, 22))
    # Escotilla de trucos en el centro del escenario
    d.rectangle([208, 226, 272, 246], outline=(42, 24, 14), width=2)

    save_indexed(im, "melies_glass_studio")


def build_hollywood_hills_1915():
    """Pueblito soleado de Hollywood, California (años 1910): sol radiante, montañas, mar lejano, desierto y set al aire libre."""
    im = Image.new("RGB", (W, H), (0, 0, 0))
    # Cielo californiano súper luminoso y despejado
    im.paste(dither_grad(0, 148, (56, 148, 236), (186, 228, 252)), (0, 0))
    d = ImageDraw.Draw(im)

    # Sol radiante arriba a la derecha
    cx, cy = 412, 48
    for r, col in ((34, (255, 236, 164)), (24, (255, 224, 112)), (15, (255, 248, 204))):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)

    # Franja de océano Pacífico a la izquierda en el horizonte
    d.rectangle([0, 134, 132, 152], fill=(42, 118, 196))
    for wx in range(8, 120, 18):
        d.line([(wx, 142), (wx + 8, 142)], fill=(188, 232, 255))

    # Colinas doradas/verdes de Hollywood y montañas al fondo
    pts_mt = [(72, 152), (130, 102), (188, 124), (254, 92), (326, 118), (396, 98), (480, 128), (480, 156)]
    d.polygon(pts_mt, fill=(158, 136, 108))
    pts_hills = [(0, 156)]
    for x in range(0, W + 12, 12):
        hy = 132 + int(math.sin(x * 0.018 + 1.2) * 12)
        pts_hills.append((x, hy))
    pts_hills.append((W, 162))
    d.polygon(pts_hills, fill=(186, 156, 92))

    # Palmeras californianas y naranjos
    for px, py, h_trunk in ((54, 158, 52), (92, 162, 44), (428, 156, 56), (456, 164, 42)):
        d.line([(px, py), (px + 3, py - h_trunk)], fill=(112, 76, 44), width=3)
        top_x, top_y = px + 3, py - h_trunk
        for dx, dy in ((-14, 4), (-10, -6), (0, -10), (10, -6), (14, 4)):
            d.line([(top_x, top_y), (top_x + dx, top_y + dy)], fill=(56, 132, 58), width=3)

    # Tarima de filmación al aire libre (con difusores de tela blanca arriba para aprovechar la luz del sol)
    d.rectangle([144, 118, 336, 192], fill=(228, 212, 178), outline=(96, 68, 38))
    # Columnas estilo western / fachada de set en el fondo
    for sx in (156, 212, 268, 324):
        d.rectangle([sx - 4, 122, sx + 4, 192], fill=(184, 146, 98), outline=(78, 52, 28))
    d.rectangle([140, 112, 340, 122], fill=(164, 118, 68), outline=(78, 52, 28))

    # Suelo de tierra soleada californiana (y=192..270)
    im.paste(dither_grad(192, H, (224, 184, 118), (176, 132, 74)), (0, 192))
    d = ImageDraw.Draw(im)
    rnd = random.Random(1915)
    for _ in range(80):
        rx, ry = rnd.randint(4, W - 8), rnd.randint(196, H - 4)
        d.rectangle([rx, ry, rx + 3, ry + 1], fill=(198, 154, 92))

    save_indexed(im, "hollywood_hills_1915")


def build_jazz_singer_theater_1927():
    """Palacio de cine Art Déco de 1927 (estreno de El cantante de jazz): arco dorado, cortinados y pantalla."""
    im = Image.new("RGB", (W, H), (0, 0, 0))
    # Interior Art Déco azul medianoche y borgoña con detalles geométricos dorados
    im.paste(dither_grad(0, 198, (18, 16, 36), (44, 22, 42)), (0, 0))
    d = ImageDraw.Draw(im)

    # Motivos geométricos Art Déco dorados en las paredes laterales y el proscenio
    for side_x in (34, 446):
        d.rectangle([side_x - 18, 20, side_x + 18, 196], fill=(32, 20, 38), outline=(214, 168, 72))
        for ry in range(32, 188, 24):
            d.polygon([(side_x, ry), (side_x + 10, ry + 10), (side_x, ry + 20), (side_x - 10, ry + 10)],
                      outline=(214, 168, 72), fill=(68, 32, 48))

    # Gran arco Art Déco escalonado sobre la pantalla (x=84..396, y=18..196)
    for i, pad in enumerate((0, 6, 12)):
        col = (228, 182, 82) if i % 2 == 0 else (142, 98, 38)
        d.rectangle([84 + pad, 20 + pad, 396 - pad, 196], outline=col, width=2)

    # Cortinados de terciopelo rojo intenso a los lados de la pantalla
    d.rectangle([100, 34, 134, 194], fill=(148, 24, 38), outline=(72, 12, 20))
    d.rectangle([346, 34, 380, 194], fill=(148, 24, 38), outline=(72, 12, 20))
    for cx in (108, 118, 126, 354, 362, 372):
        d.line([(cx, 34), (cx, 194)], fill=(104, 16, 26), width=2)

    # Pantalla luminosa de cine de los años 20 en el centro (x=136..344, y=40..176)
    d.rectangle([136, 40, 344, 176], fill=(238, 232, 214), outline=(214, 168, 72))

    # Escenario de madera lustrada y foso de orquesta / butacas (y=196..270)
    im.paste(dither_grad(196, H, (86, 44, 34), (42, 20, 22)), (0, 196))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 194, W, 200], fill=(214, 168, 72), outline=(42, 24, 14))
    # Candilejas cálidas al borde del escenario
    for lx in range(64, 420, 36):
        d.ellipse([lx - 4, 192, lx + 4, 198], fill=(255, 228, 128))

    save_indexed(im, "jazz_singer_theater_1927")


def build_technicolor_widescreen_1950s():
    """Gran sala de cine panorámica (CinemaScope / años 50-70) con pantalla ancha curva y luces vibrantes."""
    im = Image.new("RGB", (W, H), (0, 0, 0))
    # Techo y paredes acústicas de sala panorámica moderna en tonos púrpura/azul profundo y rojo rubí
    im.paste(dither_grad(0, 196, (16, 20, 46), (48, 24, 58)), (0, 0))
    d = ImageDraw.Draw(im)

    # Líneas de perspectiva del techo hacia la pantalla gigante con luces de neón ámbar/cian
    for lx in (20, 80, 140, 340, 400, 460):
        tx = int(240 + (lx - 240) * 0.55)
        d.line([(lx, 0), (tx, 34)], fill=(72, 168, 224), width=2)

    # Gran pantalla panorámica curva (CinemaScope) que abarca casi todo el ancho (x=36..444, y=36..178)
    d.rectangle([28, 30, 452, 184], fill=(124, 24, 44), outline=(244, 196, 84))
    # Marco interior dorado y pantalla panorámica brillante con destellos RGB
    d.rectangle([38, 38, 442, 176], fill=(24, 32, 56), outline=(244, 196, 84))
    # Degradado colorido de atardecer Technicolor dentro de la gran pantalla
    im.paste(dither_grad(40, 174, (238, 88, 108), (252, 208, 92), w=400), (40, 40))
    d = ImageDraw.Draw(im)

    # Cortinados laterales plisados en rojo Technicolor
    d.rectangle([16, 26, 40, 194], fill=(186, 32, 48), outline=(88, 14, 24))
    d.rectangle([440, 26, 464, 194], fill=(186, 32, 48), outline=(88, 14, 24))

    # Piso alfombrado rojo/dorado de gran estreno y fila de butacas bajas (y=194..270)
    im.paste(dither_grad(194, H, (112, 24, 38), (58, 12, 24)), (0, 194))
    d = ImageDraw.Draw(im)
    d.line([(0, 194), (W, 194)], fill=(244, 196, 84), width=2)
    # Luces de pasillo en el piso
    for py in range(208, H - 6, 14):
        d.rectangle([44, py, 50, py + 3], fill=(255, 214, 96))
        d.rectangle([430, py, 436, py + 3], fill=(255, 214, 96))

    save_indexed(im, "technicolor_widescreen_1950s")


def build_modern_cinema_1995():
    """Estudio de animación digital de los 90 / sala de cine digital moderna (azul cian y luz de proyector)."""
    im = Image.new("RGB", (W, H), (0, 0, 0))
    # Fondo de estudio digital / sala moderna en azul noche con grilla sutil 3D
    im.paste(dither_grad(0, 196, (12, 18, 38), (26, 42, 78)), (0, 0))
    d = ImageDraw.Draw(im)

    # Grilla de perspectiva wireframe 3D sutil en la pared de fondo (homenaje a CGI de 1993-1995)
    for gx in range(24, W, 32):
        d.line([(gx, 24), (gx, 194)], fill=(34, 58, 104), width=1)
    for gy in range(28, 194, 24):
        d.line([(0, gy), (W, gy)], fill=(34, 58, 104), width=1)

    # Cabina de proyección digital arriba al centro con lente láser/digital
    d.rectangle([208, 8, 272, 32], fill=(20, 28, 48), outline=(88, 198, 255))
    d.ellipse([232, 12, 248, 28], fill=(168, 238, 255), outline=(42, 118, 184))

    # Paneles acústicos modernos en los flancos con tiras LED azul/ámbar
    for sx in (14, 438):
        d.rectangle([sx, 28, sx + 28, 192], fill=(18, 26, 48), outline=(64, 138, 204))
        d.line([(sx + 14, 34), (sx + 14, 186)], fill=(90, 220, 255), width=2)

    # Piso técnico oscuro con reflejos cian donde apoyan los escritorios CGI y personajes (y=196..270)
    im.paste(dither_grad(196, H, (28, 38, 64), (16, 22, 38)), (0, 196))
    d = ImageDraw.Draw(im)
    d.line([(0, 196), (W, 196)], fill=(88, 198, 255), width=2)
    for px in range(0, W + 40, 40):
        dx = int((px - 240) * 1.35)
        d.line([(px, 196), (240 + dx, H)], fill=(36, 52, 86), width=1)

    save_indexed(im, "modern_cinema_1995")


if __name__ == "__main__":
    build_palo_alto_track_1878()
    build_paris_salon_indien_1895()
    build_melies_glass_studio()
    build_hollywood_hills_1915()
    build_jazz_singer_theater_1927()
    build_technicolor_widescreen_1950s()
    build_modern_cinema_1995()
    print("All 7 cinema backgrounds generated successfully!")
