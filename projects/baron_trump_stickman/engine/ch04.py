"""Capítulo 4: Los papeles de Tesla (Nueva York, enero de 1943)."""
import math
from PIL import Image, ImageDraw

from core import *  # noqa
from common import *  # noqa
from timeline import TL

card_ch4 = make_card(4, ["LOS PAPELES DE TESLA"], "NUEVA YORK · ENERO DE 1943")


def scene_ch4(t):
    t_01 = TL.start("c4_01")
    t_02 = TL.start("c4_02")
    t_03 = TL.start("c4_03")
    t_04 = TL.start("c4_04")
    t_05 = TL.start("c4_05")
    t_06 = TL.start("c4_06")
    t_07 = TL.start("c4_07")
    t_08 = TL.start("c4_08")
    ground_y = 224

    if t < t_02:
        # c4_01: Pasillo de hotel años 40, puerta entreabierta con luz azul
        cv = bg("hotel_hallway_1943")
        grade(cv, tint=(0.90, 0.96, 1.08), dark=0.10)
        draw_chapter_header(cv, "CAP. 4 · LOS PAPELES DE TESLA", "NUEVA YORK · 1943", t, t_01, border=CYAN)
        window(cv, 76, 46, 328, 66, fill=(12, 18, 34), border=CYAN, alpha=0.94)
        draw_text(cv, "FALTABA UNA MÁQUINA DEL TIEMPO", 240, 56, "press", 8, CYAN, align="center")
        draw_text(cv, "Y APARECIÓ OTRA HISTORIA REAL", 240, 78, "silk", 8, CREAM, align="center")
        return vignette(cv, 0.36)

    if t < t_03:
        # c4_02: Habitación de hotel con papeles, planos, bobina y reloj de bolsillo
        cv = bg("tesla_room_1943")
        grade(cv, tint=(0.90, 0.96, 1.10), dark=0.08)
        draw_chapter_header(cv, "CAP. 4 · LOS PAPELES DE TESLA", "NUEVA YORK · ENERO DE 1943", t, t_02, border=CYAN)
        floor_prop(cv, lambda c, x, f: draw_tesla_table_prop(c, x, f, powered=True, t=t), 240, ground_y)
        window(cv, 76, 44, 328, 66, fill=(12, 18, 34), border=CYAN, alpha=0.94)
        draw_text(cv, "NIKOLA TESLA · 86 AÑOS", 240, 54, "press", 8, CYAN, align="center")
        draw_text(cv, "DEJÓ BAÚLES LLENOS DE PAPELES", 240, 74, "silk", 8, CREAM, align="center")
        person_card(cv, "tesla", "NIKOLA TESLA", "INVENTOR · NUEVA YORK, 1943",
                    t, t_02 + 0.35, dur=3.5)
        return vignette(cv, 0.34)

    if t < t_04:
        # c4_03: Hombres de traje cargan baúles en un camión de noche
        cv = bg("nyc_street_1943")
        grade(cv, tint=(0.90, 0.96, 1.08), dark=0.10)
        draw_chapter_header(cv, "CAP. 4 · LOS PAPELES DE TESLA", "PLENA GUERRA · 1943", t, t_03, border=CYAN)
        floor_prop(cv, draw_trunk_prop, 240, ground_y)
        window(cv, 76, 44, 328, 66, fill=(12, 18, 34), border=CYAN, alpha=0.94)
        draw_text(cv, "GOBIERNO DE ESTADOS UNIDOS", 240, 54, "press", 8, GOLD, align="center")
        draw_text(cv, "SE LLEVÓ LOS BAÚLES DE TESLA", 240, 74, "silk", 8, CREAM, align="center")
        ax1, aw1 = walk(t, t_03, t_04, 130, 196)
        ax2, aw2 = walk(t, t_03, t_04, 350, 286)
        char(cv, "agent_a", ax1, ground_y, t, scale=2, walk=aw1, look=1)
        char(cv, "agent_b", ax2, ground_y, t, scale=2, walk=aw2, look=-1)
        return vignette(cv, 0.34)

    if t < t_05:
        # c4_04: Ingeniero genérico del MIT revisa planos bajo lámpara (sin rostro de persona real)
        cv = bg("mit_office_1943")
        grade(cv, tint=(0.92, 0.98, 1.04), dark=0.08)
        draw_chapter_header(cv, "CAP. 4 · LOS PAPELES DE TESLA", "JOHN G. TRUMP · MIT", t, t_04, border=CYAN)
        floor_prop(cv, draw_mit_desk_prop, 240, ground_y)
        window(cv, 76, 44, 328, 66, fill=(12, 22, 32), border=CYAN, alpha=0.95)
        draw_text(cv, "JOHN G. TRUMP · MIT", 240, 54, "press", 8, CYAN, align="center")
        draw_text(cv, "INGENIERO · TÍO DE DONALD TRUMP", 240, 74, "silk", 8, CREAM, align="center")
        # Silueta genérica del ingeniero revisando planos
        silhouette(cv, "engineer_mit", 156, ground_y, t, color=(24, 32, 48), scale=2, look=1, r_arm="write")
        return vignette(cv, 0.34)

    if t < t_06:
        # c4_05: Cierra carpeta, conclusión: ideas especulativas, ninguna máquina
        cv = bg("mit_office_1943")
        grade(cv, tint=(0.92, 0.98, 1.04), dark=0.08)
        draw_chapter_header(cv, "CAP. 4 · LOS PAPELES DE TESLA", "INFORME OFICIAL · 1943", t, t_05, border=GOLD)
        floor_prop(cv, draw_mit_desk_prop, 240, ground_y)
        window(cv, 76, 44, 328, 72, fill=(14, 22, 32), border=GOLD, alpha=0.95)
        draw_text(cv, "CONCLUSIÓN DEL INFORME:", 240, 54, "press", 8, GOLD, align="center")
        draw_text(cv, "«IDEAS ESPECULATIVAS, SIN PELIGRO»", 240, 74, "silk", 8, CREAM, align="center")
        draw_text(cv, "NINGUNA MÁQUINA DEL TIEMPO", 240, 92, "press", 8, PINK, align="center")
        silhouette(cv, "engineer_mit", 156, ground_y, t, color=(24, 32, 48), scale=2, look=1)
        return vignette(cv, 0.34)

    if t < t_07:
        # c4_06: Diario genérico de los años 30 con dibujo de un rayo
        cv = new_canvas((16, 20, 32))
        draw_chapter_header(cv, "CAP. 4 · LOS PAPELES DE TESLA", "ANUNCIOS DE LOS AÑOS 30", t, t_06, border=CYAN)
        d = ImageDraw.Draw(cv)
        window(cv, 76, 44, 328, 162, fill=(238, 232, 214), border=INK, alpha=0.98)
        draw_text(cv, "DIARIO · AÑOS TREINTA", 240, 54, "press", 8, INK, align="center", outline=None, shadow=False)
        d.line([(96, 70), (384, 70)], fill=(*INK, 255), width=2)
        # Dibujo esquemático de rayo cruzando el cielo
        d.rectangle([108, 80, 372, 152], fill=(24, 36, 58, 255), outline=(*INK, 255), width=2)
        d.line([(120, 140), (210, 112), (240, 122), (356, 90)], fill=(120, 234, 255, 255), width=3)
        draw_text(cv, "«RAYO CAPAZ DE DERRIBAR AVIONES»", 240, 164, "silk", 8, INK, align="center", outline=None, shadow=False)
        draw_text(cv, "PERO NADA FUNCIONABA EN SUS PAPELES", 240, 182, "press", 8, (176, 36, 42), align="center", outline=None, shadow=False)
        return vignette(cv, 0.32)

    if t < t_08:
        # c4_07: Tablero de corcho une libro 1893, bobina y torre
        cv = bg("corkboard_bg")
        draw_chapter_header(cv, "CAP. 4 · LOS PAPELES DE TESLA", "LA PIEZA QUE FALTABA", t, t_07, border=PINK)
        d = ImageDraw.Draw(cv)
        d.line([(126, 134), (240, 134), (354, 134)], fill=(224, 46, 54, 255), width=3)
        window(cv, 76, 44, 328, 72, fill=(18, 18, 28), border=PINK, alpha=0.95)
        draw_text(cv, "LA TEORÍA EN INTERNET:", 240, 54, "press", 8, PINK, align="center")
        draw_text(cv, "TESLA -> EL TÍO -> VIAJE AL PASADO", 240, 74, "silk", 8, GOLD, align="center")
        draw_text(cv, "Y PISTAS DEJADAS EN UN LIBRO", 240, 92, "silk", 8, CREAM, align="center")
        return vignette(cv, 0.34)

    # c4_08: La bobina se apaga
    cv = bg("tesla_room_1943")
    grade(cv, dark=0.38)
    floor_prop(cv, lambda c, x, f: draw_tesla_table_prop(c, x, f, powered=False, t=t), 240, ground_y)
    window(cv, 76, 52, 328, 66, fill=(14, 16, 26), border=CYAN, alpha=0.96)
    draw_text(cv, "LO DEL TÍO ES VERDAD", 240, 64, "press", 8, GOLD, align="center")
    draw_text(cv, "LA MÁQUINA NO APARECE EN NINGÚN PAPEL", 240, 86, "silk", 8, CREAM, align="center")
    return vignette(cv, 0.40)


def scenes():
    return [
        (TL.start("c4_00") - 0.1, card_ch4, None),
        (TL.start("c4_01") - 0.1, scene_ch4, lambda t: cam_push(t, TL.start("c4_01"), TL.end("c4_08"), 1.0, 1.03)),
    ]
