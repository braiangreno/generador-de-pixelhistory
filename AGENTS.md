# Instrucciones para agentes (Codex, Gemini/Antigravity, Claude)

Este repo produce documentales pixel art 16-bit de Pixeloide Studios a partir de un guion.

1. Leé primero `.claude/skills/pixeloide-video-engine/SKILL.md` (copia idéntica en `skills/pixeloide-video-engine/SKILL.md`):
   ahí está el flujo completo, las reglas de marca y los comandos.
2. Para escribir un capítulo animado: `projects/<slug>/ENGINE_GUIDE.md` y `.claude/agents/pixeloide-capitulo.md`.
3. Python: `.venv\Scripts\python.exe` (crealo con `INSTALAR.bat`). Chequeo del entorno: `scripts\verificar.py`.
4. No leas ni muestres `.env` ni `data/settings.json` (claves). ElevenLabs y las APIs de imágenes cobran: pedí OK antes.
