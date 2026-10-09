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
from timing3 import *
FPS = 30
W, H = 1080, 1920
BOARD = "#0D2620"
defs = DEFS.replace("</defs>",
    '<radialGradient id="l1" cx="50%" cy="30%" r="60%"><stop offset="0%" stop-color="#2EE59D" stop-opacity=".16"/><stop offset="100%" stop-color="#2EE59D" stop-opacity="0"/></radialGradient>'
    '<radialGradient id="l2" cx="50%" cy="85%" r="55%"><stop offset="0%" stop-color="#1FB5C8" stop-opacity=".14"/><stop offset="100%" stop-color="#1FB5C8" stop-opacity="0"/></radialGradient>'
    '<radialGradient id="rd" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#FF7A6B" stop-opacity=".28"/><stop offset="100%" stop-color="#FF7A6B" stop-opacity="0"/></radialGradient>'
    '<radialGradient id="halo" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#2EE59D" stop-opacity=".35"/><stop offset="100%" stop-color="#2EE59D" stop-opacity="0"/></radialGradient>'
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


CX = W / 2
def brand(y=300):
    mk = 80; mkw = mk * 342 / 377; lw = mkw + 16 + SEMI.width("Markazly", 56); lx = CX - lw / 2
    return f'<image href="{MARK}" x="{lx}" y="{y}" width="{mkw:.0f}" height="{mk}"/>' + T("Markaz", lx + mkw + 16, y + 60, 56, SEMI, FG) + T("ly", lx + mkw + 16 + SEMI.width("Markaz", 56), y + 60, 56, SEMI, "url(#gh)")
def badge(y=1500):
    t = "7 kun bepul sinov"; w = SEMI.width(t, 44) + 90
    return rr(CX - w / 2, y, w, 92, 46, "url(#gh)") + T(t, CX, y + 62, 44, SEMI, INK, "middle")
def save(body, name):
    im = BG.copy(); im.alpha_composite(raster(body)); im = im.convert("RGB")
    im.save(os.path.join(OUTDIR, name))
    # grid preview (3:4 centre crop)
    im.crop((0, 240, 1080, 1680)).resize((360, 480)).save(os.path.join(OUTDIR, name.replace(".png", "_tor.png")))

# cover 1 — admin report
NY = 470
c1 = brand() + '<circle cx="540" cy="900" r="600" fill="url(#rd)"/>'
c1 += rr(110, NY, 860, 250, 40, "#F4F8F6") + f'<circle cx="186" cy="{NY+72}" r="40" fill="url(#g)"/>' + T("A", 186, NY + 87, 40, SEMI, INK, "middle")
c1 += T("Admin", 246, NY + 66, 36, SEMI, INK) + T("hozir · Telegram", 246, NY + 104, 24, REG, "#5C7268")
c1 += T("Bugungi tushum:", 150, NY + 170, 32, MED, "#3F5A4D") + T("? ??? ??? so‘m", 150, NY + 226, 58, SEMI, BAD)
c1 += f'<g transform="translate(920 {NY+20}) rotate(12)"><circle r="62" fill="{BAD}"/><path d="M0 -30 V10" stroke="#fff" stroke-width="12" stroke-linecap="round"/><circle cy="32" r="8" fill="#fff"/></g>'
c1 += T("Admin", CX, 920, 118, SEMI, FG, "middle") + T("hisobotiga", CX, 1050, 118, SEMI, FG, "middle") + T("ishonasizmi?", CX, 1185, 124, SEMI, "url(#gh)", "middle")
c1 += badge(1330)
save(c1, "cover_video1.png")

# cover 3 — monthly loss
c3 = brand() + '<circle cx="540" cy="820" r="620" fill="url(#rd)"/>'
c3 += T("HAR OY", CX, 520, 56, SEMI, BAD, "middle")
c3 += T("−4 000 000", CX, 700, 168, SEMI, BAD, "middle") + T("so‘m", CX, 790, 60, MED, "#F3D6D0", "middle")
c3 += T("yo‘qotyapsizmi?", CX, 960, 116, SEMI, FG, "middle")
cols, rows, gap = 20, 4, 40; gx0 = CX - (cols - 1) * gap / 2
import random as _r; _r.seed(5); red = set(_r.sample(range(cols * rows), 10))
for i in range(cols * rows):
    x = gx0 + (i % cols) * gap; y = 1060 + (i // cols) * gap
    c3 += f'<circle cx="{x:.0f}" cy="{y}" r="{18 if i in red else 13}" fill="{BAD if i in red else "#2EE59D"}" fill-opacity="{1 if i in red else .5}"/>'
c3 += T("10 ta qarzdor = 48 mln so‘m / yil", CX, 1260, 46, MED, "#F3D6D0", "middle")
c3 += badge(1330)
save(c3, "cover_video3.png")
print("ok")
