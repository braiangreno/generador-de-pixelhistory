# Pixeloide Studios — generador de documentales pixel art 16-bit

Este repo es el motor y el agente de producción de Pixeloide Studios (`JUGAMOS EN SERIO.`): convierte un guion en un
documental 16:9 1080p + Shorts 9:16 en español, inglés y portugués.

- **Para producir o modificar un video seguí la skill `pixeloide-video-engine`** (`.claude/skills/pixeloide-video-engine/SKILL.md`).
  Subagentes: `pixeloide-capitulo` (un capítulo animado; uno por capítulo, en paralelo) y `pixeloide-arte`
  (fondos y retratos con IA de las personas reales, con Nano Banana y GPT Image).
- Python: siempre `.venv\Scripts\python.exe` (Python 3.12). Si falta, `INSTALAR.bat`. Chequeo: `scripts\verificar.py`.
- Proyecto nuevo = `scripts\nuevo_proyecto.py`; nunca edites `engine_template/` para un video puntual (es la base de todos).
  Si arreglás un error del motor, arreglalo en `engine_template/` y copialo a los proyectos que lo necesiten.
- Claves: viven en `.env`; el usuario las carga con `CLAVES.bat`. No leas, muestres ni copies `.env` ni
  `data/settings.json`, ni pidas claves en el chat. Para saber si andan: `scripts\claves.py --probar`.
- El arte del video final se genera con IA (Gemini/OpenAI, `scripts\arte.py`); el procedural es solo borrador.
- ElevenLabs y las APIs de imágenes cobran: estimá (`voces.py --estimar`, `arte.py --prompts`) y pedí OK antes de gastar.
- No hagas commit ni push sin que el usuario lo pida. Los medios (mp4/wav/mp3/gif) van por Git LFS.
- Respondé en español (el usuario es de Argentina/Uruguay y escribe informal).
