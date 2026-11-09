

# =========================================================================== montaje

def scenes():
    """Lista de (inicio, función, cámara) de la apertura y el capítulo 1."""
    w = TL.word
    c = [
        (0.0, sc_office, lambda t: cam_push(t, 0.0, TL.s("s02"), 1.0, 1.12, (240, 150), (170, 170))),
        (TL.s("s02") - 0.2, sc_ten, lambda t: (1.0 + cam_punch(t, [w("s02", "diez") + 0.05 + i * 0.11 for i in range(10)], 0.02)
                                               + cam_punch(t, [w("s02", "pensar") + 0.2], 0.08), 240, 160)),
        (TL.s("s03") - 0.2, sc_summer, lambda t: cam_push(t, TL.s("s03"), TL.s("s04") + 0.3, 1.1, 1.0, (240, 150))),
        (TL.s("s05") - 0.25, sc_title, lambda t: (1.0 + cam_punch(t, [w("s05", "inteligencia") + 0.22,
                                                                   w("s05", "artificial") + 0.22], 0.1), 240, 120)),
        (TL.s("s06") - 0.35, make_card(1, ["LA PREGUNTA"], "1950 – 1956"), None),
        (TL.s("s07") - 0.2, sc_turing, lambda t: cam_push(t, TL.s("s07"), TL.e("s07"), 1.0, 1.15, (240, 135), (300, 110))),
        (TL.s("s08") - 0.2, sc_imitation, lambda t: (1.0 + cam_punch(t, [w("s08", "importa")], 0.1), 240, 150)),
        (TL.s("s09") - 0.2, sc_dartmouth, lambda t: (1.0 + cam_punch(t, [w("s09", n) for n in
                                                                      ("McCarthy", "Minsky", "Shannon", "Rochester")], 0.04), 240, 135)),
        (w("s10", "nombre", end=True) + 0.05, sc_board, lambda t: cam_push(t, w("s10", "nombre"), TL.e("s10") + 0.6,
                                                                         1.0, 1.22, (240, 135), (300, 80))),
        (TL.s("s11") - 0.3, sc_winter, lambda t: cam_push(t, TL.s("s12"), TL.e("s12"), 1.0, 1.15, (240, 135), (240, 190))),
    ]
    return c
