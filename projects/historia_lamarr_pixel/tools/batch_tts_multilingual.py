import base64, json, os, sys, time, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY = open(os.path.join(ROOT, ".env"), encoding="utf-8").read().strip().split("=", 1)[1]

# Nota: El español (Carlos Aguilar, 8MeTTgXVwMEhRVfblXOj) SIEMPRE se genera con tools/tts.py (modelo eleven_v4).
# Este script es únicamente para EN y PT a velocidad natural speed=1.0.
VOICES = {
    "en": {"voice_id": "pNInz6obpgDQGcFmaJgB", "script": "script_full_en.json", "out": "audio/vo_en", "speed": 1.0},
    "pt": {"voice_id": "Rxw6ylGPvxzn3gsuOExL", "script": "script_full_pt.json", "out": "audio/vo_pt", "speed": 1.0},
}

def tts_call(voice_id, text, prev_text, next_text, speed=1.0):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps?output_format=mp3_44100_192"
    body = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.35,
            "use_speaker_boost": True,
            "speed": speed
        },
    }
    if prev_text:
        body["previous_text"] = prev_text
    if next_text:
        body["next_text"] = next_text

    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                 headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    for attempt in range(10):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="ignore")
            print(f"HTTP {e.code} (attempt {attempt+1}): {msg[:150]}", flush=True)
            if e.code == 400 and "previous_text" in msg:
                body.pop("previous_text", None)
                body.pop("next_text", None)
                req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                             headers={"xi-api-key": KEY, "Content-Type": "application/json"})
            time.sleep(2.5 * (attempt + 1))
        except Exception as e:
            print(f"Network error (attempt {attempt+1}): {e}", flush=True)
            time.sleep(2.5 * (attempt + 1))
    raise RuntimeError(f"TTS failed for text: {text[:40]}")

def generate_lang(lang):
    cfg = VOICES[lang]
    out_dir = os.path.join(ROOT, cfg["out"])
    os.makedirs(out_dir, exist_ok=True)
    script_path = os.path.join(ROOT, cfg["script"])
    lines = json.load(open(script_path, encoding="utf-8"))

    print(f"--- Generating {lang.upper()} ({len(lines)} lines) into {cfg['out']} ---", flush=True)
    for i, line in enumerate(lines):
        lid = line["id"]
        mp3_path = os.path.join(out_dir, f"{lid}.mp3")
        json_path = os.path.join(out_dir, f"{lid}.json")
        if os.path.exists(mp3_path) and os.path.exists(json_path) and os.path.getsize(mp3_path) > 1000:
            continue
        prev_t = lines[i - 1]["speak"] if i > 0 else None
        next_t = lines[i + 1]["speak"] if i + 1 < len(lines) else None
        t0 = time.time()
        res = tts_call(cfg["voice_id"], line["speak"], prev_t, next_t, cfg["speed"])
        open(mp3_path, "wb").write(base64.b64decode(res["audio_base64"]))
        json.dump(res.get("alignment", {}), open(json_path, "w", encoding="utf-8"), ensure_ascii=False)
        dur = time.time() - t0
        print(f"[{lang.upper()} {i+1:02d}/{len(lines):02d}] {lid} ok ({dur:.1f}s)", flush=True)
        time.sleep(0.15)

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "both"
    if target in ("en", "both", "all"):
        generate_lang("en")
    if target in ("pt", "both", "all"):
        generate_lang("pt")
    print("All multilingual TTS generation finished successfully!", flush=True)
