#!/usr/bin/env python3
"""Render nanohttp, gitlet, kontainer, pipecraft as animated terminal GIFs."""

from PIL import Image, ImageDraw, ImageFont
import os

FONT  = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 13)
FONTB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf', 13)
LH    = 20
PAD_X = 24
PAD_Y = 18
WIDTH = 760

BG     = (10, 10, 10)
DIM    = (70, 70, 70)
TEXT   = (180, 180, 180)
ACCENT = (200, 255, 0)
GREEN  = (80, 200, 80)
CYAN   = (80, 210, 210)
RED    = (220, 80, 80)
YELLOW = (220, 180, 50)
WHITE  = (220, 220, 220)
PURPLE = (180, 100, 220)
ORANGE = (220, 140, 50)
BLUE   = (80, 140, 220)
GRAY   = (110, 110, 110)


def make_gif(script, out_path, fixed_lines=14):
    """script = list of (lines, hold_ms). lines = list of (text, color)."""
    FIXED_H = PAD_Y * 2 + fixed_lines * LH

    frames, durations = [], []
    for lines, hold in script:
        img = Image.new('RGB', (WIDTH, FIXED_H), BG)
        d   = ImageDraw.Draw(img)
        for i, (text, color) in enumerate(lines):
            y = PAD_Y + i * LH
            # spans can live in either field depending on how the line was built
            spans = color if (isinstance(color, list) and len(color) > 0) \
                    else (text if isinstance(text, list) else None)
            if spans:
                x = PAD_X
                for seg, c in spans:
                    d.text((x, y), seg, font=FONT, fill=c)
                    x += int(FONT.getlength(seg))
            elif text:
                d.text((PAD_X, y), text, font=FONT, fill=color)
        frames.append(img)
        durations.append(hold)

    frames[0].save(
        out_path, save_all=True, append_images=frames[1:],
        duration=durations, loop=0, optimize=True,
    )
    kb = os.path.getsize(out_path) // 1024
    print(f'  {out_path}  ({kb} KB, {len(frames)} frames)')


# ══════════════════════════════════════════════════════════════════════════════
# NANOHTTP — HTTP/1.1 + WebSocket + JWT + SSE
# ══════════════════════════════════════════════════════════════════════════════
print('nanohttp...')
make_gif([
    ([
        ('$ node index.js --port 3000', ACCENT),
        ('listening on :3000  (HTTP/1.1 · WebSocket · SSE · gzip)', GREEN),
        ('', TEXT),
    ], 500),
    ([
        ('$ node index.js --port 3000', ACCENT),
        ('listening on :3000  (HTTP/1.1 · WebSocket · SSE · gzip)', GREEN),
        ('', TEXT),
        ([('200', GREEN), ('  POST  ', TEXT), ('/auth/login', CYAN), ('                    +2ms', DIM)], []),
        ([('200', GREEN), ('  GET   ', TEXT), ('/api/user/42', CYAN), ('           gzip  ', DIM), ('  +4ms', DIM)], []),
    ], 300),
    ([
        ('listening on :3000  (HTTP/1.1 · WebSocket · SSE · gzip)', GREEN),
        ('', TEXT),
        ([('200', GREEN), ('  POST  ', TEXT), ('/auth/login', CYAN), ('                    +2ms', DIM)], []),
        ([('200', GREEN), ('  GET   ', TEXT), ('/api/user/42', CYAN), ('           gzip  ', DIM), ('  +4ms', DIM)], []),
        ([('101', YELLOW), ('  WS    ', TEXT), ('/chat', CYAN), ('    Switching Protocols     +1ms', DIM)], []),
        ('  ↑  frame[text]  "hello"', DIM),
        ('  ↓  frame[text]  "world"', DIM),
    ], 400),
    ([
        ('', TEXT),
        ([('200', GREEN), ('  POST  ', TEXT), ('/auth/login', CYAN), ('                    +2ms', DIM)], []),
        ([('200', GREEN), ('  GET   ', TEXT), ('/api/user/42', CYAN), ('           gzip  ', DIM), ('  +4ms', DIM)], []),
        ([('101', YELLOW), ('  WS    ', TEXT), ('/chat', CYAN), ('    Switching Protocols     +1ms', DIM)], []),
        ('  ↑  frame[text]  "hello"', DIM),
        ('  ↓  frame[text]  "world"', DIM),
        ([('200', GREEN), ('  GET   ', TEXT), ('/events', CYAN), ('   text/event-stream        +1ms', DIM)], []),
        ('  stream: event=tick data={"t":1}', DIM),
        ('  stream: event=tick data={"t":2}', DIM),
    ], 400),
    ([
        ([('200', GREEN), ('  POST  ', TEXT), ('/auth/login', CYAN), ('                    +2ms', DIM)], []),
        ([('101', YELLOW), ('  WS    ', TEXT), ('/chat', CYAN), ('    Switching Protocols     +1ms', DIM)], []),
        ('  ↑  frame[text]  "hello"', DIM),
        ('  ↓  frame[text]  "world"', DIM),
        ([('200', GREEN), ('  GET   ', TEXT), ('/events', CYAN), ('   text/event-stream        +1ms', DIM)], []),
        ('  stream: event=tick data={"t":1}', DIM),
        ('  stream: event=tick data={"t":2}', DIM),
        ('', TEXT),
        ([('401', RED), ('  GET   ', TEXT), ('/api/secret', CYAN), ('   invalid JWT              +1ms', DIM)], []),
        ([('200', GREEN), ('  GET   ', TEXT), ('/api/secret', CYAN), ('   HMAC-SHA256 ✓           +2ms', DIM)], []),
        ('', TEXT),
        ('  zero dependencies · built on net.createServer', DIM),
    ], 2200),
], 'assets/nanohttp.gif', fixed_lines=14)


# ══════════════════════════════════════════════════════════════════════════════
# GITLET — Git from scratch
# ══════════════════════════════════════════════════════════════════════════════
print('gitlet...')
make_gif([
    ([
        ('$ node gitlet.js init', ACCENT),
        ('initialized empty repository  →  .gitlet/', GREEN),
        ('', TEXT),
    ], 400),
    ([
        ('$ node gitlet.js init', ACCENT),
        ('initialized empty repository  →  .gitlet/', GREEN),
        ('', TEXT),
        ('$ node gitlet.js add src/app.js', ACCENT),
        ('$ node gitlet.js commit -m "initial commit"', ACCENT),
        ([('●  ', ACCENT), ('a4f2c31', YELLOW), ('  initial commit', TEXT)], []),
        ('', TEXT),
    ], 400),
    ([
        ('$ node gitlet.js commit -m "initial commit"', ACCENT),
        ([('●  ', ACCENT), ('a4f2c31', YELLOW), ('  initial commit', TEXT)], []),
        ('', TEXT),
        ('$ node gitlet.js add src/feature.js', ACCENT),
        ('$ node gitlet.js commit -m "add feature"', ACCENT),
        ([('●  ', ACCENT), ('19df353', YELLOW), ('  add feature', TEXT)], []),
        ([('│', DIM), ('', TEXT)], []),
        ([('●  ', DIM), ('a4f2c31', DIM), ('  initial commit', DIM)], []),
        ('', TEXT),
    ], 400),
    ([
        ([('●  ', ACCENT), ('19df353', YELLOW), ('  add feature         ', TEXT), ('← HEAD', CYAN)], []),
        ([('│', DIM), ('', TEXT)], []),
        ([('●  ', DIM), ('a4f2c31', DIM), ('  initial commit', DIM)], []),
        ('', TEXT),
        ('$ node gitlet.js branch fix/auth', ACCENT),
        ('$ node gitlet.js checkout fix/auth', ACCENT),
        ('$ node gitlet.js commit -m "fix auth token"', ACCENT),
        ([('●  ', ACCENT), ('8c3e7fa', YELLOW), ('  fix auth token      ', TEXT), ('← fix/auth', PURPLE)], []),
        ([('│', DIM), ('', TEXT)], []),
        ([('●  ', DIM), ('19df353', DIM), ('  add feature', DIM)], []),
    ], 500),
    ([
        ('$ node gitlet.js checkout master', ACCENT),
        ('$ node gitlet.js merge fix/auth', ACCENT),
        ('', TEXT),
        ('  3-way merge  (LCS unified diff)', DIM),
        ([('  base: ', DIM), ('a4f2c31', YELLOW), ('  ours: ', DIM), ('19df353', YELLOW), ('  theirs: ', DIM), ('8c3e7fa', YELLOW)], []),
        ('', TEXT),
        ([('●  ', GREEN), ('f1b9e20', YELLOW), ('  merge fix/auth → master', TEXT)], []),
        ([('│\\', DIM), ('', TEXT)], []),
        ([('●  ', DIM), ('8c3e7fa', DIM), ('  fix auth token', DIM)], []),
        ([('│', DIM), ('', TEXT)], []),
        ([('●  ', DIM), ('19df353', DIM), ('  add feature', DIM)], []),
        ('', TEXT),
        ('  SHA-256 content-addressable store  ·  zero dependencies', DIM),
    ], 2200),
], 'assets/gitlet.gif', fixed_lines=14)


# ══════════════════════════════════════════════════════════════════════════════
# KONTAINER — Container runtime (Linux namespaces + cgroups)
# ══════════════════════════════════════════════════════════════════════════════
print('kontainer...')
make_gif([
    ([
        ('$ node kontainer.js run --mem 64m --cpu 50 sh', ACCENT),
        ('', TEXT),
        ('  creating namespaces:', DIM),
        ([('  user  ', CYAN), ('pid  ', CYAN), ('mount  ', CYAN), ('uts  ', CYAN), ('ipc', CYAN)], []),
    ], 400),
    ([
        ('$ node kontainer.js run --mem 64m --cpu 50 sh', ACCENT),
        ('', TEXT),
        ('  creating namespaces:', DIM),
        ([('  user  ', CYAN), ('pid  ', CYAN), ('mount  ', CYAN), ('uts  ', CYAN), ('ipc', CYAN)], []),
        ('  chroot /rootfs  →  isolated filesystem', DIM),
        ('  cgroup v2  memory.max=67108864  cpu.max=50000', DIM),
        ('  mapping uid 0 inside  →  unprivileged outside', DIM),
        ('', TEXT),
        ([('  [container] ', GREEN), ('$ ', ACCENT), ('hostname', TEXT)], []),
        ([('  ', TEXT), ('kontainer-7f3a', CYAN)], []),
    ], 500),
    ([
        ('  cgroup v2  memory.max=67108864  cpu.max=50000', DIM),
        ('  mapping uid 0 inside  →  unprivileged outside', DIM),
        ('', TEXT),
        ([('  [container] ', GREEN), ('$ ', ACCENT), ('ps aux', TEXT)], []),
        ('  PID  COMMAND', DIM),
        ([('    1  ', CYAN), ('sh', WHITE)], []),
        ('', TEXT),
        ([('  [container] ', GREEN), ('$ ', ACCENT), ('cat /etc/hostname', TEXT)], []),
        ([('  ', TEXT), ('kontainer-7f3a', CYAN)], []),
        ('', TEXT),
        ([('  [container] ', GREEN), ('$ ', ACCENT), ('exit', TEXT)], []),
    ], 500),
    ([
        ('', TEXT),
        ([('  [container] ', GREEN), ('$ ', ACCENT), ('exit', TEXT)], []),
        ('', TEXT),
        ('  cgroup  cleaned up', DIM),
        ('  namespaces  destroyed', DIM),
        ('  rootfs  unmounted', DIM),
        ('', TEXT),
        ('  no Docker · no root required · pure Node.js', ACCENT),
        ('  Linux user/pid/mount/uts/ipc namespaces  +  cgroup v2', DIM),
    ], 2200),
], 'assets/kontainer.gif', fixed_lines=12)


# ══════════════════════════════════════════════════════════════════════════════
# PIPECRAFT — CI/CD pipeline engine
# ══════════════════════════════════════════════════════════════════════════════
print('pipecraft...')

def job(status, name, duration='', note=''):
    if status == 'run':
        icon, col = '⟳', YELLOW
    elif status == 'ok':
        icon, col = '✓', GREEN
    elif status == 'fail':
        icon, col = '✗', RED
    elif status == 'wait':
        icon, col = '○', DIM
    else:
        icon, col = '·', DIM
    parts = [(f'  {icon}  ', col), (name.ljust(18), WHITE if status != 'wait' else DIM)]
    if duration:
        parts.append((duration.ljust(10), DIM))
    if note:
        parts.append((note, DIM))
    return (None, parts)

make_gif([
    ([
        ('$ node pipecraft.js run pipeline.yml', ACCENT),
        ('', TEXT),
        ('  pipeline: build-and-deploy  (6 jobs)', DIM),
        ('  dependency graph resolved  →  3 stages', DIM),
        ('', TEXT),
        job('run', 'lint',    ''),
        job('wait','test:unit'),
        job('wait','test:e2e'),
        job('wait','build'),
        job('wait','docker'),
        job('wait','deploy'),
    ], 400),
    ([
        ('$ node pipecraft.js run pipeline.yml', ACCENT),
        ('', TEXT),
        ('  pipeline: build-and-deploy  (6 jobs)', DIM),
        ('', TEXT),
        job('ok',  'lint',       '2.1s'),
        job('run', 'test:unit',  ''),
        job('run', 'test:e2e',   '', '  ← parallel'),
        job('wait','build'),
        job('wait','docker'),
        job('wait','deploy'),
    ], 400),
    ([
        ('$ node pipecraft.js run pipeline.yml', ACCENT),
        ('', TEXT),
        ('  pipeline: build-and-deploy  (6 jobs)', DIM),
        ('', TEXT),
        job('ok',  'lint',       '2.1s'),
        job('ok',  'test:unit',  '11.4s'),
        job('ok',  'test:e2e',   '14.8s'),
        job('run', 'build',      ''),
        job('wait','docker'),
        job('wait','deploy'),
    ], 400),
    ([
        ('', TEXT),
        ('  pipeline: build-and-deploy  (6 jobs)', DIM),
        ('', TEXT),
        job('ok',  'lint',       '2.1s'),
        job('ok',  'test:unit',  '11.4s'),
        job('ok',  'test:e2e',   '14.8s'),
        job('ok',  'build',      '8.2s',  '  artifacts: dist/'),
        job('run', 'docker',     ''),
        job('wait','deploy'),
    ], 300),
    ([
        ('', TEXT),
        ('  pipeline: build-and-deploy  (6 jobs)', DIM),
        ('', TEXT),
        job('ok',  'lint',       '2.1s'),
        job('ok',  'test:unit',  '11.4s'),
        job('ok',  'test:e2e',   '14.8s'),
        job('ok',  'build',      '8.2s',  '  artifacts: dist/'),
        job('ok',  'docker',     '22.7s', '  sha256:a3f9'),
        job('run', 'deploy',     ''),
    ], 300),
    ([
        ('', TEXT),
        ('  pipeline: build-and-deploy  (6 jobs)', DIM),
        ('', TEXT),
        job('ok',  'lint',       '2.1s'),
        job('ok',  'test:unit',  '11.4s'),
        job('ok',  'test:e2e',   '14.8s'),
        job('ok',  'build',      '8.2s',  '  artifacts: dist/'),
        job('ok',  'docker',     '22.7s', '  sha256:a3f9'),
        job('ok',  'deploy',     '3.1s',  '  → prod'),
        ('', TEXT),
        ([('  ✓  pipeline complete  ', GREEN), ('62.3s total', DIM), ('  ·  2 jobs ran in parallel', DIM)], []),
    ], 2200),
], 'assets/pipecraft.gif', fixed_lines=14)

print('Done.')
