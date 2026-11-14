from PIL import Image
import os

BRAIN = r"C:\Users\Braian\.gemini\antigravity\brain\6d63fc15-c960-4290-9a2f-20573778b321"
OUT = r"C:\Users\Braian\.gemini\antigravity\scratch\historia_nvidia_pixel\assets\bg"
os.makedirs(OUT, exist_ok=True)

MAPPING = {
    "diner_1993": "diner_1993_1794656482664.jpg",
    "startup_office_1995": "startup_office_1995_1794656513900.jpg",
    "tokyo_office_1996": "tokyo_office_1996_1794656538351.jpg",
    "california_chip_lab_1997": "california_chip_lab_1997_1794656567811.jpg",
    "gamer_bedroom_1999": "gamer_bedroom_1999_1794656643304.jpg",
    "stage_cuda_2006": "stage_cuda_2006_1794656680932.jpg",
    "science_gpu_lab": "science_gpu_lab_1794656494638.jpg",
    "wall_street_floor": "wall_street_floor_1794656504897.jpg",
    "green_bridge_fog": "green_bridge_fog_1794656515365.jpg",
    "toronto_dorm_2012": "toronto_dorm_2012_1794656556249.jpg",
    "sf_ai_lab_2016": "sf_ai_lab_2016_1794656565161.jpg",
    "datacenter_gold": "datacenter_gold_1794656575602.jpg",
    "gold_rush_town": "gold_rush_town_1794656485485.jpg",
    "storm_cargo_ship": "storm_cargo_ship_1794656510865.jpg",
    "boardroom_night": "boardroom_night_1794656536990.jpg",
    "empty_ceo_office": "empty_ceo_office_1794656567837.jpg",
    "capitol_dome_night": "capitol_dome_night_1794656604606.jpg",
}

for name, fname in MAPPING.items():
    src = os.path.join(BRAIN, fname)
    im = Image.open(src).convert("RGB")
    # Downscale to 240x135 then 2x nearest to 480x270 for crisp 16-bit pixel grid, quantized to 48 colors
    small = im.resize((240, 135), Image.BOX).quantize(colors=48, method=Image.MEDIANCUT).convert("RGBA")
    final = small.resize((480, 270), Image.NEAREST)
    out_path = os.path.join(OUT, f"{name}.png")
    final.save(out_path)
    print("Saved", out_path)
