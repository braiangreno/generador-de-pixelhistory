"""Convierte los assets generados (fondos y retratos) a pixel art real:
resolución nativa del lienzo (480x270) y paleta limitada."""
import glob, os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 480, 270


def quantize(im, colors):
    q = im.convert("RGB").quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    return q.convert("RGB")


def prep_backgrounds():
    out = os.path.join(ROOT, "assets", "bg")
    os.makedirs(out, exist_ok=True)
    for f in glob.glob(os.path.join(ROOT, "gen", "backgrounds_raw", "*.*")):
        im = Image.open(f).convert("RGB")
        w, h = im.size
        nw = round(w * H / h)
        im = im.resize((nw, H), Image.Resampling.BOX)
        x0 = (nw - W) // 2
        im = im.crop((x0, 0, x0 + W, H))
        im = quantize(im, 56)
        name = os.path.splitext(os.path.basename(f))[0]
        im.save(os.path.join(out, name + ".png"))
        print("bg", name, im.size)


def prep_portraits(size=64):
    out = os.path.join(ROOT, "assets", "portraits")
    os.makedirs(out, exist_ok=True)
    for f in glob.glob(os.path.join(ROOT, "gen", "portraits_raw", "*.*")):
        im = Image.open(f).convert("RGB")
        im = im.resize((size, size), Image.Resampling.BOX)
        im = quantize(im, 28)
        name = os.path.splitext(os.path.basename(f))[0]
        im.save(os.path.join(out, name + ".png"))
        print("portrait", name)


if __name__ == "__main__":
    prep_backgrounds()
    prep_portraits()
