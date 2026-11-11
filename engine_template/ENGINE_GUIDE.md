# Guía del motor: cómo escribir un capítulo (`engine/chNN.py`)

Documental en **pixel art 16-bit**. Lienzo nativo **480x270**, escalado x4 (vecino más cercano) a 1920x1080 a 30 fps.
La línea de tiempo (`TL`) sale de `script_full.json` + las voces en `audio/vo/<id>.mp3|.json` (alineación por carácter).
Cada frase tiene un id: `s01..` (apertura, sin capítulo), `c1_00` (placa del capítulo 1), `c1_01`, `c1_02`...

## Qué entregás
Un archivo `engine/chNN.py` (NN = 01, 02...) que **solo** use `from common import *` (y si hace falta `math`, `numpy`, `PIL`).
**No edites ningún otro archivo** (core, common, sprites, timeline, audio, video, vertical, outro, i18n son compartidos;
puede haber otros capítulos escribiéndose en paralelo). Para un personaje propio, definí un `dict` local (ver Personajes).

```python
from common import *

def scenes():
    """[(inicio_s, fn(t) -> Image RGBA 480x270, cam(t) -> (zoom, cx, cy) | None), ...] en orden"""

def music(A):   # banda sonora chiptune del capítulo (recomendado)
def sfx(A):     # efectos sincronizados (recomendado)
```
- `t` es SIEMPRE tiempo global en segundos. Tu capítulo va de `TL.chapter_start(N)` a `chapter_end(N)`.
- Primera escena = la placa: `(TL.chapter_start(N) - 0.3, make_card(N, ["LÍNEA 1", "LÍNEA 2"], "1957 – 1965"), None)`
  (1 o 2 líneas en MAYÚSCULAS; `snow=True` para capítulos de invierno). El sonido de la placa lo pone `audio.py`.
- La escena siguiente empieza un poco antes de la primera frase: `TL.s("cN_01") - 0.2`.
- Entre escenas hay un fundido con dithering de 0.22 s automático.
- **Último capítulo**: dejá de dibujar en `T_END = TL.e("<última frase>") + 2.8`; ahí entra solo `engine/outro.py`
  (logo «Una P que es un play» + créditos de Pixeloide Studios). Nunca lo saques ni lo tapes.
- Si el guion tiene apertura (`s01..`), esas escenas van en `ch00.py` con la misma estructura.

## Ritmo y coreografía (lo que más se nota)
- **Un cambio visual cada 2–4 s**: datos, tarjetas, personajes que entran, objetos, golpes de zoom. 4 a 7 escenas por capítulo.
- **Todo se dispara con las palabras del narrador**: `TL.word("c2_03", "consciente")` = segundo exacto en que se dice.
  `end=True` = final de la palabra; `occurrence=2` = la segunda vez. `TL.s(id)` / `TL.e(id)` = inicio/fin de la frase.
  La búsqueda ignora tildes y mayúsculas y usa el texto **hablado** (`speak`): si el guion dice
  "mil novecientos cincuenta y siete", buscá "novecientos", no "1957".
  En las hojas de revisión (`producir.py --pasos hoja`) una palabra que no existe **corta con error**: corregila.
- Caminatas: `x, ph = walk(t, t0, t1, x0, x1)` **una sola vez** para entrar o ir a un punto (pasá `walk=ph`).
  Gestos (`arms=`) y apariciones (`pop(t, t_palabra)`) en el instante de la palabra.
- **Prohibido**: loops sin sentido (caminar o rebotar todo el tiempo, brazos girando), repetir el mismo recurso en todas
  las escenas, y el robot «La Máquina» (`robot()` no dibuja nada salvo en el documental de IA).
- Cámara en cada escena: `cam_push(t, t0, t1, z0, z1, (cx0, cy0), (cx1, cy1))` (Ken Burns) y golpes
  `cam_punch(t, [instantes], amp)` sumados a 1.0. Ej.: `lambda t: (1.0 + cam_punch(t, [TL.word("c5_06", "quince")], 0.08), 240, 135)`.
  Zoom máximo ~1.3. `shake(t, t0)` + `offset_canvas(cv, dx, dy)` en impactos. Titulares con `reveal=` (se tipean).

## Personajes
`char(cv, clave_o_dict, x, feet, t, scale=3, alpha=1, walk=fase|None, talk=talk_v(t, hablando), arms=..., mood=..., look=-1/0/1, facing=1/-1, sit=True)`
- Pies en `(x, feet)`; el piso de los fondos está en **feet ≈ 260** (interiores 262–268). Sprite base 28x52: con `scale=k` mide 28k x 52k.
- **Interiores: `scale=3`** (~55% del alto). Exteriores o grupos: `scale=2`. Nunca chiquitos.
- `arms`: down, type, write, wave, point (derecha), point_l (izquierda), cheer, hold, think, shrug, cross.
  `mood`: neutral, happy, sad, worried. `silhouette(...)` = silueta negra.
- Reparto genérico (`S.CAST`): inge, prof, estudiante, ejecutivo, mujer_ejecutiva, chica, abuela, nieto, padre,
  periodista, cientifica, militar (y los históricos del documental de IA).
- Personaje propio: un dict con el formato del reparto, por ejemplo
  `HERBERT = dict(name="Frank Herbert", skin=S.SKIN["fair"], hair=S.C("6a5a4a"), hair_style="recede", beard="short", glasses="black", top="blazer", top_color=S.C("6a4a34"), shirt=S.C("e8e0d0"), pants=S.C("3a3028"))`.
  Pieles: light, fair, tan, olive, brown, asian. Pelo: bald, bangs, bun, crew, curly, fringe, long, recede, short, side, slick, wavy.
  Ropa (`top`): shirt, tshirt, sweater, hoodie, turtleneck, vest, suit, blazer, labcoat, trench, uniform.
  Extras: glasses (black/round/wire), tie, beard, mustache, hat (fedora/navy), skirt + skirt_color.
- Muebles por código delante del personaje: `desk(cv, x0, x1, top, bottom)`; objetos chicos ampliados: `scaled(cv, fn, w, h, x, y, k=2)`.

## Fondos, retratos y texto
- Fondos: `bg("nombre").copy()` (480x270, de `assets/bg/`). Retratos 64x64: `portrait_card(cv, "nombre", x, y)` (marco RPG 72x72).
  Si falta el archivo se dibuja un fondo provisorio: el video final tiene que tener todos los PNG reales.
  Abstractos: `vgradient(arriba, abajo)`, `new_canvas(color)`, `STARS.draw(cv, t)`, `SNOW.draw(cv, t, densidad)`, `RAIN`, `CONF`.
- Texto: `draw_text(cv, txt, x, y, "press"|"silk"|"silkb", tamaño, color, align="left|center|right", gradient=GOLD_RAMP|CYAN_RAMP|CREAM_RAMP, reveal=n, alpha=, outline_w=)`.
  "press" en 8/16/24/32/48 (8 px por letra cada 8 de tamaño); "silk"/"silkb" en 8. `text_size(txt, fuente, tamaño)`, `draw_text_wrap(...)`.
  **Texto en pantalla en MAYÚSCULAS** (tildes OK). Márgenes seguros: x 4–476, y 4–266. Nada se sale de su ventana.
- UI: `window(cv, x, y, w, h)`, `bubble(cv, txt, x_punta, y_punta, reveal=)`, `lower_third(cv, TÍTULO, sub, t, t0, t1)`,
  `bigyear(cv, "1965", cx, y, t, t0, size=48)`, `quest_window(cv, [(txt, color), ...], x, y, t, t0, w)`.
- **Traducción**: cada texto en mayúsculas que aparece en pantalla va a `translations_map.json` (`"en": {...}, "pt": {...}`).
  Revisá las hojas `_en` y `_pt`: si una traducción no entra, achicala ahí o ensanchá la ventana.
- Efectos: `pop(t, t0)` → (alpha, dy); `sparkle`; `spotlight(cv, cx, top, bottom, w_top, w_bot)`; `grade(img, mul, add, sat, k)`;
  `fade_to`; `dither_mix(a, b, k)`; `vignette(cv, 0.3)` (devuelve imagen nueva, ponelo al final); `draw_paper`, `scribble`,
  `bulb`, `orb`, `terminal`, `draw_sun`, `draw_moon`; easings `ease_out`, `ease_in_out`, `ease_out_back`, `prog(t, a, b)`.
- Colores: GOLD, CREAM, CYAN, NAVY, INK, GREY. Dibujo libre con `ImageDraw.Draw(cv)` en líneas de 1 px sin antialias.

## Música y efectos (`A` = módulo audio)
- `A.section(t0, t1, bpm, [("A","min"), ("F","maj"), ...], A.st_xxx)` con estilos st_mystery, st_build, st_bright,
  st_summer_lead, st_rain, st_puzzle, st_triumph, st_winter. Cubrí de `TL.chapter_start(N) + 1.6` a `chapter_end(N)` y
  cambiá de sección según el clima de cada parte.
- Extras: `A.sting(t, [midi...])`, `A.note(A.music, t, A.midi_hz(m), dur)`, `A.kick(A.music, t)`, `A.crash(A.music, t)`.
- SFX: `A.whoosh(t)`, `A.pop_sfx(t, f0)`, `A.coin(t)`, `A.join_jingle(t)`, `A.text_blips(t0, n_letras, ritmo)`, `A.typewriter(t0, t1)`,
  `A.stamp_hit(t)`, `A.blip(t, f)`, `A.wind(t0, t1)`, `A.rain_amb(t0, t1)`, `A.chalk(t0, t1)`, `A.freeze(t)`. Volúmenes por defecto: la voz manda.

## 9:16 (Shorts)
`vertical.py` redibuja cada escena a pantalla completa 270x480 interceptando `bg`, `window`, `draw_text`, `char`, `bubble`,
`portrait_card`, `chapter_card`, `bigyear` y las partículas. Usá esas funciones (no pegues imágenes armadas a mano) para que
el redibujado funcione. Revisá `frames/sheet_v_chNN.png`.

## Cómo verificar (obligatorio antes de decir "listo")
Desde la raíz del repo, con el Python del `.venv`:
- `.venv\Scripts\python.exe scripts\producir.py <proyecto> --pasos timeline` → frases con sus tiempos.
- `.venv\Scripts\python.exe scripts\producir.py <proyecto> --pasos hoja --capitulo chNN --idiomas es,en,pt`
  → `frames/sheet_chNN.png`, `_en`, `_pt` y `sheet_v_chNN*.png`. **Miralas** con la herramienta de leer archivos.
- Instantes puntuales: en la carpeta del proyecto, `..\..\.venv\Scripts\python.exe engine\video.py times 300.5 302.0` → `frames/sheet_times.png`.
- Iterá hasta que: nada se corte fuera de pantalla, textos legibles y dentro de sus cajas en los 3 idiomas, personajes
  grandes y apoyados en el piso, un cambio visual cada 2–4 s.
- No corras `render` ni `audio`: los corre el coordinador al final.
