"""Genera las Miniaturas 16:9 de YouTube (ES/EN/PT) y el Corte Vertical 9:16 (1080x1920)
con archivo .srt externo (sin subtítulos quemados en el video) para cualquier proyecto Pixeloide.
"""
import json
import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))

from common import *  # noqa
import i18n
from timeline import TL
import outro
import video as V_mod

FPS = 30
VW, VH = 270, 480          # Lienzo nativo 9:16 pixel art (4x -> 1080x1920)
OUT_VW, OUT_VH = 1080, 1920
PHOSPHOR = (100, 255, 140)

PLAN_PATH = os.path.join(ROOT, "production_plan.json")
PLAN = json.load(open(PLAN_PATH, encoding="utf-8")) if os.path.exists(PLAN_PATH) else {}


def build_thumbnail(lang="es"):
    i18n.set_lang(lang)
    bgs = PLAN.get("backgrounds", [])
    bg1_name = bgs[0]["name"] if len(bgs) > 0 else "bg_main"
    bg2_name = bgs[-1]["name"] if len(bgs) > 1 else bg1_name

    bg_left = grade(bg(bg1_name).copy(), mul=(0.82, 1.05, 0.90), add=(0, 10, 6), sat=0.95, k=0.85)
    bg_right = grade(bg(bg2_name).copy(), mul=(1.08, 0.98, 1.12), add=(10, 0, 14), sat=1.12, k=0.9)

    p_l = np.array(bg_left)
    p_r = np.array(bg_right)
    out = np.zeros_like(p_l)
    bayer4 = np.array([
        [0,  8,  2, 10],
        [12, 4, 14,  6],
        [3, 11,  1,  9],
        [15, 7, 13,  5],
    ], dtype=np.float32) / 16.0

    for y in range(H):
        split_x = 236 - (y - 135) * 0.24
        for x in range(W):
            u = clamp01((x - (split_x - 18)) / 36.0)
            out[y, x] = p_r[y, x] if u > bayer4[y % 4, x % 4] else p_l[y, x]

    cv = Image.fromarray(out, "RGBA")
    d = ImageDraw.Draw(cv)

    for dy_off, col in ((-2, (*CYAN, 220)), (0, (255, 255, 255, 255)), (2, (*outro.PX_MAGENTA, 220))):
        x_top = int(236 - (0 - 135) * 0.24) + dy_off
        x_bot = int(236 - (H - 135) * 0.24) + dy_off
        d.line([(x_top, 0), (x_bot, H)], fill=col, width=2)

    # Personajes en las esquinas
    char(cv, "inge", 42, 190, 1.2, scale=2, arms="point", mood="happy")
    robot(cv, 438, 190, 1.5, face="excited", scale=2)

    yr_start = str(PLAN.get("year_start", "ORIGEN"))
    yr_end = str(PLAN.get("year_end", "2026"))

    window(cv, 14, 12, 92, 30, fill=(6, 22, 12), border=PHOSPHOR, alpha=0.95)
    draw_text(cv, yr_start[:6], 60, 19, "press", 16 if len(yr_start) <= 4 else 8, PHOSPHOR, align="center", outline_w=2)

    window(cv, 374, 12, 92, 30, fill=(28, 10, 38), border=outro.PX_MAGENTA, alpha=0.95)
    draw_text(cv, yr_end[:6], 420, 19, "press", 16 if len(yr_end) <= 4 else 8, GOLD, align="center", outline_w=2)

    window(cv, 152, 10, 176, 26, fill=outro.PX_SURFACE, border=outro.PX_CYAN, alpha=0.95)
    outro.draw_isotipo(cv, 160, 13, size=20)
    draw_text(cv, "PIXELOIDE STUDIOS", 250, 19, "press", 8, outro.PX_PAPER, align="center")

    window(cv, 22, 188, 436, 72, fill=(9, 12, 32), border=GOLD, alpha=0.96)
    titles = PLAN.get("titles", {})
    title_str = (titles.get(lang) or PLAN.get("title") or "DOCUMENTAL PIXELOIDE").upper()
    subs = PLAN.get("subtitles", {})
    sub_str = (subs.get(lang) or PLAN.get("subtitle") or "HISTORIA COMPLETA EN PIXEL ART 16-BIT").upper()
    badge_str = {
        "es": "DOCUMENTAL PIXEL ART 16-BIT · PIXELOIDE STUDIOS",
        "en": "16-BIT PIXEL ART DOCUMENTARY · PIXELOIDE STUDIOS",
        "pt": "DOCUMENTÁRIO PIXEL ART 16-BIT · PIXELOIDE STUDIOS",
    }.get(lang, "DOCUMENTAL PIXEL ART 16-BIT")

    draw_text(cv, badge_str, 240, 196, "silk", 8, CYAN, align="center")
    fsize = 16 if text_size(title_str, "press", 16)[0] <= 410 else 8
    draw_text(cv, title_str[:38], 240, 214 if fsize == 16 else 218, "press", fsize, align="center", gradient=GOLD_RAMP, outline_w=2)
    draw_text(cv, sub_str[:46], 240, 238, "press", 8, PHOSPHOR, align="center", outline_w=1)

    cv = vignette(cv, 0.22)
    hi = cv.resize((1920, 1080), Image.NEAREST).convert("RGB")
    os.makedirs(os.path.join(ROOT, "renders"), exist_ok=True)
    out_path = os.path.join(ROOT, "renders", f"Miniatura_YouTube_{lang.upper()}.png")
    hi.save(out_path, quality=95)
    print(f"[THUMB] Saved {out_path}")
    return out_path


def _fmt_srt_time(sec):
    ms = int(round(max(0.0, sec) * 1000))
    hh = ms // 3600000
    mm = (ms % 3600000) // 60000
    ss = (ms % 60000) // 1000
    rem = ms % 1000
    return f"{hh:02d}:{mm:02d}:{ss:02d},{rem:03d}"


def render_vertical_frame(t, lang, clip_end, total_dur):
    i18n.set_lang(lang)
    cv = Image.new("RGBA", (VW, VH), (*outro.PX_INK, 255))
    d = ImageDraw.Draw(cv)

    titles = PLAN.get("titles", {})
    title_str = (titles.get(lang) or PLAN.get("title") or "DOCUMENTAL PIXELOIDE").upper()

    if t >= clip_end:
        dt = t - clip_end
        for gy in range(6, VH - 6, 12):
            for gx in range(6, VW - 6, 12):
                dist = math.hypot(gx - VW * 0.5, gy - 190)
                wave = max(0.0, 1.0 - dist / 210.0) ** 1.6
                pulse = 0.5 + 0.5 * math.sin(dist * 0.05 - t * 3.5)
                k = clamp01(wave * (0.7 + 0.3 * pulse))
                if k > 0.05:
                    mix_cm = clamp01(gy / float(VH))
                    r = int(11 + k * (outro.PX_CYAN[0] * (1 - mix_cm) + outro.PX_MAGENTA[0] * mix_cm - 11) * 0.65)
                    g = int(15 + k * (outro.PX_CYAN[1] * (1 - mix_cm) + outro.PX_MAGENTA[1] * mix_cm - 15) * 0.55)
                    b = int(42 + k * (outro.PX_CYAN[2] * (1 - mix_cm) + outro.PX_MAGENTA[2] * mix_cm - 42) * 0.75)
                    d.rectangle([gx, gy, gx + 9, gy + 9], fill=(min(255, r), min(255, g), min(255, b), 255))
                else:
                    d.rectangle([gx, gy, gx + 9, gy + 9], fill=(11, 15, 42, 255))

        window(cv, 16, 56, VW - 32, 368, fill=outro.PX_SURFACE, border=outro.PX_CYAN, alpha=0.95)
        p_c = clamp01(dt / 0.35)
        p_p = clamp01((dt - 0.10) / 0.35)
        p_m = clamp01((dt - 0.20) / 0.35)
        outro.draw_isotipo(cv, (VW - 68) // 2, 78, size=68, p_cyan=p_c, p_paper=p_p, p_mag=p_m)

        draw_text(cv, "PIXELOIDE", VW // 2, 160, "press", 16, outro.PX_PAPER, align="center", outline_w=2)
        draw_text(cv, "STUDIOS", VW // 2, 182, "silk", 8, outro.PX_CYAN, align="center")
        draw_text(cv, "JUGAMOS EN SERIO.", VW // 2, 202, "press", 8, GOLD, align="center")
        d.line([(36, 224), (VW - 36, 224)], fill=(*outro.PX_BORDER, 255), width=1)

        draw_text(cv, "EPISODIO COMPLETO", VW // 2, 240, "silk", 8, outro.PX_CYAN, align="center")
        draw_text_wrap(cv, title_str, VW // 2, 262, VW - 48, "press", 8, GOLD, align="center")
        window(cv, 28, 316, VW - 56, 34, fill=(18, 28, 68), border=GOLD, alpha=0.96)
        draw_text(cv, "MIRALO EN NUESTRO CANAL", VW // 2, 329, "press", 8, outro.PX_PAPER, align="center")
        draw_text(cv, "IDEA Y PRODUCCIÓN: BRAIAN GRENO", VW // 2, 374, "silk", 8, outro.PX_MUTED, align="center")
        return cv

    # Cabecera
    window(cv, 8, 8, VW - 16, 78, fill=outro.PX_SURFACE, border=outro.PX_CYAN, alpha=0.96)
    outro.draw_isotipo(cv, 18, 16, size=24)
    draw_text(cv, "PIXELOIDE STUDIOS", 50, 20, "press", 8, outro.PX_PAPER)
    draw_text(cv, "DOCUMENTAL PIXEL ART 16-BIT", 50, 34, "silk", 8, outro.PX_CYAN)
    d.line([(18, 49), (VW - 18, 49)], fill=(*outro.PX_BORDER, 255), width=1)
    draw_text(cv, title_str[:26], VW // 2, 58, "press", 8, GOLD, align="center")

    # Ventana central 254x254 con la escena del motor
    scene_16_9 = V_mod.frame_at(t, final=False)
    crop_w = 254
    x0 = (W - crop_w) // 2
    cropped = scene_16_9.crop((x0, 8, x0 + crop_w, 8 + 254))
    paste(cv, cropped, 8, 94)
    d.rectangle([7, 93, 8 + crop_w, 94 + 254], outline=(*PHOSPHOR, 255), width=2)

    # Tarjeta inferior (sin subtítulos quemados)
    window(cv, 8, 356, VW - 16, 116, fill=(10, 14, 36), border=GOLD, alpha=0.96)
    draw_text(cv, "PIXELOIDE STUDIOS · 2026", VW // 2, 372, "silk", 8, PHOSPHOR, align="center")
    draw_text(cv, title_str[:26], VW // 2, 396, "press", 8, GOLD, align="center")
    draw_text(cv, "DOCUMENTAL PIXEL ART 16-BIT", VW // 2, 418, "silk", 8, CYAN, align="center")

    bar_x0, bar_x1 = 22, VW - 22
    bar_y = 450
    d.rectangle([bar_x0, bar_y - 2, bar_x1, bar_y + 2], fill=(22, 30, 58, 255))
    prog_u = clamp01(t / max(1.0, clip_end))
    px_dot = int(round(bar_x0 + (bar_x1 - bar_x0) * prog_u))
    d.rectangle([bar_x0, bar_y - 2, px_dot, bar_y + 2], fill=(*PHOSPHOR, 255))
    draw_phosphor_dot(cv, px_dot, bar_y, r=3)
    return cv


def build_short(lang="es"):
    script_file = "script_full.json" if lang == "es" else f"script_full_{lang}.json"
    script_path = os.path.join(ROOT, script_file)
    if not os.path.exists(script_path):
        return None
    script_data = json.load(open(script_path, encoding="utf-8"))

    # Duración del Short: hasta 40s de apertura + 3.5s de CTA
    max_clip = min(40.5, max(12.0, TL.total - 13.0))
    srt_lines = []
    idx_srt = 1
    clip_end = max_clip
    for item in script_data:
        lid = item["id"]
        if lid not in TL.lines:
            continue
        st = TL.s(lid)
        en = TL.e(lid)
        if st >= max_clip:
            break
        clip_end = min(max_clip, en + 0.25)
        sub_txt = item.get("sub", item.get("speak", ""))
        srt_lines.append(f"{idx_srt}\n{_fmt_srt_time(st)} --> {_fmt_srt_time(en)}\n{sub_txt}\n")
        idx_srt += 1

    os.makedirs(os.path.join(ROOT, "renders", "subtitulos"), exist_ok=True)
    srt_out = os.path.join(ROOT, "renders", "subtitulos", f"Short_Vertical_{lang.upper()}.srt")
    open(srt_out, "w", encoding="utf-8").write("\n".join(srt_lines))

    cta_dur = 3.4
    total_dur = round(clip_end + cta_dur, 2)
    n_frames = int(round(total_dur * FPS))

    mix_src = os.path.join(ROOT, "audio", "mix.wav" if lang == "es" else f"mix_{lang}.wav")
    if not os.path.exists(mix_src):
        mix_src = os.path.join(ROOT, "audio", "mix.wav")
    short_wav = os.path.join(ROOT, "audio", f"short_mix_{lang}.wav")
    outro_start = max(0.0, TL.total - 11.5)
    filter_complex = (
        f"[0:a]atrim=0:{clip_end:.3f},asetpts=PTS-STARTPTS,afade=t=out:st={max(0.1, clip_end-0.35):.3f}:d=0.35[a0];"
        f"[0:a]atrim={outro_start:.3f}:{outro_start+cta_dur:.3f},asetpts=PTS-STARTPTS,"
        f"afade=t=in:st=0:d=0.20,afade=t=out:st={cta_dur-0.55:.3f}:d=0.55[a1];"
        f"[a0][a1]concat=n=2:v=0:a=1,loudnorm=I=-14:TP=-1.0:LRA=11[aout]"
    )
    subprocess.check_call([
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", mix_src,
        "-filter_complex", filter_complex,
        "-map", "[aout]",
        "-ar", "44100", "-ac", "2",
        short_wav,
    ])

    out_mp4 = os.path.join(ROOT, "renders", f"Short_Vertical_{lang.upper()}.mp4")
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{OUT_VW}x{OUT_VH}", "-r", str(FPS), "-i", "-",
        "-i", short_wav,
        "-c:v", "libx264", "-preset", "medium", "-crf", "17",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest", "-movflags", "+faststart",
        out_mp4,
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f_idx in range(n_frames):
        t = f_idx / float(FPS)
        cv = render_vertical_frame(t, lang, clip_end, total_dur)
        hi = cv.resize((OUT_VW, OUT_VH), Image.NEAREST).convert("RGB")
        proc.stdin.write(hi.tobytes())
    proc.stdin.close()
    proc.wait()
    if os.path.exists(short_wav):
        os.remove(short_wav)
    print(f"[SHORT {lang.upper()}] Saved -> {out_mp4}")
    return out_mp4


if __name__ == "__main__":
    langs = sys.argv[1:] or ["es", "en", "pt"]
    for lg in langs:
        build_thumbnail(lg)
    for lg in langs:
        build_short(lg)
