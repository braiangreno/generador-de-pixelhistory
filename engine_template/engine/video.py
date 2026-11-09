"""Montaje dinámico del video completo en pixel art.

  python engine/video.py sheet [ch]            -> hoja de contacto (todas las escenas o de un capítulo)
  python engine/video.py times t1 t2 ...       -> hoja con esos instantes
  python engine/video.py render [workers]      -> renders/video_mudo.mp4 (1920x1080, 30 fps, en paralelo)
  python engine/video.py segment ch            -> renderiza solo un capítulo (para revisar)
"""
import glob
import importlib
import os
import re
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa

ENGINE_DIR = os.path.dirname(os.path.abspath(__file__))


def discover_chapter_modules():
    ch_files = glob.glob(os.path.join(ENGINE_DIR, "ch[0-9][0-9].py"))
    mods = sorted(os.path.splitext(os.path.basename(p))[0] for p in ch_files)
    if not mods and os.path.exists(os.path.join(ENGINE_DIR, "declarative_scenes.py")):
        mods = ["declarative_scenes"]
    mods.append("outro")
    return mods


CHAPTER_MODULES = discover_chapter_modules()
XFADE = 0.22


def load_scenes():
    out = []
    for name in CHAPTER_MODULES:
        try:
            mod = importlib.import_module(name)
        except ModuleNotFoundError as e:
            if e.name == name:
                continue
            raise
        for sc in mod.scenes():
            st, fn = sc[0], sc[1]
            cam = sc[2] if len(sc) > 2 else None
            out.append((st, fn, cam, name))
    out.sort(key=lambda s: s[0])
    return out


SCENES = load_scenes()


def scene_index(t):
    idx = 0
    for i, s in enumerate(SCENES):
        if t >= s[0]:
            idx = i
    return idx


def frame_at(t, final=False):
    if not SCENES:
        return new_canvas(INK)
    idx = scene_index(t)
    st, fn, cam, _ = SCENES[idx]
    img = fn(t)
    c = cam(t) if cam else None
    if idx > 0 and t < st + XFADE:
        pst, pfn, pcam, _ = SCENES[idx - 1]
        prev = pfn(t)
        k = (t - st) / XFADE
        if final:
            a = apply_cam(prev, pcam(t) if pcam else None)
            b = apply_cam(img, c)
            return _dither_big(a, b, k)
        img = dither_mix(prev, img, k)
    if t < 0.5:
        img = fade_to(img, (0, 0, 0), 1 - t / 0.5)
    if t > TL.total - 1.2:
        img = fade_to(img, (0, 0, 0), prog(t, TL.total - 1.2, TL.total - 0.1))
    if final:
        return apply_cam(img, c)
    return img


_BIG_BAYER = None


def _dither_big(a, b, k):
    """Transición con dithering a escala de 'píxel grande' (4x4) sobre el fotograma 1080p."""
    global _BIG_BAYER
    if _BIG_BAYER is None:
        small = bayer_tile(W, H)
        _BIG_BAYER = np.repeat(np.repeat(small, 4, 0), 4, 1)
    A = np.array(a)
    B = np.array(b)
    m = _BIG_BAYER < k
    A[m] = B[m]
    return Image.fromarray(A, a.mode)


def sheet(times, name="sheet.png", cols=4):
    os.makedirs(os.path.join(ROOT, "frames"), exist_ok=True)
    if not times:
        times = [1.0]
    tiles = [frame_at(t, final=True).convert("RGB").resize((480, 270), Image.NEAREST) for t in times]
    rows = max(1, (len(tiles) + cols - 1) // cols)
    out = Image.new("RGB", (cols * 480, rows * 270))
    d = ImageDraw.Draw(out)
    for i, im in enumerate(tiles):
        out.paste(im, ((i % cols) * 480, (i // cols) * 270))
        d.text(((i % cols) * 480 + 4, (i // cols) * 270 + 258), f"{times[i]:.1f}s", fill=(255, 0, 255))
    out.save(os.path.join(ROOT, "frames", name))
    print("sheet", name, [round(x, 1) for x in times])


def scene_times(ch=None):
    ts = []
    for i, s in enumerate(SCENES):
        if ch and s[3] != ch:
            continue
        en = SCENES[i + 1][0] if i + 1 < len(SCENES) else TL.total
        ts.append(s[0] + (en - s[0]) * 0.7)
    return ts


def render_range(t0, t1, out_path):
    n0, n1 = int(round(t0 * FPS)), int(round(t1 * FPS))
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x1080",
           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
           "-pix_fmt", "yuv420p", out_path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    ts = time.time()
    for i in range(n0, n1):
        p.stdin.write(frame_at(i / FPS, final=True).convert("RGB").tobytes())
        if (i - n0) % 600 == 0:
            print(f"[{os.path.basename(out_path)}] {i - n0}/{n1 - n0}  {time.time() - ts:.0f}s", flush=True)
    p.stdin.close()
    p.wait()


def _worker(args):
    render_range(*args)
    return args[2]


def render(workers=8):
    from multiprocessing import Pool
    from i18n import get_lang
    lang = get_lang()
    suf = "" if lang == "es" else f"_{lang}"
    total = TL.total
    n_frames = int(round(total * FPS))
    seg_dir = os.path.join(ROOT, "renders", f"segments{suf}")
    os.makedirs(seg_dir, exist_ok=True)
    bounds = [round(n_frames * i / workers) for i in range(workers + 1)]
    jobs = [(bounds[i] / FPS, bounds[i + 1] / FPS, os.path.join(seg_dir, f"seg_{i:02d}.mp4")) for i in range(workers)]
    with Pool(workers) as pool:
        for p in pool.imap_unordered(_worker, jobs):
            print("listo", os.path.basename(p), flush=True)
    lst = os.path.join(seg_dir, "list.txt")
    with open(lst, "w") as f:
        for j in jobs:
            f.write(f"file '{j[2]}'\n")
    out = os.path.join(ROOT, "renders", f"video_mudo{suf}.mp4")
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                           "-c", "copy", out])
    print("done", out, round(total, 2))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "sheet"
    if cmd == "sheet":
        ch = sys.argv[2] if len(sys.argv) > 2 else None
        sheet(scene_times(ch), name=f"sheet_{ch or 'all'}.png")
    elif cmd == "times":
        sheet([float(x) for x in sys.argv[2:]], name="sheet_times.png")
    elif cmd == "render":
        render(int(sys.argv[2]) if len(sys.argv) > 2 else 8)
    elif cmd == "segment":
        ch = int(sys.argv[2])
        t0 = TL.chapter_start(ch) - 0.4 if ch > 1 else 0.0
        t1 = chapter_end(max(ch, 1))
        render_range(t0, t1, os.path.join(ROOT, "renders", f"cap{ch}.mp4"))
