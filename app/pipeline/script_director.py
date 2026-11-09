"""Stage 1 — Director de Guion y Planificador Visual 16-Bit (`script_director.py`).

Recibe un guion en texto o PDF y genera:
- `script_full.json`, `script_full_en.json`, `script_full_pt.json`
- `production_plan.json` (fondos 480x270, retratos 64x64, escenas, personajes y música por capítulo)
- `translations_map.json` (diccionario EN/PT para textos en pantalla)
- `YOUTUBE_PACK.md` (títulos, descripciones, capítulos y tags en ES/EN/PT)
"""
import json
import os
import re
import urllib.request
import urllib.error


def extract_text_from_file(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        # Intentar con pypdf, fitz (PyMuPDF) o pdfplumber
        for mod_name in ("pypdf", "PyPDF2"):
            try:
                mod = __import__(mod_name)
                reader = mod.PdfReader(file_path)
                return "\n\n".join(page.extract_text() or "" for page in reader.pages)
            except Exception:
                pass
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(file_path)
            return "\n\n".join(page.get_text() for page in doc)
        except Exception:
            pass
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


DIRECTOR_SYSTEM_PROMPT = """Eres el Director Técnico y Guionista Principal de PIXELOIDE STUDIOS ("JUGAMOS EN SERIO.").
Tu tarea es convertir el guion documental entregado por el usuario en un paquete JSON estructurado para el motor Pixeloide Video Engine 16-bit (lienzo lógico 480x270 escalado 4x a 1920x1080).

REGLAS INNEGOCIABLES:
1. Estructura la locución en frases ágiles de documental ("lines_es"), identificadas como:
   - Apertura (si aplica): "s01", "s02", ...
   - Placa de cada capítulo: "c1_00", "c2_00", ... (ej. speak: "Capítulo uno. El punto de luz.", sub: "CAPÍTULO 1 — EL PUNTO DE LUZ")
   - Frases de cada capítulo: "c1_01", "c1_02", ..., "c2_01", ...
2. Genera las traducciones completas de las líneas a Inglés ("lines_en") y Portugués ("lines_pt") manteniendo exactamente los mismos "id", "ch" y "pause", con cadencia documental natural.
3. Diseña las escenas ("scenes") asociando cada "line_id" (y "end_line") a un arquetipo visual 16-bit:
   Layouts válidos: "title_card", "chapter_card", "lab_scene", "dialogue_scene", "split_vs", "data_bars", "living_room_tv", "calendar_stamp".
4. En cada escena:
   - Todos los textos de banners ("header", "subheader") y tarjetas ("cards") deben ser cortos (máximo 32 caracteres por línea) para que NUNCA se salgan de las cajas RPG.
   - Los personajes ("characters") siempre deben tener "feet": 260 (apoyados sobre el piso) y "scale": 2 (o 3 en primeros planos). Presets disponibles: "inge", "prof", "estudiante", "ejecutivo", "mujer_ejecutiva", "chica", "abuela", "nieto", "padre".
5. Incluye en "translations_map" la traducción exacta al inglés ("en") y portugués ("pt") de TODOS los textos en mayúsculas que aparecen en "header", "subheader", "cards", "lower_third", "bubble" y "stamp".

Devuelve ÚNICAMENTE un objeto JSON válido con esta estructura exacta:
{
  "title": "TÍTULO PRINCIPAL EN ESPAÑOL",
  "subtitle": "SUBTÍTULO CORTO",
  "slug": "Nombre_Corto_Proyecto",
  "year_start": "1958",
  "year_end": "2026",
  "titles": {"es": "...", "en": "...", "pt": "..."},
  "subtitles": {"es": "...", "en": "...", "pt": "..."},
  "lines_es": [{"id": "s01", "ch": 0, "pause": 0.35, "speak": "...", "sub": "..."}],
  "lines_en": [{"id": "s01", "ch": 0, "pause": 0.35, "speak": "...", "sub": "..."}],
  "lines_pt": [{"id": "s01", "ch": 0, "pause": 0.35, "speak": "...", "sub": "..."}],
  "backgrounds": [
    {"name": "bg_lab_1958", "theme": "lab", "prompt": "16-bit SNES pixel art wide background of a 1958 physics laboratory with oscilloscope, warm lighting, no text, 480x270"}
  ],
  "portraits": [
    {"name": "protagonista_1", "prompt": "16-bit SNES Chrono Trigger style pixel art 64x64 bust portrait of ..., solid dark blue background"}
  ],
  "chapter_music": {"0": "mystery", "1": "build", "2": "bright", "3": "rain", "4": "triumph"},
  "scenes": [
    {
      "line_id": "s01",
      "end_line": "s02",
      "layout": "lab_scene",
      "bg": "bg_lab_1958",
      "header": "OCTUBRE 1958 · BROOKHAVEN",
      "subheader": "EL PRIMER PUNTO DE LUZ",
      "year": "1958",
      "portrait": "protagonista_1",
      "cards": [{"title": "DATO CLAVE", "lines": ["OSCILOSCOPIO ANALÓGICO", "CERO PATENTES"]}],
      "characters": [{"preset": "inge", "x": 115, "feet": 260, "scale": 2, "mood": "happy", "bubble": "¡FUNCIONA!"}],
      "lower_third": {"title": "WILLIAM HIGINBOTHAM", "sub": "FÍSICO NUCLEAR · 1958"}
    }
  ],
  "translations_map": {
    "en": {"OCTUBRE 1958 · BROOKHAVEN": "OCTOBER 1958 · BROOKHAVEN"},
    "pt": {"OCTUBRE 1958 · BROOKHAVEN": "OUTUBRO 1958 · BROOKHAVEN"}
  },
  "youtube_pack_md": "# Pack de YouTube completo en Markdown..."
}
"""


def _extract_json_block(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        return json.loads(text[start:end + 1])
    return json.loads(text)


def _call_gemini(api_key: str, raw_script: str, title_hint: str = "") -> dict:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={api_key}"
    prompt = f"Título sugerido: {title_hint}\n\nGUION A PRODUCIR:\n{raw_script}"
    body = {
        "systemInstruction": {"parts": [{"text": DIRECTOR_SYSTEM_PROMPT}]},
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.3,
            "responseMimeType": "application/json",
        },
    }
    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"), method="POST",
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=240) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    txt = data["candidates"][0]["content"]["parts"][0]["text"]
    return _extract_json_block(txt)


def _call_anthropic(api_key: str, raw_script: str, title_hint: str = "") -> dict:
    url = "https://api.anthropic.com/v1/messages"
    prompt = f"Título sugerido: {title_hint}\n\nGUION A PRODUCIR:\n{raw_script}\n\nResponde SOLO con el JSON válido."
    body = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 16000,
        "temperature": 0.3,
        "system": DIRECTOR_SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": prompt}],
    }
    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"), method="POST",
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }
    )
    with urllib.request.urlopen(req, timeout=240) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    txt = data["content"][0]["text"]
    return _extract_json_block(txt)


def _call_openai(api_key: str, raw_script: str, title_hint: str = "") -> dict:
    url = "https://api.openai.com/v1/chat/completions"
    prompt = f"Título sugerido: {title_hint}\n\nGUION A PRODUCIR:\n{raw_script}"
    body = {
        "model": "gpt-4o",
        "temperature": 0.3,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": DIRECTOR_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    }
    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"), method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
    )
    with urllib.request.urlopen(req, timeout=240) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    txt = data["choices"][0]["message"]["content"]
    return _extract_json_block(txt)


def _deterministic_parse_script(raw_script: str, title_hint: str = "") -> dict:
    """Parser determinístico inteligente para estructurar cualquier guion cuando no hay API key de LLM
    o como respaldo instantáneo."""
    lines_raw = [ln.strip() for ln in raw_script.splitlines() if ln.strip()]
    title = (title_hint or (lines_raw[0] if lines_raw else "DOCUMENTAL PIXELOIDE")).strip("#* ")[:42].upper()
    slug = re.sub(r"[^A-Za-z0-9]+", "_", title).strip("_")[:28] or "Documental_Pixeloide"

    years_found = re.findall(r"\b(1[89]\d{2}|20\d{2})\b", raw_script)
    yr_start = years_found[0] if years_found else "ORIGEN"
    yr_end = years_found[-1] if len(years_found) > 1 else "2026"

    # Separar por capítulos si el texto menciona "CAPÍTULO" o encabezados "##"
    chapters = []
    cur_ch = {"num": 1, "title": "EL COMIENZO", "sentences": []}
    ch_counter = 0

    for ln in lines_raw:
        # Ignorar indicaciones técnicas entre corchetes si están solas
        if ln.startswith("[") and ln.endswith("]"):
            continue
        m_ch = re.match(r"^(?:#+\s*)?(?:CAP[ÍI]TULO|CHAPTER|EPISODIO|PARTE)\s*(\d+)?[:\.\-—\s]*(.*)$", ln, re.IGNORECASE)
        if m_ch:
            if cur_ch["sentences"]:
                chapters.append(cur_ch)
            ch_counter += 1
            ch_num = int(m_ch.group(1)) if m_ch.group(1) else ch_counter
            ch_title = (m_ch.group(2) or f"CAPÍTULO {ch_num}").strip().upper()[:32]
            cur_ch = {"num": ch_num, "title": ch_title, "sentences": []}
            continue
        # Limpiar acotaciones entre corchetes dentro de la línea
        clean_ln = re.sub(r"\[[^\]]*\]", "", ln).strip()
        if not clean_ln:
            continue
        # Partir párrafos largos en oraciones de tamaño ideal para locución
        sents = re.split(r"(?<=[\.\!\?])\s+", clean_ln)
        for s in sents:
            s = s.strip()
            if len(s) >= 3:
                cur_ch["sentences"].append(s)

    if cur_ch["sentences"]:
        chapters.append(cur_ch)
    if not chapters:
        chapters = [{"num": 1, "title": title[:28], "sentences": ["Esta es una producción de Pixeloide Studios."]}]

    lines_es, lines_en, lines_pt = [], [], []
    scenes = []
    backgrounds = []
    chapter_music = {}
    presets = ["inge", "prof", "estudiante", "ejecutivo", "mujer_ejecutiva", "chica", "padre"]
    themes = ["lab", "city", "living", "arcade", "office", "desert", "neon"]
    layouts = ["lab_scene", "dialogue_scene", "living_room_tv", "data_bars", "split_vs", "calendar_stamp"]

    for c_idx, ch in enumerate(chapters):
        ch_num = c_idx + 1
        card_id = f"c{ch_num}_00"
        card_speak = f"Capítulo {ch_num}. {ch['title'].title()}."
        card_sub = f"CAPÍTULO {ch_num} — {ch['title']}"
        lines_es.append({"id": card_id, "ch": ch_num, "pause": 0.45, "speak": card_speak, "sub": card_sub})
        lines_en.append({"id": card_id, "ch": ch_num, "pause": 0.45, "speak": f"Chapter {ch_num}. {ch['title'].title()}.", "sub": f"CHAPTER {ch_num} — {ch['title']}"})
        lines_pt.append({"id": card_id, "ch": ch_num, "pause": 0.45, "speak": f"Capítulo {ch_num}. {ch['title'].title()}.", "sub": f"CAPÍTULO {ch_num} — {ch['title']}"})

        bg_name = f"bg_ch{ch_num:02d}"
        theme = themes[c_idx % len(themes)]
        backgrounds.append({
            "name": bg_name,
            "theme": theme,
            "prompt": f"16-bit SNES pixel art wide background for {ch['title']}, {theme} atmosphere, warm cinematic lighting, no text, 480x270",
        })
        chapter_music[str(ch_num)] = ["mystery", "build", "bright", "puzzle", "rain", "summer", "triumph", "winter"][c_idx % 8]

        scenes.append({
            "line_id": card_id,
            "end_line": card_id,
            "layout": "chapter_card",
            "chapter": ch_num,
            "title_lines": [ch["title"][:28]],
            "years": f"CAPÍTULO {ch_num}",
        })

        for s_idx, sent in enumerate(ch["sentences"]):
            lid = f"c{ch_num}_{s_idx + 1:02d}"
            pause = 0.75 if s_idx == len(ch["sentences"]) - 1 else 0.25
            lines_es.append({"id": lid, "ch": ch_num, "pause": pause, "speak": sent, "sub": sent})
            lines_en.append({"id": lid, "ch": ch_num, "pause": pause, "speak": sent, "sub": sent})
            lines_pt.append({"id": lid, "ch": ch_num, "pause": pause, "speak": sent, "sub": sent})

            yr_m = re.search(r"\b(1[89]\d{2}|20\d{2})\b", sent)
            yr_str = yr_m.group(1) if yr_m else ""
            words_up = [w.strip(".,;:!?\"'()") for w in sent.upper().split() if len(w) > 3]
            short_hdr = " ".join(words_up[:4])[:30] or ch["title"][:28]
            short_line1 = " ".join(words_up[4:8])[:26] or "ANÁLISIS DOCUMENTAL"
            short_line2 = " ".join(words_up[8:12])[:26] or "PIXELOIDE STUDIOS"

            lay = "title_card" if (c_idx == 0 and s_idx == 0) else layouts[(c_idx + s_idx) % len(layouts)]
            scenes.append({
                "line_id": lid,
                "end_line": lid,
                "layout": lay,
                "bg": bg_name,
                "header": f"{yr_str} · {short_hdr}".strip(" ·")[:32],
                "subheader": ch["title"][:36],
                "year": yr_str,
                "cards": [
                    {
                        "title": f"CLAVE #{s_idx + 1}",
                        "lines": [short_line1, short_line2],
                    }
                ],
                "characters": [
                    {
                        "preset": presets[(c_idx + s_idx) % len(presets)],
                        "x": 112,
                        "feet": 260,
                        "scale": 2,
                        "mood": "happy",
                    },
                    {
                        "preset": presets[(c_idx + s_idx + 2) % len(presets)],
                        "x": 368,
                        "feet": 260,
                        "scale": 2,
                        "mood": "open",
                    },
                ],
                "lower_third": {
                    "title": ch["title"][:24],
                    "sub": f"CAPÍTULO {ch_num} · {yr_str or 'HISTORIA'}",
                } if s_idx == 0 else None,
            })

    yt_pack = f"""# Pack de Publicación YouTube — {title}

## Español (ES)
- **Título**: {title} — Documental Completo en Pixel Art 16-Bit | Pixeloide Studios
- **Descripción**:
  Una producción original de **Pixeloide Studios** (`JUGAMOS EN SERIO.`).
  - Idea Original y Producción: **Braian Greno**
  - Narración: **Carlos Aguilar**
  - Subtítulos `.srt` incluidos (sin quemar en el video).

## English (EN)
- **Title**: {title} — Full 16-Bit Pixel Art Documentary | Pixeloide Studios

## Português (PT)
- **Título**: {title} — Documentário Completo em Pixel Art 16-Bit | Pixeloide Studios
"""
    return {
        "title": title,
        "subtitle": f"{yr_start} → {yr_end} · DOCUMENTAL 16-BIT",
        "slug": slug,
        "year_start": yr_start,
        "year_end": yr_end,
        "titles": {"es": title, "en": title, "pt": title},
        "subtitles": {
            "es": f"{yr_start} → {yr_end} · DOCUMENTAL PIXEL ART",
            "en": f"{yr_start} → {yr_end} · PIXEL ART DOCUMENTARY",
            "pt": f"{yr_start} → {yr_end} · DOCUMENTÁRIO PIXEL ART",
        },
        "lines_es": lines_es,
        "lines_en": lines_en,
        "lines_pt": lines_pt,
        "backgrounds": backgrounds,
        "portraits": [],
        "chapter_music": chapter_music,
        "scenes": scenes,
        "translations_map": {"en": {}, "pt": {}},
        "youtube_pack_md": yt_pack,
    }


def structure_script(raw_script: str, project_dir: str, settings: dict, title_hint: str = "", log_fn=print) -> dict:
    """Estructura el guion usando el proveedor LLM configurado (o el parser determinístico de respaldo)
    y escribe `script_full.json`, `script_full_en.json`, `script_full_pt.json`, `production_plan.json`,
    `translations_map.json` y `YOUTUBE_PACK.md` en `project_dir`."""
    provider = settings.get("llm_provider", "auto")
    plan_data = None

    providers_to_try = []
    if provider == "gemini" or (provider == "auto" and settings.get("gemini_api_key")):
        providers_to_try.append(("gemini", settings.get("gemini_api_key")))
    if provider == "anthropic" or (provider == "auto" and settings.get("anthropic_api_key")):
        providers_to_try.append(("anthropic", settings.get("anthropic_api_key")))
    if provider == "openai" or (provider == "auto" and settings.get("openai_api_key")):
        providers_to_try.append(("openai", settings.get("openai_api_key")))

    for p_name, p_key in providers_to_try:
        if not p_key:
            continue
        try:
            log_fn(f"[Stage 1] Estructurando guion y plan visual 16-bit con {p_name.upper()}...")
            if p_name == "gemini":
                plan_data = _call_gemini(p_key, raw_script, title_hint)
            elif p_name == "anthropic":
                plan_data = _call_anthropic(p_key, raw_script, title_hint)
            elif p_name == "openai":
                plan_data = _call_openai(p_key, raw_script, title_hint)
            if plan_data and plan_data.get("lines_es"):
                log_fn(f"[Stage 1] Plan generado con éxito ({len(plan_data['lines_es'])} líneas, {len(plan_data.get('scenes', []))} escenas).")
                break
        except Exception as e:
            log_fn(f"[Stage 1] Aviso con {p_name}: {e}. Probando siguiente método...")

    if not plan_data or not plan_data.get("lines_es"):
        log_fn("[Stage 1] Usando estructurador determinístico Pixeloide para el guion...")
        plan_data = _deterministic_parse_script(raw_script, title_hint)

    # Guardar archivos en project_dir
    with open(os.path.join(project_dir, "script_full.json"), "w", encoding="utf-8") as f:
        json.dump(plan_data["lines_es"], f, indent=2, ensure_ascii=False)
    with open(os.path.join(project_dir, "script_full_en.json"), "w", encoding="utf-8") as f:
        json.dump(plan_data.get("lines_en") or plan_data["lines_es"], f, indent=2, ensure_ascii=False)
    with open(os.path.join(project_dir, "script_full_pt.json"), "w", encoding="utf-8") as f:
        json.dump(plan_data.get("lines_pt") or plan_data["lines_es"], f, indent=2, ensure_ascii=False)

    with open(os.path.join(project_dir, "translations_map.json"), "w", encoding="utf-8") as f:
        json.dump(plan_data.get("translations_map", {"en": {}, "pt": {}}), f, indent=2, ensure_ascii=False)

    with open(os.path.join(project_dir, "production_plan.json"), "w", encoding="utf-8") as f:
        json.dump(plan_data, f, indent=2, ensure_ascii=False)

    yt_md = plan_data.get("youtube_pack_md") or f"# {plan_data.get('title', 'Documental Pixeloide')}\n"
    with open(os.path.join(project_dir, "YOUTUBE_PACK.md"), "w", encoding="utf-8") as f:
        f.write(yt_md)

    return plan_data
