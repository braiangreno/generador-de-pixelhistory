import os
os.chdir(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "engine"))
L = open('pilot.py', encoding='utf-8').read().split('\n')


def rng(a, b):
    return L[a - 1:b - 1]


hdr = '''"""Helpers compartidos por todas las escenas (personajes, UI, efectos, camara)."""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import *  # noqa
import sprites as S
from timeline import TL

FEET_OFFSET = 50  # fila de los pies dentro del sprite
'''
common = hdr.split('\n') + rng(24, 225) + rng(332, 351) + rng(448, 473) + [
    'STARS = Stars(140, seed=11, region=(0, 0, W, 210))',
    'RAIN = Rain(110, seed=4, region=(192, 8, 428, 142), color=(196, 210, 226), speed=210)',
    'SNOW = Snow(260, seed=8)', 'CONF = Confetti(110, seed=6)',
    'FOUR = ["mccarthy", "minsky", "shannon", "rochester"]', '']
open('common.py', 'w', encoding='utf-8').write('\n'.join(common))
skip = set(range(332, 351)) | set(range(448, 473)) | {406, 486, 729, 730, 228}
body = [l for i, l in enumerate(L[224:822], start=225) if i not in skip]
h2 = '"""Apertura + Capitulo 1 (La pregunta)."""\nfrom common import *  # noqa\n'
open('ch01.py', 'w', encoding='utf-8').write(h2 + '\n'.join(body))
print(len(common), len(body))
