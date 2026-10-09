TIMING = __TIMING__
"""Markazly target video #1 — 'Administratoringiz hisobotni to'g'ri qilyaptimi?'  1080x1920, 30fps, ovozsiz (keyin ovoz qo'shiladi)."""
import os, io, math, subprocess, sys
import cairosvg
from PIL import Image

B = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "brand")
os.chdir(B)
src = open("make_stories.py").read().split("# ───────────────────────── 1. Tariflar")[0].replace("os.path.dirname(os.path.abspath(__file__))", repr(os.getcwd()))
exec(src)
OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out"); os.makedirs(OUTDIR, exist_ok=True)
import sys; sys.path.insert(0, os.path.dirname(OUTDIR))
from importlib import import_module as _im
_tm = _im(TIMING); globals().update({k: getattr(_tm, k) for k in dir(_tm) if not k.startswith('__')})
FPS = 30
W, H = 1080, 1920
BOARD = "#0D2620"
defs = DEFS.replace("</defs>",
    '<radialGradient id="l1" cx="50%" cy="30%" r="60%"><stop offset="0%" stop-color="#2EE59D" stop-opacity=".16"/><stop offset="100%" stop-color="#2EE59D" stop-opacity="0"/></radialGradient>'
    '<radialGradient id="l2" cx="50%" cy="85%" r="55%"><stop offset="0%" stop-color="#1FB5C8" stop-opacity=".14"/><stop offset="100%" stop-color="#1FB5C8" stop-opacity="0"/></radialGradient>'
    '<radialGradient id="rd" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#FF7A6B" stop-opacity=".28"/><stop offset="100%" stop-color="#FF7A6B" stop-opacity="0"/></radialGradient>'
    '<radialGradient id="halo" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#2EE59D" stop-opacity=".35"/><stop offset="100%" stop-color="#2EE59D" stop-opacity="0"/></radialGradient>'
    '<linearGradient id="amb" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#F6C76B"/><stop offset="100%" stop-color="#E8873D"/></linearGradient>'
    '<linearGradient id="best" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#0F4A35"/><stop offset="100%" stop-color="#0E2219"/></linearGradient>'
    '</defs>')

def svg(body, w=W, h=H):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{defs}{body}</svg>'
def raster(body):
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg(body).encode()))).convert("RGBA")

grid = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="#E8F5EF" stroke-opacity=".04" stroke-width="2"/>' for x in range(0, W + 1, 40))
grid += "".join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="#E8F5EF" stroke-opacity=".04" stroke-width="2"/>' for y in range(0, H + 1, 40))
BG = raster(f'<rect width="{W}" height="{H}" fill="{BOARD}"/>{grid}<rect width="{W}" height="{H}" fill="url(#l1)"/><rect width="{W}" height="{H}" fill="url(#l2)"/>')

def ease(x): x = max(0, min(1, x)); return 1 - (1 - x) ** 3

class El:
    def __init__(self, body, t_in, t_out, dy=40, dur=.45, pop=False, bob=0, fo=.3, jit=None):
        im = raster(body); bb = im.getbbox() or (0, 0, 1, 1)
        self.im, self.x, self.y = im.crop(bb), bb[0], bb[1]
        self.t_in, self.t_out, self.dy, self.dur, self.pop, self.bob, self.fo, self.jit = t_in, t_out, dy, dur, pop, bob, fo, jit
    def draw(self, fr, t):
        if t < self.t_in or t > self.t_out: return
        a = (ease((t - self.t_in) / self.dur) if self.dur > 0 else 1) * ((1 - ease((t - (self.t_out - self.fo)) / self.fo)) if t > self.t_out - self.fo else 1)
        if a <= 0: return
        k = ease((t - self.t_in) / self.dur) if self.dur > 0 else 1
        im = self.im; x, y = self.x, self.y + (1 - k) * self.dy
        if self.pop:
            s = .85 + .15 * k + .04 * math.sin(min(1, (t - self.t_in) / .5) * math.pi)
            nw, nh = max(1, int(im.width * s)), max(1, int(im.height * s))
            x += (im.width - nw) / 2; y += (im.height - nh) / 2
            im = im.resize((nw, nh), Image.BILINEAR)
        if self.bob: y += self.bob * math.sin((t - self.t_in) * 2 * math.pi * 1.4)
        if self.jit and self.jit[0] <= t <= self.jit[1]: x += 14 * math.sin(t * 157); y += 6 * math.cos(t * 211)
        if a < 1:
            al = im.getchannel("A").point(lambda v: int(v * a)); im = im.copy(); im.putalpha(al)
        fr.alpha_composite(im, (int(round(x)), int(round(y))))

E = []
def add(*a, **k): E.append(El(*a, **k))
CX = W / 2

# persistent small brand row at the top
mk = 64; mkw = mk * 342 / 377
lw = mkw + 14 + SEMI.width("Markazly", 44)
lx = CX - lw / 2
brand = f'<image href="{MARK}" x="{lx}" y="210" width="{mkw:.0f}" height="{mk}"/>' + T("Markaz", lx + mkw + 14, 258, 44, SEMI, FG) + T("ly", lx + mkw + 14 + SEMI.width("Markaz", 44), 258, 44, SEMI, "url(#gh)")
add(brand, -1, DUR + 1, dy=0)

AMB = "#F6C76B"

class Dyn:
    """Element drawn by a python function each frame: fn(frame, t)."""
    def __init__(self, fn, t_in, t_out): self.fn, self.t_in, self.t_out = fn, t_in, t_out
    def draw(self, fr, t):
        if self.t_in <= t <= self.t_out: self.fn(fr, t)
def dyn(fn, t_in, t_out): E.append(Dyn(fn, t_in, t_out))
_txt_cache = {}
def text_img(txt, size, face, fill):
    k = (txt, size, id(face), fill)
    if k not in _txt_cache:
        im = raster(T(txt, 10, size + 10, size, face, fill)); bb = im.getbbox() or (0, 0, 1, 1); _txt_cache[k] = im.crop((0, 0, bb[2] + 4, bb[3] + 8))
    return _txt_cache[k]
def crop_el(body):
    im = raster(body); bb = im.getbbox() or (0, 0, 1, 1); return im.crop(bb), bb[0], bb[1]
