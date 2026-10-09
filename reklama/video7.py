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
from timing7 import *
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
A, B_, C_, D_, E_, F_, G_, H_ = SC
def card(x, y, w, h, fill=None): return rr(x, y, w, h, 34, fill or SURF, LINE, 2)
def title(txt, sub, t0, t1, y=420):
    add(T(sub, CX, y - 64, 34, SEMI, MINT, "middle") + T(txt, CX, y + 20, 74, SEMI, FG, "middle"), t0, t1, dur=.3)

# ── A. hook: four product screens fly in as a 2x2 collage, then the logo lands on top
mini = [
  ("Boshqaruv", lambda x, y: rr(x+24, y+70, 190, 80, 16, SURF2) + T("368", x+40, y+128, 40, SEMI, FG) + rr(x+226, y+70, 190, 80, 16, SURF2) + T("12", x+242, y+128, 40, SEMI, BAD) + "".join(rr(x+24, y+166+i*44, 392, 34, 10, "#11302A") for i in range(3))),
  ("Sayt", lambda x, y: rr(x+24, y+64, 392, 26, 13, "#06120D") + rr(x+24, y+104, 180, 22, 11, "#2A2412") + T("Ingliz tilini", x+24, y+170, 34, SEMI, FG) + T("o‘rganing", x+24, y+210, 34, SEMI, FG) + rr(x+24, y+232, 170, 44, 22, "url(#amb)")),
  ("Kabinet", lambda x, y: rr(x+24, y+70, 392, 110, 18, "url(#best)", MINT, 2) + T("achieve", x+44, y+140, 40, SEMI, FG) + rr(x+24, y+196, 190, 80, 16, SURF2) + T("92/100", x+40, y+250, 32, SEMI, GOOD) + rr(x+226, y+196, 190, 80, 16, SURF2)),
  ("Reyting", lambda x, y: "".join(rr(x+24, y+70+i*70, 392, 58, 14, "#11302A" if i else "#2A2412") + T(f"{i+1}", x+50, y+110+i*70, 30, SEMI, AMB if i == 0 else FG) + rr(x+90, y+88+i*70, 200 - i*40, 22, 11, MINT if i else AMB) for i in range(3))),
]
for i, (nm, fn) in enumerate(mini):
    x = 90 + (i % 2) * 460; y = 360 + (i // 2) * 330
    add(card(x, y, 440, 310) + T(nm, x + 24, y + 46, 26, SEMI, MINT) + fn(x, y), -0.6 + i * .18, v(3.3), dy=90, dur=.35)
add(T("Hammasi —", CX, 1110, 96, SEMI, FG, "middle") + T("bitta tizimda", CX, 1225, 104, SEMI, "url(#gh)", "middle"), -0.4, v(3.3), dur=.3)
add('<circle cx="540" cy="760" r="420" fill="url(#halo)"/>', v(3.2), B_, dy=0, dur=.4)
mh = 300; mw = mh * 342 / 377
add(f'<image href="{MARK}" x="{CX - mw/2 + 5:.0f}" y="520" width="{mw:.0f}" height="{mh}"/>', v(3.3), B_, pop=True)
add(T("Markaz", CX - (SEMI.width("Markazly", 130)) / 2, 1000, 130, SEMI, FG) + T("ly", CX - (SEMI.width("Markazly", 130)) / 2 + SEMI.width("Markaz", 130), 1000, 130, SEMI, "url(#gh)"), v(3.8), B_, dur=.3)

# ── B. management panel
title("Boshqaruv paneli", "01", B_, C_)
dx, dw = 110, 860
k = card(dx, 520, dw, 170)
for j, (lab, val) in enumerate([("O‘quvchilar", "368"), ("Guruhlar", "24"), ("O‘qituvchilar", "12")]):
    kx = dx + 30 + j * 280
    k += T(lab, kx, 580, 28, REG, MUTED) + T(val, kx, 650, 60, SEMI, FG)
add(k, v(6.23), C_, dy=50)
att = card(dx, 720, dw, 330) + T("Davomat · B1 guruh", dx + 30, 780, 32, SEMI, FG)
names = ["Aziza S.", "Jasur R.", "Madina K.", "Sardor A."]
for j, nm in enumerate(names):
    att += T(nm, dx + 30, 850 + j * 60, 30, MED, FG)
add(att, v(9.0), C_, dy=50)
for j in range(4):
    yy = 850 + j * 60 - 34
    ok = j != 2
    add(rr(dx + dw - 200, yy, 160, 46, 23, "#123A2C" if ok else "#3A1D1A") + T("Keldi" if ok else "Kelmadi", dx + dw - 120, yy + 32, 24, SEMI, GOOD if ok else BAD, "middle"), v(9.3) + j * .18, C_, pop=True, dur=.18)
add(card(dx, 1080, dw, 120) + T("To‘lov va qarzdorlar", dx + 30, 1152, 32, SEMI, FG) + rr(dx + dw - 330, 1112, 300, 56, 28, "#3A1D1A") + T("Qarzdor: 12", dx + dw - 180, 1150, 28, SEMI, BAD, "middle"), v(11.0), C_, dy=40)

# ── C. branches
title("Filiallar hisoboti", "02", C_, D_)
for j, (nm, val, pct, col, tt) in enumerate([("Chilonzor", "+ 18 mln", .85, GOOD, 15.4), ("Yunusobod", "+ 9 mln", .55, GOOD, 15.8), ("Sergeli", "− 4 mln", .25, BAD, 16.8)]):
    yy = 540 + j * 210
    add(card(dx, yy, dw, 180) + T(nm, dx + 34, yy + 66, 40, SEMI, FG) + T(val, dx + dw - 34, yy + 66, 46, SEMI, col, "end") + rr(dx + 34, yy + 104, dw - 68, 40, 20, LINE), v(tt), D_, dy=40)
    add(rr(dx + 34, yy + 104, (dw - 68) * pct, 40, 20, col), v(tt) + .3, D_, dy=0, dur=.5)
add(T("Har bir filial — aniq raqamlarda", CX, 1230, 40, MED, MUTED, "middle"), v(18.4), D_)

# ── D. website + lead into the system
title("O‘z saytingiz", "03", D_, E_)
x, y, w = 110, 500, 860
s_ = rr(x, y, w, 560, 30, "#071510", LINE, 2) + f'<path d="M{x} {y+30} Q{x} {y} {x+30} {y} H{x+w-30} Q{x+w} {y} {x+w} {y+30} V{y+62} H{x} Z" fill="#0B1D16"/>'
s_ += "".join(f'<circle cx="{x+34+j*26}" cy="{y+31}" r="8" fill="{c}"/>' for j, c in enumerate([MINT, LINE, LINE]))
s_ += rr(x + 130, y + 13, 600, 38, 19, "#06120D", LINE, 2) + ic("lock", x + 148, y + 21, 20, MUTED, 2) + T("nuracademy.uz", x + 178, y + 40, 22, MED, FG)
s_ += rr(x + 32, y + 90, 46, 46, 12, "url(#amb)") + T("N", x + 55, y + 123, 24, SEMI, "#2A1400", "middle") + T("Nur Academy", x + 92, y + 124, 28, SEMI, FG)
s_ += T("Ingliz tilida birinchi", x + 32, y + 250, 50, SEMI, FG) + T("darsdan gapiring", x + 32, y + 312, 50, SEMI, FG)
s_ += rr(x + 32, y + 360, 320, 64, 32, "url(#amb)") + T("Bepul darsga yozilish", x + 192, y + 401, 24, SEMI, "#2A1400", "middle")
s_ += rr(x + 600, y + 180, 220, 220, 28, "#12281F", LINE, 2) + ic("cap", x + 640, y + 220, 140, AMB, 1.5)
cxx = x + 32
for g, t in [("url(#amb)", "General English"), ("url(#gh)", "IELTS"), ("#7B86FF", "Kids")]:
    s_ += rr(cxx, y + 460, 250, 60, 16, "#0C1F18", LINE, 2) + rr(cxx + 16, y + 484, 12, 12, 6, g) + T(t, cxx + 40, y + 500, 24, SEMI, FG); cxx += 266
add(s_, D_ + .1, E_, dy=60, dur=.4)
add(rr(150, 1110, 780, 130, 30, FG) + rr(176, 1136, 78, 78, 22, MINT) + ic("users", 191, 1151, 48, INK, 2.4) + T("Yangi ariza tizimga tushdi", 276, 1168, 30, SEMI, INK) + T("Dilshod · IELTS · +998 90 ••• •• 12", 276, 1208, 24, REG, "#3F5A4D"), v(22.6), E_, pop=True)

# ── E. student cabinet
title("O‘quvchi kabineti", "04", E_, F_)
px, py, pw, ph = 300, 480, 480, 800
p = rr(px - 12, py - 12, pw + 24, ph + 24, 70, "#020806") + rr(px, py, pw, ph, 58, SURF) + rr(px + pw / 2 - 72, py + 20, 144, 28, 14, "#020806")
p += f'<circle cx="{px+58}" cy="{py+104}" r="30" fill="url(#g)"/>' + T("A", px + 58, py + 117, 30, SEMI, INK, "middle") + T("B1 guruh", px + 104, py + 94, 22, REG, MUTED) + T("Aziza Sobirova", px + 104, py + 128, 28, SEMI, FG)
add(p, E_ + .1, F_, dy=80, dur=.4)
items = [(27.23, rr(px + 22, py + 168, pw - 44, 110, 24, SURF2) + ic("cal", px + 46, py + 200, 44, "url(#g)", 2) + T("Bugungi dars", px + 106, py + 214, 22, REG, MUTED) + T("18:00 · 3-xona", px + 106, py + 252, 28, SEMI, FG)),
         (28.0, rr(px + 22, py + 292, pw - 44, 110, 24, SURF2) + ic("book", px + 46, py + 324, 44, "url(#g)", 2) + T("Uyga vazifa", px + 106, py + 338, 22, REG, MUTED) + T("92 / 100", px + 106, py + 376, 28, SEMI, GOOD)),
         (28.9, rr(px + 22, py + 416, pw - 44, 150, 24, "url(#best)", MINT, 2) + T("Lug‘at · kartochka", px + 46, py + 456, 22, REG, MUTED) + T("achieve", px + 46, py + 516, 44, SEMI, FG) + T("erishmoq", px + 46, py + 552, 24, REG, MUTED))]
for tt, body in items: add(body, v(tt), F_, dy=30, pop=True, dur=.25)
add(rr(120, 1110, 560, 130, 30, FG) + T("Ota-ona ko‘radi:", 150, 1162, 26, MED, "#3F5A4D") + T("Aziza darsga keldi · 18:00", 150, 1206, 30, SEMI, INK) + ic("tick", 620, 1146, 44, "#0A7A50", 2.4), v(30.4), F_, pop=True)

# ── F. gamification
add('<circle cx="540" cy="760" r="480" fill="url(#halo)"/>', F_, G_, dy=0, dur=.5)
title("Gamifikatsiya", "05", F_, G_)
for j, (tt, x, y, txt) in enumerate([(35.7, 170, 560, "+10 ball · dars"), (36.4, 600, 520, "+20 ball · vazifa"), (37.1, 380, 650, "+5 ball · lug‘at")]):
    add(rr(x, y, SEMI.width(txt, 34) + 60, 70, 35, "#2A2412", AMB, 2) + T(txt, x + 30, y + 47, 34, SEMI, AMB), v(tt), G_, pop=True, dy=0, dur=.22)
lv = card(110, 760, 860, 150) + T("Daraja: Bilimdon", 150, 822, 34, SEMI, FG) + T("1 248 ball", 930, 822, 34, SEMI, AMB, "end") + rr(150, 850, 780, 30, 15, LINE)
add(lv, v(36.0), G_, dy=40)
add(rr(150, 850, 780 * .72, 30, 15, "url(#amb)"), v(36.6), G_, dy=0, dur=.8)
lb = card(110, 940, 860, 270) + T("Reyting · B1", 150, 996, 30, SEMI, FG)
for j, (nm, pts) in enumerate([("Aziza S.", "1 248"), ("Jasur R.", "1 190"), ("Madina K.", "1 052")]):
    yy = 1020 + j * 60
    lb += rr(140, yy, 800, 52, 14, "#2A2412" if j == 0 else "#11302A") + T(str(j + 1), 172, yy + 37, 28, SEMI, AMB if j == 0 else FG, "middle") + T(nm, 210, yy + 37, 28, MED, FG) + T(pts, 910, yy + 37, 28, SEMI, AMB if j == 0 else MUTED, "end")
add(lb, v(38.65), G_, dy=40)
add(f'<g transform="translate(860 560)"><rect x="-70" y="-50" width="140" height="110" rx="18" fill="url(#amb)"/><rect x="-80" y="-78" width="160" height="40" rx="12" fill="#E8873D"/><rect x="-12" y="-78" width="24" height="138" fill="#2A1400" fill-opacity=".35"/></g>'
    + rr(700, 640, 330, 64, 32, FG) + T("Sovg‘a · 500 ball", 865, 682, 28, SEMI, INK, "middle"), v(40.0), G_, pop=True)

# ── G. phone, 4 languages, migration, training
title("Telefonda qulay", "06", G_, H_)
for j, lg in enumerate(["O‘zbekcha", "Ruscha", "Inglizcha", "Arabcha"]):
    x = 110 + (j % 2) * 440; y = 520 + (j // 2) * 130
    add(rr(x, y, 420, 110, 30, SURF, MINT if j == 0 else LINE, 2) + ic("globe", x + 30, y + 31, 48, MINT, 2) + T(lg, x + 100, y + 72, 40, SEMI, FG), v(43.4) + j * .25, H_, pop=True, dur=.2)
for j, (txt, tt) in enumerate([("Ma’lumotlarni o‘zimiz ko‘chiramiz", 45.3), ("Xodimlaringizni o‘qitamiz", 47.5)]):
    y = 830 + j * 130
    add(rr(110, y, 860, 110, 30, "#123A2C", MINT, 2) + f'<circle cx="180" cy="{y+55}" r="34" fill="{MINT}"/>' + ic("check", 162, y + 37, 36, INK, 3) + T(txt, 240, y + 68, 38, SEMI, FG), v(tt), H_, dy=30)

# ── H. CTA
add('<circle cx="540" cy="760" r="480" fill="url(#halo)"/>', H_, DUR + 1, dy=0, dur=.8)
add(T("Hoziroq", CX, 520, 76, SEMI, FG, "middle") + T("pastdagi tugmani", CX, 610, 76, SEMI, FG, "middle") + T("bosing", CX, 700, 76, SEMI, "url(#gh)", "middle"), H_, DUR + 1)
add(rr(110, 790, 860, 210, 105, "url(#gh)") + T("7 kun bepul", CX, 892, 84, SEMI, INK, "middle") + T("sinab ko‘ring", CX, 960, 46, MED, "#0A3D27", "middle"), v(52.3), DUR + 1, pop=True)
add(T("markazly.onrender.com", CX, 1090, 38, MED, MUTED, "middle"), v(52.8), DUR + 1)
arrow = f'<g transform="translate({CX-60} 1170)"><circle cx="60" cy="60" r="60" fill="#2EE59D" fill-opacity=".18"/><path d="M60 28 V92 M32 66 L60 94 L88 66" fill="none" stroke="#2EE59D" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></g>'
add(arrow, v(50.2), DUR + 1, bob=14)
add(arrow.replace("1170)", "1320)").replace('fill-opacity=".18"', 'fill-opacity=".08"').replace('stroke="#2EE59D"', 'stroke="#2EE59D" stroke-opacity=".5"'), v(50.5), DUR + 1, bob=14)

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
    add(cap, a_, b_ + .02, dy=0, dur=.1, pop=True, fo=.04)

# render
n = int(DUR * FPS)
out = os.path.join(OUTDIR, "markazly_video7_umumiy.mp4")
ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                       "-i", os.path.join(os.path.dirname(OUTDIR), "audio", "mix_v7.m4a"), "-af", "apad", "-shortest",
                       "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
for i in range(n):
    t = i / FPS
    fr = BG.copy()
    for e in E: e.draw(fr, t)
    if t < v(5.6):
        z = 1 + 0.05 * ease(t / v(5.6))
        if 99 <= t <= 1.45: z += 0.02
        cw_, ch_ = W / z, H / z
        ox = (W - cw_) / 2 + (10 * math.sin(t * 190) if 99 <= t <= 1.5 else 0)
        oy = (H - ch_) / 2 + (8 * math.cos(t * 230) if 99 <= t <= 1.5 else 0)
        fr = fr.crop((int(ox), int(oy), int(ox + cw_), int(oy + ch_))).resize((W, H), Image.BILINEAR)
        if 99 <= t <= 1.4:
            fl = Image.new("RGBA", (W, H), (255, 70, 60, int(90 * (1 - (t - 1.2) / .2))))
            fr.alpha_composite(fl)
    ff.stdin.write(fr.convert("RGB").tobytes())
    if i in [int(x * FPS) for x in (0.0, 1.5, 3.9, 10.5, 15.5, 22.0, 28.5, 36.5, 41.0, 44.0, 49.5)]:
        fr.convert("RGB").save(os.path.join(OUTDIR, f"kadr_{t:04.1f}.png"))
ff.stdin.close(); ff.wait()
print("done", out)
