---
name: pixeloide-video-engine
description: Framework y pipeline oficial de Pixeloide Studios para producir documentales animados en pixel art 16-bit (estilo SNES / Chrono Trigger) a partir de un guion en texto. Úsalo siempre que el usuario entregue un guion o pida crear un video animado en pixel art con narrador en español (Carlos Aguilar), versiones multilingües (EN/PT), música chiptune procedural y cierre oficial de Pixeloide Studios + créditos.
---

# Pixeloide Video Engine — Framework de Producción Documental 16-Bit

Este skill define el estándar de producción de **Pixeloide Studios** (`JUGAMOS EN SERIO.`) para transformar cualquier guion entregado por el usuario en un documental animado 16-bit (`1920x1080` a `30 fps`, lienzo lógico `480x270` escalado `4x` nearest-neighbor) en Español (`ES`), Inglés (`EN`) y Portugués (`PT`).

> **Repositorios base / motores de referencia**:
> - Motor documental completo: `C:\Users\Braian\.gemini\antigravity\scratch\historia_videojuegos_pixel`
> - Plataforma Web + API REST instalable en servidor: `C:\Users\Braian\.gemini\antigravity\scratch\pixeloide_studio_server` (`.\start_windows.ps1` o `docker compose up -d --build`)
> - Proyecto original IA: `C:\Users\Braian\.gemini\antigravity\scratch\historia_ia_pixel`

---

## 1. Reglas Innegociables de Marca y Audio

1. **Narrador Oficial en Español (Fijo)**:
   - Nombre: **Carlos Aguilar** (ElevenLabs)
   - `VOICE_ID`: `"8MeTTgXVwMEhRVfblXOj"`
   - Modelo: `"eleven_v4"` (o `"eleven_multilingual_v2"` con `with-timestamps`)
   - Configuración: `stability=0.45`, `similarity_boost=0.80`, `style=0.35`, `use_speaker_boost=True`, `speed=1.08`.
   - **Nunca cambies el narrador en español** a menos que el usuario lo pida explícitamente.

2. **Narradores en Inglés (`EN`) y Portugués (`PT`) — Cadencia Natural**:
   - Inglés (`EN`): `VOICE_ID = "pNInz6obpgDQGcFmaJgB"`
   - Portugués (`PT`): `VOICE_ID = "Rxw6ylGPvxzn3gsuOExL"`
   - Modelo: `"eleven_multilingual_v2"`
   - **Velocidad de generación (`speed`)**: **`1.0` (natural)**. **PROHIBIDO usar `speed=1.15`**, ya que acelera artificialmente la locución.
   - **Sincronización en mezcla (`tools/mix_multilingual.py`)**:
     - Al alinear cada línea `lid` con el timeline maestro en español, calcula siempre la ventana real disponible hasta la siguiente frase:
       ```python
       next_start = TL.s(TL.order[i + 1]) if i + 1 < len(TL.order) else (TL.e(lid) + 1.0)
       avail_dur = max(slot_dur, next_start - slot_start - 0.08)
       ```
     - Solo comprime con `atempo` cuando `d_nat > avail_dur`, evitando que las voces en inglés o portugués suenen apresuradas.

3. **Traducción Total en Pantalla (`engine/i18n.py`)**:
   - No basta con cambiar el audio: **todos los textos visibles en las escenas** (títulos de capítulos, etiquetas, diagramas, tarjetas, diálogos, banners y créditos) deben traducirse a `en` y `pt` mediante el hook automático de `engine/i18n.py` integrado en `Frame.text()` y `Frame.text_wrap()`.
   - El motor de fuentes (`engine/core.py`) soporta composición automática de diacríticos en mayúsculas (`Á, É, Í, Ó, Ú, À, Â, Ê, Ô, Ã, Õ, Ç, Ñ, Ü`).

4. **Cierre Oficial Obligatorio (`engine/outro.py`) — Manual de Marca Pixeloide Studios**:
   Todo video producido con este framework **debe** cerrar con el módulo `engine/outro.py` (`TAIL = 12.0s` en `engine/timeline.py`), dividido en dos escenas tras el fade-out del último capítulo:
   - **Escena 1 (`sc_pixeloide_logo`, ~3.8s)**:
     - Transición de barrido (`wipe`) de `520ms` en **Cyan** (`#28DCE0`) con curva `cubic-bezier(.76, 0, .24, 1)`.
     - Fondo oscuro **Ink** (`#070A1F`) con el **Campo de píxeles** reactivo iluminándose de **Cyan** (`#28DCE0`) a **Magenta** (`#E732B6`).
     - Isotipo geométrico exacto: **«Una P que es un play»** (triángulo superior en Cyan `#28DCE0`, franja diagonal en Paper `#F4F3EE` formando la punta derecha del Play, y chispa triangular inferior en Magenta `#E732B6`).
     - Logotipo **PIXELOIDE** (`#F4F3EE`) + **STUDIOS** (`#28DCE0`) y claim **`JUGAMOS EN SERIO.`** (`JUGAMOS` en Paper, `EN SERIO` en Cyan, punto `.` en Magenta; traducido en EN a `WE PLAY SERIOUSLY.` y en PT a `JOGAMOS A SÉRIO.`).
   - **Escena 2 (`sc_credits`, ~5.4s)**:
     - Header con lockup horizontal de **Pixeloide Studios** + `01 — CRÉDITOS DE PRODUCCIÓN`.
     - Dos tarjetas destacadas de autoría:
       - **IDEA ORIGINAL**: `BRAIAN GRENO`
       - **PRODUCCIÓN Y DIRECCIÓN**: `BRAIAN GRENO`
     - Panel `02 — HERRAMIENTAS DE IA Y TECNOLOGÍA` (`IA + CODE`) listando el stack completo:
       - `CLAUDE & GEMINI` — Dirección técnica · Código y animación
       - `ELEVENLABS` — Locución neuronal · Carlos Aguilar
       - `OPENAI WHISPER` — Alineación fonética y subtítulos
       - `IMAGEN / NANOBANANA` — Arte pixel base · Fondos y retratos
       - `PYTHON · PIL · NUMPY` — Motor pixel art 16-bit y chiptune
       - `FFMPEG` — Masterización 1080p · Audio -14 LUFS

---

## 2. Flujo Paso a Paso desde un Guion Nuevo

Cuando el usuario te entregue un guion nuevo, ejecuta este pipeline en orden:

### Paso 1 — Estructurar el Guion (`script_full.json`, `script_full_en.json`, `script_full_pt.json`)
Convierte el guion en una lista JSON de líneas narrativas con:
- `id`: identificador `"c{cap}_{num:02d}"` (ej. `"c1_01"`, `"c1_02"`, ...)
- `ch`: número de capítulo (`1..N`)
- `pause`: pausa dramática en segundos después de la línea (`0.35` normal, `0.65` cierre de idea, `1.1` fin de capítulo)
- `speak`: texto optimizado para fonética TTS (fechas y siglas escritas como se pronuncian en español si hace falta)
- `sub`: texto limpio para subtítulos en pantalla

Genera a la vez `script_full_en.json` y `script_full_pt.json` con los mismos `id`, `ch` y `pause`, traduciendo `speak` y `sub` con tono documental natural.

### Paso 2 — Generar Locución + Timestamps (`audio/vo/`, `audio/vo_en/`, `audio/vo_pt/`)
1. Ejecuta `python batch_tts.py` para generar `audio/vo/{id}.mp3` y `audio/vo/{id}.json` con **Carlos Aguilar** (`8MeTTgXVwMEhRVfblXOj`).
2. Ejecuta `python tools/batch_tts_multilingual.py` para generar `audio/vo_en/` y `audio/vo_pt/` a velocidad natural (`speed=1.0`).
3. Verifica que `engine/timeline.py` construya el timeline maestro a partir de `script_full.json` + `audio/vo/*.json` con `TAIL = 12.0` para dar espacio al cierre de **Pixeloide Studios**.

### Paso 3 — Generar y Preparar Assets 16-Bit (`assets/bgs/` y `assets/portraits/`)
1. Identifica los personajes clave y escenarios históricos/temáticos del guion.
2. Usa el subagente `image-generator` para crear:
   - **Retratos (`64x64`)**: pixel art 16-bit estilo SNES/Chrono Trigger, busto frontal/3-cuartos sobre fondo sólido uniforme para recorte automático.
   - **Fondos (`480x270`)**: escenarios 16-bit panorámicos sin texto incrustado y con iluminación atmosférica.
3. Procesa las imágenes con `python prep_assets.py` (escalado pixel-perfect, cuantización de paleta y eliminación de fondo en retratos).

### Paso 4 — Programar Capítulos (`engine/ch01.py` .. `engine/chNN.py`) y Traducciones (`engine/i18n.py`)
1. Cada módulo `chXX.py` debe exponer:
   - `scenes()`: lista de tuplas `(t_inicio, funcion_escena, funcion_camara_opcional)` sincronizadas al milisegundo con `TL.s(lid)`, `TL.e(lid)` y `TL.word(lid, "palabra")`.
   - `music(A)`: composición chiptune procedural acorde al tono emocional del capítulo.
   - `sfx(A)`: efectos de sonido sincronizados con las apariciones de ventanas, golpes, alertas o revelaciones.
2. **Reglas de Animación, Personajes y Ritmo Visual**:
   - **PROHIBIDO incluir `robot(...)` ("La Máquina")** en documentales cuya temática no sea Inteligencia Artificial.
   - **Personajes siempre vivos y en movimiento**: usa `walk(t, t0, t1, x0, x1)` para que los personajes entren caminando o se desplacen por la escena, interactúen entre sí (`look`, `facing`, `talk_v`), y cambien de postura (`arms="work"`, `"note"`, `"type"`, `"point"`, `"cheer"`, `"wave"`, `"shrug"`). Nunca dejes sprites estáticos durante toda la escena.
   - **Ritmo y Cámara**: incluye siempre funciones de cámara (`cam_push` y `cam_punch`) en `scenes()`, apariciones con rebote `pop(t, t0)`, sacudidas `shake()` en impactos/rechazos y revelado progresivo `reveal=` en titulares. No repitas un mismo recurso visual (como una línea/gusano en el piso) en todas las escenas.
3. En el último capítulo (`chNN.py`), define `T_END = TL.e("ultima_linea") + 2.8` para que `engine/outro.py` tome el relevo inmediatamente después.
4. Registra todas las cadenas en mayúsculas de los capítulos dentro de `engine/i18n.py` (`EN_MAP` y `PT_MAP`).

### Paso 5 — Verificación Automática de Márgenes y Cajas (QA Visual)
Antes de renderizar el video final, **siempre** verifica que ningún texto en `es`, `en` o `pt` se salga de su caja (`win` / `panel` / `banner`) ni de los márgenes seguros (`x in [4..476]`, `y in [4..266]`):
1. Usa `check_boxes` o renderiza hojas de contacto (`python engine/video.py sheet`) en los 3 idiomas.
2. Inspecciona visualmente las hojas con `read_file` y corrige cualquier texto largo ajustando el ancho de la caja, usando `text_wrap` o abreviando la traducción en `engine/i18n.py`.

### Paso 6 — Síntesis de Audio, Render Paralelo 1080p y Masterización (`-14 LUFS`)
1. Genera los stems y mezcla en español:
   ```powershell
   python engine/audio.py
   ```
2. Genera las mezclas multilingües (`EN` y `PT`) con ducking automático y cadencia natural:
   ```powershell
   python tools/mix_multilingual.py
   ```
3. Renderiza el video mudo en los 3 idiomas (`renders/video_mudo.mp4`, `renders/video_mudo_en.mp4`, `renders/video_mudo_pt.mp4`) en paralelo (8 workers):
   ```powershell
   python engine/video.py render 8
   python tools/render_multilingual.py
   ```
4. Une video + audio normalizado a `-14 LUFS` (estándar broadcast/YouTube) **sin quemar subtítulos en ningún `.mp4`** y guardando todos los archivos `.srt` dentro de `renders/subtitulos/`:
   ```powershell
   python tools/mux_all.py
   ```

### Paso 7 — Miniaturas 16:9 y Shorts Verticales 9:16 por Cada Capítulo (`renders/shorts/`)
1. **Regla obligatoria**: Además del documental 16:9 completo, **siempre** se debe generar por separado la versión vertical `9:16` (`1080x1920`, 30fps, sin subtítulos pegados) de **cada capítulo del episodio** (`Cap 00 Apertura` + `Cap 01` a `Cap 08`) en Español, Inglés y Portugués dentro de `renders/shorts/` (`Short_Cap00_Apertura_{LANG}.mp4`, `Short_Cap01_{LANG}.mp4`, ..., `Short_Cap08_{LANG}.mp4`), junto con sus `.srt` independientes en `renders/subtitulos/`:
   ```powershell
   python tools/make_thumbnails_and_shorts.py
   python tools/make_chapter_shorts.py
   ```
2. Limpia archivos temporales y deja todo versionado con `git commit`.
