#!/usr/bin/env python3
"""Render distkv distributed KV store demo as an animated terminal GIF."""

from PIL import Image, ImageDraw, ImageFont
import os

FONT  = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 13)
FONTB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf', 13)
LH    = 20
PAD_X = 24
PAD_Y = 18
WIDTH = 760

BG      = (10, 10, 10)
DIM     = (70, 70, 70)
TEXT    = (180, 180, 180)
ACCENT  = (200, 255, 0)
GREEN   = (80, 200, 80)
CYAN    = (80, 210, 210)
RED     = (220, 80, 80)
YELLOW  = (220, 180, 50)
WHITE   = (220, 220, 220)
GRAY    = (110, 110, 110)

FIXED_H = PAD_Y * 2 + 14 * LH   # tall enough for longest frame

def render(lines):
    img = Image.new('RGB', (WIDTH, FIXED_H), BG)
    d   = ImageDraw.Draw(img)

    for i, (text, color) in enumerate(lines):
        y = PAD_Y + i * LH
        # Handle mixed-color segments (list of (str, color))
        if isinstance(color, list):
            x = PAD_X
            for seg, c in color:
                d.text((x, y), seg, font=FONT, fill=c)
                x += int(FONT.getlength(seg))
        else:
            d.text((PAD_X, y), text, font=FONT, fill=color)

    return img

# ── Script ────────────────────────────────────────────────────────────────────

def spans(parts):
    """parts = [(text, color), ...]"""
    return parts   # render() handles lists

SCRIPT = [
    # (lines_to_show, hold_ms)

    # ── Server startup ────────────────────────────────────────────────────────
    ([
        ('$ node server/index.js --port 6379 --replicas 2', ACCENT),
    ], 400),
    ([
        ('$ node server/index.js --port 6379 --replicas 2', ACCENT),
        ('', TEXT),
        ('[primary]  listening on :6379', GREEN),
        ('[replica-001]  listening on :6380', CYAN),
        ('[replica-002]  listening on :6381', CYAN),
        ('[WAL]  write-ahead log ready  →  wal.log', DIM),
        ('', TEXT),
    ], 700),

    # ── Client connects + PING ────────────────────────────────────────────────
    ([
        ('$ node server/index.js --port 6379 --replicas 2', ACCENT),
        ('', TEXT),
        ('[primary]  listening on :6379', GREEN),
        ('[replica-001]  listening on :6380', CYAN),
        ('[replica-002]  listening on :6381', CYAN),
        ('[WAL]  write-ahead log ready  →  wal.log', DIM),
        ('', TEXT),
        ('$ node client.js', ACCENT),
        ('connected to primary :6379', DIM),
        ('', TEXT),
        ('> PING', TEXT),
        ('+PONG', GREEN),
    ], 500),

    # ── SET commands + WAL flush ──────────────────────────────────────────────
    ([
        ('$ node client.js', ACCENT),
        ('connected to primary :6379', DIM),
        ('', TEXT),
        ('> PING', TEXT),
        ('+PONG', GREEN),
        ('', TEXT),
        ('> SET user:1 "Abdul Hadi Khan"', TEXT),
    ], 250),
    ([
        ('> PING', TEXT),
        ('+PONG', GREEN),
        ('', TEXT),
        ('> SET user:1 "Abdul Hadi Khan"', TEXT),
        ('[WAL]  append  SET user:1  →  offset 1', DIM),
        ('[replica-001]  ✓  replicated offset 1', CYAN),
        ('[replica-002]  ✓  replicated offset 1', CYAN),
        ('+OK', GREEN),
        ('', TEXT),
        ('> SET user:2 "Istanbul, Turkey"', TEXT),
    ], 250),
    ([
        ('> SET user:1 "Abdul Hadi Khan"', TEXT),
        ('[WAL]  append  SET user:1  →  offset 1', DIM),
        ('[replica-001]  ✓  replicated offset 1', CYAN),
        ('[replica-002]  ✓  replicated offset 1', CYAN),
        ('+OK', GREEN),
        ('', TEXT),
        ('> SET user:2 "Istanbul, Turkey"', TEXT),
        ('[WAL]  append  SET user:2  →  offset 2', DIM),
        ('[replica-001]  ✓  replicated offset 2', CYAN),
        ('[replica-002]  ✓  replicated offset 2', CYAN),
        ('+OK', GREEN),
        ('', TEXT),
        ('> GET user:1', TEXT),
        ('"Abdul Hadi Khan"', ACCENT),
        ('', TEXT),
        ('> GET user:2', TEXT),
        ('"Istanbul, Turkey"', ACCENT),
    ], 700),

    # ── SIGKILL + WAL replay ──────────────────────────────────────────────────
    ([
        ('[WAL]  append  SET user:2  →  offset 2', DIM),
        ('[replica-001]  ✓  replicated offset 2', CYAN),
        ('[replica-002]  ✓  replicated offset 2', CYAN),
        ('+OK', GREEN),
        ('', TEXT),
        ('> GET user:1', TEXT),
        ('"Abdul Hadi Khan"', ACCENT),
        ('', TEXT),
        ('$ kill -9 $(pgrep -f "index.js")', YELLOW),
        ('[primary]  SIGKILL received — process terminated', RED),
    ], 500),
    ([
        ('+OK', GREEN),
        ('', TEXT),
        ('$ kill -9 $(pgrep -f "index.js")', YELLOW),
        ('[primary]  SIGKILL received — process terminated', RED),
        ('', TEXT),
        ('$ node server/index.js --port 6379 --replicas 2', ACCENT),
        ('[primary]  restarting...', DIM),
        ('[WAL]  replaying wal.log  (2 entries)', YELLOW),
        ('[WAL]  ✓  offset 1  SET user:1', GREEN),
        ('[WAL]  ✓  offset 2  SET user:2', GREEN),
        ('[WAL]  replay complete  —  2 keys recovered', ACCENT),
        ('[primary]  listening on :6379', GREEN),
    ], 900),

    # ── Benchmark ─────────────────────────────────────────────────────────────
    ([
        ('[WAL]  replay complete  —  2 keys recovered', ACCENT),
        ('[primary]  listening on :6379', GREEN),
        ('', TEXT),
        ('$ node bench.js --pipeline 64', ACCENT),
        ('', TEXT),
        ('  PING   19,312 ops/sec  (pipeline=64)', ACCENT),
        ('  SET     7,240 ops/sec  (WAL flush + 2-replica fan-out)', CYAN),
        ('  GET    14,891 ops/sec', TEXT),
        ('', TEXT),
        ('  latency p50=0.18ms  p99=1.2ms', DIM),
    ], 2000),
]

frames, durations = [], []
for lines, hold in SCRIPT:
    frames.append(render(lines))
    durations.append(hold)

print(f'Total frames: {len(frames)}')

out = '/home/xo/portfolio/assets/distkv.gif'
frames[0].save(
    out, save_all=True, append_images=frames[1:],
    duration=durations, loop=0, optimize=True,
)
print(f'Saved: {out}  ({os.path.getsize(out)//1024} KB)')
