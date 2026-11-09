import os
os.chdir(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "engine"))
src = open('ch01.py', encoding='utf-8', newline='').read()
src = src.replace('robot(cv, 240, 226, t, face="sad" if not frozen else "off", frozen=frozen, alpha=a)',
                  'robot(cv, 240, 266, t, face="sad" if not frozen else "off", frozen=frozen, alpha=a, scale=2)')
if 'def sc_ch2(t):' in src:
    src = src[:src.index('def sc_ch2(t):')]
# `scaled` vive ahora en common.py
if 'def scaled(cv, fn' in src:
    a = src.index('def scaled(cv, fn')
    b = src.index('def booth_bg():')
    src = src[:a] + src[b:]
open('ch01.py', 'w', encoding='utf-8', newline='').write(src)
c = open('common.py', encoding='utf-8', newline='').read()
if 'def scaled(' not in c:
    c += '''

def scaled(cv, fn, w, h, x, y, k=2):
    """Dibuja con fn(img) en un lienzo chico (w x h) y lo pega ampliado x k (pixel art)."""
    tmp = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    fn(tmp)
    a = upscale(np.array(tmp), k)
    paste_arr(cv, a, x, y)
'''
open('common.py', 'w', encoding='utf-8', newline='').write(c)
print('ok')
