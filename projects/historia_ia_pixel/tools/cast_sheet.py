"""Hoja de personajes: retrato 16-bit + sprite de cada personaje, agrupados por capítulo.
Genera renders/personajes.png y un GIF animado del elenco (renders/personajes_sprites.gif)."""
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "engine"))
from core import *  # noqa
import sprites as S

CAST = [
    ("APERTURA Y CAP. 1 · LA PREGUNTA", [
        ("alan_turing", "turing", "ALAN TURING", "1950"),
        ("john_mccarthy", "mccarthy", "JOHN McCARTHY", "1956"),
        ("marvin_minsky", "minsky", "MARVIN MINSKY", "1956"),
        ("claude_shannon", "shannon", "CLAUDE SHANNON", "1956"),
        ("nathaniel_rochester", "rochester", "N. ROCHESTER", "1956"),
        ("la_maquina", "robot", "LA MÁQUINA", "1955–HOY"),
    ]),
    ("CAP. 2 · LA MÁQUINA QUE IBA A SER CONSCIENTE", [
        ("frank_rosenblatt", "rosenblatt", "F. ROSENBLATT", "1958"),
        ("navy_officer_1958", "navy", "MARINA DE EE.UU.", "1958"),
        ("nyt_reporter_1958", "reporter", "PERIODISTA NYT", "1958"),
        ("seymour_papert", "papert", "SEYMOUR PAPERT", "1969"),
    ]),
    ("CAP. 3 · EL PRIMER INVIERNO", [
        ("marvin_minsky_1970", "minsky70", "MARVIN MINSKY", "1970"),
        ("james_lighthill", "lighthill", "J. LIGHTHILL", "1973"),
        ("darpa_official_1974", "darpa", "DARPA", "1974"),
    ]),
    ("CAP. 4 · REGLAS, EXPERTOS Y EL SEGUNDO INVIERNO", [
        ("expert_engineer_1985", "kengineer", "ING. DEL CONOC.", "1985"),
        ("david_rumelhart", "rumelhart", "D. RUMELHART", "1986"),
        ("geoffrey_hinton_1986", "hinton86", "GEOFFREY HINTON", "1986"),
        ("ronald_williams", "williams", "RONALD WILLIAMS", "1986"),
    ]),
    ("CAP. 5 · PLACAS DE VIDEOJUEGOS", [
        ("garry_kasparov", "kasparov", "GARRY KASPAROV", "1997"),
        ("deep_blue_operator", "ibm_op", "EQUIPO DEEP BLUE", "1997"),
        ("fei_fei_li", "feifei", "FEI-FEI LI", "2009"),
        ("alex_krizhevsky", "krizhevsky", "A. KRIZHEVSKY", "2012"),
        ("ilya_sutskever", "sutskever", "ILYA SUTSKEVER", "2012"),
        ("geoffrey_hinton_2012", "hinton12", "GEOFFREY HINTON", "2012"),
    ]),
    ("CAP. 6 · LA JUGADA 37", [
        ("lee_sedol", "leesedol", "LEE SEDOL", "2016"),
        ("aja_huang", "ajahuang", "AJA HUANG", "2016"),
    ]),
    ("CAP. 7 · ATENCIÓN", [
        ("google_researcher_2017", "googler", "AUTORES TRANSFORMER", "2017"),
        ("sam_altman", "altman", "SAM ALTMAN", "2022"),
        ("chatgpt_user_2022", "user", "USUARIA DE CHATGPT", "2022"),
    ]),
    ("CAP. 8 · EL VERANO QUE NO TERMINÓ", [
        ("john_hopfield", "hopfield", "JOHN HOPFIELD", "2024"),
        ("geoffrey_hinton_2024", "hinton24", "GEOFFREY HINTON", "2024"),
        ("demis_hassabis", "hassabis", "DEMIS HASSABIS", "2024"),
        ("john_jumper", "jumper", "JOHN JUMPER", "2024"),
        ("david_baker", "baker", "DAVID BAKER", "2024"),
    ]),
]

CELL_W, CELL_H = 112, 118
COLS = 6


def sprite_img(key, t=0.4, **pose):
    if key == "robot":
        return Image.fromarray(S.render_robot("happy", int(t * 30) % 90), "RGBA")
    return Image.fromarray(S.render(S.CAST[key], t, **pose), "RGBA")


def build_sheet():
    rows = sum((len(g) + COLS - 1) // COLS for _, g in CAST)
    Wd = 16 + COLS * CELL_W
    Hd = 44 + rows * CELL_H + len(CAST) * 22 + 10
    cv = Image.new("RGBA", (Wd, Hd), (*NAVY, 255))
    cv_bg = vgradient((10, 12, 28), (30, 36, 70)).resize((Wd, Hd), Image.NEAREST)
    cv.alpha_composite(cv_bg)
    # usamos un lienzo intermedio de tamaño libre: dibujamos con funciones propias
    d = ImageDraw.Draw(cv)
    y = 10

    def text(s, x, yy, fname="press", size=8, color=CREAM, align="left", gradient=None):
        img = render_text(s, fname, size, color, INK, True, tuple(map(tuple, gradient)) if gradient else None, 1)
        tw = img.size[0] - 6
        xx = x - tw // 2 if align == "center" else x
        cv.alpha_composite(img, (int(xx) - 3, int(yy) - 3 - top_pad(fname, size)))

    text("PERSONAJES · LA HISTORIA DE LA IA", Wd // 2, y, "press", 16, align="center", gradient=GOLD_RAMP)
    y += 34
    for title, group in CAST:
        text(title, 12, y, "press", 8, CYAN)
        y += 16
        for i, (pfile, skey, name, year) in enumerate(group):
            if i and i % COLS == 0:
                y += CELL_H
            cx = 8 + (i % COLS) * CELL_W
            # ventana
            box = Image.new("RGBA", (CELL_W - 6, CELL_H - 8))
            cv2 = Image.new("RGBA", (Wd, Hd), (0, 0, 0, 0))
            # retrato
            p = portrait(pfile)
            d.rectangle([cx + 2, y + 2, cx + 69, y + 69], fill=(*INK, 255), outline=(*GOLD, 255))
            cv.alpha_composite(p, (cx + 4, y + 4))
            # sprite al lado
            spr = sprite_img(skey)
            sx = cx + 74 + (28 - spr.size[0]) // 2
            d.ellipse([cx + 76, y + 64, cx + 98, y + 69], fill=(0, 0, 0, 90))
            cv.alpha_composite(spr, (sx, y + 68 - spr.size[1]))
            text(name, cx + 4, y + 76, "silkb", 8, CREAM)
            text(year, cx + 4, y + 88, "silk", 8, GOLD)
        y += CELL_H - 12
    cv = cv.crop((0, 0, Wd, y + 6))
    out = cv.convert("RGB").resize((cv.size[0] * 3, cv.size[1] * 3), Image.NEAREST)
    os.makedirs(os.path.join(ROOT, "renders"), exist_ok=True)
    out.save(os.path.join(ROOT, "renders", "personajes.png"))
    print("sheet", out.size)


def build_gif():
    keys = list(S.CAST.keys()) + ["robot"]
    cols = 10
    rows = (len(keys) + cols - 1) // cols
    poses = [dict(arms="down"), dict(arms="wave", mood="happy"), dict(arms="down", walk=None),
             dict(arms="cheer", mood="happy"), dict(arms="think"), dict(arms="type")]
    frames = []
    for f in range(48):
        t = f / 12
        pose = poses[(f // 8) % len(poses)]
        cv = Image.new("RGBA", (cols * 34 + 8, rows * 60 + 8), (*NAVY, 255))
        for i, k in enumerate(keys):
            x, y = 4 + (i % cols) * 34, 4 + (i // cols) * 60
            if k == "robot":
                spr = Image.fromarray(S.render_robot(["happy", "talk", "think", "question", "heart", "happy"][(f // 8) % 6],
                                                      int(t * 30) % 90), "RGBA")
            else:
                spr = Image.fromarray(S.render(S.CAST[k], t, talk=[0, 1, 2, 1][f % 4] if (f // 8) % 2 else 0, **pose),
                                      "RGBA")
            cv.alpha_composite(spr, (x + (30 - spr.size[0]) // 2, y + 54 - spr.size[1]))
        frames.append(cv.convert("RGB").resize((cv.size[0] * 3, cv.size[1] * 3), Image.NEAREST))
    frames[0].save(os.path.join(ROOT, "renders", "personajes_sprites.gif"), save_all=True,
                   append_images=frames[1:], duration=83, loop=0)
    print("gif ok")


if __name__ == "__main__":
    build_sheet()
    build_gif()
