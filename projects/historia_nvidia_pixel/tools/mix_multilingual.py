import json, os, subprocess, sys
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
from timeline import TL
import audio as A_mod

SR = 44100

def load_wav(p):
    out = subprocess.check_output(["ffmpeg", "-v", "error", "-i", p, "-f", "f32le", "-ar", str(SR), "-ac", "1", "-"])
    return np.frombuffer(out, dtype=np.float32)

def save_wav(arr, p):
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",
           "-ar", "44100", p]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    proc.stdin.write(arr.astype(np.float32).tobytes())
    proc.stdin.close()
    proc.wait()

def movavg(x, k):
    if k <= 1: return x
    c = np.cumsum(np.pad(x, (k // 2, k - 1 - k // 2), mode='edge'))
    return (c[k:] - c[:-k]) / k

def dur(p):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p])
    return float(out.decode().strip())

def build_voice_stem(lang, total_samples):
    vo_dir = os.path.join(ROOT, "audio", f"vo_{lang}")
    stem = np.zeros(total_samples, dtype=np.float32)
    tmp_out = os.path.join(ROOT, "audio", f"_tmp_{lang}.wav")
    
    print(f"[{lang.upper()}] Building voice stem (naturalized pacing)...")
    for i, lid in enumerate(TL.order):
        mp3 = os.path.join(vo_dir, f"{lid}.mp3")
        if not os.path.exists(mp3):
            continue
        d_nat = dur(mp3)
        slot_start = TL.s(lid)
        slot_dur = TL.lines[lid]["dur"]
        next_start = TL.s(TL.order[i + 1]) if i + 1 < len(TL.order) else (TL.e(lid) + 1.0)
        avail_dur = max(slot_dur, next_start - slot_start - 0.08)

        # vo_en and vo_pt are synthesized at natural speed=1.0; only compress if d_nat exceeds avail_dur
        atempo = min(1.38, max(1.0, (d_nat + 0.02) / avail_dur))
        if abs(atempo - 1.0) > 0.015:
            cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", mp3, "-af", f"atempo={atempo:.3f}",
                   "-ar", str(SR), "-ac", "1", "-f", "f32le", "-"]
        else:
            cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", mp3, "-ar", str(SR), "-ac", "1", "-f", "f32le", "-"]
        out = subprocess.check_output(cmd)
        arr = np.frombuffer(out, dtype=np.float32)
        
        idx0 = int(round(slot_start * SR))
        idx1 = min(total_samples, idx0 + len(arr))
        chunk_len = idx1 - idx0
        if chunk_len > 0:
            stem[idx0:idx1] += arr[:chunk_len]
            
    print(f"[{lang.upper()}] Voice stem created, raw amp={np.max(np.abs(stem)):.3f}")
    pk = np.max(np.abs(stem))
    if pk > 0.05:
        stem = stem * (0.90 / pk)
    print(f"[{lang.upper()}] Voice stem normalized, max amp={np.max(np.abs(stem)):.3f}")
    return stem

def mix_language(lang):
    music_stem_path = os.path.join(ROOT, "audio", "music_stem.wav")
    sfx_stem_path = os.path.join(ROOT, "audio", "sfx_stem.wav")
    
    music = load_wav(music_stem_path)
    sfx = load_wav(sfx_stem_path)
    total_samples = len(music)
    
    voice = build_voice_stem(lang, total_samples)
    save_wav(voice, os.path.join(ROOT, "audio", f"voice_stem_{lang}.wav"))
    
    # Ducking profundo para acompañar la voz sin competir
    print(f"[{lang.upper()}] Ducking music & sfx...")
    step = 512
    v_abs = np.abs(voice[::step])
    kern_samples = int(0.32 * SR / step)
    v_env = movavg(v_abs, max(3, kern_samples))
    duck_m = np.clip(1.0 - 0.70 * (v_env / 0.10), 0.30, 1.0)
    duck_s = np.clip(1.0 - 0.38 * (v_env / 0.10), 0.62, 1.0)
    duck_m_full = np.interp(np.arange(total_samples), np.arange(len(duck_m)) * step, duck_m)
    duck_s_full = np.interp(np.arange(total_samples), np.arange(len(duck_s)) * step, duck_s)
    
    # Mix
    mix = music * duck_m_full + sfx * duck_s_full + voice * 1.0
    fade_n = int(1.5 * SR)
    mix[-fade_n:] *= np.linspace(1.0, 0.0, fade_n, dtype=np.float32)
    pk = np.max(np.abs(mix))
    if pk > 0.98:
        mix = mix * (0.98 / pk)
    print(f"[{lang.upper()}] Master mix peak: {np.max(np.abs(mix)):.3f}")
    
    mix_path = os.path.join(ROOT, "audio", f"mix_{lang}.wav")
    save_wav(mix, mix_path)
    print(f"[{lang.upper()}] Saved {mix_path}")

if __name__ == "__main__":
    mix_language("en")
    mix_language("pt")
