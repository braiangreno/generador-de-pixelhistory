"""Genera las Miniaturas 16:9 de YouTube (ES/EN/PT) y el Corte Vertical 9:16 (1080x1920, 44s)
para YouTube Shorts / Reels / TikTok siguiendo el Manual de Marca de Pixeloide Studios (2026)
y la sección 'Todo lo que hay que hacer' (Página 13 del guion).
"""
import json, math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))

from common import *  # noqa
import i18n
from timeline import TL
import ch01
import outro

FPS = 30
VW, VH = 270, 480          # Canvas nativo 9:16 pixel art (4x -> 1080x1920)
OUT_VW, OUT_VH = 1080, 1920
PHOSPHOR = (100, 255, 140)


def draw_phosphor_dot(cv, cx, cy, r=3, trail=None):
    """Punto de luz verde de fósforo con halo suave y estela opcional."""
    d = ImageDraw.Draw(cv)
    if trail:
        n = len(trail)
        for i, (tx, ty) in enumerate(trail):
            u = (i + 1) / (n + 1)
            tr = max(1, int(r * u * 0.85))
            a = int(110 * u)
            d.ellipse([tx - tr, ty - tr, tx + tr, ty + tr], fill=(70, 235, 115, a))
    for hr, ha in ((r + 5, 45), (r + 3, 95), (r + 1, 175)):
        d.ellipse([cx - hr, cy - hr, cx + hr, cy + hr], fill=(80, 245, 125, ha))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(215, 255, 225, 255))



# ---------------------------------------------------------------------------
# 1. MINIATURA DE YOUTUBE 16:9 (480x270 -> 1920x1080 NEAREST)
# ---------------------------------------------------------------------------
def build_thumbnail(lang="es"):
    i18n.set_lang(lang)

    # Fondo izquierdo: Laboratorio Brookhaven 1958 + osciloscopio verde fósforo
    bg_1958 = bg("bg_brookhaven_lab_1958").copy()
    bg_1958 = grade(bg_1958, mul=(0.75, 1.08, 0.85), add=(0, 14, 6), sat=0.9, k=0.85)
    d58 = ImageDraw.Draw(bg_1958)
    # Tubo de osciloscopio brillante a la izquierda (cx=108, cy=146, r=66)
    cx58, cy58, r58 = 108, 146, 64
    d58.ellipse([cx58 - r58 - 6, cy58 - r58 - 6, cx58 + r58 + 6, cy58 + r58 + 6],
                fill=(18, 28, 22, 255), outline=(70, 110, 82, 255), width=2)
    d58.ellipse([cx58 - r58, cy58 - r58, cx58 + r58, cy58 + r58],
                fill=(4, 22, 12, 255), outline=(*PHOSPHOR, 255), width=2)
    for gx in range(cx58 - 48, cx58 + 49, 16):
        d58.line([(gx, cy58 - 52), (gx, cy58 + 52)], fill=(12, 58, 28, 255))
    for gy in range(cy58 - 48, cy58 + 49, 16):
        d58.line([(cx58 - 52, gy), (cx58 + 52, gy)], fill=(12, 58, 28, 255))
    # Cancha y red de Tennis for Two (1958)
    d58.line([(cx58 - 48, cy58 + 22), (cx58 + 48, cy58 + 22)], fill=(*PHOSPHOR, 255), width=2)
    d58.line([(cx58, cy58 - 4), (cx58, cy58 + 22)], fill=(*PHOSPHOR, 255), width=2)

    # Fondo derecho: Costa Neón 2026 con el gran sol synthwave a la derecha
    bg_2026_raw = bg("bg_neon_coast_2026").copy()
    # Espejamos horizontalmente para que el gran sol synthwave quede del lado derecho (x ~ 372)
    bg_2026 = bg_2026_raw.transpose(Image.FLIP_LEFT_RIGHT)
    bg_2026 = grade(bg_2026, mul=(1.08, 0.98, 1.12), add=(10, 0, 14), sat=1.15, k=0.9)

    # Composición diagonal 1958 (izquierda) <-> 2026 (derecha) con dithering Bayer en la frontera
    cv = new_canvas(INK)
    p58 = np.array(bg_1958)
    p26 = np.array(bg_2026)
    out = np.zeros_like(p58)
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
            use_26 = u > bayer4[y % 4, x % 4]
            out[y, x] = p26[y, x] if use_26 else p58[y, x]

    cv = Image.fromarray(out, "RGBA")
    d = ImageDraw.Draw(cv)

    # Rayo / divisoria diagonal cian + magenta
    for dy_off, col in ((-2, (*CYAN, 220)), (0, (255, 255, 255, 255)), (2, (*outro.PX_MAGENTA, 220))):
        x_top = int(236 - (0 - 135) * 0.24) + dy_off
        x_bot = int(236 - (H - 135) * 0.24) + dy_off
        d.line([(x_top, 0), (x_bot, H)], fill=col, width=2)

    # Arco luminoso del punto de fósforo que salta desde el osciloscopio (1958) hasta el sol neón (2026)
    arc_pts = []
    for k in range(28):
        u = k / 27.0
        ax = int(round((cx58 - 22) * (1 - u) + 372 * u))
        ay = int(round((cy58 + 16) * (1 - u) + 128 * u - math.sin(u * math.pi) * 64))
        arc_pts.append((ax, ay))
    for i in range(len(arc_pts) - 1):
        u = i / len(arc_pts)
        col_arc = (
            int(PHOSPHOR[0] * (1 - u) + GOLD[0] * u),
            int(PHOSPHOR[1] * (1 - u) + GOLD[1] * u),
            int(PHOSPHOR[2] * (1 - u) + GOLD[2] * u),
            235,
        )
        d.line([arc_pts[i], arc_pts[i + 1]], fill=col_arc, width=2)
    # Punto de fósforo brillante en el osciloscopio y sobre el arco
    draw_phosphor_dot(cv, cx58 + 16, cy58 - 18, r=4, trail=arc_pts[:6])
    draw_phosphor_dot(cv, arc_pts[14][0], arc_pts[14][1], r=5, trail=arc_pts[9:14])

    # Personajes icónicos en las esquinas (por encima del cartel inferior): Higinbotham (1958) y La Máquina Pixeloide
    char(cv, ch01.HIGINBOTHAM, 38, 190, 1.2, scale=2, arms="point", look=1, mood="happy")
    robot(cv, 442, 190, 1.5, face="excited", scale=2)

    # Placas de año "1958" (verde fósforo) y "2026" (magenta/oro)
    window(cv, 14, 12, 86, 30, fill=(6, 22, 12), border=PHOSPHOR, alpha=0.95)
    draw_text(cv, "1958", 57, 19, "press", 16, PHOSPHOR, align="center", outline_w=2)

    window(cv, 380, 12, 86, 30, fill=(28, 10, 38), border=outro.PX_MAGENTA, alpha=0.95)
    draw_text(cv, "2026", 423, 19, "press", 16, GOLD, align="center", outline_w=2)

    # Sello Pixeloide Studios arriba al centro
    window(cv, 152, 10, 176, 26, fill=outro.PX_SURFACE, border=outro.PX_CYAN, alpha=0.95)
    outro.draw_isotipo(cv, 160, 13, size=20)
    draw_text(cv, "PIXELOIDE STUDIOS", 250, 19, "press", 8, outro.PX_PAPER, align="center")

    # Cartel central de alto impacto para YouTube
    window(cv, 22, 188, 436, 72, fill=(9, 12, 32), border=GOLD, alpha=0.96)
    title_str = {
        "es": "PARA QUE NO SE ABURRAN",
        "en": "SO THEY DON'T GET BORED",
        "pt": "PARA NÃO SE ENTEDIAREM",
    }[lang]
    sub_str = {
        "es": "DE UN PUNTO DE LUZ A US$ 201.600 MILLONES",
        "en": "FROM ONE DOT OF LIGHT TO $201.6 BILLION",
        "pt": "DE UM PONTO DE LUZ A US$ 201,6 BILHÕES",
    }[lang]
    badge_str = {
        "es": "DOCUMENTAL PIXEL ART 16-BIT · 68 AÑOS DE HISTORIA",
        "en": "16-BIT PIXEL ART DOCUMENTARY · 68 YEARS OF HISTORY",
        "pt": "DOCUMENTÁRIO PIXEL ART 16-BIT · 68 ANOS DE HISTÓRIA",
    }[lang]

    draw_text(cv, badge_str, 240, 196, "silk", 8, CYAN, align="center")
    draw_text(cv, title_str, 240, 212, "press", 16, align="center", gradient=GOLD_RAMP, outline_w=2)
    draw_text(cv, sub_str, 240, 238, "press", 8, PHOSPHOR, align="center", outline_w=1)

    cv = vignette(cv, 0.22)
    hi = cv.resize((1920, 1080), Image.NEAREST).convert("RGB")
    out_path = os.path.join(ROOT, "renders", f"Miniatura_YouTube_{lang.upper()}.png")
    hi.save(out_path, quality=95)
    print(f"[THUMB] Saved {out_path}")
    return out_path


# ---------------------------------------------------------------------------
# 2. CORTE VERTICAL 9:16 (1080x1920) DE LA APERTURA (40.6s + 3.4s CTA = 44.0s)
# ---------------------------------------------------------------------------
def _crop_focus_x(t):
    """Devuelve el centro X (en el canvas 480x270) que sigue la acción de la Apertura (s01..s08)."""
    s2 = TL.s("s02")
    s3 = TL.s("s03")
    s4 = TL.s("s04")
    s6 = TL.s("s06")
    s8 = TL.s("s08")
    if t < s2:
        # s01: Higinbotham en x=122 y osciloscopio en x=240
        return 210
    if t < s3:
        # s02: Fila de visitantes -> acercamiento al osciloscopio central
        return 235
    if t < s4:
        # s03: Cartel 1958 y cajas a la derecha -> centrado en 240
        return 240
    if t < s6:
        # s04-s05: Split screen 1958 (izq) vs 2026 (der): paneo suave de izquierda a centro-derecha
        u = clamp01((t - s4) / max(0.1, s6 - s4))
        return int(round(165 + (285 - 165) * ease_in_out(u)))
    if t < s8:
        # s06-s07: Tarjeta de título principal
        return 240
    return 240


def _wrap_sub_lines(text, max_chars=28):
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
    return lines[:3]


_CH1_SCENES = ch01.scenes()


def _render_ch1_at(t):
    fn = _CH1_SCENES[0][1]
    for entry in _CH1_SCENES:
        if t >= entry[0]:
            fn = entry[1]
    return fn(t)


def render_vertical_frame(t, lang, sub_entries, clip_end, total_dur):
    """Renderiza un cuadro 270x480 nativo (que se escala 4x NEAREST a 1080x1920)."""
    i18n.set_lang(lang)
    cv = Image.new("RGBA", (VW, VH), (*outro.PX_INK, 255))
    d = ImageDraw.Draw(cv)

    # Si estamos en los últimos 3.4s (clip_end .. total_dur): Tarjeta vertical oficial Pixeloide Studios + CTA
    if t >= clip_end:
        dt = t - clip_end
        # Fondo de campo de píxeles reactivo vertical
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

        cta_top = {
            "es": "EPISODIO COMPLETO",
            "en": "FULL EPISODE",
            "pt": "EPISÓDIO COMPLETO",
        }[lang]
        cta_mid = {
            "es": "PARA QUE NO SE",
            "en": "SO THEY DON'T",
            "pt": "PARA NÃO SE",
        }[lang]
        cta_mid2 = {
            "es": "ABURRAN",
            "en": "GET BORED",
            "pt": "ENTEDIAREM",
        }[lang]
        cta_bot = {
            "es": "MIRALO EN NUESTRO CANAL",
            "en": "WATCH ON OUR CHANNEL",
            "pt": "ASSISTA NO NOSSO CANAL",
        }[lang]

        draw_text(cv, cta_top, VW // 2, 238, "silk", 8, outro.PX_CYAN, align="center")
        draw_text(cv, cta_mid, VW // 2, 258, "press", 16, align="center", gradient=GOLD_RAMP, outline_w=2)
        draw_text(cv, cta_mid2, VW // 2, 280, "press", 16, align="center", gradient=GOLD_RAMP, outline_w=2)

        window(cv, 28, 316, VW - 56, 34, fill=(18, 28, 68), border=GOLD, alpha=0.96)
        draw_text(cv, cta_bot, VW // 2, 329, "press", 8, outro.PX_PAPER, align="center")

        draw_text(cv, "IDEA Y PRODUCCIÓN: BRAIAN GRENO", VW // 2, 374, "silk", 8, outro.PX_MUTED, align="center")
        draw_text(cv, "1958 → 2026 · 8 CAPÍTULOS", VW // 2, 392, "silk", 8, PHOSPHOR, align="center")
        return cv

    # --- 1. CABECERA SUPERIOR (y=0..92) ---
    window(cv, 8, 8, VW - 16, 78, fill=outro.PX_SURFACE, border=outro.PX_CYAN, alpha=0.96)
    outro.draw_isotipo(cv, 18, 16, size=24)
    draw_text(cv, "PIXELOIDE STUDIOS", 50, 20, "press", 8, outro.PX_PAPER)
    hdr_sub = {
        "es": "HISTORIA DE LOS VIDEOJUEGOS",
        "en": "THE HISTORY OF VIDEO GAMES",
        "pt": "HISTÓRIA DOS VIDEOGAMES",
    }[lang]
    draw_text(cv, hdr_sub, 50, 34, "silk", 8, outro.PX_CYAN)

    d.line([(18, 49), (VW - 18, 49)], fill=(*outro.PX_BORDER, 255), width=1)
    hdr_title = {
        "es": "1958 → 2026 · APERTURA",
        "en": "1958 → 2026 · OPENING",
        "pt": "1958 → 2026 · ABERTURA",
    }[lang]
    draw_text(cv, hdr_title, VW // 2, 58, "press", 8, GOLD, align="center")

    # --- 2. VENTANA CENTRAL 254x254 CON LA ESCENA 16:9 RECORTADA INTELIGENTEMENTE (y=94..352) ---
    scene_16_9 = _render_ch1_at(t)
    fx = _crop_focus_x(t)
    crop_w = 254
    x0 = max(0, min(W - crop_w, int(round(fx - crop_w // 2))))
    cropped = scene_16_9.crop((x0, 8, x0 + crop_w, 8 + 254))
    paste(cv, cropped, 8, 94)
    d.rectangle([7, 93, 8 + crop_w, 94 + 254], outline=(*PHOSPHOR, 255), width=2)

    # --- 3. TARJETA INFERIOR DE LÍNEA DE TIEMPO (SIN SUBTÍTULOS PEGADOS, y=356..472) ---
    window(cv, 8, 356, VW - 16, 116, fill=(10, 14, 36), border=GOLD, alpha=0.96)

    cur_lid = "s01"
    for ent in sub_entries:
        if ent["start"] - 0.08 <= t <= ent["end"] + 0.18:
            cur_lid = ent["id"]
            break

    # Etiqueta de año / contexto
    if cur_lid in ("s01", "s02", "s03", "s04", "s05"):
        era_badge = {
            "es": "BROOKHAVEN · OCTUBRE 1958",
            "en": "BROOKHAVEN · OCTOBER 1958",
            "pt": "BROOKHAVEN · OUTUBRO 1958",
        }[lang]
        main_card = "TENNIS FOR TWO · 1958"
    else:
        era_badge = {
            "es": "1958 - 2026 · 68 AÑOS",
            "en": "1958 - 2026 · 68 YEARS",
            "pt": "1958 - 2026 · 68 ANOS",
        }[lang]
        main_card = {
            "es": "PARA QUE NO SE ABURRAN",
            "en": "SO THEY DON'T GET BORED",
            "pt": "PARA NÃO SE ENTEDIAREM",
        }[lang]

    draw_text(cv, era_badge, VW // 2, 370, "silk", 8, PHOSPHOR, align="center")
    draw_text(cv, main_card, VW // 2, 396, "press", 8, GOLD, align="center")
    sub_card = {
        "es": "DOCUMENTAL PIXEL ART 16-BIT",
        "en": "16-BIT PIXEL ART DOCUMENTARY",
        "pt": "DOCUMENTÁRIO PIXEL ART 16-BIT",
    }[lang]
    draw_text(cv, sub_card, VW // 2, 418, "silk", 8, CYAN, align="center")

    # Barra de progreso con el punto verde de fósforo
    bar_x0, bar_x1 = 22, VW - 22
    bar_y = 450
    d.rectangle([bar_x0, bar_y - 2, bar_x1, bar_y + 2], fill=(22, 30, 58, 255))
    prog_u = clamp01(t / clip_end)
    px_dot = int(round(bar_x0 + (bar_x1 - bar_x0) * prog_u))
    d.rectangle([bar_x0, bar_y - 2, px_dot, bar_y + 2], fill=(*PHOSPHOR, 255))
    draw_phosphor_dot(cv, px_dot, bar_y, r=3)

    return cv


def _fmt_srt_time(sec):
    ms = int(round(max(0.0, sec) * 1000))
    hh = ms // 3600000
    mm = (ms % 3600000) // 60000
    ss = (ms % 60000) // 1000
    rem = ms % 1000
    return f"{hh:02d}:{mm:02d}:{ss:02d},{rem:03d}"


def build_short(lang="es"):
    script_file = "script_full.json" if lang == "es" else f"script_full_{lang}.json"
    with open(os.path.join(ROOT, script_file), encoding="utf-8") as f:
        script_data = json.load(f)

    # Extraemos las líneas de la Apertura (s01..s08) con sus tiempos del timeline y generamos el .srt externo del Short
    sub_entries = []
    srt_lines = []
    idx_srt = 1
    for item in script_data:
        lid = item["id"]
        if lid.startswith("s"):
            st = TL.s(lid)
            en = TL.e(lid)
            sub_txt = item.get("sub", item.get("text", ""))
            sub_entries.append({
                "id": lid,
                "start": st,
                "end": en,
                "sub": sub_txt,
            })
            srt_lines.append(f"{idx_srt}\n{_fmt_srt_time(st)} --> {_fmt_srt_time(en)}\n{sub_txt}\n")
            idx_srt += 1

    srt_out = os.path.join(ROOT, "renders", f"Short_Vertical_{lang.upper()}.srt")
    with open(srt_out, "w", encoding="utf-8") as f_srt:
        f_srt.write("\n".join(srt_lines))

    clip_end = round(TL.s("c1_00") - 0.25, 2)   # ~40.63s (toda la Apertura completa)
    cta_dur = 3.37
    total_dur = round(clip_end + cta_dur, 2)    # 44.00s exactos
    n_frames = int(round(total_dur * FPS))

    # Preparamos el audio del Short (primeros clip_end s del mix + cierre musical de Pixeloide Studios)
    mix_src = os.path.join(ROOT, "audio", "mix.wav" if lang == "es" else f"mix_{lang}.wav")
    short_wav = os.path.join(ROOT, "audio", f"short_mix_{lang}.wav")
    outro_start = TL.e("c8_09") + 0.35
    filter_complex = (
        f"[0:a]atrim=0:{clip_end:.3f},asetpts=PTS-STARTPTS,afade=t=out:st={clip_end-0.35:.3f}:d=0.35[a0];"
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
    print(f"[SHORT {lang.upper()}] Rendering {n_frames} frames ({total_dur:.2f}s @ 1080x1920)...")
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f_idx in range(n_frames):
        t = f_idx / float(FPS)
        cv = render_vertical_frame(t, lang, sub_entries, clip_end, total_dur)
        hi = cv.resize((OUT_VW, OUT_VH), Image.NEAREST).convert("RGB")
        proc.stdin.write(hi.tobytes())
        if f_idx % 300 == 0 or f_idx == n_frames - 1:
            print(f"  [{lang.upper()}] frame {f_idx + 1}/{n_frames} (t={t:.1f}s)")
    proc.stdin.close()
    ret = proc.wait()
    if ret != 0:
        raise RuntimeError(f"ffmpeg failed for Short {lang} with code {ret}")
    if os.path.exists(short_wav):
        os.remove(short_wav)
    print(f"[SHORT {lang.upper()}] Saved -> {out_mp4}")

    # Guardamos también un frame de muestra del Short para verificación visual
    sample_cv = render_vertical_frame(20.5, lang, sub_entries, clip_end, total_dur)
    sample_hi = sample_cv.resize((OUT_VW, OUT_VH), Image.NEAREST).convert("RGB")
    sample_path = os.path.join(ROOT, "frames", f"short_preview_{lang}.png")
    sample_hi.save(sample_path)
    return out_mp4


if __name__ == "__main__":
    for lg in ("es", "en", "pt"):
        build_thumbnail(lg)
    for lg in ("es", "en", "pt"):
        build_short(lg)
    print("ALL THUMBNAILS & SHORTS COMPLETED.")
