"""Genera la locución en Español con ElevenLabs (Carlos Aguilar, modelo eleven_v4) frase por frase,
guardando audio + alineación por carácter para sincronizar la animación."""
import base64, json, os, sys, time, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY = open(os.path.join(ROOT, ".env"), encoding="utf-8").read().strip().split("=", 1)[1]
VOICE = os.environ.get("VOICE_ID", "8MeTTgXVwMEhRVfblXOj")  # Carlos Aguilar
MODEL = "eleven_v4"
OUT = os.path.join(ROOT, "audio", "vo")
os.makedirs(OUT, exist_ok=True)

LINES = json.load(open(os.path.join(ROOT, os.environ.get("SCRIPT", "script_full.json")), encoding="utf-8"))


def tts(idx, text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_192"
    body = {
        "text": text,
        "model_id": MODEL,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.35,
            "use_speaker_boost": True,
            "speed": float(os.environ.get("SPEED", "1.1")),
        },
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode(),
        method="POST",
        headers={"xi-api-key": KEY, "Content-Type": "application/json"},
    )
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="ignore")
            print("HTTP", e.code, msg[:300], flush=True)
            time.sleep(2 * (attempt + 1))
        except Exception as e:
            print("ERR", e, flush=True)
            time.sleep(2 * (attempt + 1))
    raise RuntimeError("TTS failed")


only = set(sys.argv[1:])
for i, line in enumerate(LINES):
    lid = line["id"]
    if only and lid not in only:
        continue
    mp3 = os.path.join(OUT, f"{lid}.mp3")
    js = os.path.join(OUT, f"{lid}.json")
    if os.path.exists(mp3) and os.path.exists(js) and os.path.getsize(mp3) > 1000 and not only:
        continue
    res = tts(i, line["speak"])
    open(mp3, "wb").write(base64.b64decode(res["audio_base64"]))
    json.dump(res.get("alignment"), open(js, "w", encoding="utf-8"), ensure_ascii=False)
    print(f"ok [{i+1}/{len(LINES)}] {lid}", flush=True)
