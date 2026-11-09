"""Configuración global de Pixeloide Studio Server.
Gestiona API Keys, voces oficiales del Manual de Marca y rutas de proyectos.
"""
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECTS_DIR = os.path.join(BASE_DIR, "projects")
TEMPLATE_DIR = os.path.join(BASE_DIR, "engine_template")
DATA_DIR = os.path.join(BASE_DIR, "data")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")

os.makedirs(PROJECTS_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

DEFAULT_SETTINGS = {
    "elevenlabs_api_key": os.environ.get("ELEVENLABS_API_KEY", ""),
    "gemini_api_key": os.environ.get("GEMINI_API_KEY", ""),
    "anthropic_api_key": os.environ.get("ANTHROPIC_API_KEY", ""),
    "openai_api_key": os.environ.get("OPENAI_API_KEY", ""),
    "llm_provider": os.environ.get("LLM_PROVIDER", "auto"),      # auto | gemini | anthropic | openai
    "image_provider": os.environ.get("IMAGE_PROVIDER", "auto"),  # auto | gemini | openai | procedural
    "voice_es_id": "8MeTTgXVwMEhRVfblXOj",                       # Fijo: Carlos Aguilar
    "voice_es_name": "Carlos Aguilar (Oficial Pixeloide)",
    "voice_es_speed": 1.08,
    "voice_en_id": "pNInz6obpgDQGcFmaJgB",
    "voice_en_speed": 1.0,                                       # Velocidad natural 1.0x
    "voice_pt_id": "Rxw6ylGPvxzn3gsuOExL",
    "voice_pt_speed": 1.0,                                       # Velocidad natural 1.0x
    "render_workers": int(os.environ.get("RENDER_WORKERS", "6")),
}


def _load_env_fallback():
    """Intenta leer .env local o de proyectos hermanos si aún no se configuró."""
    candidates = [
        os.path.join(BASE_DIR, ".env"),
        os.path.join(os.path.dirname(BASE_DIR), "historia_videojuegos_pixel", ".env"),
        os.path.join(os.path.dirname(BASE_DIR), "historia_ia_pixel", ".env"),
    ]
    found = {}
    for p in candidates:
        if os.path.exists(p):
            try:
                for line in open(p, encoding="utf-8"):
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        found.setdefault(k.strip(), v.strip())
            except Exception:
                pass
    return found


def get_settings() -> dict:
    cfg = dict(DEFAULT_SETTINGS)
    env_vals = _load_env_fallback()
    if env_vals.get("ELEVENLABS_API_KEY") and not cfg["elevenlabs_api_key"]:
        cfg["elevenlabs_api_key"] = env_vals["ELEVENLABS_API_KEY"]
    if env_vals.get("GEMINI_API_KEY") and not cfg["gemini_api_key"]:
        cfg["gemini_api_key"] = env_vals["GEMINI_API_KEY"]
    if env_vals.get("ANTHROPIC_API_KEY") and not cfg["anthropic_api_key"]:
        cfg["anthropic_api_key"] = env_vals["ANTHROPIC_API_KEY"]
    if env_vals.get("OPENAI_API_KEY") and not cfg["openai_api_key"]:
        cfg["openai_api_key"] = env_vals["OPENAI_API_KEY"]

    if os.path.exists(SETTINGS_FILE):
        try:
            saved = json.load(open(SETTINGS_FILE, encoding="utf-8"))
            for k, v in saved.items():
                if v not in (None, ""):
                    cfg[k] = v
        except Exception:
            pass
    # Garantizar regla innegociable: Carlos Aguilar en ES y velocidad natural 1.0 en EN/PT
    if not cfg.get("voice_es_id"):
        cfg["voice_es_id"] = "8MeTTgXVwMEhRVfblXOj"
    cfg["voice_en_speed"] = 1.0
    cfg["voice_pt_speed"] = 1.0
    return cfg


def save_settings(new_data: dict) -> dict:
    cur = get_settings()
    for k in DEFAULT_SETTINGS:
        if k in new_data and new_data[k] is not None:
            # Si viene enmascarado con "***", no pisar la key real
            val = new_data[k]
            if isinstance(val, str) and "***" in val:
                continue
            cur[k] = val
    json.dump(cur, open(SETTINGS_FILE, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    return cur


def mask_key(k: str) -> str:
    if not k or len(k) < 8:
        return ""
    return k[:4] + "***" + k[-4:]
