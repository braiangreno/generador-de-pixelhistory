# Historia de la Inteligencia Artificial · Pixel Art 16-Bit

Documental animado en pixel art estilo 16-bit (SNES) que recorre los más de 70 años de historia de la inteligencia artificial, desde la propuesta fundacional de Alan Turing y el taller de Dartmouth (1956) hasta el nacimiento del Perceptrón, los dos inviernos de la IA, el surgimiento del Deep Learning, AlphaGo, los Transformers, ChatGPT y los Premios Nobel de 2024 (AlphaFold y Hopfield/Hinton).

---

## 🎬 Características Principales

- **Estética 16-Bit Auténtica:**
  - Lienzo nativo de renderizado a **480x270** escalado con interpolación *Nearest Neighbor* a resolución **1080p** (1920x1080) a 30 FPS.
  - Tipografías bitmap pixel art (`Press Start 2P` y `Silkscreen`) con composición procedural de acentos y diacríticos (agudos, graves, circunflejos y tildes).
  - Partículas, transiciones con dithering Bayer ordenado, iluminación procedural, sprites animados y ventanas estilo JRPG retro.
- **Traducción y Localización Integral (3 Idiomas):**
  - **Español (ES)**, **Inglés (EN)** y **Portugués (PT)**.
  - No solo las voces y los subtítulos están localizados: **el 100% de los textos en escena** (títulos, placas de capítulos, diarios, pizarrones, terminales CRT, globos de diálogo y la interfaz de ChatGPT) están traducidos y adaptados dinámicamente a sus márgenes.
- **Banda Sonora y Diseño de Sonido Procedural:**
  - Música chiptune / FM sintetizada por software en Python con `NumPy` y `SciPy` (ondas cuadradas, sierra, triángulos y percusión de ruido blanco).
  - Efectos de sonido retro integrados (blips, whooshes, máquinas de escribir, golpes, monedas y alertas).
  - Locución sintetizada con ElevenLabs, alineada fonéticamente con Whisper y normalizada a **-14 LUFS** (estándar broadcast/YouTube).

---

## 📁 Estructura del Proyecto

```text
historia_ia_pixel/
├── assets/             # Fondos pixel art (20+ escenarios) y retratos de figuras históricas
│   ├── bg/             # Oficinas, laboratorios, salas de prensa, auditorios
│   └── portraits/      # Turing, Rosenblatt, Minsky, Hinton, Hassabis, Altman, etc.
├── audio/              # Master mixes, stems y archivos de locución por idioma
│   ├── mix.wav         # Mezcla maestra Español (-14 LUFS)
│   ├── mix_en.wav      # Mezcla maestra Inglés (-14 LUFS)
│   ├── mix_pt.wav      # Mezcla maestra Portugués (-14 LUFS)
│   ├── vo/             # Clips de voz por frase (Español)
│   ├── vo_en/          # Clips de voz por frase (Inglés)
│   └── vo_pt/          # Clips de voz por frase (Portugués)
├── engine/             # Motor gráfico y lógico en Python
│   ├── core.py         # Lienzo, dibujo de texto pixel, dithering, ventanas RPG
│   ├── common.py       # Sprites base, cámaras Ken Burns, placas de capítulo
│   ├── sprites.py      # Generador procedural de personajes y robots
│   ├── timeline.py     # Línea de tiempo precisa vinculada a las locuciones
│   ├── i18n.py         # Diccionarios y motor de traducción EN / PT / ES
│   ├── video.py        # Compilador y renderizador multiproceso de video
│   ├── ch01.py - ch08  # Módulos de escena para cada capítulo (1 al 8)
│   └── outro.py        # Cierre animado oficial de Pixeloide Studios + Créditos
├── .agents/skills/     # Skill local de Antigravity (pixeloide-video-engine)
├── fonts/              # Tipografías TTF bitmap (Press Start 2P, Silkscreen)
├── frames/             # Hojas de contacto y capturas de verificación de calidad
├── renders/            # Masters finales de video y subtítulos
│   ├── Historia_IA_PixelArt_ES.mp4 / .srt
│   ├── Historia_IA_PixelArt_EN.mp4 / .srt
│   ├── Historia_IA_PixelArt_PT.mp4 / .srt
│   └── video_mudo[_en|_pt].mp4
├── tools/              # Scripts de automatización y pipeline
│   ├── new_project.py             # Generador de nuevos proyectos desde el motor
│   ├── batch_tts_multilingual.py  # Síntesis TTS multilingüe (cadencia natural 1.0x)
│   ├── mix_multilingual.py        # Mezcla y ducking con cadencia naturalizada
│   ├── render_multilingual.py     # Render paralelo 1080p para EN y PT
│   ├── update_outro_video.py      # Actualización incremental de la cola/outro
│   └── mux_all.py                 # Muxing y masterización a -14 LUFS con FFmpeg
├── guion.txt           # Guion maestro del documental
└── script_full*.json   # Estructuras de datos de subtítulos y timings (ES, EN, PT)
```

---

## 🚀 Requisitos e Instalación

1. **Python 3.10+**
2. **Dependencias de Python:**
   ```bash
   pip install pillow numpy scipy elevenlabs openai-whisper
   ```
3. **FFmpeg** instalado y disponible en el `PATH` del sistema.
4. *(Opcional para regenerar voces)* Archivo `.env` basado en `.env.example` con tu clave de ElevenLabs:
   ```env
   ELEVENLABS_API_KEY=tu_api_key_aqui
   ```

---

## 🛠️ Comandos Principales

### 1. Renderizar Hojas de Contacto (Vista Previa Rápida)
Genera una grilla con capturas de todas las escenas o de un capítulo específico:
```bash
python engine/video.py sheet         # Todas las escenas
python engine/video.py sheet ch02    # Solo capítulo 2
```

### 2. Renderizar Video Mudo (Multiproceso)
Compila los fotogramas en paralelo utilizando 8 núcleos de CPU:
```bash
# Español:
python engine/video.py render 8

# Inglés:
$env:VIDEO_LANG="en"; python engine/video.py render 8

# Portugués:
$env:VIDEO_LANG="pt"; python engine/video.py render 8
```

### 3. Muxing y Entrega Final
Une los videos mudos renderizados con sus respectivas pistas de audio normalizadas y subtítulos:
```bash
python tools/mux_all.py
```

Los masters finales resultantes se almacenan en `renders/`:
- `Historia_IA_PixelArt_ES.mp4`
- `Historia_IA_PixelArt_EN.mp4`
- `Historia_IA_PixelArt_PT.mp4`
