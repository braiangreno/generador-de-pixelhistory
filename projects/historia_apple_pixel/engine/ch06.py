"""Capítulo 6: El Sonido que Significa «Entonces Demándame» (1985–1991)."""
import math
from PIL import Image, ImageDraw

from core import *  # noqa
from common import *  # noqa
from timeline import TL

card_ch6 = make_card(6, ["ENTONCES DEMÁNDAME"], "CUPERTINO Y LONDRES · 1985–1991")


def scene_ch6_main(t):
    t_01 = TL.start("c6_01")
    t_02 = TL.start("c6_02")
    t_03 = TL.start("c6_03")
    t_04 = TL.start("c6_04")
    t_05 = TL.start("c6_05")

    ground_y = 224

    if t < t_02:
        # c6_01: 1985 · Jobs echado de Apple y el cubo negro perfecto de 100.000 dólares
        cv = bg("cupertino_office_1977")
        grade(cv, tint=(0.94, 0.96, 1.06), dark=0.08)
        draw_chapter_header(cv, t, t_01, "CAP. 6", "ENTONCES DEMÁNDAME",
                            "1985 · ECHADO DE SU PROPIA EMPRESA A LOS 30 AÑOS")
        floor_prop(cv, draw_next_cube_prop, 240, ground_y)

        window(cv, 94, 48, 292, 68, fill=(16, 20, 38), border=GOLD, alpha=0.95)
        draw_text(cv, "1985 · EL DIRECTORIO ECHA A STEVE JOBS", 240, 58, "press", 8, CORAL, align="center")
        draw_text(cv, "CREA UN CUBO NEGRO DE MAGNESIO PERFECTO", 240, 76, "silk", 8, CREAM, align="center")
        draw_text(cv, "PAGÓ 100.000 $ POR EL DIBUJO DE LA MARCA", 240, 94, "silk", 8, GOLD, align="center")

        char(cv, "jobs_1977", 142, ground_y, t, scale=2, look=1, r_arm="point", talk=talk_v(t, True))
        char(cv, "mike_scott", 344, ground_y, t, scale=2, look=-1)

    elif t < t_03:
        # c6_02: El estudio de abogados de Londres y la empresa de Los Beatles (pacto de 1981)
        cv = bg("law_office_london_1989")
        grade(cv, tint=(1.04, 0.96, 0.88), dark=0.06)
        draw_place_only(cv, "LONDRES · LA OTRA APPLE (LA EMPRESA DE LOS BEATLES)", t, t_02, border=GOLD)
        floor_prop(cv, draw_lawyer_desk_prop, 240, ground_y)

        window(cv, 94, 42, 292, 74, fill=(22, 18, 30), border=GOLD, alpha=0.95)
        draw_text(cv, "LOS BEATLES TENÍAN «APPLE CORPS» DESDE 1968", 240, 52, "press", 8, GOLD, align="center")
        draw_text(cv, "ACUERDO FIRMADO EN 1981:", 240, 70, "silk", 8, CYAN, align="center")
        draw_text(cv, "«PUEDEN USAR EL NOMBRE SI NO HACEN MÚSICA»", 240, 88, "silk", 8, CREAM, align="center")

        char(cv, "lawyer_london", 146, ground_y, t, scale=2, look=1, r_arm="point", talk=talk_v(t, True))
        char(cv, "jim_reekes", 338, ground_y, t, scale=2, look=-1)

    elif t < t_04:
        # c6_03: 1989 · Las computadoras empiezan a grabar sonidos -> juicio y pánico de abogados
        cv = bg("law_office_london_1989")
        grade(cv, tint=(1.06, 0.94, 0.88), dark=0.07)
        draw_place_only(cv, "1989 · NUEVA DEMANDA MILLONARIA POR LOS SONIDOS", t, t_03, border=CORAL)
        floor_prop(cv, draw_lawyer_desk_prop, 240, ground_y)

        window(cv, 94, 42, 292, 76, fill=(28, 16, 24), border=CORAL, alpha=0.95)
        draw_text(cv, "1989 · LA MAC EMPEZÓ A TOCAR NOTAS", 240, 52, "press", 8, CORAL, align="center")
        draw_text(cv, "LOS ABOGADOS ENTRARON EN PÁNICO:", 240, 70, "silk", 8, CREAM, align="center")
        draw_text(cv, "«PROHIBIDO USAR NOMBRES QUE SUENEN A MÚSICA»", 240, 88, "silk", 8, GOLD, align="center")

        char(cv, "lawyer_london", 142, ground_y, t, scale=2, look=1, brows="angry", r_arm="up", talk=talk_v(t, True))
        char(cv, "jim_reekes", 342, ground_y, t, scale=2, look=-1, brows="sad")
        bubble(cv, "¡CÁMBIALE EL NOMBRE!", 142, ground_y - 104, align="center")

    elif t < t_05:
        # c6_04: Jim Reekes propone "SOSUMI" ("Es una palabra japonesa") y los abogados lo aprueban
        cv = bg("law_office_london_1989")
        grade(cv, tint=(1.02, 0.98, 0.92), dark=0.06)
        draw_place_only(cv, "JIM REEKES · LA VENGANZA DEL INGENIERO DE SONIDO", t, t_04, border=CYAN)
        floor_prop(cv, draw_lawyer_desk_prop, 240, ground_y)

        window(cv, 94, 40, 292, 78, fill=(14, 22, 38), border=CYAN, alpha=0.95)
        draw_text(cv, "NOMBRE TACHADO: «CAMPANITA» (MUY MUSICAL)", 240, 50, "silk", 8, CORAL, align="center")
        draw_text(cv, "NUEVO NOMBRE: «SOSUMI»", 240, 68, "press", 8, GOLD, align="center")
        draw_text(cv, "«ES UNA PALABRA JAPONESA, NO TIENE MÚSICA»", 240, 86, "silk", 8, CREAM, align="center")
        draw_text(cv, "DEPARTAMENTO LEGAL: ¡APROBADO!", 240, 102, "press", 8, CHALK_GREEN, align="center")

        char(cv, "lawyer_london", 138, ground_y, t, scale=2, look=1, smile=True)
        char(cv, "jim_reekes", 344, ground_y, t, scale=2, look=-1, smile=True, l_arm="up", talk=talk_v(t, True))
        person_card(cv, "jim_reekes", "JIM REEKES", "INGENIERO DE SONIDO DE APPLE · 1991",
                    t, t_04 + 0.35, dur=3.5)

    else:
        # c6_05: SOSUMI = "SO SUE ME" ("Entonces demándame") sonando hasta hoy
        cv = bg("law_office_london_1989")
        grade(cv, tint=(0.98, 1.02, 1.06), dark=0.06)
        draw_place_only(cv, "SOSUMI = «SO SUE ME» («ENTONCES DEMÁNDAME»)", t, t_05, border=GOLD)
        floor_prop(cv, draw_lawyer_desk_prop, 240, ground_y)

        window(cv, 94, 40, 292, 86, fill=(16, 22, 40), border=GOLD, alpha=0.96)
        draw_text(cv, "LÉELO EN VOZ ALTA EN INGLÉS:", 240, 50, "silk", 8, CYAN, align="center")
        draw_text(cv, "SO - SU - MI  =  «SO SUE ME»", 240, 68, "press", 8, GOLD, align="center")
        draw_text(cv, "«ENTONCES DEMÁNDAME»", 240, 86, "press", 8, CHALK_GREEN, align="center")
        draw_text(cv, "SIGUE ADENTRO DE TODAS LAS MAC HASTA HOY", 240, 106, "silk", 8, CREAM, align="center")

        char(cv, "lawyer_london", 138, ground_y, t, scale=2, look=1, brows="angry", frown=True)
        char(cv, "jim_reekes", 344, ground_y, t, scale=2, look=-1, smile=True, l_arm="up")

    return vignette(cv, 0.34)


def scenes():
    return [
        (TL.chapter_start(6) - 0.15, card_ch6, None),
        (TL.start("c6_01"), scene_ch6_main, lambda t: cam_push(t, TL.start("c6_01"), chapter_end(6), 1.0, 1.03)),
    ]
