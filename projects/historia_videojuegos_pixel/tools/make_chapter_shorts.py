"""Genera los Shorts verticales 9:16 (1080x1920, 30fps) por separado para CADA capítulo
del episodio (Apertura Cap 00 + Capítulos 01 a 08) en ES, EN y PT, sin subtítulos pegados
y con archivos .srt independientes en renders/subtitulos/.
"""
import json, math, os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))

from common import *  # noqa
import i18n
from timeline import TL
import outro

FPS = 30
VW, VH = 270, 480          # Canvas nativo 9:16 pixel art (4x NEAREST -> 1080x1920)
OUT_VW, OUT_VH = 1080, 1920

PROJECT_NAME = os.path.basename(ROOT)

PROJECT_META = {
    "historia_videojuegos_pixel": {
        "accent": (100, 255, 140),
        "series": {
            "es": "HISTORIA DE LOS VIDEOJUEGOS",
            "en": "THE HISTORY OF VIDEO GAMES",
            "pt": "HISTÓRIA DOS VIDEOGAMES",
        },
        "ep_title": {
            "es": "PARA QUE NO SE ABURRAN",
            "en": "SO THEY DON'T GET BORED",
            "pt": "PARA NÃO SE ENTEDIAREM",
        },
        "ep_title_2lines": {
            "es": ("PARA QUE NO SE", "ABURRAN"),
            "en": ("SO THEY DON'T", "GET BORED"),
            "pt": ("PARA NÃO SE", "ENTEDIAREM"),
        },
        "years": "1958 → 2026",
    },
    "historia_ia_pixel": {
        "accent": (72, 229, 255),
        "series": {
            "es": "HISTORIA DE LA IA",
            "en": "THE HISTORY OF AI",
            "pt": "HISTÓRIA DA IA",
        },
        "ep_title": {
            "es": "LA HISTORIA DE LA IA",
            "en": "THE STORY OF AI",
            "pt": "A HISTÓRIA DA IA",
        },
        "ep_title_2lines": {
            "es": ("HISTORIA DE LA", "INTELIGENCIA ARTIFICIAL"),
            "en": ("THE HISTORY OF", "ARTIFICIAL INTELLIGENCE"),
            "pt": ("A HISTÓRIA DA", "INTELIGÊNCIA ARTIFICIAL"),
        },
        "years": "1950 → 2026",
    },
    "historia_dune_pixel": {
        "accent": (255, 195, 85),
        "series": {
            "es": "LA HISTORIA DE DUNE",
            "en": "THE STORY OF DUNE",
            "pt": "A HISTÓRIA DE DUNE",
        },
        "ep_title": {
            "es": "LA ARENA QUE NUNCA SE DETUVO",
            "en": "THE SAND THAT NEVER STOPPED",
            "pt": "A AREIA QUE NUNCA PAROU",
        },
        "ep_title_2lines": {
            "es": ("LA ARENA QUE", "NUNCA SE DETUVO"),
            "en": ("THE SAND THAT", "NEVER STOPPED"),
            "pt": ("A AREIA QUE", "NUNCA PAROU"),
        },
        "years": "1957 → 2026",
    },
}


def get_meta():
    if PROJECT_NAME in PROJECT_META:
        return PROJECT_META[PROJECT_NAME]
    return PROJECT_META["historia_dune_pixel"]


def draw_accent_dot(cv, cx, cy, col, r=3):
    d = ImageDraw.Draw(cv)
    for hr, ha in ((r + 5, 45), (r + 3, 95), (r + 1, 175)):
        d.ellipse([cx - hr, cy - hr, cx + hr, cy + hr], fill=(col[0], col[1], col[2], ha))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(245, 255, 245, 255))


def _fmt_srt_time(sec):
    ms = int(round(max(0.0, sec) * 1000))
    hh = ms // 3600000
    mm = (ms % 3600000) // 60000
    ss = (ms % 60000) // 1000
    rem = ms % 1000
    return f"{hh:02d}:{mm:02d}:{ss:02d},{rem:03d}"


def group_chapters(script_data, lang="es"):
    """Agrupa las líneas del guion en 9 capítulos: 0 (Apertura) y 1..8."""
    chapters = {}
    cur_ch = 0
    for item in script_data:
        lid = item["id"]
        spk = (item.get("speak") or item.get("sub") or item.get("text") or "").strip()
        m = re.match(r"^c(\d+)_00$", lid)
        if m:
            cur_ch = int(m.group(1))
        elif lid == "s06" and PROJECT_NAME == "historia_ia_pixel":
            cur_ch = 1
        elif lid == "s13" and PROJECT_NAME == "historia_ia_pixel":
            cur_ch = 2
        elif item.get("ch", 0) > 0:
            cur_ch = int(item["ch"])
        chapters.setdefault(cur_ch, []).append(item)

    out = []
    for ch_num in sorted(chapters.keys()):
        items = chapters[ch_num]
        first_id = items[0]["id"]
        last_id = items[-1]["id"]
        t_start = max(0.0, TL.s(first_id) - 0.15) if ch_num > 0 else 0.0
        t_end = TL.e(last_id) + 0.30

        if ch_num == 0:
            raw_title = {
                "es": "APERTURA",
                "en": "OPENING",
                "pt": "ABERTURA",
            }[lang]
            short_slug = "Cap00_Apertura"
        else:
            raw_line = (items[0].get("sub") or items[0].get("speak") or "").strip()
            # Extraer nombre limpio después de "Capítulo X." o "CAPÍTULO X —"
            cleaned = re.sub(
                r"^(cap[ií]tulo|chapter)\s+([0-9]+|uno|dos|tres|cuatro|cinco|seis|siete|ocho|one|two|three|four|five|six|seven|eight|um|dois|tr[eê]s|quatro|cinco|seis|sete|oito)\s*[\.\:\—\-\–]\s*",
                "",
                raw_line,
                flags=re.IGNORECASE,
            ).strip(" .")
            raw_title = cleaned.upper() if cleaned else f"CAPÍTULO {ch_num}"
            short_slug = f"Cap{ch_num:02d}"

        out.append({
            "ch": ch_num,
            "slug": short_slug,
            "title": raw_title,
            "items": items,
            "t_start": round(t_start, 3),
            "t_end": round(t_end, 3),
        })
    return out


def _wrap_title(text, max_chars=26):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        cand = (cur + " " + w).strip()
        if len(cand) <= max_chars or not cur:
            cur = cand
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines[:2]


def decode_16_9_frames(video_mudo_path, t_start, duration, n_frames):
    """Decodifica los cuadros 480x270 desde el master 16:9 ya renderizado para máxima velocidad y fidelidad."""
    cmd = [
        "ffmpeg", "-loglevel", "error",
        "-ss", f"{t_start:.3f}",
        "-t", f"{duration:.3f}",
        "-i", video_mudo_path,
        "-vf", f"fps={FPS},scale=480:270:flags=neighbor",
        "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-",
    ]
    raw = subprocess.check_output(cmd)
    frame_bytes = 480 * 270 * 3
    frames = []
    total_got = len(raw) // frame_bytes
    for i in range(n_frames):
        idx = min(i, max(0, total_got - 1))
        buf = raw[idx * frame_bytes:(idx + 1) * frame_bytes]
        if len(buf) == frame_bytes:
            im = Image.frombytes("RGB", (480, 270), buf).convert("RGBA")
        else:
            im = Image.new("RGBA", (480, 270), (11, 15, 42, 255))
        frames.append(im)
    return frames


def render_vertical_frame(scene_16_9, local_t, clip_dur, total_dur, ch_info, total_chs, lang, meta):
    """Compone un cuadro 270x480 nativo para el capítulo actual."""
    accent = meta["accent"]
    cv = Image.new("RGBA", (VW, VH), (*outro.PX_INK, 255))
    d = ImageDraw.Draw(cv)

    # Cierre vertical oficial de Pixeloide Studios (últimos 3.2s)
    if local_t >= clip_dur:
        dt = local_t - clip_dur
        for gy in range(6, VH - 6, 12):
            for gx in range(6, VW - 6, 12):
                dist = math.hypot(gx - VW * 0.5, gy - 190)
                wave = max(0.0, 1.0 - dist / 210.0) ** 1.6
                pulse = 0.5 + 0.5 * math.sin(dist * 0.05 - local_t * 3.5)
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

        cta_top = {
            "es": "EPISODIO COMPLETO",
            "en": "FULL EPISODE",
            "pt": "EPISÓDIO COMPLETO",
        }[lang]
        l1, l2 = meta["ep_title_2lines"][lang]
        cta_bot = {
            "es": "MIRALO EN NUESTRO CANAL",
            "en": "WATCH ON OUR CHANNEL",
            "pt": "ASSISTA NO NOSSO CANAL",
        }[lang]

        draw_text(cv, cta_top, VW // 2, 238, "silk", 8, outro.PX_CYAN, align="center")
        draw_text(cv, l1, VW // 2, 258, "press", 8 if len(l1) > 15 else 16, align="center", gradient=GOLD_RAMP, outline_w=2)
        draw_text(cv, l2, VW // 2, 280, "press", 8 if len(l2) > 15 else 16, align="center", gradient=GOLD_RAMP, outline_w=2)

        window(cv, 24, 316, VW - 48, 34, fill=(18, 28, 68), border=GOLD, alpha=0.96)
        draw_text(cv, cta_bot, VW // 2, 329, "press", 8, outro.PX_PAPER, align="center")

        draw_text(cv, "IDEA Y PRODUCCIÓN: BRAIAN GRENO", VW // 2, 374, "silk", 8, outro.PX_MUTED, align="center")
        draw_text(cv, f"{meta['years']} · 8 CAPÍTULOS", VW // 2, 392, "silk", 8, accent, align="center")
        return cv

    # --- 1. CABECERA SUPERIOR (y=8..86) ---
    window(cv, 8, 8, VW - 16, 78, fill=outro.PX_SURFACE, border=outro.PX_CYAN, alpha=0.96)
    outro.draw_isotipo(cv, 18, 16, size=24)
    draw_text(cv, "PIXELOIDE STUDIOS", 50, 20, "press", 8, outro.PX_PAPER)
    draw_text(cv, meta["series"][lang], 50, 34, "silk", 8, outro.PX_CYAN)

    d.line([(18, 49), (VW - 18, 49)], fill=(*outro.PX_BORDER, 255), width=1)
    ch_num = ch_info["ch"]
    if ch_num == 0:
        hdr_badge = f"{meta['years']} · {ch_info['title']}"
    else:
        ch_lbl = {"es": "CAPÍTULO", "en": "CHAPTER", "pt": "CAPÍTULO"}[lang]
        hdr_badge = f"{ch_lbl} {ch_num} · {meta['years']}"
    draw_text(cv, hdr_badge, VW // 2, 58, "press", 8, GOLD, align="center")

    # --- 2. VENTANA CENTRAL 254x254 CON PANEO SUAVE INTELIGENTE (y=94..348) ---
    crop_w = 254
    # Paneo suave sinusoidal alrededor del centro (240 +- 18px) para dar dinamismo sin cortar bordes
    fx = 240 + int(round(16 * math.sin(local_t * 0.35)))
    x0 = max(0, min(W - crop_w, fx - crop_w // 2))
    cropped = scene_16_9.crop((x0, 8, x0 + crop_w, 8 + 254))
    paste(cv, cropped, 8, 94)
    d.rectangle([7, 93, 8 + crop_w, 94 + 254], outline=(*accent, 255), width=2)

    # --- 3. TARJETA INFERIOR DE CAPÍTULO (SIN SUBTÍTULOS PEGADOS, y=356..472) ---
    window(cv, 8, 356, VW - 16, 116, fill=(10, 14, 36), border=GOLD, alpha=0.96)

    if ch_num == 0:
        part_badge = {
            "es": f"APERTURA · PARTE 1 DE {total_chs}",
            "en": f"OPENING · PART 1 OF {total_chs}",
            "pt": f"ABERTURA · PARTE 1 DE {total_chs}",
        }[lang]
    else:
        part_badge = {
            "es": f"CAPÍTULO {ch_num} · PARTE {ch_num + 1} DE {total_chs}",
            "en": f"CHAPTER {ch_num} · PART {ch_num + 1} OF {total_chs}",
            "pt": f"CAPÍTULO {ch_num} · PARTE {ch_num + 1} DE {total_chs}",
        }[lang]

    draw_text(cv, part_badge, VW // 2, 368, "silk", 8, accent, align="center")

    t_lines = _wrap_title(ch_info["title"], max_chars=26)
    if len(t_lines) == 1:
        draw_text(cv, t_lines[0], VW // 2, 392, "press", 8, GOLD, align="center")
    else:
        draw_text(cv, t_lines[0], VW // 2, 385, "press", 8, GOLD, align="center")
        draw_text(cv, t_lines[1], VW // 2, 399, "press", 8, GOLD, align="center")

    draw_text(cv, meta["ep_title"][lang], VW // 2, 419, "silk", 8, CYAN, align="center")

    # Barra de progreso del capítulo
    bar_x0, bar_x1 = 22, VW - 22
    bar_y = 450
    d.rectangle([bar_x0, bar_y - 2, bar_x1, bar_y + 2], fill=(22, 30, 58, 255))
    prog_u = clamp01(local_t / max(0.1, clip_dur))
    px_dot = int(round(bar_x0 + (bar_x1 - bar_x0) * prog_u))
    d.rectangle([bar_x0, bar_y - 2, px_dot, bar_y + 2], fill=(*accent, 255))
    draw_accent_dot(cv, px_dot, bar_y, accent, r=3)

    return cv


def build_chapter_short(ch_info, total_chs, lang, meta, outro_audio_start):
    slug = ch_info["slug"]
    t_start = ch_info["t_start"]
    t_end = ch_info["t_end"]
    clip_dur = round(t_end - t_start, 2)
    cta_dur = 3.20
    total_dur = round(clip_dur + cta_dur, 2)
    n_clip_frames = int(round(clip_dur * FPS))
    n_total_frames = int(round(total_dur * FPS))

    shorts_dir = os.path.join(ROOT, "renders", "shorts")
    subs_dir = os.path.join(ROOT, "renders", "subtitulos")
    os.makedirs(shorts_dir, exist_ok=True)
    os.makedirs(subs_dir, exist_ok=True)

    # 1. Generar archivo .srt independiente (relativo a t_start=0) en renders/subtitulos/
    srt_lines = []
    for idx_s, item in enumerate(ch_info["items"], 1):
        lid = item["id"]
        st = max(0.0, TL.s(lid) - t_start)
        en = max(st + 0.2, TL.e(lid) - t_start)
        sub_txt = item.get("sub") or item.get("text") or item.get("speak") or ""
        srt_lines.append(f"{idx_s}\n{_fmt_srt_time(st)} --> {_fmt_srt_time(en)}\n{sub_txt}\n")

    srt_path = os.path.join(subs_dir, f"Short_{slug}_{lang.upper()}.srt")
    with open(srt_path, "w", encoding="utf-8") as f_srt:
        f_srt.write("\n".join(srt_lines))

    # 2. Preparar audio del capítulo + cierre musical de Pixeloide Studios
    mix_src = os.path.join(ROOT, "audio", "mix.wav" if lang == "es" else f"mix_{lang}.wav")
    short_wav = os.path.join(ROOT, "audio", f"tmp_short_{slug}_{lang}.wav")
    filter_complex = (
        f"[0:a]atrim={t_start:.3f}:{t_end:.3f},asetpts=PTS-STARTPTS,"
        f"afade=t=in:st=0:d=0.12,afade=t=out:st={max(0.1, clip_dur-0.30):.3f}:d=0.30[a0];"
        f"[0:a]atrim={outro_audio_start:.3f}:{outro_audio_start+cta_dur:.3f},asetpts=PTS-STARTPTS,"
        f"afade=t=in:st=0:d=0.18,afade=t=out:st={cta_dur-0.50:.3f}:d=0.50[a1];"
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

    # 3. Decodificar frames 480x270 del video_mudo del idioma
    vm_name = "video_mudo.mp4" if lang == "es" else f"video_mudo_{lang}.mp4"
    vm_path = os.path.join(ROOT, "renders", vm_name)
    if not os.path.exists(vm_path):
        vm_path = os.path.join(ROOT, "renders", "video_mudo.mp4")

    frames_16_9 = decode_16_9_frames(vm_path, t_start, clip_dur, n_clip_frames)

    out_mp4 = os.path.join(shorts_dir, f"Short_{slug}_{lang.upper()}.mp4")
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{OUT_VW}x{OUT_VH}", "-r", str(FPS), "-i", "-",
        "-i", short_wav,
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest", "-movflags", "+faststart",
        out_mp4,
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    blank_16_9 = frames_16_9[-1] if frames_16_9 else Image.new("RGBA", (480, 270), (11, 15, 42, 255))

    for f_idx in range(n_total_frames):
        local_t = f_idx / float(FPS)
        sc_frame = frames_16_9[f_idx] if f_idx < len(frames_16_9) else blank_16_9
        cv = render_vertical_frame(sc_frame, local_t, clip_dur, total_dur, ch_info, total_chs, lang, meta)
        hi = cv.resize((OUT_VW, OUT_VH), Image.NEAREST).convert("RGB")
        proc.stdin.write(hi.tobytes())

    proc.stdin.close()
    ret = proc.wait()
    if os.path.exists(short_wav):
        os.remove(short_wav)
    if ret != 0:
        raise RuntimeError(f"ffmpeg failed for {out_mp4} (code {ret})")

    # Si es Cap00_Apertura, actualizar también Short_Vertical_{LANG}.mp4 en renders/
    if ch_info["ch"] == 0:
        import shutil
        shutil.copy2(out_mp4, os.path.join(ROOT, "renders", f"Short_Vertical_{lang.upper()}.mp4"))

    print(f"  [OK] {os.path.basename(out_mp4)} ({total_dur:.1f}s)")
    return out_mp4


def build_all_for_lang(lang="es"):
    i18n.set_lang(lang)
    meta = get_meta()
    script_file = "script_full.json" if lang == "es" else f"script_full_{lang}.json"
    with open(os.path.join(ROOT, script_file), encoding="utf-8") as f:
        script_data = json.load(f)

    chapters = group_chapters(script_data, lang=lang)
    last_lid = script_data[-1]["id"]
    outro_audio_start = TL.e(last_lid) + 0.35

    print(f"=== [{PROJECT_NAME}] Generando {len(chapters)} Shorts 9:16 en {lang.upper()} ===")
    for ch_info in chapters:
        build_chapter_short(ch_info, len(chapters), lang, meta, outro_audio_start)


if __name__ == "__main__":
    langs = sys.argv[1:] if len(sys.argv) > 1 else ["es", "en", "pt"]
    for lg in langs:
        build_all_for_lang(lg)
    print(f"ALL CHAPTER SHORTS COMPLETED FOR {PROJECT_NAME}!")
