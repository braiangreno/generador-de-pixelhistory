"""Generador procedural de fondos pixel-art 16-bit (480x270) para 'UNA LLAMADA AL RIVAL'."""
import math
import os
import sys
import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
from core import W, H, bayer_tile, vgradient, shade, INK

OUT_DIR = os.path.join(ROOT, "assets", "bg")
os.makedirs(OUT_DIR, exist_ok=True)


def quantize_16bit(im, colors=56):
    q = im.convert("RGB").quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    return q.convert("RGBA")


def dither_rect(cv, x0, y0, x1, y1, c1, c2, ratio=0.5):
    a = np.array(cv)
    th = bayer_tile(W, H)
    x0, x1 = max(0, int(x0)), min(W, int(x1))
    y0, y1 = max(0, int(y0)), min(H, int(y1))
    if x1 <= x0 or y1 <= y0:
        return
    sub = a[y0:y1, x0:x1]
    m = th[y0:y1, x0:x1] < ratio
    sub[:, :, :3] = np.where(m[:, :, None], np.array(c1, dtype=np.uint8), np.array(c2, dtype=np.uint8))
    sub[:, :, 3] = 255
    a[y0:y1, x0:x1] = sub
    cv.paste(Image.fromarray(a, "RGBA"), (0, 0))


def draw_windows_grid(d, x0, y0, x1, y1, wx=6, wy=8, gx=10, gy=13, lit_col=(248, 214, 130), dark_col=(42, 34, 38), seed=1):
    idx = seed
    for y in range(y0, y1 - wy, gy):
        for x in range(x0, x1 - wx, gx):
            idx = (idx * 1103515245 + 12345) & 0x7FFFFFFF
            col = lit_col if (idx % 5 in (0, 1)) else dark_col
            d.rectangle([x, y, x + wx, y + wy], fill=(*col, 255), outline=(22, 18, 24, 255))


def draw_taxi_1973(d, x, y):
    # Classic 1973 NYC Checker Taxi in warm yellow
    yel = (238, 184, 44, 255)
    yel_sh = (194, 138, 28, 255)
    win_c = (72, 92, 114, 255)
    d.rectangle([x, y + 8, x + 56, y + 20], fill=yel, outline=(*INK, 255))
    d.rectangle([x + 2, y + 15, x + 54, y + 20], fill=yel_sh)
    d.polygon([(x + 10, y + 8), (x + 16, y), (x + 40, y), (x + 46, y + 8)], fill=yel, outline=(*INK, 255))
    d.polygon([(x + 13, y + 7), (x + 17, y + 2), (x + 27, y + 2), (x + 27, y + 7)], fill=win_c)
    d.polygon([(x + 29, y + 7), (x + 29, y + 2), (x + 39, y + 2), (x + 43, y + 7)], fill=win_c)
    # Checker stripe
    for cx in range(x + 4, x + 52, 4):
        c_chk = (20, 18, 22, 255) if ((cx // 4) % 2 == 0) else (245, 240, 220, 255)
        d.rectangle([cx, y + 11, cx + 2, y + 13], fill=c_chk)
    # Roof light
    d.rectangle([x + 25, y - 3, x + 31, y], fill=(255, 232, 140, 255), outline=(*INK, 255))
    # Wheels
    for wx in (x + 11, x + 43):
        d.ellipse([wx - 6, y + 15, wx + 6, y + 25], fill=(26, 24, 28, 255), outline=(*INK, 255))
        d.ellipse([wx - 2, y + 18, wx + 2, y + 22], fill=(168, 164, 156, 255))


def bg_nyc_sixth_ave_1973():
    """1973 Sixth Avenue in New York in warm ochre/brown tones with yellow cabs and phone booth."""
    cv = vgradient((218, 168, 108), (154, 104, 64), 10)
    d = ImageDraw.Draw(cv)
    # Distant Manhattan skyscrapers silhouettes
    sky_blds = [
        (0, 26, 64, 190, (96, 68, 52)),
        (58, 14, 128, 190, (112, 78, 56)),
        (122, 34, 188, 190, (88, 62, 48)),
        (182, 8, 268, 190, (124, 86, 60)),
        (262, 28, 336, 190, (98, 70, 52)),
        (330, 16, 412, 190, (116, 80, 56)),
        (406, 24, 480, 190, (92, 64, 48)),
    ]
    for x0, y0, x1, y1, col in sky_blds:
        d.rectangle([x0, y0, x1, y1], fill=(*col, 255), outline=(*INK, 255))
        draw_windows_grid(d, x0 + 6, y0 + 8, x1 - 4, y1 - 24, lit_col=(244, 198, 118),
                          dark_col=shade(col, 0.65), seed=x0 + y0)

    # Foreground storefront & NY Hilton facade at street level (y=138..194)
    d.rectangle([0, 142, 480, 194], fill=(104, 68, 44, 255), outline=(*INK, 255))
    # Awning "SIXTH AVE · 1973"
    d.polygon([(140, 146), (340, 146), (352, 162), (128, 162)], fill=(156, 52, 38, 255), outline=(*INK, 255))
    for sx in range(136, 348, 12):
        d.line([(sx, 147), (sx - 3, 161)], fill=(232, 198, 148, 200), width=2)

    # Asphalt street with yellow cabs (y=190..218)
    d.rectangle([0, 190, W, 218], fill=(64, 54, 52, 255), outline=(*INK, 255))
    for lx in range(8, W, 32):
        d.rectangle([lx, 203, lx + 16, 205], fill=(228, 182, 68, 255))
    draw_taxi_1973(d, 28, 180)
    draw_taxi_1973(d, 376, 182)

    # Classic NYC glass & aluminum phone booth on the sidewalk (left-back at x=84..116)
    bx, by = 82, 142
    d.rectangle([bx, by, bx + 32, 222], fill=(58, 76, 88, 220), outline=(*INK, 255))
    d.rectangle([bx + 2, by + 2, bx + 30, by + 10], fill=(192, 64, 44, 255), outline=(*INK, 255))
    d.rectangle([bx + 4, by + 13, bx + 28, 218], fill=(168, 194, 198, 140), outline=(188, 184, 172, 255))
    d.line([(bx + 16, by + 13), (bx + 16, 218)], fill=(188, 184, 172, 255), width=1)
    # Rotary payphone silhouette inside booth
    d.rectangle([bx + 11, by + 28, bx + 21, by + 44], fill=(32, 30, 36, 255))

    # Broad NYC sidewalk pavement where characters stand (y=218..270, feet=248)
    dither_rect(cv, 0, 218, W, 270, (176, 148, 118), (162, 134, 104), 0.5)
    d = ImageDraw.Draw(cv)
    d.rectangle([0, 218, W, 223], fill=(198, 172, 138, 255), outline=(*INK, 255))
    for sx in range(0, W, 48):
        d.line([(sx, 223), (sx - 18, 270)], fill=(128, 102, 78, 255), width=1)
    d.line([(0, 256), (W, 256)], fill=(134, 108, 84, 255), width=1)
    return quantize_16bit(cv)


def bg_motorola_lab_1973():
    """1970s Motorola electronics lab and boardroom."""
    cv = vgradient((68, 56, 48), (46, 36, 32), 10)
    d = ImageDraw.Draw(cv)
    # Wood paneling & upper lab wall
    d.rectangle([0, 0, W, 168], fill=(92, 74, 58, 255))
    dither_rect(cv, 0, 128, W, 220, (76, 52, 36), (64, 44, 30), 0.5)
    d = ImageDraw.Draw(cv)
    for vx in range(0, W, 24):
        d.line([(vx, 128), (vx, 220)], fill=(48, 32, 22, 255), width=1)
    d.line([(0, 128), (W, 128)], fill=(138, 98, 62, 255), width=2)

    # Ceiling fluorescent lamps
    for lx in (72, 240, 408):
        d.rectangle([lx - 42, 6, lx + 42, 14], fill=(248, 244, 218, 255), outline=(*INK, 255))

    # Left & Right electronics racks and oscilloscopes in background
    for rx in (18, 396):
        d.rectangle([rx, 46, rx + 64, 220], fill=(58, 64, 72, 255), outline=(*INK, 255))
        for ry in range(54, 196, 28):
            d.rectangle([rx + 6, ry, rx + 58, ry + 22], fill=(42, 46, 54, 255), outline=(*INK, 255))
            # Oscilloscope screen
            d.rectangle([rx + 10, ry + 4, rx + 34, ry + 18], fill=(16, 44, 32, 255))
            d.line([(rx + 12, ry + 11), (rx + 18, ry + 7), (rx + 24, ry + 15), (rx + 32, ry + 11)],
                   fill=(96, 238, 142, 255), width=1)
            # Dials
            for dx in (rx + 40, rx + 48):
                d.ellipse([dx, ry + 6, dx + 5, ry + 11], fill=(196, 188, 168, 255))

    # Blueprint board in center-back
    d.rectangle([156, 44, 324, 118], fill=(32, 64, 98, 255), outline=(188, 152, 96, 255), width=2)
    for gx in range(166, 320, 16):
        d.line([(gx, 48), (gx, 114)], fill=(46, 84, 124, 255))
    for gy in range(52, 114, 16):
        d.line([(160, gy), (320, gy)], fill=(46, 84, 124, 255))

    # Tiled laboratory floor (y=220..270)
    dither_rect(cv, 0, 220, W, 270, (148, 138, 122), (132, 122, 108), 0.5)
    d = ImageDraw.Draw(cv)
    d.line([(0, 220), (W, 220)], fill=(*INK, 255), width=2)
    for tx in range(0, W + 32, 32):
        d.line([(tx, 220), (tx - 20, 270)], fill=(108, 98, 86, 255), width=1)
    for ty in (234, 250, 264):
        d.line([(0, ty), (W, ty)], fill=(108, 98, 86, 255), width=1)
    return quantize_16bit(cv)


def bg_bell_labs_honeycomb_1970():
    """Bell Labs office with hexagonal city map on wall and mid-century wood tones."""
    cv = vgradient((42, 52, 72), (28, 36, 52), 10)
    d = ImageDraw.Draw(cv)
    # Mid-century acoustic wall panels
    for wx in range(0, W, 32):
        d.rectangle([wx, 0, wx + 31, 218], fill=(52, 62, 82, 255) if (wx // 32) % 2 == 0 else (46, 56, 76, 255))
        d.line([(wx, 0), (wx, 218)], fill=(32, 40, 56, 255))

    # Large illuminated hexagonal cellular map on back wall
    d.rectangle([124, 38, 356, 154], fill=(16, 28, 44, 255), outline=(186, 146, 78, 255), width=3)
    # Hexagons inside wall map
    r_hex = 14
    for row in range(-2, 3):
        for col in range(-4, 5):
            cx = 240 + col * int(r_hex * 1.55)
            cy = 96 + row * int(r_hex * 1.75) + (int(r_hex * 0.87) if col % 2 else 0)
            if 138 < cx < 342 and 52 < cy < 140:
                pts = [(cx + int(r_hex * math.cos(a * math.pi / 3)),
                        cy + int(r_hex * math.sin(a * math.pi / 3))) for a in range(6)]
                d.polygon(pts, outline=(72, 168, 212, 200), fill=(22, 42, 64, 255))
                d.point((cx, cy), fill=(248, 204, 96, 255))

    # Reel-to-reel computers on left and right
    for rx in (20, 396):
        d.rectangle([rx, 58, rx + 64, 218], fill=(68, 76, 92, 255), outline=(*INK, 255))
        d.rectangle([rx + 6, 66, rx + 58, 118], fill=(34, 40, 52, 255), outline=(*INK, 255))
        for cx_r in (rx + 19, rx + 45):
            d.ellipse([cx_r - 10, 82, cx_r + 10, 102], fill=(188, 194, 206, 255), outline=(*INK, 255))
            d.ellipse([cx_r - 3, 89, cx_r + 3, 95], fill=(42, 48, 62, 255))

    # Warm wood floor (y=218..270)
    dither_rect(cv, 0, 218, W, 270, (124, 88, 56), (108, 74, 46), 0.5)
    d = ImageDraw.Draw(cv)
    d.line([(0, 218), (W, 218)], fill=(*INK, 255), width=2)
    for ty in (230, 244, 258):
        d.line([(0, ty), (W, ty)], fill=(86, 58, 36, 255), width=1)
    return quantize_16bit(cv)


def bg_uk_sms_office_1992():
    """1992 English telecom office in December & 1990s workstation backdrop."""
    cv = vgradient((38, 48, 68), (26, 34, 52), 10)
    d = ImageDraw.Draw(cv)
    # Office wallpaper
    dither_rect(cv, 0, 0, W, 218, (54, 66, 88), (46, 58, 78), 0.45)
    d = ImageDraw.Draw(cv)

    # Large window on left showing snowy December night in England
    d.rectangle([28, 36, 152, 146], fill=(14, 22, 42, 255), outline=(182, 188, 204, 255), width=3)
    d.line([(90, 36), (90, 146)], fill=(182, 188, 204, 255), width=2)
    d.line([(28, 91), (152, 91)], fill=(182, 188, 204, 255), width=2)
    # Stars & snow dots outside window
    for i in range(18):
        sx = 34 + (i * 23) % 110
        sy = 42 + (i * 19) % 96
        d.rectangle([sx, sy, sx + 1, sy + 1], fill=(236, 244, 255, 255))
    # Small festive holly garland on window top
    for gx in range(36, 146, 12):
        d.ellipse([gx, 38, gx + 8, 44], fill=(46, 142, 68, 255))
        d.point((gx + 4, 41), fill=(228, 62, 54, 255))

    # Telecom server rack on right
    d.rectangle([348, 42, 446, 218], fill=(64, 72, 86, 255), outline=(*INK, 255))
    for ry in range(52, 204, 22):
        d.rectangle([356, ry, 438, ry + 16], fill=(32, 38, 48, 255), outline=(*INK, 255))
        for lx in range(362, 410, 8):
            col_l = (96, 238, 142, 255) if ((lx + ry) % 16 == 0) else (244, 184, 72, 255)
            d.rectangle([lx, ry + 6, lx + 3, ry + 9], fill=col_l)

    # Carpeted 90s office floor (y=218..270)
    dither_rect(cv, 0, 218, W, 270, (78, 88, 108), (68, 76, 96), 0.5)
    d = ImageDraw.Draw(cv)
    d.line([(0, 218), (W, 218)], fill=(*INK, 255), width=2)
    return quantize_16bit(cv)


def bg_maternity_ward_1997():
    """1997 California maternity waiting room."""
    cv = vgradient((82, 98, 116), (62, 76, 94), 10)
    d = ImageDraw.Draw(cv)
    # Warm hospital waiting room walls
    dither_rect(cv, 0, 0, W, 218, (96, 114, 132), (84, 102, 120), 0.4)
    d = ImageDraw.Draw(cv)
    d.rectangle([0, 142, W, 218], fill=(74, 88, 106, 255), outline=(*INK, 255))
    d.line([(0, 142), (W, 142)], fill=(196, 208, 222, 255), width=2)

    # Nursery viewing window on back wall
    d.rectangle([144, 42, 336, 128], fill=(184, 218, 236, 255), outline=(232, 236, 242, 255), width=3)
    d.rectangle([148, 46, 332, 124], fill=(42, 68, 92, 255))
    # Maternity sign
    d.rectangle([28, 48, 116, 78], fill=(236, 240, 246, 255), outline=(*INK, 255))
    d.rectangle([38, 56, 48, 68], fill=(224, 72, 72, 255))
    d.rectangle([34, 60, 52, 64], fill=(224, 72, 72, 255))

    # Clean hospital floor (y=218..270)
    dither_rect(cv, 0, 218, W, 270, (176, 188, 202), (160, 174, 188), 0.5)
    d = ImageDraw.Draw(cv)
    d.line([(0, 218), (W, 218)], fill=(*INK, 255), width=2)
    for tx in range(0, W + 32, 32):
        d.line([(tx, 218), (tx - 16, 270)], fill=(138, 152, 168, 255), width=1)
    return quantize_16bit(cv)


def bg_storefront_simon_1994():
    """1994 electronics storefront display."""
    cv = vgradient((24, 28, 54), (44, 38, 72), 10)
    d = ImageDraw.Draw(cv)
    # Brick electronics shop facade
    dither_rect(cv, 0, 24, W, 218, (68, 48, 58), (54, 38, 48), 0.5)
    d = ImageDraw.Draw(cv)

    # Large glass shop display window in center
    d.rectangle([64, 42, 416, 198], fill=(18, 28, 48, 255), outline=(196, 164, 96, 255), width=3)
    d.rectangle([68, 46, 412, 194], outline=(84, 148, 196, 255), width=1)
    # Diagonal glass reflection streaks
    d.line([(84, 184), (164, 54)], fill=(48, 76, 112, 255), width=3)
    d.line([(98, 184), (178, 54)], fill=(36, 58, 88, 255), width=2)

    # Shelving inside display window
    for sy in (118, 168):
        d.rectangle([82, sy, 398, sy + 5], fill=(88, 104, 132, 255), outline=(*INK, 255))

    # Sidewalk & showroom floor (y=218..270)
    dither_rect(cv, 0, 218, W, 270, (92, 86, 104), (78, 72, 90), 0.5)
    d = ImageDraw.Draw(cv)
    d.rectangle([0, 216, W, 221], fill=(132, 124, 146, 255), outline=(*INK, 255))
    for sx in range(0, W, 40):
        d.line([(sx, 221), (sx - 14, 270)], fill=(58, 52, 68, 255), width=1)
    return quantize_16bit(cv)


def bg_sf_keynote_stage_2007():
    """2007 San Francisco dark keynote stage with giant glowing screen."""
    cv = vgradient((8, 12, 26), (18, 26, 52), 12)
    d = ImageDraw.Draw(cv)
    # Subtle stage curtains on left and right
    for cx in list(range(0, 76, 8)) + list(range(404, W, 8)):
        c_cur = (16, 22, 44, 255) if (cx // 8) % 2 == 0 else (10, 14, 30, 255)
        d.rectangle([cx, 0, cx + 7, 216], fill=c_cur)

    # Giant keynote projection screen frame on stage wall
    d.rectangle([96, 28, 384, 174], fill=(12, 20, 42, 255), outline=(72, 148, 224, 255), width=2)
    # Overhead stage truss lights
    for lx in (130, 200, 280, 350):
        d.rectangle([lx - 6, 4, lx + 6, 12], fill=(84, 96, 122, 255), outline=(*INK, 255))
        d.ellipse([lx - 4, 10, lx + 4, 16], fill=(212, 238, 255, 255))

    # Polished dark keynote stage floor with blue edge glow (y=216..270)
    dither_rect(cv, 0, 216, W, 270, (28, 34, 56), (20, 24, 42), 0.5)
    d = ImageDraw.Draw(cv)
    d.line([(0, 216), (W, 216)], fill=(96, 188, 255, 255), width=2)
    d.line([(0, 218), (W, 218)], fill=(38, 78, 138, 255), width=1)
    for sx in range(0, W, 48):
        d.line([(sx, 218), (sx - 16, 270)], fill=(16, 20, 36, 255), width=1)
    return quantize_16bit(cv)


def bg_indie_dev_room_2008():
    """2008 developer bedroom/studio at night with city window & bookshelves."""
    cv = vgradient((22, 26, 48), (36, 38, 66), 10)
    d = ImageDraw.Draw(cv)
    dither_rect(cv, 0, 0, W, 218, (34, 38, 64), (28, 32, 54), 0.45)
    d = ImageDraw.Draw(cv)

    # Night window on left with city skyline
    d.rectangle([28, 38, 136, 142], fill=(12, 16, 34, 255), outline=(96, 78, 64, 255), width=3)
    for bx, bh in ((36, 42), (56, 64), (82, 52), (106, 70)):
        d.rectangle([bx, 140 - bh, bx + 18, 140], fill=(24, 32, 56, 255))
        draw_windows_grid(d, bx + 2, 144 - bh, bx + 16, 138, wx=3, wy=4, gx=6, gy=7,
                          lit_col=(248, 212, 118), dark_col=(18, 24, 42), seed=bx)

    # Bookshelf on right
    d.rectangle([356, 48, 448, 218], fill=(78, 52, 36, 255), outline=(*INK, 255))
    for sy in (84, 122, 160, 198):
        d.rectangle([360, sy, 444, sy + 4], fill=(104, 70, 48, 255))
        for kx in range(364, 436, 7):
            bcol = [(198, 68, 62), (68, 138, 196), (218, 174, 64), (76, 168, 104)][(kx + sy) % 4]
            d.rectangle([kx, sy - 18, kx + 5, sy], fill=(*bcol, 255), outline=(*INK, 255))

    # Warm wooden bedroom floor (y=218..270)
    dither_rect(cv, 0, 218, W, 270, (112, 76, 48), (96, 64, 40), 0.5)
    d = ImageDraw.Draw(cv)
    d.line([(0, 218), (W, 218)], fill=(*INK, 255), width=2)
    for ty in (232, 248, 262):
        d.line([(0, ty), (W, ty)], fill=(74, 48, 30, 255), width=1)
    return quantize_16bit(cv)


def bg_earth_orbit_gps():
    """Deep space view of Earth with GPS satellite constellation."""
    cv = vgradient((6, 8, 20), (14, 24, 52), 12)
    d = ImageDraw.Draw(cv)
    # Stars
    for i in range(120):
        sx = (i * 73 + 19) % W
        sy = (i * 41 + 7) % 210
        c_st = (240, 246, 255, 255) if i % 4 == 0 else (142, 164, 204, 255)
        d.point((sx, sy), fill=c_st)

    # Orbital ellipse tracks
    d.arc([-60, 28, W + 60, 240], 190, 350, fill=(46, 96, 148, 255), width=1)
    d.arc([-40, 56, W + 40, 260], 195, 345, fill=(38, 78, 124, 255), width=1)

    # Curved Earth horizon at bottom (y=212..270) so characters/props have a solid ground plane
    d.ellipse([-120, 206, W + 120, 420], fill=(28, 98, 168, 255), outline=(108, 224, 255, 255), width=3)
    d.ellipse([-110, 214, W + 110, 420], fill=(22, 76, 138, 255))
    # Continents in pixel green/ochre on Earth curvature
    for cx, cy, rw, rh in ((120, 238, 46, 14), (250, 232, 62, 18), (370, 242, 42, 12)):
        d.ellipse([cx - rw, cy - rh, cx + rw, cy + rh], fill=(56, 138, 88, 255))
    return quantize_16bit(cv)


def bg_modern_street_2026():
    """Modern vibrant 2026 Sixth Avenue sidewalk matching the 1973 angle."""
    cv = vgradient((54, 118, 196), (124, 184, 232), 10)
    d = ImageDraw.Draw(cv)
    # Sleek glass skyscrapers matching 1973 positions
    sky_blds = [
        (0, 22, 64, 190, (58, 92, 134)),
        (58, 10, 128, 190, (72, 112, 158)),
        (122, 28, 188, 190, (52, 84, 124)),
        (182, 6, 268, 190, (82, 128, 176)),
        (262, 24, 336, 190, (64, 102, 146)),
        (330, 12, 412, 190, (76, 118, 166)),
        (406, 20, 480, 190, (56, 88, 130)),
    ]
    for x0, y0, x1, y1, col in sky_blds:
        d.rectangle([x0, y0, x1, y1], fill=(*col, 255), outline=(*INK, 255))
        draw_windows_grid(d, x0 + 6, y0 + 8, x1 - 4, y1 - 24, lit_col=(188, 236, 255),
                          dark_col=shade(col, 0.72), seed=x0 + y0)

    # Modern ground-level glass retail facade (y=142..194)
    d.rectangle([0, 142, 480, 194], fill=(42, 64, 96, 255), outline=(*INK, 255))
    # Glowing cyan LED canopy where the 1973 awning was
    d.polygon([(140, 146), (340, 146), (352, 160), (128, 160)], fill=(28, 168, 204, 255), outline=(*INK, 255))

    # Street with modern electric yellow cabs (y=190..218)
    d.rectangle([0, 190, W, 218], fill=(52, 58, 68, 255), outline=(*INK, 255))
    for lx in range(8, W, 32):
        d.rectangle([lx, 203, lx + 16, 205], fill=(244, 204, 72, 255))
    draw_taxi_1973(d, 32, 180)
    draw_taxi_1973(d, 372, 182)

    # Modern LinkNYC / glass kiosk where the 1973 phone booth stood (x=86..110)
    bx, by = 86, 146
    d.rectangle([bx, by, bx + 22, 222], fill=(38, 48, 66, 255), outline=(*INK, 255))
    d.rectangle([bx + 3, by + 8, bx + 19, by + 48], fill=(72, 224, 248, 255), outline=(*INK, 255))

    # Modern granite sidewalk (y=218..270, feet=248)
    dither_rect(cv, 0, 218, W, 270, (168, 176, 188), (152, 160, 174), 0.5)
    d = ImageDraw.Draw(cv)
    d.rectangle([0, 218, W, 223], fill=(196, 204, 216, 255), outline=(*INK, 255))
    for sx in range(0, W, 48):
        d.line([(sx, 223), (sx - 18, 270)], fill=(122, 130, 144, 255), width=1)
    d.line([(0, 256), (W, 256)], fill=(122, 130, 144, 255), width=1)
    return quantize_16bit(cv)


def main():
    builders = {
        "nyc_sixth_ave_1973": bg_nyc_sixth_ave_1973,
        "motorola_lab_1973": bg_motorola_lab_1973,
        "bell_labs_honeycomb_1970": bg_bell_labs_honeycomb_1970,
        "uk_sms_office_1992": bg_uk_sms_office_1992,
        "maternity_ward_1997": bg_maternity_ward_1997,
        "storefront_simon_1994": bg_storefront_simon_1994,
        "sf_keynote_stage_2007": bg_sf_keynote_stage_2007,
        "indie_dev_room_2008": bg_indie_dev_room_2008,
        "earth_orbit_gps": bg_earth_orbit_gps,
        "modern_street_2026": bg_modern_street_2026,
    }
    for name, fn in builders.items():
        im = fn()
        path = os.path.join(OUT_DIR, f"{name}.png")
        im.save(path)
        print(f"Saved {path} ({im.size})")


if __name__ == "__main__":
    main()
