"""Genera los Shorts verticales 9:16 (1080x1920, 30fps) a PANTALLA COMPLETA por separado para CADA capítulo
del episodio (Apertura Cap 00 + Capítulos 01 a 08) en ES, EN y PT, redibujando nativamente cada escena
en 270x480 (escalado 4x NEAREST a 1080x1920), sin recortes laterales, sin subtítulos pegados
y con archivos .srt independientes en renders/subtitulos/.
"""
import json
import math
import os
import re
import shutil
import subprocess
import sys
from multiprocessing import Pool
import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))

import core
import common
from common import *  # noqa
import i18n
from timeline import TL
import outro
import video
import vertical

FPS = 30
VW, VH = 270, 480          # Lienzo nativo 9:16 pixel art a pantalla completa (4x NEAREST -> 1080x1920)
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
    "historia_tesla_pixel": {
        "accent": (108, 236, 255),
        "series": {
            "es": "LA HISTORIA DE NIKOLA TESLA",
            "en": "THE STORY OF NIKOLA TESLA",
            "pt": "A HISTÓRIA DE NIKOLA TESLA",
        },
        "ep_title": {
            "es": "EL DIBUJO QUE ENCENDIÓ EL MUNDO",
            "en": "THE DRAWING THAT LIT UP THE WORLD",
            "pt": "O DESENHO QUE ACENDEU O MUNDO",
        },
        "ep_title_2lines": {
            "es": ("EL DIBUJO QUE", "ENCENDIÓ EL MUNDO"),
            "en": ("THE DRAWING THAT", "LIT UP THE WORLD"),
            "pt": ("O DESENHO QUE", "ACENDEU O MUNDO"),
        },
        "years": "1856 -> 2026",
        "chapter_titles": {
            "es": {
                1: "HIJO DE LA TORMENTA",
                2: "EL DIBUJO EN LA ARENA",
                3: "DOS DÓLARES POR DÍA",
                4: "LA GUERRA DE LAS CORRIENTES",
                5: "LA CIUDAD BLANCA",
                6: "EL MAGO",
                7: "LA TORRE",
                8: "EL HOMBRE DE LAS PALOMAS",
            },
            "en": {
                1: "CHILD OF THE STORM",
                2: "THE DRAWING IN THE SAND",
                3: "TWO DOLLARS A DAY",
                4: "THE WAR OF THE CURRENTS",
                5: "THE WHITE CITY",
                6: "THE WIZARD",
                7: "THE TOWER",
                8: "THE PIGEON MAN",
            },
            "pt": {
                1: "FILHO DA TEMPESTADE",
                2: "O DESENHO NA AREIA",
                3: "DOIS DÓLARES POR DIA",
                4: "A GUERRA DAS CORRENTES",
                5: "A CIDADE BRANCA",
                6: "O MAGO",
                7: "A TORRE",
                8: "O HOMEM DOS POMBOS",
            },
        },
    },
    "historia_lamarr_pixel": {
        "accent": (40, 220, 224),
        "series": {
            "es": "LA HISTORIA DE HEDY LAMARR",
            "en": "THE STORY OF HEDY LAMARR",
            "pt": "A HISTÓRIA DE HEDY LAMARR",
        },
        "ep_title": {
            "es": "UN PIANO DENTRO DE UN TORPEDO",
            "en": "A PIANO INSIDE A TORPEDO",
            "pt": "UM PIANO DENTRO DE UM TORPEDO",
        },
        "ep_title_2lines": {
            "es": ("UN PIANO DENTRO", "DE UN TORPEDO"),
            "en": ("A PIANO INSIDE", "A TORPEDO"),
            "pt": ("UM PIANO DENTRO", "DE UM TORPEDO"),
        },
        "years": "1914 -> 2026",
        "chapter_titles": {
            "es": {
                1: "LA CAJA DE MÚSICA",
                2: "LA JAULA DE ORO",
                3: "LA MÁS LINDA DEL MUNDO",
                4: "EL PROBLEMA DEL TORPEDO",
                5: "UN PIANO EN UN TORPEDO",
                6: "BONOS Y BESOS",
                7: "EL CAJÓN",
                8: "MIL SEISCIENTOS SALTOS",
            },
            "en": {
                1: "THE MUSIC BOX",
                2: "THE GOLDEN CAGE",
                3: "THE MOST BEAUTIFUL WOMAN",
                4: "THE TORPEDO PROBLEM",
                5: "A PIANO IN A TORPEDO",
                6: "BONDS AND KISSES",
                7: "THE DRAWER",
                8: "SIXTEEN HUNDRED HOPS",
            },
            "pt": {
                1: "A CAIXA DE MÚSICA",
                2: "A GAIOLA DE OURO",
                3: "A MAIS LINDA DO MUNDO",
                4: "O PROBLEMA DO TORPEDO",
                5: "UM PIANO EM UM TORPEDO",
                6: "BÔNUS E BEIJOS",
                7: "A GAVETA",
                8: "MIL E SEISCENTOS SALTOS",
            },
        },
    },
    "historia_tv_pixel": {
        "accent": (128, 238, 158),
        "series": {
            "es": "LA HISTORIA DE LA TELEVISIÓN",
            "en": "THE HISTORY OF TELEVISION",
            "pt": "A HISTÓRIA DA TELEVISÃO",
        },
        "ep_title": {
            "es": "LÍNEA POR LÍNEA",
            "en": "LINE BY LINE",
            "pt": "LINHA POR LINHA",
        },
        "ep_title_2lines": {
            "es": ("LÍNEA POR LÍNEA", "LA TELEVISIÓN"),
            "en": ("LINE BY LINE", "TELEVISION"),
            "pt": ("LINHA POR LINHA", "A TELEVISÃO"),
        },
        "years": "1883 -> 2026",
        "chapter_titles": {
            "es": {
                1: "UN TELESCOPIO ELÉCTRICO",
                2: "LA CABEZA DEL MUÑECO",
                3: "LOS SURCOS",
                4: "EL SIGNO DE DÓLAR",
                5: "GOLIAT",
                6: "UNA VENTANA EN EL LIVING",
                7: "DOCTOR X",
                8: "VALIÓ LA PENA",
            },
            "en": {
                1: "AN ELECTRIC TELESCOPE",
                2: "THE DUMMY'S HEAD",
                3: "THE FURROWS",
                4: "THE DOLLAR SIGN",
                5: "GOLIATH",
                6: "A WINDOW IN THE LIVING ROOM",
                7: "DOCTOR X",
                8: "IT WAS WORTH IT",
            },
            "pt": {
                1: "UM TELESCÓPIO ELÉTRICO",
                2: "A CABEÇA DO BONECO",
                3: "OS SULCOS",
                4: "O CIFRÃO",
                5: "GOLIAS",
                6: "UMA JANELA NA SALA",
                7: "DOUTOR X",
                8: "VALEU A PENA",
            },
        },
    },
    "historia_cine_pixel": {
        "accent": (255, 204, 96),
        "series": {
            "es": "LA HISTORIA DEL CINE",
            "en": "THE HISTORY OF CINEMA",
            "pt": "A HISTÓRIA DO CINEMA",
        },
        "ep_title": {
            "es": "UN CABALLO EN EL AIRE",
            "en": "A HORSE IN THE AIR",
            "pt": "UM CAVALO NO AR",
        },
        "ep_title_2lines": {
            "es": ("UN CABALLO", "EN EL AIRE"),
            "en": ("A HORSE", "IN THE AIR"),
            "pt": ("UM CAVALO", "NO AR"),
        },
        "years": "1878 -> 2026",
        "chapter_titles": {
            "es": {
                1: "DOCE CÁMARAS",
                2: "TREINTA Y TRES ESPECTADORES",
                3: "EL MAGO",
                4: "HOLLYWOOD",
                5: "LAS PELÍCULAS HABLAN",
                6: "COLOR Y PANTALLA GIGANTE",
                7: "VEINTICUATRO POR SEGUNDO",
            },
            "en": {
                1: "TWELVE CAMERAS",
                2: "THIRTY-THREE SPECTATORS",
                3: "THE MAGICIAN",
                4: "HOLLYWOOD",
                5: "THE MOVIES TALK",
                6: "COLOR AND GIANT SCREEN",
                7: "TWENTY-FOUR PER SECOND",
            },
            "pt": {
                1: "DOZE CÂMERAS",
                2: "TRINTA E TRÊS ESPECTADORES",
                3: "O MÁGICO",
                4: "HOLLYWOOD",
                5: "OS FILMES FALAM",
                6: "COR E TELA GIGANTE",
                7: "VINTE E QUATRO POR SEGUNDO",
            },
        },
    },
    "historia_smartphone_pixel": {
        "accent": (108, 236, 255),
        "series": {
            "es": "LA HISTORIA DEL SMARTPHONE",
            "en": "THE HISTORY OF THE SMARTPHONE",
            "pt": "A HISTÓRIA DO SMARTPHONE",
        },
        "ep_title": {
            "es": "UNA LLAMADA AL RIVAL",
            "en": "A CALL TO THE RIVAL",
            "pt": "UMA CHAMADA AO RIVAL",
        },
        "ep_title_2lines": {
            "es": ("UNA LLAMADA", "AL RIVAL"),
            "en": ("A CALL TO", "THE RIVAL"),
            "pt": ("UMA CHAMADA", "AO RIVAL"),
        },
        "years": "1947 -> 2026",
        "chapter_titles": {
            "es": {
                1: "EL LADRILLO",
                2: "EL PANAL",
                3: "ESCRIBIR Y MIRAR",
                4: "SIMON",
                5: "UNA PANTALLA QUE SIENTE",
                6: "QUINIENTAS APLICACIONES",
                7: "EINSTEIN EN EL BOLSILLO",
                8: "UNA LLAMADA AL RIVAL",
            },
            "en": {
                1: "THE BRICK",
                2: "THE HONEYCOMB",
                3: "WRITING AND SEEING",
                4: "SIMON",
                5: "A SCREEN THAT FEELS",
                6: "FIVE HUNDRED APPS",
                7: "EINSTEIN IN YOUR POCKET",
                8: "A CALL TO THE RIVAL",
            },
            "pt": {
                1: "O TIJOLO",
                2: "A COLMEIA",
                3: "ESCREVER E OLHAR",
                4: "SIMON",
                5: "UMA TELA QUE SENTE",
                6: "QUINHENTOS APLICATIVOS",
                7: "EINSTEIN NO BOLSO",
                8: "UMA CHAMADA AO RIVAL",
            },
        },
    },
}


def get_meta():
    if PROJECT_NAME in PROJECT_META:
        return PROJECT_META[PROJECT_NAME]
    return PROJECT_META["historia_dune_pixel"]


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
        elif "chapter_titles" in get_meta() and ch_num in get_meta()["chapter_titles"].get(lang, {}):
            raw_title = get_meta()["chapter_titles"][lang][ch_num]
            short_slug = f"Cap{ch_num:02d}"
        else:
            raw_line = (items[0].get("sub") or items[0].get("speak") or "").strip()
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


def render_outro_cta_vertical(local_t, clip_dur, lang, meta):
    """Dibuja la tarjeta de cierre oficial de Pixeloide Studios a pantalla completa 270x480."""
    vertical._install_hooks()
    accent = meta["accent"]
    cv = Image.new("RGBA", (VW, VH), (*outro.PX_INK, 255))
    d = ImageDraw.Draw(cv)
    dt = max(0.0, local_t - clip_dur)

    for gy in range(6, VH - 6, 12):
        for gx in range(6, VW - 6, 12):
            dist = math.hypot(gx - VW * 0.5, gy - 190)
            wave = max(0.0, 1.0 - dist / 210.0) ** 1.6
            pulse = 0.5 + 0.5 * math.sin(dist * 0.05 - local_t * 3.5)
            k = core.clamp01(wave * (0.7 + 0.3 * pulse))
            if k > 0.05:
                mix_cm = core.clamp01(gy / float(VH))
                r = int(11 + k * (outro.PX_CYAN[0] * (1 - mix_cm) + outro.PX_MAGENTA[0] * mix_cm - 11) * 0.65)
                g = int(15 + k * (outro.PX_CYAN[1] * (1 - mix_cm) + outro.PX_MAGENTA[1] * mix_cm - 15) * 0.55)
                b = int(42 + k * (outro.PX_CYAN[2] * (1 - mix_cm) + outro.PX_MAGENTA[2] * mix_cm - 42) * 0.75)
                d.rectangle([gx, gy, gx + 9, gy + 9], fill=(min(255, r), min(255, g), min(255, b), 255))
            else:
                d.rectangle([gx, gy, gx + 9, gy + 9], fill=(11, 15, 42, 255))

    core._orig_window(cv, 14, 52, VW - 28, 376, fill=outro.PX_SURFACE, border=outro.PX_CYAN, alpha=0.95)
    p_c = core.clamp01(dt / 0.35)
    p_p = core.clamp01((dt - 0.10) / 0.35)
    p_m = core.clamp01((dt - 0.20) / 0.35)
    outro.draw_isotipo(cv, (VW - 68) // 2, 74, size=68, p_cyan=p_c, p_paper=p_p, p_mag=p_m)

    core._orig_draw_text(cv, "PIXELOIDE", VW // 2, 156, "press", 16, outro.PX_PAPER, align="center", outline_w=2)
    core._orig_draw_text(cv, "STUDIOS", VW // 2, 178, "silk", 8, outro.PX_CYAN, align="center")
    core._orig_draw_text(cv, "JUGAMOS EN SERIO.", VW // 2, 198, "press", 8, core.GOLD, align="center")

    d.line([(32, 220), (VW - 32, 220)], fill=(*outro.PX_BORDER, 255), width=1)

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

    core._orig_draw_text(cv, cta_top, VW // 2, 234, "silk", 8, outro.PX_CYAN, align="center")
    core._orig_draw_text(cv, l1, VW // 2, 254, "press", 8 if len(l1) > 13 else 16,
                         align="center", gradient=core.GOLD_RAMP, outline_w=2)
    core._orig_draw_text(cv, l2, VW // 2, 276, "press", 8 if len(l2) > 13 else 16,
                         align="center", gradient=core.GOLD_RAMP, outline_w=2)

    core._orig_window(cv, 22, 314, VW - 44, 34, fill=(18, 28, 68), border=core.GOLD, alpha=0.96)
    core._orig_draw_text(cv, cta_bot, VW // 2, 327, "press", 8, outro.PX_PAPER, align="center")

    n_caps = len(meta.get("chapter_titles", {}).get("es", {})) or 8
    core._orig_draw_text(cv, "IDEA Y PRODUCCIÓN: BRAIAN GRENO", VW // 2, 372, "silk", 8, outro.PX_MUTED, align="center")
    core._orig_draw_text(cv, f"{meta['years']} · {n_caps} CAPÍTULOS", VW // 2, 392, "silk", 8, accent, align="center")
    return cv


def build_chapter_short(args):
    ch_info, total_chs, lang, meta, outro_audio_start = args
    i18n.set_lang(lang)
    vertical._install_hooks()

    slug = ch_info["slug"]
    t_start = ch_info["t_start"]
    t_end = ch_info["t_end"]
    clip_dur = round(t_end - t_start, 2)
    cta_dur = 3.20
    total_dur = round(clip_dur + cta_dur, 2)
    n_total_frames = int(round(total_dur * FPS))
    accent = meta["accent"]

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

    # 3. Renderizar cada fotograma nativamente a pantalla completa 270x480 -> 1080x1920
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

    for f_idx in range(n_total_frames):
        local_t = f_idx / float(FPS)
        if local_t < clip_dur:
            global_t = t_start + local_t
            cv = vertical.frame_at_vertical(global_t, video.SCENES, xfade=video.XFADE, final=False)
            # Sutil barra de progreso de 2px en el borde inferior (y=478..479)
            prog_w = max(2, int(round(VW * core.clamp01(local_t / max(0.1, clip_dur)))))
            d_bar = ImageDraw.Draw(cv)
            d_bar.rectangle([0, VH - 2, VW, VH - 1], fill=(16, 20, 38, 220))
            d_bar.rectangle([0, VH - 2, prog_w, VH - 1], fill=(*accent, 255))
        else:
            cv = render_outro_cta_vertical(local_t, clip_dur, lang, meta)

        hi = cv.resize((OUT_VW, OUT_VH), Image.NEAREST).convert("RGB")
        proc.stdin.write(hi.tobytes())

    proc.stdin.close()
    ret = proc.wait()
    if os.path.exists(short_wav):
        os.remove(short_wav)
    if ret != 0:
        raise RuntimeError(f"ffmpeg failed for {out_mp4} (code {ret})")

    if ch_info["ch"] == 0:
        shutil.copy2(out_mp4, os.path.join(ROOT, "renders", f"Short_Vertical_{lang.upper()}.mp4"))

    print(f"  [OK] {os.path.basename(out_mp4)} ({total_dur:.1f}s)", flush=True)
    return out_mp4


def build_all_for_lang(lang="es", workers=6):
    i18n.set_lang(lang)
    meta = get_meta()
    script_file = "script_full.json" if lang == "es" else f"script_full_{lang}.json"
    with open(os.path.join(ROOT, script_file), encoding="utf-8") as f:
        script_data = json.load(f)

    chapters = group_chapters(script_data, lang=lang)
    last_lid = script_data[-1]["id"]
    outro_audio_start = outro.T_LOGO

    print(f"=== [{PROJECT_NAME}] Generando {len(chapters)} Shorts 9:16 FULLSCREEN en {lang.upper()} ===", flush=True)
    jobs = [(ch_info, len(chapters), lang, meta, outro_audio_start) for ch_info in chapters]
    with Pool(min(workers, len(jobs))) as pool:
        for _ in pool.imap_unordered(build_chapter_short, jobs):
            pass


if __name__ == "__main__":
    langs = sys.argv[1:] if len(sys.argv) > 1 else ["es", "en", "pt"]
    for lg in langs:
        build_all_for_lang(lg)
    print(f"ALL CHAPTER SHORTS COMPLETED FOR {PROJECT_NAME}!", flush=True)
