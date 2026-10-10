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

E = []
def add(*a, **k): E.append(El(*a, **k))
CX = W / 2

# persistent small brand row at the top
mk = 64; mkw = mk * 342 / 377
lw = mkw + 14 + SEMI.width("Markazly", 44)
lx = CX - lw / 2
brand = f'<image href="{MARK}" x="{lx}" y="210" width="{mkw:.0f}" height="{mk}"/>' + T("Markaz", lx + mkw + 14, 258, 44, SEMI, FG) + T("ly", lx + mkw + 14 + SEMI.width("Markaz", 44), 258, 44, SEMI, "url(#gh)")
add(brand, -1, DUR + 1, dy=0)

# ── A. hook: the loss counter spins up, glitches, headline lands
add('<circle cx="540" cy="760" r="560" fill="url(#rd)"/>', -1, S_B, dy=0, dur=.1)
add(T("HAR OY", CX, 470, 44, SEMI, BAD, "middle"), -1, S_B, dy=0, dur=.1)
steps = 14
for k in range(steps + 1):
    val = int(4_000_000 * (0.55 + 0.45 * (1 - (1 - k / steps) ** 2)) // 10000 * 10000)
    txt = "−" + f"{val:,}".replace(",", " ")
    t0 = -1 if k == 0 else 0.06 * k
    t1 = 0.06 * (k + 1) + .02 if k < steps else S_B
    add(T(txt, CX, 640, 150, SEMI, BAD, "middle") + T("so‘m", CX, 720, 54, MED, "#F3D6D0", "middle"), t0, t1, dy=0, dur=0.0001, fo=.0001,
        jit=(0.9, 1.15) if k == steps else None)
for i, (t, c) in enumerate([("Markazingiz", FG), ("millionlab so‘m", FG), ("yo‘qotyapti", BAD)]):
    add(T(t, CX, 900 + i * 118, 100, SEMI, c, "middle"), -0.4 + i * .5, S_B, dur=.3)
s_ = "…va siz buni sezmayapsiz"
sw_ = SEMI.width(s_, 52) + 90
add(rr(CX - sw_ / 2, 1250, sw_, 104, 52, "#3A1D1A", BAD, 3) + T(s_, CX, 1318, 52, SEMI, BAD, "middle"), v(3.27), S_B, pop=True)

# ── B. 300 students, 10 forget to pay
add(T("Keling, hisoblaymiz", CX, 470, 66, SEMI, FG, "middle"), S_B, S_C)
cols, rows, r_, gap = 20, 15, 15, 41
gx0 = CX - (cols - 1) * gap / 2; gy0 = 560
dots = "".join(f'<circle cx="{gx0 + c * gap:.0f}" cy="{gy0 + r * gap:.0f}" r="{r_}" fill="#2EE59D" fill-opacity=".55"/>' for r in range(rows) for c in range(cols))
add(dots, v(6.94), S_C, dy=30, dur=.5)
add(T("300 ta o‘quvchi", CX, 1225, 54, SEMI, MINT, "middle"), v(7.2), v(8.9), dy=10)
import random as _r
_r.seed(3); red = _r.sample([(r, c) for r in range(rows) for c in range(cols)], 10)
for k, (r, c) in enumerate(red):
    x, y = gx0 + c * gap, gy0 + r * gap
    add(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r_+5}" fill="{BAD}"/><circle cx="{x:.0f}" cy="{y:.0f}" r="{r_+16}" fill="none" stroke="{BAD}" stroke-opacity=".5" stroke-width="3"/>', v(9.0) + k * .09, S_C, dy=0, pop=True, dur=.2)
add(T("10 tasi to‘lamadi", CX, 1225, 54, SEMI, BAD, "middle"), v(9.4), S_C, dy=10)
add(T("…va hech kim eslamadi", CX, 1300, 40, MED, MUTED, "middle"), v(11.67), S_C, dy=10)

# ── C. the math
def eq(y, left, right, col, size=74, sub=""):
    b = rr(110, y, 860, 170, 36, SURF, LINE, 2) + T(left, 150, y + 72, 34, MED, MUTED) + T(right, 150, y + 140, size, SEMI, col)
    if sub: b += T(sub, 930, y + 140, 34, MED, MUTED, "end")
    return b
add(eq(470, "10 ta o‘quvchi ×", "400 000 so‘m", FG), v(13.02), S_D)
add(eq(670, "bir oyda", "−4 000 000", BAD, sub="so‘m"), v(15.56), S_D, pop=True)
add(rr(90, 870, 900, 230, 42, "#3A1D1A", BAD, 4) + T("bir yilda", 140, 940, 36, MED, "#F3D6D0") + T("−48 000 000", 140, 1050, 104, SEMI, BAD) + T("so‘m", 950, 1050, 40, MED, "#F3D6D0", "end"),
    v(17.13), S_D, pop=True, jit=(v(17.13), v(17.13) + .3))

# ── D. the insight
add(f'<g transform="translate({CX} 560)"><circle r="120" fill="#2A1D1B" stroke="{BAD}" stroke-width="4"/>'
    f'<path d="M-46 30 h92 l-14 -20 v-40 a32 32 0 0 0 -64 0 v40 z M-14 44 a14 14 0 0 0 28 0" fill="none" stroke="#F3D6D0" stroke-width="9" stroke-linejoin="round"/>'
    f'<path d="M-80 -80 L80 80" stroke="{BAD}" stroke-width="12" stroke-linecap="round"/></g>', S_D, S_E, pop=True)
add(T("Bu pul yo‘qolmagan —", CX, 820, 70, SEMI, FG, "middle"), v(20.03), S_E)
add(T("hech kim", CX, 930, 84, SEMI, BAD, "middle") + T("eslatmagan", CX, 1030, 84, SEMI, BAD, "middle"), v(21.36), S_E, pop=True)

# ── E. Markazly debtor list
add('<circle cx="540" cy="420" r="300" fill="url(#halo)"/>', S_E, S_F, dy=0, dur=.8)
mh = 160; mw = mh * 342 / 377
add(f'<image href="{MARK}" x="{CX - mw/2 + 3:.0f}" y="330" width="{mw:.0f}" height="{mh}"/>', S_E, S_F, pop=True)
dx, dy_, dw = 110, 540, 860
hdr = rr(dx, dy_, dw, 660, 34, SURF, LINE, 2) + T("Qarzdorlar", dx + 34, dy_ + 70, 40, SEMI, FG)
p_, pw_ = pill("10 ta · 4 000 000 so‘m", 0, 0, 26, "#3A1D1A", BAD, SEMI, 18, 50)
hdr += f'<g transform="translate({dx + dw - 34 - pw_} {dy_ + 30})">{p_}</g>'
add(hdr, v(24.3), S_F, dy=60)
people = [("JR", "Jasur R. · IELTS", "3 kun"), ("MK", "Madina K. · B1", "5 kun"), ("SA", "Sardor A. · A2", "1 hafta"), ("NT", "Nilufar T. · Kids", "2 kun"), ("BO", "Bobur O. · B2", "4 kun")]
for i, (av, nm, late) in enumerate(people):
    ry = dy_ + 110 + i * 106
    row = rr(dx + 26, ry, dw - 52, 92, 18, "#11302A") + f'<circle cx="{dx+74}" cy="{ry+46}" r="26" fill="{SURF2}"/>' + T(av, dx + 74, ry + 55, 20, SEMI, MINT, "middle")
    row += T(nm, dx + 116, ry + 44, 30, MED, FG) + T("kechikdi: " + late, dx + 116, ry + 76, 22, REG, MUTED) + T("400 000", dx + dw - 50, ry + 58, 32, SEMI, BAD, "end")
    add(row, v(24.9) + i * .22, S_F, dy=24, dur=.3)
add(rr(dx, 1230, dw, 100, 50, "#123A2C", MINT, 2) + ic("cal", dx + 34, 1256, 48, MINT, 2) + T("Har kuni yangilanadi", dx + 100, 1293, 40, SEMI, FG), v(27.44), S_F, pop=True)
add(f'<g transform="translate(918 1280) scale(.78)"><circle r="54" fill="{MINT}" stroke="{BOARD}" stroke-width="6"/><path d="M-24 2 L-6 20 L26 -16" fill="none" stroke="{INK}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/></g>', v(30.57), S_F, pop=True)

# ── F. CTA
add('<circle cx="540" cy="760" r="480" fill="url(#halo)"/>', S_F, DUR + 1, dy=0, dur=.8)
add(T("Hoziroq", CX, 520, 76, SEMI, FG, "middle") + T("pastdagi tugmani", CX, 610, 76, SEMI, FG, "middle") + T("bosing", CX, 700, 76, SEMI, "url(#gh)", "middle"), S_F, DUR + 1)
add(rr(110, 790, 860, 210, 105, "url(#gh)") + T("7 kun bepul", CX, 892, 84, SEMI, INK, "middle") + T("sinab ko‘ring", CX, 960, 46, MED, "#0A3D27", "middle"), v(35.0), DUR + 1, pop=True)
add(T("markazly.uz", CX, 1090, 44, SEMI, MUTED, "middle"), v(36.0), DUR + 1)
arrow = f'<g transform="translate({CX-60} 1170)"><circle cx="60" cy="60" r="60" fill="#2EE59D" fill-opacity=".18"/><path d="M60 28 V92 M32 66 L60 94 L88 66" fill="none" stroke="#2EE59D" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></g>'
add(arrow, v(33.6), DUR + 1, bob=14)
add(arrow.replace("1170)", "1320)").replace('fill-opacity=".18"', 'fill-opacity=".08"').replace('stroke="#2EE59D"', 'stroke="#2EE59D" stroke-opacity=".5"'), v(33.9), DUR + 1, bob=14)

# ── captions: short 2-3 word chunks that pop in, key words coloured
for a_, b_, ws in chunks():
    if a_ < S_B - .1 or a_ >= S_F - .05: continue
    words = [w[2] for w in ws]
    size = 66
    widths = [SEMI.width(w, size) for w in words]
    sp = SEMI.width(" ", size)
    tw = sum(widths) + sp * (len(words) - 1)
    if tw > 900:
        size = int(size * 900 / tw); widths = [SEMI.width(w, size) for w in words]; sp = SEMI.width(" ", size); tw = sum(widths) + sp * (len(words) - 1)
    x = CX - tw / 2; yb = 1530
    cap = rr(CX - tw / 2 - 34, yb - size - 20, tw + 68, size + 52, 26, "#04140D").replace('fill="#04140D"', 'fill="#04140D" fill-opacity=".78"')
    for w, wd in zip(words, widths):
        col = BAD if w in BAD_KEY else (MINT if w in KEY else FG)
        cap += T(w, x, yb, size, SEMI, col); x += wd + sp
    add(cap, a_ - .04, b_ + .06, dy=0, dur=.12, pop=True, fo=.06)

# render
n = int(DUR * FPS)
out = os.path.join(OUTDIR, "markazly_video3.mp4")
ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                       "-i", os.path.join(os.path.dirname(OUTDIR), "audio", "mix_v3.m4a"), "-af", "apad", "-shortest",
                       "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
for i in range(n):
    t = i / FPS
    fr = BG.copy()
    for e in E: e.draw(fr, t)
    if t < v(5.6):
        z = 1 + 0.05 * ease(t / v(5.6))
        if 0.9 <= t <= 1.15: z += 0.02
        cw_, ch_ = W / z, H / z
        ox = (W - cw_) / 2 + (10 * math.sin(t * 190) if 0.9 <= t <= 1.2 else 0)
        oy = (H - ch_) / 2 + (8 * math.cos(t * 230) if 0.9 <= t <= 1.2 else 0)
        fr = fr.crop((int(ox), int(oy), int(ox + cw_), int(oy + ch_))).resize((W, H), Image.BILINEAR)
        if 0.9 <= t <= 1.1:
            fl = Image.new("RGBA", (W, H), (255, 70, 60, int(90 * (1 - (t - 0.9) / .2))))
            fr.alpha_composite(fl)
    ff.stdin.write(fr.convert("RGB").tobytes())
    if i in [int(x * FPS) for x in (0.0, 0.6, 3.6, 7.5, 10.6, 14.0, 17.4, 21.0, 25.0, 30.0, 33.5)]:
        fr.convert("RGB").save(os.path.join(OUTDIR, f"kadr_{t:04.1f}.png"))
ff.stdin.close(); ff.wait()
print("done", out)
