"""Generación de imágenes con IA para el motor Pixeloide: Nano Banana (Gemini) y GPT Image (OpenAI).

Lo usan el agente (scripts/arte.py) y el panel web (app/pipeline/asset_generator.py). Incluye los prompts de
retratos con parecido a la persona real y fondos de época, y la conversión a pixel art del motor
(fondos 480x270 con 56 colores, retratos 64x64 con 28 colores, sin difuminado).
Modelos configurables con GEMINI_IMAGE_MODEL y OPENAI_IMAGE_MODEL; si uno no existe se prueban los de respaldo.
"""
import base64
import io
import json
import mimetypes
import os
import urllib.error
import urllib.request
import uuid

from PIL import Image

W, H = 480, 270
GEMINI_MODELOS = ["gemini-3.1-flash-image", "gemini-3.1-flash-image-preview", "gemini-3-pro-image",
                  "gemini-3-pro-image-preview", "gemini-2.5-flash-image"]
OPENAI_MODELOS = ["gpt-image-2", "gpt-image-1.5", "gpt-image-1"]

ESTILO = "16-bit SNES pixel art in the style of Chrono Trigger and Octopath Traveler"
PIXELES = "crisp hard-edged pixels with no anti-aliasing and no blur, limited color palette"


def prompt_retrato(item):
    if item.get("persona"):
        quien = f", {item['quien']}," if item.get("quien") else ""
        anio = f" around {item['anio']}" if item.get("anio") else ""
        rasgos = f": {item['rasgos']}" if item.get("rasgos") else ""
        base = (f"Head-and-shoulders bust of {item['persona']}{quien} the real person as they looked{anio}{rasgos}. "
                "It must be a recognizable likeness of the real person: face shape, hair, facial hair, glasses, age.")
        if item.get("prompt"):
            base += " " + item["prompt"]
    else:
        base = "Head-and-shoulders bust of " + (item.get("prompt") or item.get("name", "a person"))
    return (f"{ESTILO} character portrait. {base} Three-quarter view, soft key light, {PIXELES}, "
            "plain solid dark navy blue background, centered, no text, no frame, no border.")


def prompt_fondo(item):
    return (f"{ESTILO} wide cinematic background: {item.get('prompt') or item.get('name')}. "
            "The lower third is a flat open floor with empty space for characters to stand. "
            f"No characters, no people, no text, no letters, no signs with writing, no UI. {PIXELES}, atmospheric lighting.")


def cuantizar(im, colores):
    q = im.convert("RGB").quantize(colors=colores, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    return q.convert("RGB")


def a_fondo(im):
    im = im.convert("RGB")
    w, h = im.size
    if w / h > W / H:  # más ancha que 16:9: ajusto alto y recorto los costados
        nw, nh = max(W, round(w * H / h)), H
    else:              # más alta: ajusto ancho y recorto arriba (conservo el piso)
        nw, nh = W, max(H, round(h * W / w))
    im = im.resize((nw, nh), Image.Resampling.BOX)
    x0 = (nw - W) // 2
    y0 = nh - H if nh > H else 0
    return cuantizar(im.crop((x0, y0, x0 + W, y0 + H)), 56)


def a_retrato(im):
    im = im.convert("RGB")
    w, h = im.size
    lado = min(w, h)
    im = im.crop(((w - lado) // 2, 0, (w - lado) // 2 + lado, lado))
    return cuantizar(im.resize((64, 64), Image.Resampling.BOX), 28)


def _post_json(url, body, headers):
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), method="POST",
                                 headers={"Content-Type": "application/json", **headers})
    with urllib.request.urlopen(req, timeout=240) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _post_multipart(url, campos, archivos, headers):
    borde = uuid.uuid4().hex
    partes = []
    for k, v in campos.items():
        partes.append(f'--{borde}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode("utf-8"))
    for k, (nombre, datos, mime) in archivos:
        partes.append((f'--{borde}\r\nContent-Disposition: form-data; name="{k}"; filename="{nombre}"\r\n'
                       f"Content-Type: {mime}\r\n\r\n").encode("utf-8") + datos + b"\r\n")
    partes.append(f"--{borde}--\r\n".encode("utf-8"))
    req = urllib.request.Request(url, data=b"".join(partes), method="POST",
                                 headers={"Content-Type": f"multipart/form-data; boundary={borde}", **headers})
    with urllib.request.urlopen(req, timeout=240) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _modelos(env, defecto):
    elegido = os.environ.get(env, "").strip()
    return ([elegido] + [m for m in defecto if m != elegido]) if elegido else list(defecto)


def _error_de_modelo(e):
    return e.code == 404 or (e.code == 400 and "model" in getattr(e, "_texto", "").lower())


def gen_gemini(key, prompt, aspect, ref=None):
    """Nano Banana (modelos de imagen de Gemini). ref = (bytes, mime) de una foto de referencia."""
    partes = []
    if ref:
        partes.append({"inlineData": {"mimeType": ref[1], "data": base64.b64encode(ref[0]).decode()}})
        prompt += " Use the attached photo only as a likeness reference for the person; redraw them in the pixel-art style."
    partes.append({"text": prompt})
    ultimo = None
    for modelo in _modelos("GEMINI_IMAGE_MODEL", GEMINI_MODELOS):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent"
        body = {"contents": [{"parts": partes}],
                "generationConfig": {"responseModalities": ["TEXT", "IMAGE"], "imageConfig": {"aspectRatio": aspect}}}
        try:
            data = _post_json(url, body, {"x-goog-api-key": key})
        except urllib.error.HTTPError as e:
            e._texto = e.read().decode("utf-8", errors="ignore")
            ultimo = f"{modelo}: HTTP {e.code} {e._texto[:200]}"
            if _error_de_modelo(e):
                continue
            raise RuntimeError(ultimo) from None
        for cand in data.get("candidates", []):
            for p in (cand.get("content") or {}).get("parts", []):
                if "inlineData" in p:
                    return Image.open(io.BytesIO(base64.b64decode(p["inlineData"]["data"]))), f"Nano Banana ({modelo})"
        motivo = (data.get("candidates") or [{}])[0].get("finishReason") or data.get("promptFeedback") or "sin imagen"
        raise RuntimeError(f"{modelo} no devolvió imagen ({motivo})")
    raise RuntimeError(f"Ningún modelo de Gemini disponible. Último error: {ultimo}")


def gen_openai(key, prompt, size, ref=None):
    """GPT Image. Con foto de referencia usa /images/edits."""
    ultimo = None
    for modelo in _modelos("OPENAI_IMAGE_MODEL", OPENAI_MODELOS):
        try:
            if ref:
                ext = mimetypes.guess_extension(ref[1]) or ".png"
                data = _post_multipart("https://api.openai.com/v1/images/edits",
                                       {"model": modelo, "prompt": prompt + " Keep the likeness of the person in the "
                                        "reference photo, redrawn in the pixel-art style.", "size": size, "n": "1"},
                                       [("image[]", ("referencia" + ext, ref[0], ref[1]))],
                                       {"Authorization": f"Bearer {key}"})
            else:
                data = _post_json("https://api.openai.com/v1/images/generations",
                                  {"model": modelo, "prompt": prompt, "size": size, "n": 1},
                                  {"Authorization": f"Bearer {key}"})
        except urllib.error.HTTPError as e:
            e._texto = e.read().decode("utf-8", errors="ignore")
            ultimo = f"{modelo}: HTTP {e.code} {e._texto[:200]}"
            if _error_de_modelo(e):
                continue
            raise RuntimeError(ultimo) from None
        return Image.open(io.BytesIO(base64.b64decode(data["data"][0]["b64_json"]))), f"GPT Image ({modelo})"
    raise RuntimeError(f"Ningún modelo de OpenAI disponible. Último error: {ultimo}")
