"""Render every sequence of episode 1 in order and concatenate them into one video.

    python render.py               # 480p preview  -> media/ep01/ep01_480p15.mp4
    python render.py -q f          # 1080p30 final -> media/ep01/ep01_1080p30.mp4
    python render.py --only s03    # re-render one sequence, then re-assemble
    python render.py --frames s03  # save one PNG every 4 s of that sequence (quick visual check)
"""
import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MEDIA = HERE.parent / "media" / "ep01"
SEQUENCE = [
    ("s00_cold_open", "ColdOpen"),
    ("s01_what", "WhatIsIt"),
    ("s02_ensembles", "Ensembles"),
    ("s03_repulsion", "Repulsion"),
    ("s04_coulomb", "CoulombGas"),
    ("s05_semicircle", "Semicircle"),
    ("s06_computations", "Computations"),
    ("s07_recap", "Recap"),
]
QUALITY = {"f": "1080p30", "l": "480p15", "m": "720p30", "h": "1080p60", "k": "2160p60"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-q", default="l", choices=QUALITY)
    ap.add_argument("--only", nargs="*", default=None, help="file prefixes to re-render, e.g. s03 s04")
    ap.add_argument("--no-render", action="store_true")
    ap.add_argument("--frames", nargs="*", default=None, help="dump PNG frames of these sequences")
    a = ap.parse_args()
    folder = QUALITY[a.q]
    parts = []
    for f, scene in SEQUENCE:
        out = MEDIA / "videos" / f / folder / f"{scene}.mp4"
        todo = not a.no_render and (a.only is None or any(f.startswith(o) for o in a.only))
        if todo or not out.exists():
            print(f"--> {f}.{scene} [{folder}]", flush=True)
            qflag = ["-r", "1920,1080", "--fps", "30"] if a.q == "f" else [f"-q{a.q}"]
            subprocess.run([sys.executable, "-m", "manim", *qflag, "--media_dir", str(MEDIA),
                            str(HERE / "scenes" / f"{f}.py"), scene], check=True, cwd=HERE / "scenes")
        parts.append(out)
        if a.frames is not None and any(f.startswith(o) for o in a.frames):
            fr = MEDIA / "frames" / f
            fr.mkdir(parents=True, exist_ok=True)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(out), "-vf", "fps=1/4",
                            str(fr / "%03d.png")], check=True)
    lst = MEDIA / f"ep01_{folder}.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in parts))
    final = MEDIA / f"ep01_{folder}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-c", "copy", str(final)], check=True)
    print(f"Episode assembled: {final}")


if __name__ == "__main__":
    sys.exit(main())
