"""Stage 3 — Generador de Arte Pixel 16-Bit (`asset_generator.py`).
Genera fondos (480x270) y retratos (64x64) usando Google Gemini / Imagen API, OpenAI Image API
o el motor procedural 16-bit de respaldo, y luego los procesa con cuantización pixel-art.
"""
import base64
import json
import math
import os
import random
import urllib.error
import urllib.request

from PIL import Image, ImageDraw

W, H = 480, 270


def quantize_pixel(im: Image.Image, colors: int = 56) -> Image.Image:
    q = im.convert("RGB").quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    return q.convert("RGBA")


def _generate_image_gemini(api_key: str, prompt: str, aspect: str = "16:9") -> Image.Image:
    """Llama a Imagen 3 / Gemini Image Generation."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key={api_key}"
    body = {
        "instances": [{"prompt": prompt}],
        "parameters": {"sampleCount": 1, "aspectRatio": aspect},
    }
    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"), method="POST",
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    b64 = data["predictions"][0]["bytesBase64Encoded"]
    import io
    return Image.open(io.BytesIO(base64.b64decode(b64))).convert("RGB")


def _generate_image_openai(api_key: str, prompt: str, size: str = "1536x1024") -> Image.Image:
    url = "https://api.openai.com/v1/images/generations"
    body = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": "1792x1024" if size != "1024x1024" else "1024x1024",
        "response_format": "b64_json",
    }
    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"), method="POST",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    b64 = data["data"][0]["b64_json"]
    import io
    return Image.open(io.BytesIO(base64.b64decode(b64))).convert("RGB")


def _procedural_16bit_bg(name: str, theme: str = "lab", seed: int = 1) -> Image.Image:
    """Genera un escenario 16-bit estilo SNES/Chrono Trigger detallado (480x270) con piso en y=222..270."""
    rnd = random.Random(seed)
    im = Image.new("RGBA", (W, H), (14, 18, 36, 255))
    d = ImageDraw.Draw(im)

    palettes = {
        "lab": ((24, 32, 48), (46, 58, 76), (82, 62, 44), (110, 82, 54)),
        "city": ((12, 16, 42), (28, 36, 78), (36, 38, 52), (52, 56, 74)),
        "living": ((58, 44, 38), (94, 72, 58), (118, 78, 48), (142, 96, 62)),
        "arcade": ((18, 10, 38), (44, 18, 76), (32, 22, 54), (58, 34, 92)),
        "office": ((26, 36, 56), (48, 64, 92), (72, 76, 88), (96, 102, 118)),
        "desert": ((32, 24, 58), (168, 92, 54), (194, 132, 68), (156, 102, 52)),
        "neon": ((10, 8, 28), (48, 16, 68), (22, 28, 54), (40, 220, 224)),
    }
    top_c, mid_c, floor_c, trim_c = palettes.get(theme, palettes["lab"])

    # Pared / Cielo con bandas 16-bit
    for y in range(222):
        k = (y // 6) / 37.0
        r = int(top_c[0] + (mid_c[0] - top_c[0]) * k)
        g = int(top_c[1] + (mid_c[1] - top_c[1]) * k)
        b = int(top_c[2] + (mid_c[2] - top_c[2]) * k)
        d.line([(0, y), (W, y)], fill=(r, g, b, 255))

    # Piso con perspectiva y baldosas/tablones (y=222..270)
    d.rectangle([0, 222, W, H], fill=(*floor_c, 255))
    d.rectangle([0, 218, W, 223], fill=(*trim_c, 255))
    for gy in range(228, H, 10):
        d.line([(0, gy), (W, gy)], fill=(max(0, floor_c[0] - 16), max(0, floor_c[1] - 16), max(0, floor_c[2] - 16), 255))
    for gx in range(0, W + 40, 40):
        d.line([(gx, 222), (gx - 24 + (gx - 240) // 4, H)], fill=(max(0, floor_c[0] - 14), max(0, floor_c[1] - 14), max(0, floor_c[2] - 14), 255))

    if theme in ("city", "neon"):
        # Horizonte de edificios pixel-art con ventanas encendidas
        for bx in range(8, W - 20, 38):
            bw = rnd.choice([28, 32, 36])
            bh = rnd.randint(70, 145)
            by = 218 - bh
            d.rectangle([bx, by, bx + bw, 218], fill=(18, 22, 44, 255), outline=(42, 52, 88, 255))
            for wy in range(by + 8, 210, 10):
                for wx in range(bx + 5, bx + bw - 5, 8):
                    if rnd.random() > 0.35:
                        wcol = (255, 220, 120, 255) if theme == "city" else rnd.choice([(40, 220, 224, 255), (231, 50, 182, 255)])
                        d.rectangle([wx, wy, wx + 4, wy + 5], fill=wcol)
    elif theme == "living":
        # Ventana izquierda + mueble y televisor en (211, 70 .. 309, 129)
        d.rectangle([24, 42, 104, 162], fill=(140, 195, 235, 255), outline=(92, 62, 38, 255), width=3)
        d.line([(64, 42), (64, 162)], fill=(92, 62, 38, 255), width=2)
        d.line([(24, 102), (104, 102)], fill=(92, 62, 38, 255), width=2)
        # Mueble bajo y TV
        d.rectangle([186, 152, 334, 220], fill=(82, 52, 32, 255), outline=(24, 16, 12, 255))
        d.rectangle([205, 64, 315, 135], fill=(38, 42, 52, 255), outline=(18, 20, 28, 255), width=2)
        d.rectangle([211, 70, 309, 129], fill=(14, 24, 48, 255))
    else:
        # Laboratorio / Oficina: estanterías, mesa técnica y osciloscopio en (293..311, 148..166)
        for sx in (36, 352):
            d.rectangle([sx, 48, sx + 92, 218], fill=(42, 34, 28, 255), outline=(18, 14, 12, 255))
            for sy in (84, 124, 164):
                d.rectangle([sx + 4, sy, sx + 88, sy + 5], fill=(78, 58, 40, 255))
        # Escritorio central
        d.rectangle([136, 170, 344, 222], fill=(106, 72, 44, 255), outline=(22, 16, 12, 255))
        # Osciloscopio en x=286..320, y=140..170
        d.rectangle([286, 140, 320, 170], fill=(150, 158, 148, 255), outline=(22, 26, 24, 255))
        d.rectangle([292, 147, 312, 167], fill=(10, 28, 16, 255))

    return quantize_pixel(im, 56)


def _procedural_16bit_portrait(name: str, seed: int = 1) -> Image.Image:
    rnd = random.Random(seed)
    im = Image.new("RGBA", (64, 64), (20, 26, 54, 255))
    d = ImageDraw.Draw(im)
    skin = rnd.choice([(245, 205, 172), (226, 178, 138), (186, 132, 94)])
    hair = rnd.choice([(52, 36, 26), (96, 68, 38), (195, 198, 208), (28, 26, 36)])
    suit = rnd.choice([(44, 82, 148), (138, 52, 68), (46, 112, 84), (78, 66, 128)])
    # Hombros/traje
    d.rectangle([10, 42, 54, 63], fill=(*suit, 255), outline=(14, 12, 24, 255))
    d.rectangle([26, 42, 38, 58], fill=(242, 240, 234, 255))
    # Cabeza
    d.rectangle([18, 14, 46, 42], fill=(*skin, 255), outline=(14, 12, 24, 255))
    # Cabello
    d.rectangle([16, 10, 48, 20], fill=(*hair, 255), outline=(14, 12, 24, 255))
    # Ojos y boca
    d.rectangle([24, 25, 27, 29], fill=(14, 12, 24, 255))
    d.rectangle([37, 25, 40, 29], fill=(14, 12, 24, 255))
    d.rectangle([28, 35, 36, 37], fill=(148, 72, 64, 255))
    return quantize_pixel(im, 28)


def generate_project_assets(project_dir: str, plan: dict, settings: dict, log_fn=print):
    bg_dir = os.path.join(project_dir, "assets", "bg")
    por_dir = os.path.join(project_dir, "assets", "portraits")
    os.makedirs(bg_dir, exist_ok=True)
    os.makedirs(por_dir, exist_ok=True)

    img_provider = settings.get("image_provider", "auto")
    gemini_key = settings.get("gemini_api_key", "").strip()
    openai_key = settings.get("openai_api_key", "").strip()

    bgs = plan.get("backgrounds", [])
    if not bgs:
        bgs = [{"name": "bg_main", "theme": "lab", "prompt": "16-bit SNES pixel art laboratory background"}]

    log_fn(f"[Stage 3] Generando y cuantizando {len(bgs)} fondos pixel-art (480x270)...")
    for idx, b_item in enumerate(bgs):
        b_name = b_item.get("name", f"bg_{idx:02d}")
        out_path = os.path.join(bg_dir, f"{b_name}.png")
        if os.path.exists(out_path) and os.path.getsize(out_path) > 500:
            continue
        prompt = b_item.get("prompt", f"16-bit SNES pixel art background {b_name}, 480x270, no text")
        theme = b_item.get("theme", "lab")
        raw_im = None
        if img_provider in ("auto", "gemini") and gemini_key:
            try:
                raw_im = _generate_image_gemini(gemini_key, prompt, aspect="16:9")
            except Exception as e:
                log_fn(f"  [Aviso Imagen Gemini {b_name}] {e}")
        if raw_im is None and img_provider in ("auto", "openai") and openai_key:
            try:
                raw_im = _generate_image_openai(openai_key, prompt, size="1792x1024")
            except Exception as e:
                log_fn(f"  [Aviso Imagen OpenAI {b_name}] {e}")

        if raw_im is not None:
            w, h = raw_im.size
            nw = max(W, round(w * H / h))
            im_resized = raw_im.resize((nw, H), Image.Resampling.BOX)
            x0 = (nw - W) // 2
            im_crop = im_resized.crop((x0, 0, x0 + W, H))
            final_bg = quantize_pixel(im_crop, 56)
            final_bg.save(out_path)
            log_fn(f"  [BG {idx + 1}/{len(bgs)}] {b_name}.png generado con IA y cuantizado a 56 colores.")
        else:
            final_bg = _procedural_16bit_bg(b_name, theme=theme, seed=idx + 10)
            final_bg.save(out_path)
            log_fn(f"  [BG {idx + 1}/{len(bgs)}] {b_name}.png generado con motor procedural 16-bit ({theme}).")

    portraits = plan.get("portraits", [])
    if portraits:
        log_fn(f"[Stage 3] Generando {len(portraits)} retratos 16-bit (64x64)...")
    for idx, p_item in enumerate(portraits):
        p_name = p_item.get("name", f"portrait_{idx:02d}")
        out_path = os.path.join(por_dir, f"{p_name}.png")
        if os.path.exists(out_path) and os.path.getsize(out_path) > 200:
            continue
        prompt = p_item.get("prompt", f"16-bit SNES pixel art 64x64 portrait {p_name}")
        raw_im = None
        if img_provider in ("auto", "gemini") and gemini_key:
            try:
                raw_im = _generate_image_gemini(gemini_key, prompt, aspect="1:1")
            except Exception:
                pass
        if raw_im is None and img_provider in ("auto", "openai") and openai_key:
            try:
                raw_im = _generate_image_openai(openai_key, prompt, size="1024x1024")
            except Exception:
                pass
        if raw_im is not None:
            im_64 = raw_im.resize((64, 64), Image.Resampling.BOX)
            final_p = quantize_pixel(im_64, 28)
        else:
            final_p = _procedural_16bit_portrait(p_name, seed=idx + 100)
        final_p.save(out_path)
        log_fn(f"  [PORTRAIT {idx + 1}/{len(portraits)}] {p_name}.png listo (64x64).")
