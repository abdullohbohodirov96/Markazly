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
from timing import *
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

# ── A. hook 0–5.1 : a notification from the admin, then the number glitches into "?"
NY = 360
add('<circle cx="540" cy="900" r="560" fill="url(#rd)"/>', 1.15, S_B, dy=0, dur=.15, fo=.6)
note = rr(90, NY, 900, 300, 44, "#F4F8F6") + f'<circle cx="170" cy="{NY+80}" r="44" fill="url(#g)"/>' + T("A", 170, NY + 96, 44, SEMI, INK, "middle")
note += T("Admin", 236, NY + 74, 38, SEMI, INK) + T("hozir · Telegram", 236, NY + 114, 26, REG, "#5C7268")
note += T("Bugungi tushum:", 130, NY + 196, 34, MED, "#3F5A4D")
add(note, -0.5, S_B, dy=-60, dur=.35)
add(T("5 960 000 so‘m", 130, NY + 262, 62, SEMI, "#0A7A50"), -0.5, 1.25, dy=0, dur=.1, fo=.06, jit=(0.95, 1.25))
add(f'<line x1="122" y1="{NY+240}" x2="{130+SEMI.width("5 960 000 so‘m", 62)+8}" y2="{NY+240}" stroke="{BAD}" stroke-width="8" stroke-linecap="round"/>', 0.8, 1.25, dy=0, dur=.12, fo=.06)
add(T("? ??? ??? so‘m", 130, NY + 262, 62, SEMI, BAD), 1.2, S_B, dy=0, dur=.05, pop=True, jit=(1.2, 1.45))
add(f'<g transform="translate(860 {NY+40}) rotate(12)"><circle r="62" fill="{BAD}"/><path d="M0 -30 V10" stroke="#fff" stroke-width="12" stroke-linecap="round"/><circle cy="32" r="8" fill="#fff"/></g>', 1.25, S_B, dy=0, dur=.25, pop=True)
for i, (t, c) in enumerate([("Administratoringiz", FG), ("hisobotni to‘g‘ri", FG), ("qilyaptimi?", "url(#gh)")]):
    add(T(t, CX, 830 + i * 120, 96 if i < 2 else 112, SEMI, c, "middle"), -0.3 + i * .45, S_B, dur=.3)
s_ = "Siz buni bilmaysiz."
sw_ = SEMI.width(s_, 64) + 100
add(rr(CX - sw_ / 2, 1150, sw_, 120, 60, "#3A1D1A", BAD, 3) + T(s_, CX, 1232, 64, SEMI, BAD, "middle"), v(3.25), S_B, pop=True)

# ── B. admin's evening message
cx0, cw = 120, 840
add(rr(cx0, 470, cw, 110, 30, SURF2) + f'<circle cx="{cx0+60}" cy="525" r="34" fill="url(#g)"/>' + T("A", cx0 + 60, 540, 34, SEMI, INK, "middle")
    + T("Admin", cx0 + 112, 518, 34, SEMI, FG) + T("bugun, 21:47", cx0 + 112, 556, 26, REG, MUTED), S_B, S_C)
for i, (t, tt) in enumerate([("Bugun 14 ta to‘lov tushdi", v(6.45)), ("Yangi o‘quvchilar: 3 ta", v(7.55)), ("Hammasi joyida, ustoz", v(8.6))]):
    w = MED.width(t, 40) + 80
    add(rr(cx0, 630 + i * 140, w, 112, 34, "#16392D") + T(t, cx0 + 40, 630 + i * 140 + 70, 40, MED, FG) + T("21:4" + str(7 + i), cx0 + w - 24, 630 + i * 140 + 100, 20, REG, MUTED, "end"), tt, S_C)
add(f'<g transform="translate(760 1090) rotate(-8)">' + rr(-170, -60, 340, 120, 24, "none", BAD, 6) + T("TEKSHIRIB", 0, -6, 40, SEMI, BAD, "middle") + T("BO‘LMAYDI", 0, 42, 40, SEMI, BAD, "middle") + '</g>', v(9.75), S_C, pop=True)

# ── C. what you can't see
add(T("Siz bilmaysiz:", CX, 520, 72, SEMI, FG, "middle"), S_C, S_D)
for i, (t, tt) in enumerate([("Raqamni kim o‘zgartirdi?", 11.3), ("Kim to‘lamay qoldi?", 12.75), ("Qaysi guruh bo‘sh qoldi?", 13.75)]):
    y = 610 + i * 170
    add(rr(110, y, 860, 140, 36, "#2A1D1B", "#5A2A24", 3) + f'<circle cx="190" cy="{y+70}" r="40" fill="{BAD}"/>' + T("?", 190, y + 90, 56, SEMI, "#2A0E0A", "middle")
        + T(t, 256, y + 86, 46, MED, "#F3D6D0"), v(tt), S_D)

# ── D. Markazly — everything recorded
add('<circle cx="540" cy="520" r="360" fill="url(#halo)"/>', S_D, S_E, dy=0, dur=.8)
mh = 230; mw = mh * 342 / 377
add(f'<image href="{MARK}" x="{CX - mw/2 + 4:.0f}" y="360" width="{mw:.0f}" height="{mh}"/>', S_D, S_E, pop=True)
add(T("Markazly'da hammasi", CX, 700, 64, SEMI, FG, "middle") + T("tizimga yoziladi", CX, 780, 64, SEMI, "url(#gh)", "middle"), v(17.6), S_E)
dx, dy_, dw = 110, 850, 860
kw = (dw - 52 - 26) / 3
kpi = rr(dx, dy_, dw, 470, 34, SURF, LINE, 2)
kx = dx + 26
for lab, val, col in [("To‘lovlar", "14", FG), ("Davomat", "96%", FG), ("Qarzdor", "4", BAD)]:
    kpi += rr(kx, dy_ + 26, kw, 140, 22, SURF2) + T(lab, kx + 24, dy_ + 72, 28, REG, MUTED) + T(val, kx + 24, dy_ + 138, 52, SEMI, col)
    kx += kw + 13
kpi += T("Bugungi to‘lovlar", dx + 26, dy_ + 222, 30, SEMI, FG)
add(kpi, v(18.6), S_E, dy=80)
for i, (av, nm, sm, who) in enumerate([("JR", "Jasur R. · IELTS", "590 000", "Admin: Dilnoza, 14:02"), ("MK", "Madina K. · B1", "400 000", "Admin: Dilnoza, 16:35")]):
    ry = dy_ + 250 + i * 100
    row = rr(dx + 26, ry, dw - 52, 86, 18, "#11302A") + f'<circle cx="{dx+72}" cy="{ry+43}" r="24" fill="{SURF2}"/>' + T(av, dx + 72, ry + 52, 20, SEMI, MINT, "middle")
    row += T(nm, dx + 112, ry + 40, 28, MED, FG) + T(who, dx + 112, ry + 72, 20, REG, MUTED) + T("+" + sm, dx + dw - 50, ry + 54, 30, SEMI, GOOD, "end")
    add(row, v(22.4 + i * .8), S_E, dy=30)

# ── E. on your phone
px, py, pw, ph = 300, 500, 480, 800
p = rr(px - 12, py - 12, pw + 24, ph + 24, 70, "#020806") + rr(px, py, pw, ph, 58, SURF) + rr(px + pw / 2 - 72, py + 20, 144, 28, 14, "#020806")
p += T("Bugun", px + 40, py + 110, 26, REG, MUTED) + T("Tushum", px + 40, py + 150, 34, SEMI, FG)
p += T("5 960 000", px + 40, py + 240, 70, SEMI, "url(#gh)") + T("so‘m", px + 40, py + 285, 28, REG, MUTED)
for i, (l, val) in enumerate([("Darsga keldi", "212 / 220"), ("Qarzdorlar", "4 ta"), ("Filiallar", "2 ta · foyda")]):
    yy = py + 330 + i * 130
    p += rr(px + 22, yy, pw - 44, 110, 24, SURF2) + T(l, px + 46, yy + 46, 24, REG, MUTED) + T(val, px + 46, yy + 88, 32, SEMI, FG)
add(T("Telefoningizdan,", CX, 370, 60, SEMI, FG, "middle") + T("istalgan payt", CX, 440, 60, SEMI, "url(#gh)", "middle"), S_E, S_F)
add(p, S_E + .1, S_F, dy=120, dur=.6)
tx, ty = 130, 890
add(rr(tx, ty, 420, 130, 28, FG) + rr(tx + 24, ty + 26, 78, 78, 22, MINT) + ic("check", tx + 43, ty + 45, 40, INK, 3)
    + T("To‘lov qabul", tx + 124, ty + 60, 32, SEMI, INK) + T("590 000 so‘m", tx + 124, ty + 102, 28, REG, "#3F5A4D"), v(26.6), S_F, pop=True)

# ── F. CTA
add('<circle cx="540" cy="760" r="480" fill="url(#halo)"/>', S_F, DUR + 1, dy=0, dur=.8)
add(T("Hoziroq", CX, 520, 76, SEMI, FG, "middle") + T("pastdagi tugmani", CX, 610, 76, SEMI, FG, "middle") + T("bosing", CX, 700, 76, SEMI, "url(#gh)", "middle"), S_F, DUR + 1)
add(rr(110, 790, 860, 210, 105, "url(#gh)") + T("7 kun bepul", CX, 892, 84, SEMI, INK, "middle") + T("sinab ko‘ring", CX, 960, 46, MED, "#0A3D27", "middle"), v(32.0), DUR + 1, pop=True)
add(T("markazly.uz", CX, 1090, 44, SEMI, MUTED, "middle"), v(33.0), DUR + 1)
arrow = f'<g transform="translate({CX-60} 1170)"><circle cx="60" cy="60" r="60" fill="#2EE59D" fill-opacity=".18"/><path d="M60 28 V92 M32 66 L60 94 L88 66" fill="none" stroke="#2EE59D" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></g>'
add(arrow, v(30.9), DUR + 1, bob=14)
add(arrow.replace("1170)", "1320)").replace('fill-opacity=".18"', 'fill-opacity=".08"').replace('stroke="#2EE59D"', 'stroke="#2EE59D" stroke-opacity=".5"'), v(31.2), DUR + 1, bob=14)

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
out = os.path.join(OUTDIR, "markazly_video1_v2.mp4")
ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                       "-i", os.path.join(os.path.dirname(OUTDIR), "audio", "mix_v2.m4a"), "-af", "apad", "-shortest",
                       "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
for i in range(n):
    t = i / FPS
    fr = BG.copy()
    for e in E: e.draw(fr, t)
    if t < v(5.6):
        z = 1 + 0.05 * ease(t / v(5.6))
        if 1.2 <= t <= 1.45: z += 0.02
        cw_, ch_ = W / z, H / z
        ox = (W - cw_) / 2 + (10 * math.sin(t * 190) if 1.2 <= t <= 1.5 else 0)
        oy = (H - ch_) / 2 + (8 * math.cos(t * 230) if 1.2 <= t <= 1.5 else 0)
        fr = fr.crop((int(ox), int(oy), int(ox + cw_), int(oy + ch_))).resize((W, H), Image.BILINEAR)
        if 1.2 <= t <= 1.4:
            fl = Image.new("RGBA", (W, H), (255, 70, 60, int(90 * (1 - (t - 1.2) / .2))))
            fr.alpha_composite(fl)
    ff.stdin.write(fr.convert("RGB").tobytes())
    if i in [int(x * FPS) for x in (0.0, 1.3, 3.5, 6.6, 9.5, 12.5, 18.5, 22.6, 26.0, 31.5)]:
        fr.convert("RGB").save(os.path.join(OUTDIR, f"kadr_{t:04.1f}.png"))
ff.stdin.close(); ff.wait()
print("done", out)
