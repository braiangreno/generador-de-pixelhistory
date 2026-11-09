# Pixeloide Studio Server — Plataforma de Producción Documental 16-Bit

Aplicación web + API REST auto-hospedable de **Pixeloide Studios** (`JUGAMOS EN SERIO.`) para transformar cualquier guion (en `.PDF`, `.TXT`, `.MD` o texto pegado) en un pack documental completo en Pixel Art 16-bit (`1920x1080` + Shorts `1080x1920`) en **Español**, **Inglés** y **Portugués**.

---

## Qué genera automáticamente con cada guion (Pipeline de 8 Etapas)

1. **Estructuración del Guion + Plan Visual 16-Bit + Traducciones (`ES` / `EN` / `PT`)**:
   - Divide el guion en capítulos y frases con pausas dramáticas (`script_full.json`, `script_full_en.json`, `script_full_pt.json`).
   - Diseña el plan de escenas (`production_plan.json`) y traduce todos los textos visibles en pantalla (`translations_map.json`).
2. **Locución Neuronal + Alineación Fonética (ElevenLabs `with-timestamps`)**:
   - **Español (Fijo)**: **Carlos Aguilar** (`8MeTTgXVwMEhRVfblXOj`, `speed=1.08`).
   - **Inglés (`EN`) y Portugués (`PT`)**: Velocidad natural `1.0x` con cálculo dinámico de ventana disponible (`avail_dur`) para que nunca suenen acelerados.
3. **Generación y Cuantización de Arte Pixel 16-Bit (`assets/bg/` y `assets/portraits/`)**:
   - Fondos panorámicos `480x270` cuantizados a 56 colores sin dithering y retratos `64x64` a 28 colores (vía Gemini Imagen 3 / OpenAI o motor procedural SNES).
4. **Escenas Animadas + Reglas Visuales Seguras + Cierre Oficial Pixeloide (`outro.py`)**:
   - Personajes siempre apoyados sobre el piso (`feet=260`) con escala proporcional.
   - Ventanas RPG (`window`) que miden el texto traducido y lo envuelven automáticamente para que ningún texto se salga de su caja.
   - Cierre obligatorio con la animación del logo **Pixeloide Studios** («Una P que es un play» + `JUGAMOS EN SERIO.`) y la placa de créditos (**Idea Original y Producción: Braian Greno** + stack de IA).
5. **Auditoría Visual y Hoja de Contacto (`frames/sheet_all.png`)**.
6. **Banda Sonora Chiptune Original + SFX + Ducking Automático (`audio.py` + `mix_multilingual.py`)**.
7. **Render 1080p Paralelo, Masterización `-14 LUFS` y Subtítulos `.SRT` Externos (`video.py` + `mux_all.py`)**:
   - **Ningún video lleva subtítulos quemados en la imagen**: todos los `.srt` se entregan como archivos separados junto a cada `.mp4`.
8. **Miniaturas de YouTube 16:9 (`1920x1080`) + Shorts Verticales 9:16 (`1080x1920`) + `YOUTUBE_PACK.md`**.

---

## Instalación en un Servidor (Linux VPS / Docker / Windows)

### Opción A — Docker Compose (Recomendado para cualquier servidor)
```bash
cp .env.example .env
# Edita .env con tu ELEVENLABS_API_KEY y GEMINI_API_KEY (o configúralas luego desde la Web UI)
docker compose up -d --build
```
El panel web queda disponible en `http://TU_IP_DEL_SERVER:8080`.

### Opción B — Instalación directa en Ubuntu / Debian (con servicio `systemd`)
```bash
chmod +x install_ubuntu.sh
./install_ubuntu.sh
```

### Opción C — Ejecución en Windows
```powershell
.\start_windows.ps1
```
Abre `http://localhost:8080` en tu navegador.

---

## Uso por API REST (enviar un guion desde terminal, n8n, Make o scripts)

Puedes disparar una producción completa enviando un archivo PDF/TXT o texto plano por `POST /api/projects`:

```bash
curl -X POST "http://localhost:8080/api/projects" \
  -F "title=LA HISTORIA DEL INTERNET" \
  -F "languages=es,en,pt" \
  -F "file=@Mi_Guion.pdf"
```

Consultar estado del proyecto:
```bash
curl "http://localhost:8080/api/projects/{project_id}"
```

Descargar el paquete completo (`.zip` con los `.mp4` en ES/EN/PT, los `.srt` separados, los Shorts `9:16`, las Miniaturas `16:9` y `YOUTUBE_PACK.md`):
```bash
curl -O -J "http://localhost:8080/api/projects/{project_id}/download-zip"
```
