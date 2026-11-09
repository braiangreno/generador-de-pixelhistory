# Guía del motor (para escribir un capítulo)

Proyecto: `C:\Users\Braian\.gemini\antigravity\scratch\historia_ia_pixel`
Video documental en **pixel art 16-bit** sobre la historia de la IA. Lienzo nativo **480x270**, se escala x4 a 1080p.
La locución (ElevenLabs, voz Carlos Aguilar) ya está generada; cada frase tiene id (`c2_01`, `c3_00`...) y alineación por palabra.

## Qué tenés que entregar
Un archivo `engine/chNN.py` (NN = 02..08) que **solo** use `from common import *` (y opcionalmente `math`, `numpy`, `PIL`).
**No edites ningún otro archivo** (common.py, core.py, sprites.py, ch01.py, audio.py, video.py, timeline.py son compartidos y otros agentes trabajan en paralelo).
Si necesitás un personaje que no está en el reparto, definí un `dict` local con el mismo formato que `sprites.CAST` y pasalo a `char()` en lugar de la clave.

El módulo debe exponer:
```python
def scenes():
    """[(inicio_s, fn(t)->Image RGBA 480x270, cam(t)->(zoom,cx,cy) o None), ...] ordenadas"""
def music(A):   # opcional pero recomendado: banda sonora chiptune de TU capítulo
def sfx(A):     # opcional pero recomendado: efectos sincronizados
```
- `t` es SIEMPRE tiempo global en segundos. Tu capítulo va de `TL.chapter_start(N)` a `chapter_end(N)`.
- La primera escena es la placa: `(TL.chapter_start(N) - 0.3, make_card(N, ["LÍNEA 1", "LÍNEA 2"], "1958 – 1969"), None)` (1 ó 2 líneas, MAYÚSCULAS). `snow=True` para capítulos de invierno. El sonido de la placa ya lo pone audio.py: no lo dupliques.
- La siguiente escena debe empezar poco antes de la primera frase del capítulo (`TL.s("cN_01") - 0.2`).
- Entre escenas se hace un fundido con dithering de 0.22 s automáticamente.

## Ritmo (MUY importante, el cliente lo pidió)
La narración es rápida. **Un cambio visual cada 2–4 s**: aparecen datos, tarjetas, personajes, objetos, golpes de zoom. Usá entre 4 y 7 escenas por capítulo.
Sincronizá todo con palabras: `TL.word("c2_03", "consciente")` → segundo exacto en que se dice la palabra (`end=True` para el final de la palabra; `occurrence=2` para la 2da aparición). `TL.s(id)` / `TL.e(id)` inicio/fin de frase. Las búsquedas ignoran tildes y mayúsculas. Si una palabra no existe, lanza KeyError: verificá con `python engine/timeline.py`.
Cámara: `cam_push(t, t0, t1, z0, z1, (cx0,cy0), (cx1,cy1))` (Ken Burns) y `cam_punch(t, [instantes], amp)` (golpe de zoom; sumalo a 1.0). Ej: `lambda t: (1.0 + cam_punch(t, [TL.word("c5_06","quince")], 0.08), 240, 135)`. Zoom máximo ~1.3.

## Escala de personajes (corrección del cliente: no deben verse chiquitos)
- Sprite base 28x52 px; con `scale=k` mide 28k x 52k. Pies en `(x, feet)`; la cabeza queda en `feet - 50*k`.
- **Interiores (habitaciones): `scale=3`**, pies en y≈262–268 (el personaje mide ~150 px, ~55% de la altura).
- Exteriores o grupos grandes: `scale=2`. Escenarios abstractos: 1–2.
- `robot(cv, x, feet, t, face=..., scale=k)` ("La Máquina", hilo conductor: aparece en cada capítulo). Caras: happy, talk, think, question, sad, off, heart; `frozen=True` (congelado).
- Muebles dibujados por código delante de personajes: `desk(cv, x0, x1, top, bottom)`; cosas chicas ampliadas: `scaled(cv, lambda im: terminal(im, 0, 0, t), 31, 27, x, y, k=2)`.

## API principal (`from common import *`)
- Fondos: `bg("nombre").copy()` (480x270). Disponibles (en assets/bg):
  bg_press_room_1958, bg_perceptron_lab, bg_mit_office_1969, bg_lab_1970s_empty, bg_british_office_1973,
  bg_corporate_1985, bg_ucsd_office_1986, bg_chess_stage_1997, bg_stanford_office_2009, bg_bedroom_2012,
  bg_seoul_match_2016, bg_google_office_2017, bg_living_room_2022, bg_nobel_stage_2024, bg_protein_lab_2024,
  y los del piloto: bg_office_1955, bg_turing_study, bg_dartmouth_summer, bg_classroom_1956.
  Mirá `frames/new_bgs.png` (tiene reglas de Y) para ubicar mesas/pisos. También podés crear fondos abstractos con `vgradient(top, bottom)`, `new_canvas(color)`, `STARS.draw(cv,t)`, `SNOW.draw(cv,t,density)`, `RAIN`, `CONF` (confeti).
- Personajes: `char(cv, key_o_dict, x, feet, t, scale=3, alpha=1, walk=fase|None, talk=talk_v(t, hablando), arms=..., mood=..., look=-1/0/1, facing=1/-1, sit=True, blink=...)`.
  arms: down, type, write, wave, point (derecha), point_l (izquierda), cheer, hold, think, shrug, cross. mood: neutral, happy, sad, worried.
  `x, ph = walk(t, t0, t1, x0, x1)` → posición y fase de caminata (pasar `walk=ph`). `silhouette(...)` = silueta negra.
- Claves del reparto (`S.CAST`): turing, mccarthy, minsky, shannon, rochester, solomonoff, selfridge, more, samuel, newell, simon, judge, human_b,
  rosenblatt, navy, reporter, papert, minsky70, lighthill, darpa, kengineer, rumelhart, hinton86, williams, kasparov, ibm_op, feifei,
  krizhevsky, sutskever, hinton12, leesedol, ajahuang, googler, user, hopfield, hinton24, hassabis, jumper, baker.
- Retratos 64x64 (assets/portraits): alan_turing, john_mccarthy, marvin_minsky, claude_shannon, nathaniel_rochester, la_maquina,
  frank_rosenblatt, navy_officer_1958, nyt_reporter_1958, seymour_papert, marvin_minsky_1970, james_lighthill, darpa_official_1974,
  expert_engineer_1985, david_rumelhart, geoffrey_hinton_1986, ronald_williams, garry_kasparov, deep_blue_operator, fei_fei_li,
  alex_krizhevsky, ilya_sutskever, geoffrey_hinton_2012, lee_sedol, aja_huang, google_researcher_2017, chatgpt_user_2022,
  john_hopfield, geoffrey_hinton_2024, demis_hassabis, john_jumper, david_baker.
  `portrait_card(cv, nombre, x, y)` (marco RPG 72x72). Patrón de presentación (ver `sc_turing` en ch01.py): retrato + ventana con NOMBRE (press 16) y subtítulo (silk 8).
- Texto: `draw_text(cv, txt, x, y, fname, size, color, align="left|center|right", gradient=GOLD_RAMP|ICE_RAMP|CYAN_RAMP|CREAM_RAMP, reveal=n_chars, alpha=, outline_w=)`.
  Fuentes: "press" (Press Start 2P; tamaños 8/16/24/32/48 — 8 px por carácter por cada 8 de tamaño), "silk"/"silkb" (Silkscreen 8). `text_size(txt, fname, size)`.
  **El texto en pantalla va en MAYÚSCULAS** (estilo del video), tildes OK.
- UI: `window(cv, x, y, w, h)`, `bubble(cv, txt, x_punta, y_punta, reveal=)`, `lower_third(cv, TITULO, sub, t, t0, t1, x=16, y=222)`, `bigyear(cv, "1958", cx, y, t, t0, size=48)` (año gigante dorado que cae), `quest_window(cv, [(txt,color),...], x, y, t, t0, w)`, `chapter_card` (no hace falta, usá make_card).
- Efectos: `pop(t, t0)` → (alpha, dy) rebote de aparición; `shake(t, t0)` → (dx,dy) + `offset_canvas(cv, dx, dy)`; `sparkle(cv,x,y,t)`; `spotlight(cv, cx, top, bottom, w_top, w_bot)` (devuelve nueva imagen); `grade(img, mul, add, sat, k)` (color: noche, invierno); `fade_to(cv, color, k)`; `dither_mix(a,b,k)`; `vignette(cv, 0.35)` (devuelve imagen nueva; ponelo al final); `draw_paper(cv,x,y,w,h)`; `scribble(...)`; `bulb`, `orb`, `terminal`, `draw_sun`, `draw_moon`; `bars70(cv, lit, t)` (fila de 70 años); easings `ease_out`, `ease_in_out`, `ease_out_back`, `prog(t,a,b)`.
- Colores: GOLD, CREAM, CYAN, NAVY, INK, GREY. Paleta del video: oscuro, dorado y cian.
- Dibujo libre: `ImageDraw.Draw(cv)` con colores RGBA (líneas de 1 px, sin antialias) — mantené el look pixel (nada de degradados suaves).

## Música y efectos (A = módulo audio)
`A.section(t0, t1, bpm, [("A","min"),("F","maj"),...], A.st_xxx)` estilos: st_mystery, st_build, st_bright, st_summer_lead, st_rain, st_puzzle, st_triumph, st_winter.
Tu música debe cubrir desde `TL.chapter_start(N) + 1.6` (la placa ya tiene sting) hasta `chapter_end(N)`. Cambiá de sección según el clima de cada parte.
Extras: `A.sting(t, [midi...])`, `A.note(A.music, t, A.midi_hz(m), dur, ...)`, `A.kick(A.music, t)`, `A.crash(A.music, t)`.
SFX: `A.whoosh(t)`, `A.pop_sfx(t, f0)`, `A.coin(t)`, `A.join_jingle(t)` (presentación de personaje), `A.text_blips(t0, n_chars, rate)` (texto que se tipea), `A.typewriter(t0,t1)`, `A.robot_beep(t)`, `A.freeze(t)`, `A.wind(t0,t1)`, `A.rain_amb(t0,t1)`, `A.chalk(t0,t1)`, `A.blip(t, f)`.
Volúmenes bajos (la voz manda): usá los valores por defecto.

## Cómo verificar (obligatorio)
- `python engine/timeline.py` → lista de frases con tiempos.
- `python engine/video.py sheet chNN` → `frames/sheet_chNN.png` (un fotograma por escena). Miralo con la herramienta de lectura de archivos.
- `python engine/video.py times 300.5 302.0 ...` → `frames/sheet_times.png` con instantes específicos (revisá momentos clave).
- `python -c "import sys; sys.path.insert(0,'engine'); import audio"` no hace falta; NO corras `video.py render` ni `audio.py` (los corre el coordinador).
- Iterá hasta que se vea bien: nada recortado fuera de pantalla, textos legibles sin superponerse, personajes grandes, buen ritmo.

Referencia de estilo completa: `engine/ch01.py` (apertura y capítulo 1 ya aprobados por el cliente).
