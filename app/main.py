"""Servidor Web y API REST de Pixeloide Studio Server (`app/main.py`).
Permite subir un guion (PDF, TXT, MD o texto pegado) y producir automáticamente el documental
16-bit completo en Español (con Carlos Aguilar), Inglés y Portugués, incluyendo Shorts, Miniaturas y SRTs.
"""
import io
import json
import os
import tempfile
import zipfile
from typing import List, Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.config import BASE_DIR, PROJECTS_DIR, get_settings, mask_key, save_settings
from app.pipeline.orchestrator import (
    STAGE_NAMES,
    append_log,
    bootstrap_existing_projects,
    create_project,
    get_project_dir,
    list_deliverables,
    load_meta,
    save_meta,
    start_pipeline_async,
)
from app.pipeline.script_director import extract_text_from_file

app = FastAPI(
    title="Pixeloide Studio Server",
    description="Plataforma de producción automática de documentales en Pixel Art 16-Bit — Pixeloide Studios",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.on_event("startup")
def on_startup():
    bootstrap_existing_projects()


@app.get("/", response_class=HTMLResponse)
def index():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return open(index_path, encoding="utf-8").read()
    return "<h1>Pixeloide Studio Server</h1>"


@app.get("/api/health")
def health():
    return {"status": "ok", "studio": "Pixeloide Studios", "claim": "JUGAMOS EN SERIO."}


@app.get("/api/settings")
def api_get_settings():
    cfg = get_settings()
    return {
        "elevenlabs_api_key_masked": mask_key(cfg.get("elevenlabs_api_key", "")),
        "has_elevenlabs": bool(cfg.get("elevenlabs_api_key")),
        "gemini_api_key_masked": mask_key(cfg.get("gemini_api_key", "")),
        "has_gemini": bool(cfg.get("gemini_api_key")),
        "anthropic_api_key_masked": mask_key(cfg.get("anthropic_api_key", "")),
        "has_anthropic": bool(cfg.get("anthropic_api_key")),
        "openai_api_key_masked": mask_key(cfg.get("openai_api_key", "")),
        "has_openai": bool(cfg.get("openai_api_key")),
        "llm_provider": cfg.get("llm_provider", "auto"),
        "image_provider": cfg.get("image_provider", "auto"),
        "voice_es_id": cfg.get("voice_es_id", "8MeTTgXVwMEhRVfblXOj"),
        "voice_es_name": cfg.get("voice_es_name", "Carlos Aguilar (Oficial Pixeloide)"),
        "voice_es_speed": cfg.get("voice_es_speed", 1.08),
        "voice_en_id": cfg.get("voice_en_id", "pNInz6obpgDQGcFmaJgB"),
        "voice_en_speed": 1.0,
        "voice_pt_id": cfg.get("voice_pt_id", "Rxw6ylGPvxzn3gsuOExL"),
        "voice_pt_speed": 1.0,
        "render_workers": cfg.get("render_workers", 6),
    }


class SettingsUpdate(BaseModel):
    elevenlabs_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    llm_provider: Optional[str] = None
    image_provider: Optional[str] = None
    voice_es_id: Optional[str] = None
    voice_es_speed: Optional[float] = None
    render_workers: Optional[int] = None


@app.post("/api/settings")
def api_save_settings(body: SettingsUpdate):
    save_settings(body.dict(exclude_none=True))
    return api_get_settings()


@app.get("/api/projects")
def api_list_projects():
    bootstrap_existing_projects()
    items = []
    if os.path.exists(PROJECTS_DIR):
        for pid in os.listdir(PROJECTS_DIR):
            meta = load_meta(pid)
            if meta:
                meta["deliverables"] = list_deliverables(pid)
                items.append(meta)
    items.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return {"projects": items, "stages": STAGE_NAMES}


@app.post("/api/projects")
async def api_create_project(
    title: str = Form("Nuevo Documental Pixeloide"),
    script_text: str = Form(""),
    languages: str = Form("es,en,pt"),
    auto_start: bool = Form(True),
    file: Optional[UploadFile] = File(None),
):
    raw_content = (script_text or "").strip()
    if file and file.filename:
        suffix = os.path.splitext(file.filename)[1] or ".txt"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            content_bytes = await file.read()
            tmp.write(content_bytes)
            tmp_path = tmp.name
        try:
            extracted = extract_text_from_file(tmp_path)
            if extracted.strip():
                raw_content = (raw_content + "\n\n" + extracted).strip() if raw_content else extracted.strip()
            if (not title or title == "Nuevo Documental Pixeloide") and file.filename:
                title = os.path.splitext(file.filename)[0].replace("_", " ")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    if not raw_content:
        raise HTTPException(status_code=400, detail="Debes pegar un guion o subir un archivo PDF/TXT/MD.")

    langs = [x.strip().lower() for x in languages.split(",") if x.strip()] or ["es", "en", "pt"]
    meta = create_project(title=title, raw_script=raw_content, languages=langs)
    if auto_start:
        start_pipeline_async(meta["id"], start_stage=1)
    return meta


@app.get("/api/projects/{project_id}")
def api_get_project(project_id: str):
    meta = load_meta(project_id)
    if not meta:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    pdir = get_project_dir(project_id)
    meta["deliverables"] = list_deliverables(project_id)
    script_path = os.path.join(pdir, "script_full.json")
    meta["script_lines"] = json.load(open(script_path, encoding="utf-8")) if os.path.exists(script_path) else []
    yt_path = os.path.join(pdir, "YOUTUBE_PACK.md")
    meta["youtube_pack"] = open(yt_path, encoding="utf-8").read() if os.path.exists(yt_path) else ""
    return meta


@app.get("/api/projects/{project_id}/logs")
def api_get_logs(project_id: str):
    log_path = os.path.join(PROJECTS_DIR, project_id, "build.log")
    if not os.path.exists(log_path):
        return {"logs": ""}
    txt = open(log_path, encoding="utf-8", errors="replace").read()
    return {"logs": txt[-24000:]}


class RunRequest(BaseModel):
    start_stage: int = 1


@app.post("/api/projects/{project_id}/run")
def api_run_project(project_id: str, body: RunRequest):
    meta = load_meta(project_id)
    if not meta:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    started = start_pipeline_async(project_id, start_stage=max(1, min(8, body.start_stage)))
    return {"started": started, "project_id": project_id, "start_stage": body.start_stage}


class ScriptLinesUpdate(BaseModel):
    lines_es: list
    rerun_from_stage: Optional[int] = None


@app.put("/api/projects/{project_id}/script")
def api_update_script(project_id: str, body: ScriptLinesUpdate):
    pdir = get_project_dir(project_id)
    if not os.path.exists(pdir):
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    with open(os.path.join(pdir, "script_full.json"), "w", encoding="utf-8") as f:
        json.dump(body.lines_es, f, indent=2, ensure_ascii=False)
    append_log(project_id, f"Guion en español actualizado manualmente ({len(body.lines_es)} líneas).")
    if body.rerun_from_stage:
        start_pipeline_async(project_id, start_stage=body.rerun_from_stage)
    return {"ok": True}


@app.get("/api/projects/{project_id}/file/{subpath:path}")
def api_get_project_file(project_id: str, subpath: str):
    pdir = get_project_dir(project_id)
    safe_sub = os.path.normpath(subpath).lstrip("\\/")
    full = os.path.abspath(os.path.join(pdir, safe_sub))
    if not full.startswith(os.path.abspath(pdir)) or not os.path.isfile(full):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    return FileResponse(full)


@app.get("/api/projects/{project_id}/download-zip")
def api_download_zip(project_id: str):
    pdir = get_project_dir(project_id)
    if not os.path.exists(pdir):
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        renders_dir = os.path.join(pdir, "renders")
        if os.path.exists(renders_dir):
            for fname in os.listdir(renders_dir):
                fpath = os.path.join(renders_dir, fname)
                if os.path.isfile(fpath) and not fname.startswith("video_mudo"):
                    zf.write(fpath, arcname=f"renders/{fname}")
            sub_dir = os.path.join(renders_dir, "subtitulos")
            if os.path.exists(sub_dir):
                for fname in os.listdir(sub_dir):
                    fpath = os.path.join(sub_dir, fname)
                    if os.path.isfile(fpath):
                        zf.write(fpath, arcname=f"renders/subtitulos/{fname}")
        for doc in ("YOUTUBE_PACK.md", "script_full.json", "script_full_en.json", "script_full_pt.json"):
            dpath = os.path.join(pdir, doc)
            if os.path.isfile(dpath):
                zf.write(dpath, arcname=doc)
    buf.seek(0)
    headers = {"Content-Disposition": f'attachment; filename="{project_id}_Pixeloide_Pack.zip"'}
    return StreamingResponse(buf, media_type="application/zip", headers=headers)
