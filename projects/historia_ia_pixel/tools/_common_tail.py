

# --------------------------------------------------------------------------- placas de capítulo

CARD_YEARS = {}


def make_card(num, lines, years, snow=False, robot_face="question"):
    """Escena genérica de placa de capítulo (ventana RPG que se abre + robot)."""
    def sc(t):
        cv = vgradient((4, 6, 16), (20, 30, 56), 10) if snow else vgradient((2, 2, 8), (14, 16, 36), 10)
        if snow:
            SNOW.draw(cv, t, density=0.7)
        else:
            STARS.draw(cv, t * 0.5, alpha=0.6)
        t0 = TL.chapter_start(num) - 0.3
        chapter_card(cv, t, t0, num, lines, years)
        if t > t0 + 0.8:
            robot(cv, 240, 256, t, face=robot_face, alpha=prog(t, t0 + 0.8, t0 + 1.1))
        return cv
    return sc


def chapter_end(num):
    """Inicio del capítulo siguiente (o fin del video)."""
    return TL.chapter_start(num + 1) if num < 8 else TL.total
