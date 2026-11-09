"""Genera subtítulos .srt a partir de la alineación por carácter de ElevenLabs."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "engine"))
from timeline import TL, ROOT


def ts(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


out, i = [], 1
for lid, L in TL.lines.items():
    al = L["align"]
    text = "".join(al["characters"])
    st, en = al["character_start_times_seconds"], al["character_end_times_seconds"]
    start = 0
    while start < len(text):
        end = min(len(text), start + 42)
        if end < len(text):
            cut = max(text.rfind(p, start, end) for p in ", .:?")
            end = cut + 1 if cut > start + 10 else end
        seg = text[start:end].strip()
        if seg:
            t_s = L["start"] + st[start]
            t_e = L["start"] + (st[end] - 0.02 if end < len(text) else en[end - 1] + 0.08)
            out.append(f"{i}\n{ts(t_s)} --> {ts(max(t_s + 0.2, t_e))}\n{seg}\n")
            i += 1
        start = end
srt_text = "\n".join(out)
open(os.path.join(ROOT, "renders", "Historia_IA_PixelArt_Completo.srt"), "w", encoding="utf-8").write(srt_text)
open(os.path.join(ROOT, "renders", "Piloto_Historia_IA_PixelArt.srt"), "w", encoding="utf-8").write(srt_text)
print(i - 1, "subtitles")
