#!/usr/bin/env python3
"""
Convert a video clip to an optimised GIF for the portfolio card hover effect.

Usage:
    python3 make_gif.py <input_video> <output_name> [start_sec] [end_sec]

Examples:
    python3 make_gif.py ~/Videos/evomind.mkv evomind 10 25
    python3 make_gif.py ~/Videos/eduhas.mp4 eduhas 5 20

Output: assets/<output_name>.gif
Settings: 15fps, 640px wide, 40 colours (dark UI looks great with 40)
"""

import cv2, sys, os, subprocess
from pathlib import Path

def make_gif(video_path, name, start=0, end=None, fps=15, width=640, colors=48):
    cap = cv2.VideoCapture(video_path)
    src_fps = cap.get(cv2.CAP_PROP_FPS)
    total = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    duration = total / src_fps
    end = end if end is not None else duration

    print(f"Source: {duration:.1f}s @ {src_fps:.1f}fps  →  extracting {start}s–{end}s")

    out_dir = Path("assets/_tmp_frames")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Clear old frames
    for f in out_dir.glob("*.png"):
        f.unlink()

    step = max(1, round(src_fps / fps))
    frame_num = 0
    saved = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        t = frame_num / src_fps
        if t < start:
            frame_num += 1
            continue
        if t > end:
            break
        if (frame_num - round(start * src_fps)) % step == 0:
            h, w = frame.shape[:2]
            new_h = int(h * width / w)
            resized = cv2.resize(frame, (width, new_h), interpolation=cv2.INTER_AREA)
            cv2.imwrite(str(out_dir / f"frame_{saved:04d}.png"), resized)
            saved += 1
        frame_num += 1

    cap.release()
    print(f"Extracted {saved} frames")

    out_gif = f"assets/{name}.gif"
    print(f"Converting to GIF → {out_gif}")
    cmd = [
        "convert",
        "-delay", str(round(100 / fps)),
        "-loop", "0",
        "-dither", "Riemersma",
        "-colors", str(colors),
        "-layers", "optimize",
        str(out_dir / "frame_*.png"),
        out_gif,
    ]
    subprocess.run(cmd, check=True)

    size_kb = os.path.getsize(out_gif) // 1024
    print(f"Done: {out_gif}  ({size_kb} KB)")

    # Cleanup
    for f in out_dir.glob("*.png"):
        f.unlink()
    out_dir.rmdir()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    video = sys.argv[1]
    name = sys.argv[2]
    start = float(sys.argv[3]) if len(sys.argv) > 3 else 0
    end = float(sys.argv[4]) if len(sys.argv) > 4 else None
    make_gif(video, name, start, end)
