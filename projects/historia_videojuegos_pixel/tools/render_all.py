"""Renderiza los tres videos mudos (ES, EN, PT) en paralelo (8 workers) y ejecuta mux_all.py."""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    for tmp in ["scratch_strings.txt", "scratch_overflows.txt"]:
        p = os.path.join(ROOT, tmp)
        if os.path.exists(p):
            os.remove(p)

    for lang in ["es", "en", "pt"]:
        print(f"================ RENDERING {lang.upper()} (1080p, 8 workers) ================", flush=True)
        env = os.environ.copy()
        env["VIDEO_LANG"] = lang
        subprocess.check_call([sys.executable, os.path.join(ROOT, "engine", "video.py"), "render", "8"], env=env)

    print("================ MUXING ALL MASTERS (-14 LUFS) ================", flush=True)
    subprocess.check_call([sys.executable, os.path.join(ROOT, "tools", "mux_all.py")])


if __name__ == "__main__":
    main()
