"""Actualiza incrementalmente la cola (outro + créditos) de renders/video_mudo*.mp4
a partir del último keyframe previo al final del capítulo 8, evitando re-renderizar los 8 minutos completos.
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
import i18n
import video as V
from timeline import TL

SPLIT_FRAME = 14831  # Exact I-frame at 494.366667s before c8_08 ends


def update_all():
    t0 = SPLIT_FRAME / 30.0
    t1 = TL.total
    for lang, suf in [("es", ""), ("en", "_en"), ("pt", "_pt")]:
        i18n.set_lang(lang)
        src = os.path.join(ROOT, "renders", f"video_mudo{suf}.mp4")
        head = os.path.join(ROOT, "renders", f"_head{suf}.mp4")
        tail = os.path.join(ROOT, "renders", f"_tail{suf}.mp4")
        lst = os.path.join(ROOT, "renders", f"_concat{suf}.txt")
        out = os.path.join(ROOT, "renders", f"_new_mudo{suf}.mp4")

        print(f"=== [{lang.upper()}] Extrayendo tramo 0..{SPLIT_FRAME} frames ===", flush=True)
        subprocess.check_call([
            "ffmpeg", "-y", "-loglevel", "error",
            "-i", src, "-frames:v", str(SPLIT_FRAME), "-c", "copy", head
        ])

        print(f"=== [{lang.upper()}] Renderizando cola + outro Pixeloide ({t0:.3f}s..{t1:.2f}s) ===", flush=True)
        V.render_range(t0, t1, tail)

        with open(lst, "w", encoding="utf-8") as f:
            p_head = os.path.abspath(head).replace("\\", "/")
            p_tail = os.path.abspath(tail).replace("\\", "/")
            f.write(f"file '{p_head}'\n")
            f.write(f"file '{p_tail}'\n")

        subprocess.check_call([
            "ffmpeg", "-y", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out
        ])
        os.replace(out, src)
        for tmp in (head, tail, lst):
            if os.path.exists(tmp):
                os.remove(tmp)
        print(f"=== [{lang.upper()}] Actualizado {src} ({t1:.2f}s) ===", flush=True)


if __name__ == "__main__":
    update_all()
