"""Capítulo 9: Cincuenta Años Después: un Beatle en el Anillo de Vidrio (2011–2026) + CTA."""
import math
from PIL import Image, ImageDraw

from core import *  # noqa
from common import *  # noqa
from timeline import TL
import outro

card_ch9 = make_card(9, ["UN BEATLE EN EL ANILLO"], "APPLE PARK · 2011–2026")


def scene_ch9_main(t):
    t_01 = TL.start("c9_01")
    t_02 = TL.start("c9_02")
    t_03 = TL.start("c9_03")
    t_04 = TL.start("c9_04")
    t_05 = TL.start("c9_05")
    t_06 = TL.start("c9_06")
    t_07 = TL.start("c9_07")

    cv = bg("apple_park_ring_2026")
    grade(cv, tint=(0.96, 1.0, 1.08), dark=0.06)
    d = ImageDraw.Draw(cv)
    ground_y = 224

    if t < t_02:
        # c9_01: Octubre de 2011 · Muere Jobs a los 56 años, Tim Cook y el anillo gigante de vidrio
        draw_chapter_header(cv, t, t_01, "CAP. 9", "UN BEATLE EN EL ANILLO",
                            "CUPERTINO · 2011–2026 · LA NAVE ESPACIAL DE VIDRIO")
        floor_prop(cv, draw_apple_park_stage_prop, 240, ground_y)

        window(cv, 94, 48, 292, 66, fill=(14, 22, 38), border=GOLD, alpha=0.95)
        draw_text(cv, "OCTUBRE DE 2011 · ADIÓS A STEVE JOBS", 240, 58, "press", 8, GOLD, align="center")
        draw_text(cv, "SU ÚLTIMO PLANO: EL ANILLO DE VIDRIO", 240, 76, "silk", 8, CYAN, align="center")
        draw_text(cv, "TIM COOK CONVIRTIÓ A APPLE EN UN GIGANTE", 240, 94, "silk", 8, CREAM, align="center")

        char(cv, "tim_cook", 152, ground_y, t, scale=2, look=1, r_arm="point", talk=talk_v(t, True))
        char(cv, "iphone_eng", 338, ground_y, t, scale=2, look=-1)
        person_card(cv, "tim_cook", "TIM COOK", "SUCESOR DE STEVE JOBS · CEO (2011–2026)",
                    t, t_01 + 0.4, dur=3.5)

    elif t < t_03:
        # c9_02: Marzo de 2026 · 50 años de Apple con Paul McCartney tocando en vivo
        draw_place_only(cv, "MARZO DE 2026 · 50 AÑOS DE APPLE EN EL GRAN PATIO", t, t_02, border=GOLD)
        floor_prop(cv, draw_apple_park_stage_prop, 240, ground_y)
        CONF.draw(cv, t)

        window(cv, 94, 42, 292, 72, fill=(16, 20, 38), border=GOLD, alpha=0.95)
        draw_text(cv, "1976 — 2026 · MEDIO SIGLO DE HISTORIA", 240, 52, "press", 8, GOLD, align="center")
        draw_text(cv, "INVITADO SORPRESA EN EL ESCENARIO:", 240, 70, "silk", 8, CYAN, align="center")
        draw_text(cv, "PAUL MCCARTNEY CANTANDO EN VIVO", 240, 88, "press", 8, CHALK_GREEN, align="center")

        char(cv, "mccartney_2026", 148, ground_y, t, scale=2, look=1, smile=True, r_arm="up", talk=talk_v(t, True))
        char(cv, "tim_cook", 342, ground_y, t, scale=2, look=-1, smile=True, l_arm="up")
        person_card(cv, "paul_mccartney", "PAUL MCCARTNEY", "LEYENDA DE LOS BEATLES · FIESTA 50 AÑOS",
                    t, t_02 + 0.35, dur=3.5)

    elif t < t_04:
        # c9_03: El círculo cerrado tras 30 años de juicios y el sonido Sosumi
        draw_place_only(cv, "LAS DOS «APPLE» RECONCILIADAS · EL CÍRCULO CERRADO", t, t_03, border=CYAN)
        floor_prop(cv, draw_apple_park_stage_prop, 240, ground_y)

        window(cv, 94, 42, 292, 74, fill=(14, 22, 38), border=CYAN, alpha=0.95)
        draw_text(cv, "30 AÑOS DE PELEAS EN LOS TRIBUNALES", 240, 52, "press", 8, CORAL, align="center")
        draw_text(cv, "EL SONIDO SECRETO «SOSUMI» EN 1991", 240, 70, "silk", 8, GOLD, align="center")
        draw_text(cv, "Y EN 2026, UN BEATLE CANTANDO EN CASA", 240, 88, "silk", 8, CHALK_GREEN, align="center")

        char(cv, "mccartney_2026", 148, ground_y, t, scale=2, look=1, smile=True, talk=talk_v(t, True))
        char(cv, "jim_reekes", 342, ground_y, t, scale=2, look=-1, smile=True, l_arm="up")

    elif t < t_05:
        # c9_04: 2026 · John Ternus nuevo CEO, teléfono plegable y batalla rumbo a 5 billones con NVIDIA
        draw_place_only(cv, "2026 · NUEVO DIRECTOR, TELÉFONO PLEGABLE Y 5 BILLONES", t, t_04, border=GOLD)
        floor_prop(cv, draw_apple_park_stage_prop, 240, ground_y)

        window(cv, 94, 40, 292, 86, fill=(14, 22, 40), border=GOLD, alpha=0.96)
        # Dibujo del iPhone plegable abriéndose como un libro
        open_w = 12 + int(round(10 * (0.5 + 0.5 * math.sin(t * 3.2))))
        d.rectangle([126 - open_w, 54, 126, 86], fill=(64, 156, 232, 255), outline=(*CREAM, 255))
        d.rectangle([126, 54, 126 + open_w, 86], fill=(84, 182, 248, 255), outline=(*CREAM, 255))
        draw_text(cv, "NUEVO CEO: JOHN TERNUS", 268, 52, "press", 8, GOLD, align="center")
        draw_text(cv, "TELÉFONO PLEGABLE (COMO UN LIBRO)", 268, 70, "silk", 8, CYAN, align="center")
        draw_text(cv, "≈ 5 BILLONES DE DÓLARES", 240, 92, "press", 8, CHALK_GREEN, align="center")
        draw_text(cv, "CABEZA A CABEZA CON NVIDIA EN LA CIMA", 240, 108, "silk", 8, CREAM, align="center")

        char(cv, "tim_cook", 136, ground_y, t, scale=2, look=1, smile=True)
        char(cv, "john_ternus", 344, ground_y, t, scale=2, look=-1, smile=True, l_arm="up", talk=talk_v(t, True))
        person_card(cv, "john_ternus", "JOHN TERNUS", "INGENIERO · NUEVO DIRECTOR DE APPLE (2026)",
                    t, t_04 + 0.35, dur=3.5)

    elif t < t_06:
        # c9_05: 150.000 empleados hoy vs la credencial número cero y las historias humanas
        draw_place_only(cv, "DE UN GARAJE CON TRES SOCIOS A 150.000 EMPLEADOS", t, t_05, border=CYAN)
        floor_prop(cv, draw_pirate_flag_prop, 240, ground_y)

        window(cv, 94, 40, 292, 86, fill=(14, 20, 38), border=CYAN, alpha=0.96)
        draw_employee_badge(cv, 138, 82, num_str="0", flip_p=math.cos(t * 2.2), scale=1)
        draw_text(cv, "150.000 PERSONAS EN EL ANILLO", 266, 52, "press", 8, CYAN, align="center")
        draw_text(cv, "SILBATO · 800 $ · CUADERNO DE 2,50 $", 266, 72, "silk", 8, GOLD, align="center")
        draw_text(cv, "SONIDO SOSUMI · 4.000 CAFÉS", 266, 88, "silk", 8, CREAM, align="center")
        draw_text(cv, "Y UNA CREDENCIAL CON EL NÚMERO CERO", 266, 106, "silk", 8, CHALK_GREEN, align="center")

        char(cv, "jobs_1977", 136, ground_y, t, scale=2, look=1, smile=True)
        char(cv, "wozniak_1977", 344, ground_y, t, scale=2, look=-1, smile=True)

    elif t < t_07:
        # c9_06: "¿Prefieres ser parte de la marina... o todavía te animas a ser un poco pirata?"
        draw_place_only(cv, "EL EMPLEADO NÚMERO CERO · LA PREGUNTA FINAL", t, t_06, border=GOLD)
        floor_prop(cv, draw_pirate_flag_prop, 240, ground_y)

        window(cv, 94, 38, 292, 92, fill=(16, 20, 38), border=GOLD, alpha=0.96)
        draw_employee_badge(cv, 136, 84, num_str="0", name_str="JOBS", flip_p=1.0, scale=2)
        draw_text(cv, "CUANDO EMPIECES UN PROYECTO:", 278, 54, "silk", 8, CREAM, align="center")
        draw_text(cv, "¿PREFIERES LA MARINA...", 278, 72, "press", 8, CYAN, align="center")
        draw_text(cv, "...O ANIMARTE A SER", 278, 92, "press", 8, GOLD, align="center")
        draw_text(cv, "UN POCO PIRATA?", 278, 108, "press", 8, CHALK_GREEN, align="center")

        char(cv, "jobs_1977", 124, ground_y, t, scale=2, look=1, smile=True, r_arm="up")
        char(cv, "wozniak_1977", 356, ground_y, t, scale=2, look=-1, smile=True, l_arm="up")

    else:
        # c9_07: CTA antes del cierre de Pixeloide Studios invitando a comentar el próximo episodio
        draw_place_only(cv, "PIXELOIDE STUDIOS · ¿QUÉ HISTORIA CONTAMOS AHORA?", t, t_07, border=GOLD)
        floor_prop(cv, draw_pirate_flag_prop, 240, ground_y)
        CONF.draw(cv, t)

        window(cv, 94, 40, 292, 88, fill=(16, 20, 40), border=GOLD, alpha=0.96)
        draw_text(cv, "¿QUÉ HISTORIA TE GUSTARÍA VER", 240, 52, "press", 8, GOLD, align="center")
        draw_text(cv, "EN EL PRÓXIMO EPISODIO?", 240, 68, "press", 8, CYAN, align="center")
        draw_text(cv, "DÉJALO EN LOS COMENTARIOS", 240, 90, "press", 8, CHALK_GREEN, align="center")
        draw_text(cv, "Y SUSCRÍBETE A PIXELOIDE STUDIOS", 240, 108, "silk", 8, CREAM, align="center")

        char(cv, "jobs_1977", 118, ground_y, t, scale=2, look=1, smile=True, r_arm="up", talk=talk_v(t, True))
        char(cv, "wozniak_1977", 176, ground_y, t, scale=2, look=1, smile=True, r_arm="up")
        char(cv, "susan_kare", 312, ground_y, t, scale=2, look=-1, smile=True, l_arm="up")
        char(cv, "mccartney_2026", 368, ground_y, t, scale=2, look=-1, smile=True, l_arm="up")

    return vignette(cv, 0.34)


def scenes():
    return [
        (TL.chapter_start(9) - 0.15, card_ch9, None),
        (TL.start("c9_01"), scene_ch9_main, lambda t: cam_push(t, TL.start("c9_01"), outro.T_LOGO, 1.0, 1.03)),
    ]
