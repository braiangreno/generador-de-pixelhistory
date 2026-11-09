"""Stage 2 — Servicio de Locución Neuronal + Timestamps (`tts_service.py`).
Genera audio/vo (Español con Carlos Aguilar), audio/vo_en (Inglés natural 1.0x) y audio/vo_pt (Portugués natural 1.0x).
"""
import base64
import json
import math
import os
import subprocess
import time
import urllib.error
import urllib.request
import wave

import numpy as np


def _elevenlabs_tts_with_timestamps(api_key: str, voice_id: str, text: str, prev_text: str, next_text: str,
                                    model_id: str = "eleven_multilingual_v2", speed: float = 1.0) -> dict:
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps?output_format=mp3_44100_192"
    body = {
        "text": text,
        "model_id": model_id,
        "voice_settings": {
            "stability": 0.48,
            "similarity_boost": 0.78,
            "style": 0.35,
            "use_speaker_boost": True,
            "speed": speed,
        },
    }
    if prev_text:
        body["previous_text"] = prev_text
    if next_text:
        body["next_text"] = next_text

    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"), method="POST",
        headers={"xi-api-key": api_key, "Content-Type": "application/json"}
    )
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", errors="ignore")
            if e.code == 400 and ("previous_text" in msg or "model" in msg):
                body.pop("previous_text", None)
                body.pop("next_text", None)
                body["model_id"] = "eleven_multilingual_v2"
                req = urllib.request.Request(
                    url, data=json.dumps(body).encode("utf-8"), method="POST",
                    headers={"xi-api-key": api_key, "Content-Type": "application/json"}
                )
            time.sleep(1.5 * (attempt + 1))
        except Exception:
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"ElevenLabs TTS falló para: {text[:50]}")


def _fallback_synth_voice(text: str, mp3_path: str, json_path: str):
    """Generador de voz sintética / cadencia suave de respaldo cuando se prueba sin API key."""
    chars = list(text)
    n_chars = max(1, len(chars))
    dur = max(1.6, min(9.5, n_chars * 0.062))
    sr = 44100
    n_samples = int(dur * sr)
    t = np.arange(n_samples) / sr
    # Síntesis suave tipo narrador retro (múltiples armónicos suaves modulados por sílabas)
    syl_env = np.clip(0.5 + 0.5 * np.sin(2 * np.pi * 4.2 * t), 0.1, 1.0)
    f0 = 125.0 + 12.0 * np.sin(2 * np.pi * 0.8 * t)
    sig = (
        0.55 * np.sin(2 * np.pi * f0 * t)
        + 0.25 * np.sin(2 * np.pi * f0 * 2 * t)
        + 0.12 * np.sin(2 * np.pi * f0 * 3 * t)
    ) * syl_env * 0.18
    fade = min(int(0.08 * sr), n_samples // 4)
    if fade > 0:
        sig[:fade] *= np.linspace(0, 1, fade)
        sig[-fade:] *= np.linspace(1, 0, fade)

    tmp_wav = mp3_path + ".tmp.wav"
    with wave.open(tmp_wav, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes((np.clip(sig, -1, 1) * 32767).astype(np.int16).tobytes())
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp_wav, "-b:a", "192k", mp3_path])
    if os.path.exists(tmp_wav):
        os.remove(tmp_wav)

    st_times = [round(i * dur / n_chars, 4) for i in range(n_chars)]
    en_times = [round((i + 1) * dur / n_chars, 4) for i in range(n_chars)]
    align = {
        "characters": chars,
        "character_start_times_seconds": st_times,
        "character_end_times_seconds": en_times,
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(align, f, ensure_ascii=False)


def generate_project_tts(project_dir: str, settings: dict, languages=("es", "en", "pt"), force_ids=None, log_fn=print):
    api_key = settings.get("elevenlabs_api_key", "").strip()
    lang_configs = {
        "es": {
            "script": "script_full.json",
            "out_dir": os.path.join(project_dir, "audio", "vo"),
            "voice_id": settings.get("voice_es_id", "8MeTTgXVwMEhRVfblXOj"),  # Carlos Aguilar
            "model": "eleven_v4",
            "speed": float(settings.get("voice_es_speed", 1.08)),
        },
        "en": {
            "script": "script_full_en.json",
            "out_dir": os.path.join(project_dir, "audio", "vo_en"),
            "voice_id": settings.get("voice_en_id", "pNInz6obpgDQGcFmaJgB"),
            "model": "eleven_multilingual_v2",
            "speed": 1.0,  # Siempre natural 1.0x
        },
        "pt": {
            "script": "script_full_pt.json",
            "out_dir": os.path.join(project_dir, "audio", "vo_pt"),
            "voice_id": settings.get("voice_pt_id", "Rxw6ylGPvxzn3gsuOExL"),
            "model": "eleven_multilingual_v2",
            "speed": 1.0,  # Siempre natural 1.0x
        },
    }

    for lg in languages:
        if lg not in lang_configs:
            continue
        cfg = lang_configs[lg]
        script_path = os.path.join(project_dir, cfg["script"])
        if not os.path.exists(script_path):
            continue
        os.makedirs(cfg["out_dir"], exist_ok=True)
        lines = json.load(open(script_path, encoding="utf-8"))
        log_fn(f"[Stage 2] Generando locución {lg.upper()} ({len(lines)} líneas, voz={cfg['voice_id']}, speed={cfg['speed']}x)...")

        for i, row in enumerate(lines):
            lid = row["id"]
            if force_ids and lid not in force_ids:
                continue
            mp3_path = os.path.join(cfg["out_dir"], f"{lid}.mp3")
            json_path = os.path.join(cfg["out_dir"], f"{lid}.json")
            if not force_ids and os.path.exists(mp3_path) and os.path.exists(json_path) and os.path.getsize(mp3_path) > 800:
                continue
            prev_t = lines[i - 1]["speak"] if i > 0 else None
            next_t = lines[i + 1]["speak"] if i + 1 < len(lines) else None
            if api_key:
                try:
                    res = _elevenlabs_tts_with_timestamps(
                        api_key, cfg["voice_id"], row["speak"], prev_t, next_t,
                        model_id=cfg["model"], speed=cfg["speed"]
                    )
                    open(mp3_path, "wb").write(base64.b64decode(res["audio_base64"]))
                    with open(json_path, "w", encoding="utf-8") as jf:
                        json.dump(res.get("alignment", {}), jf, ensure_ascii=False)
                    log_fn(f"  [{lg.upper()} {i + 1:02d}/{len(lines):02d}] {lid} OK (ElevenLabs)")
                    continue
                except Exception as e:
                    log_fn(f"  [Aviso TTS {lg.upper()} {lid}] {e} -> usando respaldo sintético")
            _fallback_synth_voice(row["speak"], mp3_path, json_path)
            log_fn(f"  [{lg.upper()} {i + 1:02d}/{len(lines):02d}] {lid} OK (Synth Fallback)")
