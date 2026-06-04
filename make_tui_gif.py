#!/usr/bin/env python3
"""Render tui system monitor as an animated terminal GIF."""

from PIL import Image, ImageDraw, ImageFont
import math, random, os

random.seed(7)

FONT   = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 13)
FONTB  = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf', 13)
CW     = 8     # char width px (approx)
LH     = 19    # line height px
PAD    = 0

W, H   = 780, 420

BG      = (10, 10, 10)
BG2     = (18, 18, 18)
ACCENT  = (200, 255, 0)
DIM     = (70, 70, 70)
TEXT    = (180, 180, 180)
WHITE   = (220, 220, 220)
CYAN    = (80, 210, 210)
GREEN   = (80, 200, 80)
YELLOW  = (220, 180, 50)
GRAY    = (100, 100, 100)
BORDER  = (45, 45, 45)
SEL_BG  = (30, 50, 10)

def img():
    i = Image.new('RGB', (W, H), BG)
    return i, ImageDraw.Draw(i)

def ch(draw, x, y, text, color=TEXT, bold=False):
    draw.text((x, y), text, font=FONTB if bold else FONT, fill=color)

def hline(draw, y, x1=0, x2=None, color=BORDER):
    draw.line([(x1, y), (x2 or W, y)], fill=color)

def vline(draw, x, y1, y2, color=BORDER):
    draw.line([(x, y1), (x, y2)], fill=color)

def box(draw, x, y, w, h, title='', color=BORDER):
    draw.rectangle([x, y, x+w, y+h], outline=color)
    if title:
        tx = x + 8
        draw.rectangle([tx-2, y-1, tx + len(title)*CW + 2, y+1], fill=BG)
        ch(draw, tx, y - LH//2, title, color)

def bar(draw, x, y, w, pct, color=GREEN, bg=(30,30,30)):
    draw.rectangle([x, y, x+w, y+LH-4], fill=bg)
    fill_w = int(w * pct / 100)
    if fill_w > 0:
        draw.rectangle([x, y, x+fill_w, y+LH-4], fill=color)
    label = f'{pct}%'
    ch(draw, x+w+6, y, label, TEXT)

def sparkline(draw, x, y, w, data, color=ACCENT):
    if not data or max(data) == 0:
        return
    step = w / len(data)
    maxv = max(data) or 1
    pts = []
    for i, v in enumerate(data):
        px = x + int(i * step)
        py = y + 14 - int(v / maxv * 14)
        pts.append((px, py))
    if len(pts) > 1:
        draw.line(pts, fill=color, width=1)

def titlebar(draw, tab_idx):
    draw.rectangle([0, 0, W, LH+4], fill=BG2)
    ch(draw, 10, 4, '  tui — system monitor  ', ACCENT, bold=True)
    ch(draw, W-140, 4, 'uptime 00:04:17', GRAY)
    # tabs
    tabs = ['System', 'Processes', 'Disks', 'Help']
    tx = 10
    ty = LH + 8
    for i, t in enumerate(tabs):
        tw = len(t)*CW + 16
        active = (i == tab_idx)
        bg = BG if active else BG2
        draw.rectangle([tx, ty, tx+tw, ty+LH+2], fill=bg)
        color = ACCENT if active else DIM
        ch(draw, tx+8, ty+3, t, color, bold=active)
        tx += tw + 2
    hline(draw, ty+LH+3, color=BORDER)

def footer(draw, tab_idx):
    draw.rectangle([0, H-LH-4, W, H], fill=BG2)
    parts = ['[q] quit', '[←/→] tabs', '[1-4] jump tab']
    if tab_idx == 1:
        parts += ['[Tab] focus', '[↑↓] select', '[k] kill']
    txt = '  ' + '  ·  '.join(parts)
    ch(draw, 8, H-LH-1, txt, DIM)

CONTENT_Y = LH*2 + 16

# ── SYSTEM TAB ────────────────────────────────────────────────────────────────

def render_system(cpu_hist, mem_hist, cpu_now, mem_now):
    i, d = img()
    titlebar(d, 0)
    footer(d, 0)

    half = W // 2 - 10
    # CPU box
    box(d, 8, CONTENT_Y, half, 110, 'CPU', CYAN)
    cpu_color = (220,80,80) if cpu_now > 80 else (YELLOW if cpu_now > 50 else GREEN)
    bar(d, 18, CONTENT_Y+18, half-28, cpu_now, cpu_color)
    ch(d, 18, CONTENT_Y+38, f'Current: {cpu_now}%  Cores: 4', DIM)
    sparkline(d, 18, CONTENT_Y+58, half-28, cpu_hist, CYAN)
    ch(d, 18, CONTENT_Y+80, 'Intel Core i5-6300U @ 2.40GHz', DIM)

    # Memory box
    mx = half + 20
    mw = W - mx - 12
    box(d, mx, CONTENT_Y, mw, 110, 'Memory', CYAN)
    bar(d, mx+10, CONTENT_Y+18, mw-28, mem_now, CYAN)
    used_gb = mem_now * 7.6 / 100
    ch(d, mx+10, CONTENT_Y+38, f'Used: {used_gb:.1f} GB / 7.6 GB', DIM)
    sparkline(d, mx+10, CONTENT_Y+58, mw-28, mem_hist, CYAN)
    ch(d, mx+10, CONTENT_Y+80, f'Free: {7.6 - used_gb:.1f} GB', DIM)

    # System info box
    iw = int(W * 0.55) - 10
    iy = CONTENT_Y + 122
    box(d, 8, iy, iw, 100, 'System Info', DIM)
    for j, line in enumerate([
        'OS:       Linux 6.18.7-pop',
        'Hostname: pop-os',
        'Arch:     x86_64   Platform: linux',
        'Uptime:   00:04:17',
    ]):
        ch(d, 18, iy + 14 + j*LH, line, WHITE)

    # Load average box
    lx = iw + 18
    lw = W - lx - 12
    box(d, lx, iy, lw, 100, 'Load Average', DIM)
    loads = [0.8, 1.2, 1.5]
    lbls  = ['1 min', '5 min', '15 min']
    for j, (lv, lb) in enumerate(zip(loads, lbls)):
        lc = (220,80,80) if lv > 3 else (YELLOW if lv > 2 else GREEN)
        bar(d, lx+10, iy + 14 + j*26, lw-60, int(lv/4*100), lc, (25,25,25))
        ch(d, lx+10, iy + 14 + j*26 - 1, lb, DIM)
        ch(d, lx+lw-52, iy + 14 + j*26, f'{lv:.1f}', lc)

    return i

# ── PROCESSES TAB ─────────────────────────────────────────────────────────────

PROCS = [
    (1000, 'systemd',       0.1, 0.5),
    (1037, 'kworker',       2.1, 0.1),
    (1074, 'sshd',          0.0, 0.2),
    (1111, 'nginx',         1.4, 1.2),
    (1148, 'postgres',      3.2, 4.1),
    (1185, 'redis-server',  0.8, 0.9),
    (1222, 'node',          8.5, 3.2),
    (1259, 'python3',       5.1, 2.4),
    (1296, 'bash',          0.0, 0.1),
    (1333, 'vim',           0.1, 0.3),
    (1370, 'chrome',       12.4, 5.8),
    (1407, 'firefox',       7.2, 4.2),
    (1444, 'electron',      9.8, 3.7),
    (1481, 'docker',        1.1, 1.5),
    (1518, 'containerd',    0.5, 0.8),
]

def render_processes(selected=3, filter_text=''):
    i, d = img()
    titlebar(d, 1)
    footer(d, 1)

    cy = CONTENT_Y
    ch(d, 8, cy, 'Filter processes:', DIM)
    # Filter input box
    iw = 300
    draw_c = ACCENT if not filter_text else GREEN
    d.rectangle([8, cy+LH, 8+iw, cy+LH*2], outline=draw_c)
    ch(d, 14, cy+LH+3, filter_text if filter_text else 'type to filter...', DIM if not filter_text else WHITE)

    # Header
    hy = cy + LH*2 + 8
    ch(d, 8,   hy, 'PID    ', ACCENT, bold=True)
    ch(d, 66,  hy, 'NAME              ', ACCENT, bold=True)
    ch(d, 234, hy, 'CPU%    ', ACCENT, bold=True)
    ch(d, 306, hy, 'MEM%', ACCENT, bold=True)
    hline(d, hy+LH, x1=8, x2=W-8, color=BORDER)

    procs = [p for p in PROCS if not filter_text or filter_text.lower() in p[1]]
    for j, (pid, name, cpu, mem) in enumerate(procs[:12]):
        py = hy + LH + 4 + j * LH
        if j == selected:
            d.rectangle([8, py-2, W-8, py+LH-2], fill=SEL_BG)
        col = WHITE if j == selected else TEXT
        ch(d, 8,   py, str(pid).ljust(6), col)
        ch(d, 66,  py, name.ljust(18),    col)
        cc = (220,80,80) if cpu > 10 else (YELLOW if cpu > 5 else TEXT)
        ch(d, 234, py, f'{cpu:.1f}'.ljust(7), cc if j != selected else WHITE)
        ch(d, 306, py, f'{mem:.1f}', col)

    return i

# ── DISKS TAB ─────────────────────────────────────────────────────────────────

DISKS = [
    ('/',     62, '118.2 GB', '45.3 GB',  '193.1 GB'),
    ('/tmp',  12, '1.2 GB',   '8.9 GB',   '10.2 GB'),
    ('/home', 48, '89.4 GB',  '96.8 GB',  '186.2 GB'),
]

def render_disks():
    i, d = img()
    titlebar(d, 2)
    footer(d, 2)

    ch(d, 8, CONTENT_Y, 'Disk Usage', ACCENT, bold=True)
    cy = CONTENT_Y + LH + 4

    for mp, pct, used, free, total in DISKS:
        box(d, 8, cy, W-16, 80, mp, DIM)
        color = (220,80,80) if pct > 90 else (YELLOW if pct > 70 else GREEN)
        bar(d, 18, cy+16, 460, pct, color)
        ch(d, 18, cy+38, f'Used: {used}  Free: {free}  Total: {total}', DIM)
        # Gauge on right
        gx = 510
        d.rectangle([gx, cy+14, gx+200, cy+34], fill=(25,25,25))
        d.rectangle([gx, cy+14, gx+int(200*pct/100), cy+34], fill=color)
        ch(d, gx+208, cy+16, f'{pct}% used', color)
        cy += 90

    return i

# ── COMPOSE FRAMES ────────────────────────────────────────────────────────────

frames, durations = [], []

def add(frame, ms):
    frames.append(frame)
    durations.append(ms)

# Simulate evolving CPU/memory history
cpu_hist = [random.randint(15, 55) for _ in range(40)]
mem_hist = [random.randint(60, 72) for _ in range(40)]

# 1. System tab — several ticks showing live sparkline
for tick in range(8):
    cpu_now = random.randint(18, 65)
    mem_now = random.randint(61, 74)
    cpu_hist = cpu_hist[1:] + [cpu_now]
    mem_hist = mem_hist[1:] + [mem_now]
    hold = 150 if tick < 7 else 600
    add(render_system(cpu_hist, mem_hist, cpu_now, mem_now), hold)

# 2. Switch to Processes tab — browse
add(render_processes(selected=0), 400)
for sel in range(1, 6):
    add(render_processes(selected=sel), 180)
add(render_processes(selected=5), 500)

# 3. Type filter
add(render_processes(selected=0, filter_text='n'), 180)
add(render_processes(selected=0, filter_text='no'), 180)
add(render_processes(selected=0, filter_text='nod'), 280)
add(render_processes(selected=0, filter_text='node'), 600)

# 4. Switch to Disks tab
add(render_disks(), 1800)

# 5. Back to System tab
cpu_hist2 = cpu_hist[:]
mem_hist2 = mem_hist[:]
for tick in range(4):
    cpu_now = random.randint(20, 60)
    mem_now = random.randint(62, 75)
    cpu_hist2 = cpu_hist2[1:] + [cpu_now]
    mem_hist2 = mem_hist2[1:] + [mem_now]
    add(render_system(cpu_hist2, mem_hist2, cpu_now, mem_now), 200)

print(f'Total frames: {len(frames)}')

out = '/home/xo/portfolio/assets/tui.gif'
frames[0].save(
    out, save_all=True, append_images=frames[1:],
    duration=durations, loop=0, optimize=True,
)
print(f'Saved: {out}  ({os.path.getsize(out)//1024} KB)')
