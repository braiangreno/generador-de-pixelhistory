---
name: pixeloide-video-engine
description: Produce documentales animados en pixel art 16-bit (estilo SNES / Chrono Trigger) de Pixeloide Studios a partir de un guion — video 16:9 1080p y Shorts 9:16 a pantalla completa por capítulo, en español, inglés y portugués, con locución de ElevenLabs sincronizada palabra por palabra, música chiptune procedural, subtítulos .srt externos, miniaturas y el cierre oficial de marca. Usala cuando el usuario entregue un guion, pida un documental, un video o un Short en pixel art, quiera rehacer una parte de un video existente, o necesite placas, zócalos o motion graphics de marca con Remotion.
---

# Pixeloide Video Engine — producción documental 16-bit

Todo vive en este repo (`generador-de-pixelhistory`). Rutas relativas a su raíz:

| Qué | Dónde |
|---|---|
| Motor base (se copia a cada proyecto) | `engine_template/` (`engine/`, `tools/`, `fonts/`, `ENGINE_GUIDE.md`) |
| Proyectos | `projects/<slug>/` (los 3 de referencia: `historia_ia_pixel`, `historia_videojuegos_pixel`, `historia_dune_pixel`) |
| Scripts del agente | `scripts/` (`verificar`, `nuevo_proyecto`, `voces`, `arte`, `producir`, `transcribir`) |
| Motion graphics de marca | `remotion-pixeloide/` (Remotion 4) |
| Panel web + API REST (opcional) | `app/` (`start_windows.ps1`) |
| Python | **siempre** `.venv\Scripts\python.exe` (Python 3.12 con Pillow, NumPy, faster-whisper) |

Ejecutá los scripts desde la raíz del repo, con `PYTHONUTF8=1` si vas a leer la salida (si no, las tildes salen rotas).

## 1. Reglas innegociables

**Marca y audio**
1. Narrador en español fijo: **Carlos Aguilar** (`8MeTTgXVwMEhRVfblXOj`, speed 1.08). No lo cambies salvo pedido explícito.
2. Inglés `pNInz6obpgDQGcFmaJgB` y portugués `Rxw6ylGPvxzn3gsuOExL` con `eleven_multilingual_v2` a **speed 1.0** (prohibido 1.15).
   La mezcla solo los comprime con `atempo` si no entran en su ventana (`tools/mix_multilingual.py` ya lo hace).
3. **Todo texto en pantalla traducido** a EN y PT (títulos, placas, tarjetas, globos, sellos, créditos).
4. **Nunca subtítulos quemados**: los `.srt` van aparte en `renders/subtitulos/`.
5. **Cierre oficial obligatorio** (`engine/outro.py`, 12 s): logo «Una P que es un play», claim `JUGAMOS EN SERIO.`
   y créditos (Idea original y Producción: **Braian Greno** + stack de IA). No se saca ni se tapa.
6. Sin el robot «La Máquina» salvo en documentales de IA. Sin loops sin sentido. Coreografía atada a las palabras (`TL.word`).

**Costos, claves y permisos**
- ElevenLabs cobra por carácter. Antes de generar voces corré `voces.py --estimar`, decile al usuario cuántos caracteres
  son y **esperá su OK** (salvo que ya lo haya autorizado en el pedido). Lo mismo con imágenes por API (Gemini/OpenAI):
  `arte.py --prompts` dice cuántas faltan.
- Las claves van en `.env` en la raíz del repo (`ELEVENLABS_API_KEY`, `GEMINI_API_KEY`, `OPENAI_API_KEY`). Las carga el
  usuario con **doble clic en `CLAVES.bat`** (las pide sin mostrarlas, las prueba y dice qué modelos de imagen tiene).
  **Nunca leas, muestres ni copies** `.env` ni `data/settings.json`, y no le pidas que las pegue en el chat;
  `scripts\claves.py --probar` y `verificar.py` dicen si andan sin mostrarlas.
- **El arte del video final es generado con IA** (Nano Banana o GPT Image), con retratos que se parecen a las personas
  reales. El procedural es solo para borradores: deja `assets/ARTE_PROVISORIO.txt` y `producir.py` avisa.
- `voces.py --prueba` es una voz sintética de prueba: sirve para armar y revisar borradores, **nunca para entregar**
  (deja `audio/VOZ_DE_PRUEBA.txt` y `producir.py` avisa en grande mientras exista).
- No hagas `git commit`/`push` sin que el usuario lo pida (los proyectos usan Git LFS para mp4/wav/mp3).

## 2. Flujo desde un guion nuevo

### Paso 0 — Entorno
`.venv\Scripts\python.exe scripts\verificar.py` → si falta algo imprescindible, `INSTALAR.bat` (doble clic) lo instala.
`.venv\Scripts\python.exe scripts\claves.py --probar` → qué claves andan. Si faltan, pedile al usuario `CLAVES.bat`.

### Paso 1 — Proyecto
`.venv\Scripts\python.exe scripts\nuevo_proyecto.py "Título" --guion <archivo .txt/.md/.pdf>` (o pegá el texto en
`projects/<slug>/guion.txt`). Imprime `SLUG=<slug>`: usalo en todos los pasos.

### Paso 2 — Guion estructurado (lo escribís vos, en el proyecto)
`script_full.json` (ES), `script_full_en.json` y `script_full_pt.json`: listas con los **mismos** `id`, `ch` y `pause`.
```json
[{"id": "s01", "ch": 0, "pause": 0.35, "speak": "Mil novecientos cincuenta y siete. Florence, Oregón.", "sub": "1957. Florence, Oregón."},
 {"id": "c1_00", "ch": 1, "pause": 0.35, "speak": "Capítulo uno. El artículo que nunca terminó.", "sub": "CAPÍTULO 1 — EL ARTÍCULO QUE NUNCA TERMINÓ"},
 {"id": "c1_01", "ch": 1, "pause": 0.35, "speak": "...", "sub": "..."}]
```
- `s01, s02...` = apertura (capítulo 0). `cN_00` = placa del capítulo N ("Capítulo N. Título."). `cN_01...` = frases.
- `speak` es lo que lee la voz: fechas, números y siglas **escritos como se dicen** en ese idioma. `sub` es el texto limpio.
- Frases de 8 a 25 palabras. `pause` después de la frase: 0.35 normal, 0.65 cierre de idea, 1.0–1.1 fin de capítulo.
- Respetá el guion del usuario: dividilo y pulilo para voz, pero no inventes datos. Si algo es dudoso, preguntá.
- Traducciones EN/PT con tono documental natural (no literal).

### Paso 3 — Plan de producción (`production_plan.json`)
```json
{"title": "LA HISTORIA DE DUNE", "subtitle": "DE UN ARTÍCULO A UNA SAGA", "slug": "Historia_Dune_PixelArt",
 "year_start": "1957", "year_end": "2026", "accent": [255, 195, 85],
 "titles": {"es": "...", "en": "...", "pt": "..."}, "subtitles": {"es": "...", "en": "...", "pt": "..."},
 "backgrounds": [{"name": "bg_dunas_1957", "theme": "desert",
                  "prompt": "coastal sand dunes of Florence, Oregon in 1957 swallowing a road, pine trees, warm afternoon light"}],
 "portraits": [{"name": "frank_herbert", "persona": "Frank Herbert",
                "quien": "American journalist and science-fiction writer, author of Dune", "anio": 1957,
                "rasgos": "short dark beard and mustache, receding hair, horn-rimmed glasses, tweed jacket"}],
 "creditos": {"imagenes": "NANO BANANA / GPT IMAGE"},
 "chapter_music": {"0": "mystery", "1": "build", "2": "puzzle"},
 "scenes": [ ...escenas automáticas (opcional, ver abajo)... ],
 "translations_map": {"en": {"TEXTO EN PANTALLA": "SCREEN TEXT"}, "pt": {"TEXTO EN PANTALLA": "TEXTO NA TELA"}}}
```
- `slug` = nombre de los masters (`<slug>_ES.mp4`). `titles`/`subtitles`/`year_*` alimentan miniaturas y Shorts
  (`titles_2lines: {"es": ["LÍNEA 1", "LÍNEA 2"]}` si el título largo se corta mal en la tarjeta vertical).
- Retratos = **personas reales de la historia**: `persona` (nombre real), `quien` (por qué es conocido), `anio` (cuándo
  aparece) y `rasgos` (pelo, barba, anteojos, ropa de esa época), en inglés: con eso se arma el prompt de parecido.
  Fondos: lugar y año concretos, en inglés. `creditos.imagenes` = qué IA hizo el arte (sale en los créditos finales).
- Música: mystery, build, bright, summer, rain, puzzle, triumph, winter.
- `"robot": true` solo en documentales de IA: sin eso, las placas automáticas (title_card, chapter_card) no dibujan al robot.
- `scripts\estado.py <slug>` revisa el plan contra el motor del proyecto (frases, fondos, retratos, presets y textos en pantalla sin
  traducir) y dice qué falta para entregar (`--json` para leerlo desde otro programa).
- **Escenas automáticas** (`scenes`): sirven para un borrador completo rápido y para capítulos simples. Cada una:
  `line_id`, `end_line`, `layout` (`title_card`, `chapter_card`, `dialogue_scene`, `lab_scene`, `split_vs`, `data_bars`,
  `living_room_tv`, `calendar_stamp`), `bg`, `header`, `subheader`, `year`, `portrait`, `cards` (`title` + `lines`, máx. ~32
  letras por línea), `characters` (`preset`, `x`, `feet` 260–264, `scale` 2 o 3, `arms`, `mood`, `bubble`), `lower_third`
  (`title`, `sub`), `stamp`, `weather` (rain/snow/confetti), `bars` (para data_bars), `chapter`/`title_lines`/`years` (placas).
  Presets de personaje: inge, prof, estudiante, ejecutivo, mujer_ejecutiva, chica, abuela, nieto, padre, periodista,
  cientifica, militar.
- Un capítulo con `engine/chNN.py` escrito a mano **reemplaza** sus escenas automáticas (el resto sigue saliendo del plan).

### Paso 4 — Voces
1. `.venv\Scripts\python.exe scripts\voces.py <slug> --estimar` → caracteres por idioma → **pedí OK**.
2. `.venv\Scripts\python.exe scripts\voces.py <slug>` → `audio/vo*/<id>.mp3` + `.json` (alineación por carácter).
   Sin `ELEVENLABS_API_KEY`, pedile al usuario que la cargue con `CLAVES.bat`. Mientras tanto: `--prueba` (nunca pisa
   una voz real, ni con `--forzar`). `--huella`/`--max-caracteres` atan una corrida a lo que se estimó (los usa Agent 009).
3. Si las voces vienen de otro lado (grabación, otro TTS): dejá los mp3 como `audio/vo/<id>.mp3` y corré
   `scripts\transcribir.py <slug>`: Whisper `large-v3-turbo` en la RTX 4090 (9 frases en ~8 s; sin GPU usa la CPU).

### Paso 5 — Arte con IA (fondos 480x270 y retratos 64x64 de las personas reales)
Cada `name` del plan termina en `assets/bg/<name>.png` / `assets/portraits/<name>.png`, convertido a pixel art del motor
(56 colores los fondos, 28 los retratos, sin difuminado). Con varias imágenes, delegalo al subagente **`pixeloide-arte`**
(en paralelo con los capítulos) pasándole el proyecto y si tiene OK de gasto.
1. `scripts\arte.py <slug> --prompts` → cuántas faltan y sus prompts → **pedí OK** del gasto.
2. Retratos: `scripts\arte.py <slug> --comparar --solo <retratos>` genera cada uno con **Nano Banana** (Gemini) y con
   **GPT Image** (OpenAI) → mirá `frames/arte_candidatos.png` → `scripts\arte.py <slug> --elegir <nombre>=nanobanana|gptimage`
   con el que más se parece a la persona real. Fondos: `scripts\arte.py <slug>` (Nano Banana primero, GPT Image si falla).
3. Persona poco conocida (sale una cara genérica): foto de referencia de uso libre en `gen/referencias/<nombre>.jpg` y
   rehacer con `--solo <nombre> --forzar`: se le pasa al modelo para clavar el parecido.
4. Sin claves pero con un conector de imágenes en la sesión (Higgsfield: `nano_banana_2`, `gpt_image_2_6`): generá con
   los prompts de `--prompts` y bajalas con `scripts\arte.py <slug> --traer <nombre>=<url>` (las procesa sola).
5. Mirá cada PNG ampliado: parecido y edad correctos, época del fondo, piso libre abajo (y≈260), sin texto ni carteles.
Modelos por defecto: `gemini-3.1-flash-image` (Nano Banana 2) y `gpt-image-2`, con respaldos si la cuenta no los tiene
(se cambian con `GEMINI_IMAGE_MODEL` / `OPENAI_IMAGE_MODEL` en `.env`). Solo para borradores: `--motor procedural`.

### Paso 6 — Borrador y revisión
`.venv\Scripts\python.exe scripts\producir.py <slug> --pasos timeline,hoja`
→ `frames/sheet_all.png`, `sheet_all_en.png`, `sheet_all_pt.png` (16:9) y `sheet_v_all*.png` (9:16). **Mirá las hojas.**

### Paso 7 — Capítulos a mano (la calidad de los documentales de referencia)
Para cada capítulo, un `engine/chNN.py` según `ENGINE_GUIDE.md` del proyecto (apertura `s..` en `ch00.py`).
- Con varios capítulos, lanzá **un subagente `pixeloide-capitulo` por capítulo, en paralelo** (no tocan archivos
  compartidos; cada uno escribe su `chNN.py` y sus traducciones en `translations/chNN.json`). Pasale: proyecto,
  capítulo, ids de sus frases, fondos y retratos disponibles, y la idea visual de cada escena.
- Referencia de estilo aprobada: `projects/historia_dune_pixel/engine/ch01.py` … `ch08.py` y `projects/historia_ia_pixel/engine/ch01.py`
  (ojo: el `sprites.py` de Dune tiene campos propios; en proyectos nuevos usá el formato de `ENGINE_GUIDE.md`).
- Después revisá vos: `producir.py <slug> --pasos hoja --capitulo chNN` y corregí lo que haga falta.

### Paso 8 — Control de calidad (antes del render final)
- Ningún texto fuera de su caja ni de los márgenes (x 4–476, y 4–266) en **ES, EN y PT**; en 9:16 nada cortado.
- Personajes grandes y apoyados en el piso; un cambio visual cada 2–4 s; nada que se mueva sin motivo.
- Palabras de sincronización existentes (la hoja corre en modo estricto: si falta una palabra, falla con su nombre).
- Fondos y retratos generados con IA (sin `assets/ARTE_PROVISORIO.txt`) y voces reales (sin `audio/VOZ_DE_PRUEBA.txt`).

### Paso 9 — Producción final
`.venv\Scripts\python.exe scripts\producir.py <slug> --pasos audio,video,master,srt,miniaturas,shorts --workers 16`
(o `--pasos todo`). En esta PC (32 núcleos) 1 minuto de video 1080p tarda ~25 s por idioma.

### Paso 10 — Entrega
- `renders/<slug>_ES|EN|PT.mp4` (1920x1080, 30 fps, audio -14 LUFS), `renders/subtitulos/*.srt`,
  `renders/Miniatura_YouTube_*.png`, `renders/Short_Vertical_*.mp4` y `renders/shorts/Short_CapNN_*.mp4` (+ sus `.srt`).
- Escribí `YOUTUBE_PACK.md` (títulos, descripciones con capítulos y tiempos, tags; ES/EN/PT; créditos: Idea original y
  Producción Braian Greno, narración Carlos Aguilar, "Subtítulos .srt incluidos").
- Verificá con `ffprobe` duraciones y resolución, y mirá al menos un cuadro de cada master y de un Short.
- Contale al usuario qué se entregó, dónde, y qué no se pudo verificar.

## 3. Cambios puntuales
- Rehacer frases: `voces.py <slug> --solo c3_04,c3_05 --forzar` → después `producir.py --pasos hoja` (revisar
  sincronía) y `audio,video,master,srt,miniaturas,shorts`.
- Cambiar una escena: editar `chNN.py` → `hoja --capitulo chNN` → render.
- Un solo idioma: `--idiomas es`.
- Instantes concretos: en la carpeta del proyecto, `..\..\.venv\Scripts\python.exe engine\video.py times 12.5 30.2`.

## 4. Remotion (motion graphics de marca)
`remotion-pixeloide/` tiene composiciones con la marca (fuentes Press Start 2P / Silkscreen, colores Ink, Cyan, Magenta,
Paper e isotipo exportado del motor):
- `PixeloideTitulo` (1920x1080) y `PixeloideTituloVertical` (1080x1920): placa con campo de píxeles, título que se tipea y claim
  (props: `titulo`, `subtitulo`, `idioma` es|en|pt).
- `PixeloideZocalo` (1920x1080, **fondo transparente**): zócalo RPG para usar encima de cualquier video
  (props: `nombre`, `rol`, `acento` cyan|dorado).
Comandos (en `remotion-pixeloide/`):
- Vista previa interactiva: `npm run dev` (Remotion Studio).
- MP4: `npx remotion render PixeloideTitulo out/titulo.mp4 --props='{"titulo":"...","subtitulo":"...","idioma":"es"}'`
- Con transparencia para editores: `npx remotion render PixeloideZocalo out/zocalo.mov --codec=prores --prores-profile=4444 --pixel-format=yuva444p10le --image-format=png`
- Un cuadro: `npx remotion still PixeloideTitulo out/cuadro.png --frame=100`
Usalo para: intros/placas, zócalos, end screens, promos y anuncios, piezas para redes que no sean pixel art puro.
Antes de escribir código de Remotion cargá la skill `remotion-best-practices`. Licencia: gratis para personas y empresas de
hasta 3 personas; empresas más grandes necesitan licencia de Remotion.

## 5. Panel web (opcional)
`start_windows.ps1` levanta Pixeloide Studio Server en http://localhost:8080 (solo en esta PC): subir un guion y que el
pipeline automático haga todo con escenas del plan. No tiene usuarios ni contraseña: no lo abras a internet sin ponerle
autenticación adelante.

## 6. Problemas comunes
| Síntoma | Qué hacer |
|---|---|
| Tildes rotas en la consola | `PYTHONUTF8=1` |
| `KeyError: TL.word: no encuentro ...` | La palabra no está en el `speak` de esa frase (los números van escritos en letras) |
| Fondo azul liso con una línea | Falta `assets/bg/<name>.png` (es el provisorio del motor) |
| `ElevenLabs rechazó la clave (401)` / sin créditos | Que el usuario revise la clave o el plan |
| Render se corta con muchos workers | Bajar `--workers` (cada encoder ya usa pocos hilos) |
| GPT Image: HTTP 403 "organization must be verified" | El usuario verifica la organización en platform.openai.com; mientras, Nano Banana |
| Nano Banana "no devolvió imagen" (filtro) | Reformular sin pedir "foto"/"realista", o probar GPT Image (`--motor openai`) |
| Retrato con cara genérica | La persona es poco conocida: foto de referencia en `gen/referencias/<nombre>.jpg` |
| Whisper "usa la CPU" | Faltan cuBLAS/cuDNN: `INSTALAR.bat` los instala si hay placa NVIDIA |
| Shorts con el título equivocado | Completar `titles` (y `titles_2lines`) en `production_plan.json` |
