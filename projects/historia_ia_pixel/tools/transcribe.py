import json, sys
from faster_whisper import WhisperModel

src = r"C:\Users\Braian\.gemini\antigravity\scratch\historia_ia_pixel\src_project\assets\12d6c681-de62-44ad-9fe0-c865740232b1\voice_el.wav"
out = r"C:\Users\Braian\.gemini\antigravity\scratch\historia_ia_pixel\transcript.json"
try:
    model = WhisperModel("large-v3", device="cuda", compute_type="float16")
except Exception as e:
    print("cuda failed", e)
    model = WhisperModel("medium", device="cpu", compute_type="int8")
segs, info = model.transcribe(src, language="es", word_timestamps=True, beam_size=5)
res = []
for s in segs:
    res.append({"start": s.start, "end": s.end, "text": s.text.strip(),
                "words": [{"w": w.word, "s": w.start, "e": w.end} for w in s.words]})
    print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text.strip()}")
json.dump(res, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
