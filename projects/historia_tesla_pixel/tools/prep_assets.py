"""Convierte los assets generados (fondos y retratos) a pixel art real:
resolución nativa del lienzo (480x270) y paleta limitada."""
import glob
import os
import re
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAIN_DIR = r"C:\Users\Braian\.gemini\antigravity\brain\6d63fc15-c960-4290-9a2f-20573778b321"
W, H = 480, 270

TESLA_BGS = [
    "bg_dark_room_screen",
    "bg_night_grid_city",
    "bg_budapest_park_sunset",
    "bg_smiljan_storm_1856",
    "bg_candle_room_1856",
    "bg_graz_lecture_1875",
    "bg_budapest_telegraph_1881",
    "bg_ny_harbor_1884",
    "bg_edison_workshop_1884",
    "bg_ny_winter_ditch_1886",
    "bg_investors_room_1887",
    "bg_westinghouse_office_1888",
    "bg_stage_tubes_1891",
    "bg_chicago_fair_1893",
    "bg_electricity_pavilion_1893",
    "bg_niagara_power_1895",
    "bg_tesla_lab_ny_1894",
    "bg_madison_pond_1898",
    "bg_colorado_springs_1899",
    "bg_wardenclyffe_1901",
    "bg_marconi_station_1901",
    "bg_ny_plaza_pigeons_1930",
    "bg_hotel_3327_winter_1943",
    "bg_hospital_factory_1960",
]


def quantize(im, colors):
    q = im.convert("RGB").quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    return q.convert("RGB")


def process_one(src_path, out_path):
    im = Image.open(src_path).convert("RGB")
    w, h = im.size
    nw = max(W, round(w * H / h))
    im = im.resize((nw, H), Image.Resampling.BOX)
    x0 = max(0, (nw - W) // 2)
    im = im.crop((x0, 0, x0 + W, H))
    im = quantize(im, 56)
    im.save(out_path)


def prep_backgrounds():
    out = os.path.join(ROOT, "assets", "bg")
    os.makedirs(out, exist_ok=True)
    for name in TESLA_BGS:
        matches = sorted(glob.glob(os.path.join(BRAIN_DIR, f"{name}_*.*")), key=os.path.getmtime)
        if not matches:
            matches = sorted(glob.glob(os.path.join(ROOT, "gen", "backgrounds_raw", f"{name}.*")))
        if not matches:
            print("MISSING:", name)
            continue
        src = matches[-1]
        dst = os.path.join(out, f"{name}.png")
        process_one(src, dst)
        print("bg ok:", name, "<-", os.path.basename(src))


if __name__ == "__main__":
    prep_backgrounds()
