"""Orquestador del Pipeline de Producción de Pixeloide Studio Server (`orchestrator.py`).
Ejecuta los 8 pasos del motor en segundo plano, registra logs en tiempo real y mantiene el catálogo de proyectos.
"""
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import traceback

from app.config import BASE_DIR, PROJECTS_DIR, TEMPLATE_DIR, get_settings
from app.pipeline.script_director import extract_text_from_file, structure_script
from app.pipeline.tts_service import generate_project_tts
from app.pipeline.asset_generator import generate_project_assets

_ACTIVE_JOBS = {}
_LOCK = threading.Lock()

STAGE_NAMES = {
    1: "1. Estructuración de Guion y Plan Visual 16-Bit (ES/EN/PT)",
    2: "2. Locución Neuronal (Carlos Aguilar ES + EN/PT 1.0x) y Timestamps",
    3: "3. Generación y Cuantización de Fondos (480x270) y Retratos (64x64)",
    4: "4. Compilación de Escenas, i18n y Cierre Pixeloide Studios",
    5: "5. Auditoría Visual de Márgenes/Cajas y Hoja de Contacto",
    6: "6. Síntesis Chiptune, SFX y Mezcla con Ducking (ES/EN/PT)",
    7: "7. Render 1080p Paralelo, Masterización -14 LUFS y Subtítulos .SRT",
    8: "8. Miniaturas YouTube 16:9 y Shorts Verticales 9:16 + Pack Final",
}


def _meta_path(project_id: str) -> str:
    return os.path.join(PROJECTS_DIR, project_id, "project_meta.json")


def get_project_dir(project_id: str) -> str:
    pmeta = _meta_path(project_id)
    if os.path.exists(pmeta):
        try:
            data = json.load(open(pmeta, encoding="utf-8"))
            if data.get("external_path") and os.path.exists(data["external_path"]):
                return data["external_path"]
        except Exception:
            pass
    return os.path.join(PROJECTS_DIR, project_id)


def load_meta(project_id: str) -> dict:
    p = _meta_path(project_id)
    if os.path.exists(p):
        try:
            return json.load(open(p, encoding="utf-8"))
        except Exception:
            pass
    return {}


def save_meta(project_id: str, meta: dict):
    d = os.path.join(PROJECTS_DIR, project_id)
    os.makedirs(d, exist_ok=True)
    with _LOCK:
        with open(_meta_path(project_id), "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)


def append_log(project_id: str, msg: str):
    d = os.path.join(PROJECTS_DIR, project_id)
    os.makedirs(d, exist_ok=True)
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}\n"
    with open(os.path.join(d, "build.log"), "a", encoding="utf-8") as f:
        f.write(line)
    try:
        print(line, end="", flush=True)
    except UnicodeEncodeError:
        print(line.encode("ascii", errors="replace").decode("ascii"), end="", flush=True)


def list_deliverables(project_id: str) -> dict:
    pdir = get_project_dir(project_id)
    renders_dir = os.path.join(pdir, "renders")
    frames_dir = os.path.join(pdir, "frames")
    out = {
        "videos": [],
        "subtitles": [],
        "shorts": [],
        "thumbnails": [],
        "sheets": [],
        "docs": [],
    }
    if os.path.exists(renders_dir):
        for fname in sorted(os.listdir(renders_dir)):
            fpath = os.path.join(renders_dir, fname)
            if not os.path.isfile(fpath):
                continue
            if fname.startswith("video_mudo"):
                continue
            size_mb = round(os.path.getsize(fpath) / (1024 * 1024), 2)
            item = {"name": fname, "url": f"/api/projects/{project_id}/file/renders/{fname}", "size_mb": size_mb}
            if fname.lower().endswith(".mp4"):
                if "short" in fname.lower():
                    out["shorts"].append(item)
                else:
                    out["videos"].append(item)
            elif fname.lower().endswith(".srt"):
                out["subtitles"].append(item)
            elif fname.lower().endswith(".png") or fname.lower().endswith(".jpg"):
                out["thumbnails"].append(item)

        sub_dir = os.path.join(renders_dir, "subtitulos")
        if os.path.exists(sub_dir):
            for fname in sorted(os.listdir(sub_dir)):
                fpath = os.path.join(sub_dir, fname)
                if os.path.isfile(fpath) and fname.lower().endswith(".srt"):
                    size_mb = round(os.path.getsize(fpath) / (1024 * 1024), 2)
                    out["subtitles"].append({
                        "name": fname,
                        "url": f"/api/projects/{project_id}/file/renders/subtitulos/{fname}",
                        "size_mb": size_mb,
                    })

    if os.path.exists(frames_dir):
        for fname in sorted(os.listdir(frames_dir)):
            if fname.lower().endswith(".png"):
                out["sheets"].append({
                    "name": fname,
                    "url": f"/api/projects/{project_id}/file/frames/{fname}",
                })

    for doc_name in ("YOUTUBE_PACK.md", "script_full.json", "script_full_en.json", "script_full_pt.json", "production_plan.json"):
        if os.path.exists(os.path.join(pdir, doc_name)):
            out["docs"].append({
                "name": doc_name,
                "url": f"/api/projects/{project_id}/file/{doc_name}",
            })
    return out


def bootstrap_existing_projects():
    """Importa automáticamente los proyectos hermanos (`historia_videojuegos_pixel` e `historia_ia_pixel`)
    al catálogo del servidor para que estén disponibles desde el primer arranque."""
    scratch_root = os.path.dirname(BASE_DIR)
    candidates = [
        (
            "historia_videojuegos_pixel",
            "PARA QUE NO SE ABURRAN — Historia de los Videojuegos (1958 → 2026)",
            "De un punto de luz en un osciloscopio a una industria de US$ 201.600 millones.",
        ),
        (
            "historia_ia_pixel",
            "LA HISTORIA DE LA INTELIGENCIA ARTIFICIAL (1950 → 2026)",
            "De Alan Turing y Dartmouth a los modelos fundacionales modernos.",
        ),
    ]
    for folder, title, sub in candidates:
        ext_dir = os.path.join(scratch_root, folder)
        if not os.path.exists(ext_dir):
            continue
        meta_file = _meta_path(folder)
        if os.path.exists(meta_file):
            continue
        meta = {
            "id": folder,
            "title": title,
            "subtitle": sub,
            "status": "completed",
            "stage": 8,
            "stage_name": "Producción completada (ES / EN / PT)",
            "progress": 100,
            "languages": ["es", "en", "pt"],
            "created_at": datetime.datetime.now().isoformat(timespec="seconds"),
            "updated_at": datetime.datetime.now().isoformat(timespec="seconds"),
            "external_path": ext_dir,
        }
        save_meta(folder, meta)
        append_log(folder, f"Proyecto existente '{title}' vinculado al catálogo de Pixeloide Studio Server.")


def create_project(title: str, raw_script: str, languages=("es", "en", "pt")) -> dict:
    slug = re.sub(r"[^a-z0-9]+", "_", (title or "documental").lower()).strip("_")[:24] or "documental"
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    project_id = f"{slug}_{stamp}"
    pdir = os.path.join(PROJECTS_DIR, project_id)
    os.makedirs(pdir, exist_ok=True)

    # Copiar plantilla del motor (engine, tools, fonts)
    for sub in ("engine", "tools", "fonts"):
        src_sub = os.path.join(TEMPLATE_DIR, sub)
        dst_sub = os.path.join(pdir, sub)
        if os.path.exists(src_sub):
            shutil.copytree(src_sub, dst_sub, dirs_exist_ok=True)

    for folder in ("assets/bg", "assets/portraits", "audio/vo", "audio/vo_en", "audio/vo_pt", "frames", "renders"):
        os.makedirs(os.path.join(pdir, folder), exist_ok=True)

    with open(os.path.join(pdir, "raw_script.txt"), "w", encoding="utf-8") as f:
        f.write(raw_script)

    meta = {
        "id": project_id,
        "title": title or "Nuevo Documental Pixeloide",
        "subtitle": "En cola de producción 16-bit",
        "status": "queued",
        "stage": 0,
        "stage_name": "En espera de iniciar...",
        "progress": 0,
        "languages": list(languages),
        "created_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "updated_at": datetime.datetime.now().isoformat(timespec="seconds"),
    }
    save_meta(project_id, meta)
    append_log(project_id, f"Proyecto '{meta['title']}' creado ({project_id}). Idiomas: {', '.join(languages).upper()}")
    return meta


def _run_cmd(cmd, cwd, project_id, env_extra=None):
    env = os.environ.copy()
    if env_extra:
        env.update(env_extra)
    proc = subprocess.Popen(
        cmd, cwd=cwd, env=env,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, encoding="utf-8", errors="replace"
    )
    for line in proc.stdout:
        line = line.rstrip()
        if line:
            append_log(project_id, f"  {line}")
    ret = proc.wait()
    if ret != 0:
        raise RuntimeError(f"Comando falló (código {ret}): {' '.join(cmd)}")


def _update_stage(project_id: str, stage: int, progress: int, status: str = "running", extra: dict = None):
    meta = load_meta(project_id)
    meta["stage"] = stage
    meta["stage_name"] = STAGE_NAMES.get(stage, "")
    meta["progress"] = progress
    meta["status"] = status
    meta["updated_at"] = datetime.datetime.now().isoformat(timespec="seconds")
    if extra:
        meta.update(extra)
    save_meta(project_id, meta)


def _pipeline_worker(project_id: str, start_stage: int = 1):
    pdir = get_project_dir(project_id)
    settings = get_settings()
    meta = load_meta(project_id)
    langs = meta.get("languages") or ["es", "en", "pt"]
    workers = str(settings.get("render_workers", 6))
    py = sys.executable

    try:
        raw_path = os.path.join(pdir, "raw_script.txt")
        raw_script = open(raw_path, encoding="utf-8").read() if os.path.exists(raw_path) else ""

        # STAGE 1: Estructuración de Guion + Plan Visual + i18n
        if start_stage <= 1:
            _update_stage(project_id, 1, 8)
            plan = structure_script(
                raw_script, pdir, settings,
                title_hint=meta.get("title", ""),
                log_fn=lambda m: append_log(project_id, m)
            )
            _update_stage(project_id, 1, 16, extra={
                "title": plan.get("title", meta.get("title")),
                "subtitle": plan.get("subtitle", ""),
            })
        else:
            plan_path = os.path.join(pdir, "production_plan.json")
            plan = json.load(open(plan_path, encoding="utf-8")) if os.path.exists(plan_path) else {}

        # STAGE 2: Locución Neuronal + Timestamps (Carlos Aguilar ES + EN/PT 1.0x)
        if start_stage <= 2:
            _update_stage(project_id, 2, 24)
            generate_project_tts(
                pdir, settings, languages=langs,
                log_fn=lambda m: append_log(project_id, m)
            )
            _update_stage(project_id, 2, 36)

        # STAGE 3: Fondos 480x270 y Retratos 64x64
        if start_stage <= 3:
            _update_stage(project_id, 3, 42)
            generate_project_assets(
                pdir, plan, settings,
                log_fn=lambda m: append_log(project_id, m)
            )
            _update_stage(project_id, 3, 50)

        # STAGE 4 & 5: Compilación de Escenas, Auditoría Visual y Hoja de Contacto
        if start_stage <= 5:
            _update_stage(project_id, 4, 55)
            append_log(project_id, "[Stage 4] Sincronizando timeline maestro y cierre de Pixeloide Studios (outro.py)...")
            _run_cmd([py, "engine/timeline.py"], pdir, project_id)
            _update_stage(project_id, 5, 62)
            append_log(project_id, "[Stage 5] Generando hoja de contacto visual (frames/sheet_all.png) y verificando márgenes...")
            _run_cmd([py, "engine/video.py", "sheet"], pdir, project_id)

        # STAGE 6: Síntesis Chiptune, SFX y Mezcla con Ducking
        if start_stage <= 6:
            _update_stage(project_id, 6, 70)
            append_log(project_id, "[Stage 6] Sintetizando banda sonora chiptune original, efectos y mezcla en Español...")
            _run_cmd([py, "engine/audio.py"], pdir, project_id)
            if "en" in langs or "pt" in langs:
                append_log(project_id, "[Stage 6] Generando mezclas multilingües (EN/PT) con cadencia natural...")
                _run_cmd([py, "tools/mix_multilingual.py"], pdir, project_id)

        # STAGE 7: Render Paralelo 1080p, Masterización -14 LUFS y Subtítulos .SRT Externos
        if start_stage <= 7:
            _update_stage(project_id, 7, 78)
            for idx_l, lg in enumerate(langs):
                append_log(project_id, f"[Stage 7] Renderizando video 1080p en {lg.upper()} con {workers} workers...")
                _run_cmd([py, "engine/video.py", "render", workers], pdir, project_id, env_extra={"PX_LANG": lg})
                _update_stage(project_id, 7, 78 + (idx_l + 1) * 4)

            append_log(project_id, "[Stage 7] Masterizando audio a -14 LUFS y generando archivos .MP4 sin subtítulos quemados...")
            _run_cmd([py, "tools/mux_all.py"], pdir, project_id)
            append_log(project_id, "[Stage 7] Generando subtítulos externos .SRT sincronizados...")
            _run_cmd([py, "tools/make_multilingual_subtitles.py"], pdir, project_id)

        # STAGE 8: Miniaturas de YouTube 16:9 y Shorts Verticales 9:16 + .SRT
        if start_stage <= 8:
            _update_stage(project_id, 8, 94)
            append_log(project_id, "[Stage 8] Generando Miniaturas 1080p y Shorts Verticales 9:16 (1080x1920)...")
            _run_cmd([py, "tools/make_thumbnails_and_shorts.py", *langs], pdir, project_id)

        _update_stage(project_id, 8, 100, status="completed", extra={
            "stage_name": "¡Producción completada con éxito!",
        })
        append_log(project_id, "✅ PRODUCCIÓN FINALIZADA. Todos los videos MP4, subtítulos SRT, Shorts y Miniaturas están listos.")
    except Exception as e:
        tb = traceback.format_exc()
        append_log(project_id, f"❌ ERROR EN EL PIPELINE: {e}\n{tb}")
        meta = load_meta(project_id)
        meta["status"] = "failed"
        meta["error"] = str(e)
        meta["updated_at"] = datetime.datetime.now().isoformat(timespec="seconds")
        save_meta(project_id, meta)
    finally:
        with _LOCK:
            _ACTIVE_JOBS.pop(project_id, None)


def start_pipeline_async(project_id: str, start_stage: int = 1) -> bool:
    with _LOCK:
        if project_id in _ACTIVE_JOBS and _ACTIVE_JOBS[project_id].is_alive():
            return False
        th = threading.Thread(target=_pipeline_worker, args=(project_id, start_stage), daemon=True)
        _ACTIVE_JOBS[project_id] = th
        th.start()
        return True
