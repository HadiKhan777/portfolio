#!/usr/bin/env python3
"""Render neuralkit training output as an animated terminal GIF."""

from PIL import Image, ImageDraw, ImageFont
import os

FONT_PATH = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
FONT_SIZE = 14
PAD_X, PAD_Y = 28, 22
LINE_H = 22
WIDTH = 720

BG      = (10, 10, 10)
DIM     = (80, 80, 80)
TEXT    = (180, 180, 180)
ACCENT  = (200, 255, 0)    # lime
GREEN   = (100, 200, 80)
CYAN    = (80, 200, 200)
WHITE   = (220, 220, 220)

font      = ImageFont.truetype(FONT_PATH, FONT_SIZE)
font_bold = ImageFont.truetype(FONT_PATH, FONT_SIZE)

def color_line(text):
    """Return list of (text, color) spans for a line."""
    if text.startswith('  neuralkit'):
        return [(text, ACCENT)]
    if '──' in text:
        return [(text, DIM)]
    if text.strip().startswith('epoch'):
        parts = []
        # parse: "  epoch   1/80  loss=X  val_acc=Y  [bar]  lr=Z"
        import re
        m = re.match(r'(\s*epoch\s+\d+/\d+\s+)(loss=[\d.]+\s+)(val_acc=[\d.]+\s+)(\[)(█+)(░*)(\])(.*)', text)
        if m:
            parts = [
                (m.group(1), DIM),
                (m.group(2), TEXT),
                (m.group(3), CYAN),
                (m.group(4), DIM),
                (m.group(5), ACCENT),
                (m.group(6), (40, 40, 40)),
                (m.group(7), DIM),
                (m.group(8), DIM),
            ]
            return parts
        return [(text, TEXT)]
    if 'Accuracy' in text or 'val_acc' in text:
        return [(text, GREEN)]
    if any(k in text for k in ['Precision', 'Recall', 'F1']):
        return [(text, TEXT)]
    if text.strip().startswith('Dense') or text.strip().startswith('BatchNorm') or text.strip().startswith('ReLU'):
        import re
        m = re.match(r'(\s+)(\S+\(.*?\))(\s+)([\d,]+)', text)
        if m:
            return [(m.group(1), TEXT), (m.group(2), CYAN), (m.group(3)+m.group(4), DIM)]
    if 'Total' in text:
        return [(text, ACCENT)]
    if 'Final results' in text:
        return [(text, ACCENT)]
    if 'Layer' in text and 'Params' in text:
        return [(text, DIM)]
    if 'Confusion Matrix' in text:
        return [(text, ACCENT)]
    if 'Training curves' in text:
        return [(text, ACCENT)]
    if text.strip().startswith('loss') or text.strip().startswith('val_acc'):
        # sparkline rows
        if '▂▃▁' in text or '████' in text or 'min=' in text:
            return [(text, DIM)]
    if '████' in text or '▂▃' in text:
        parts = []
        for ch in text:
            if ch in '█▇▆▅▄':
                parts.append((ch, ACCENT))
            elif ch in '▂▃▁░':
                parts.append((ch, DIM))
            else:
                parts.append((ch, DIM))
        return parts
    return [(text, TEXT)]


def render_frame(lines, highlight_last=0):
    """Render a list of text lines to a PIL Image."""
    h = PAD_Y * 2 + max(len(lines), 1) * LINE_H
    img = Image.new('RGB', (WIDTH, h), BG)
    draw = ImageDraw.Draw(img)

    for i, line in enumerate(lines):
        y = PAD_Y + i * LINE_H
        spans = color_line(line)
        x = PAD_X
        for text, color in spans:
            if not text:
                continue
            draw.text((x, y), text, font=font, fill=color)
            x += font.getlength(text)

    return img


# ── Build the script ─────────────────────────────────────────────────────────

HEADER = [
    '',
    '  neuralkit — spiral / default / 80 epochs',
    '',
    '  Layer                    Params',
    '  ────────────────────── ────────',
    '  Dense(2, 64)                192',
    '  BatchNorm1d(64)             128',
    '  ReLU()                        0',
    '  Dense(64, 64)             4,160',
    '  BatchNorm1d(64)             128',
    '  ReLU()                        0',
    '  Dense(64, 3)                195',
    '  ──────────────────────────────',
    '  Total                     4,803',
    '',
]

EPOCHS = [
    '  epoch    1/80  loss=0.7022  val_acc=0.6778  [█████████████░░░░░░░]  lr=3.00e-03',
    '  epoch    8/80  loss=0.2847  val_acc=0.9444  [██████████████████░░]  lr=2.93e-03',
    '  epoch   16/80  loss=0.2277  val_acc=0.9778  [███████████████████░]  lr=2.72e-03',
    '  epoch   24/80  loss=0.3377  val_acc=0.9556  [███████████████████░]  lr=2.39e-03',
    '  epoch   32/80  loss=0.1806  val_acc=0.9778  [███████████████████░]  lr=1.97e-03',
    '  epoch   40/80  loss=0.2228  val_acc=0.9667  [███████████████████░]  lr=1.52e-03',
    '  epoch   48/80  loss=0.2238  val_acc=0.9667  [███████████████████░]  lr=1.06e-03',
    '  epoch   56/80  loss=0.2223  val_acc=0.9778  [███████████████████░]  lr=6.42e-04',
    '  epoch   64/80  loss=0.2815  val_acc=0.9778  [███████████████████░]  lr=3.14e-04',
    '  epoch   72/80  loss=0.1679  val_acc=0.9778  [███████████████████░]  lr=1.03e-04',
    '  epoch   80/80  loss=0.2286  val_acc=0.9778  [███████████████████░]  lr=3.00e-05',
]

RESULTS = [
    '',
    '  ── Final results ──────────────────────────────────',
    '  Accuracy   0.9778  (97.8%)',
    '  Precision  0.9761  (macro avg)',
    '  Recall     0.9787  (macro avg)',
    '  F1         0.9771  (macro avg)',
    '',
    '  Confusion Matrix',
    '',
    '       0      1      2  ',
    '  ─────────────────────────',
    '  0    51     0      1  ',
    '  1    3      64     0  ',
    '  2    0      0      61 ',
    '',
    '  Training curves (80 epochs)',
    '',
    '  loss     min=0.1586  final=0.2286',
    '  ────────────────────────────────────────────────────────',
    '  ▂▃▂▂▂▂▁▁▂▂▂▁▂▂▂▁▂▂▂▁▁▁▁▁▂▂▂▁▁▁▁▁▁▂▂▁▁▂▁▂▁▁▂▁▂▂▁▁▂▁▂▁▁▂▂▂',
    '',
    '  val_acc  min=0.6778  final=0.9778',
    '  ────────────────────────────────────────────────────────',
    '  ████▇███████████████████████████████████████████████████',
    '',
]

# ── Compose frames ────────────────────────────────────────────────────────────
frames, durations = [], []

def add(lines, hold_ms):
    frames.append(render_frame(lines))
    durations.append(hold_ms)

# 1. Header fades in (hold 1.2s)
add(HEADER, 1200)

# 2. Epoch 1 appears (slow — show the partial bar)
for i, epoch_line in enumerate(EPOCHS):
    lines = HEADER + EPOCHS[:i+1]
    hold = 120 if i < len(EPOCHS) - 1 else 600
    add(lines, hold)

# 3. Final results appear line by line
base = HEADER + EPOCHS
for i in range(1, len(RESULTS) + 1):
    hold = 80 if i < len(RESULTS) else 2500
    add(base + RESULTS[:i], hold)

# 4. Hold final frame then loop back (handled by loop=0)

print(f"Total frames: {len(frames)}")

# ── Save GIF ──────────────────────────────────────────────────────────────────
out = '/home/xo/portfolio/assets/neuralkit.gif'
frames[0].save(
    out,
    save_all=True,
    append_images=frames[1:],
    duration=durations,
    loop=0,
    optimize=True,
)
size_kb = os.path.getsize(out) // 1024
print(f"Saved: {out}  ({size_kb} KB)")
