TIMING = 'timing8'
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
from PIL import ImageDraw, ImageFont
E.pop(0)  # no top brand row here: both panels are labelled
FB = os.path.join(B, "Poppins-SemiBold.ttf"); FM = os.path.join(B, "Poppins-Medium.ttf")
def pf(sz, bold=True): return ImageFont.truetype(FB if bold else FM, sz)
T_B, T_C, T_D, T_E, T_F = at("Qarang"), at("Davomat ham"), at("Oy oxiridagi"), at("Excel'da bir soat"), at("Hoziroq")
PX, PW = 60, 960
P1Y, P2Y, PH = 300, 880, 540
C1 = (PX + 20, P1Y + 84, PX + PW - 20, P1Y + PH - 20)   # excel content box
C2 = (PX + 20, P2Y + 84, PX + PW - 20, P2Y + PH - 20)   # markazly content box
EXR = "#C0392B"; XLG = "#1D6F42"
# ---- panel frames
fr1 = rr(PX, P1Y, PW, PH, 30, "#F2F4F3") + f'<path d="M{PX} {P1Y+30} Q{PX} {P1Y} {PX+30} {P1Y} H{PX+PW-30} Q{PX+PW} {P1Y} {PX+PW} {P1Y+30} V{P1Y+68} H{PX} Z" fill="{XLG}"/>'
fr1 += rr(PX + 24, P1Y + 14, 42, 42, 8, "#fff") + T("X", PX + 45, P1Y + 47, 30, SEMI, XLG, "middle") + T("Excel", PX + 80, P1Y + 47, 32, SEMI, "#fff")
fr2 = rr(PX, P2Y, PW, PH, 30, SURF, MINT, 3) + f'<path d="M{PX} {P2Y+30} Q{PX} {P2Y} {PX+30} {P2Y} H{PX+PW-30} Q{PX+PW} {P2Y} {PX+PW} {P2Y+30} V{P2Y+68} H{PX} Z" fill="#123A2C"/>'
fr2 += f'<image href="{MARK}" x="{PX+24}" y="{P2Y+12}" width="{44*342/377:.0f}" height="44"/>' + T("Markaz", PX + 72, P2Y + 47, 32, SEMI, FG) + T("ly", PX + 72 + SEMI.width("Markaz", 32), P2Y + 47, 32, SEMI, "url(#gh)")
add(fr1, -1, T_E, dy=0, dur=.01, fo=.3); add(fr2, -1, T_E, dy=0, dur=.01, fo=.3)
# ---- timers
def piece(segs):
    def f(t):
        for a, b, x0, x1 in segs:
            if a <= t < b: return x0 + (x1 - x0) * min(1, (t - a) / max(.01, b - a) * 1.0)
        return None
    return f
xa = at("o‘n daqiqa"); ma = at("uch soniya")
ex_t = piece([(-1, 0, 0, 0), (0, xa + .6, 0, 600), (xa + .6, T_B, 600, 600), (T_B, T_C - .3, 0, 600), (T_C - .3, T_C, 600, 600), (T_C, T_D - .3, 0, 900), (T_D - .3, T_D, 900, 900), (T_D, T_E, 0, 2100)])
mk_t = piece([(-1, 0, 0, 0), (0, ma + .4, 0, 3), (ma + .4, T_B, 3, 3), (T_B, at("«Qarzdorlar»") + .5, 0, 0), (at("«Qarzdorlar»") + .5, at("«Qarzdorlar»") + 1.5, 0, 3), (at("«Qarzdorlar»") + 1.5, T_C, 3, 3),
              (T_C, at("bitta bosishda"), 0, 0), (at("bitta bosishda"), at("bitta bosishda") + 1.6, 0, 5), (at("bitta bosishda") + 1.6, T_D, 5, 5),
              (T_D, at("Markazly'da «Hisobot»") + .6, 0, 0), (at("Markazly'da «Hisobot»") + .6, at("Markazly'da «Hisobot»") + 1.4, 0, 2), (at("Markazly'da «Hisobot»") + 1.4, T_E, 2, 2)])
def timer_draw(fn, y, col_bg, col_fg, label):
    def d(fr, t):
        s = fn(t)
        if s is None: return
        s = int(s); txt = f"{s // 60:02d}:{s % 60:02d}"
        dr = ImageDraw.Draw(fr); f = pf(34)
        w = dr.textlength(txt, font=f) + 70
        x1 = PX + PW - 24; x0 = x1 - w
        dr.rounded_rectangle((x0, y + 12, x1, y + 58), 23, fill=col_bg)
        dr.ellipse((x0 + 16, y + 26, x0 + 34, y + 44), outline=col_fg, width=3); dr.line((x0 + 25, y + 30, x0 + 25, y + 35), fill=col_fg, width=3)
        dr.text((x0 + 46, y + 13), txt, font=f, fill=col_fg)
    return d
dyn(timer_draw(ex_t, P1Y, "#FFFFFF", EXR, "Excel"), -1, T_E)
dyn(timer_draw(mk_t, P2Y, "#0B2A20", "#3CF2A8", "Markazly"), -1, T_E)

# ---- EXCEL task 1: sheet of payments, slow scroll + highlight hunting
import random as _r; _r.seed(11)
first = ["Aziza", "Jasur", "Madina", "Sardor", "Nilufar", "Bobur", "Dilnoza", "Otabek", "Malika", "Sherzod", "Kamola", "Javohir", "Zarina", "Akmal", "Shahnoza", "Ulug‘bek", "Gulnora", "Timur", "Laylo", "Rustam"]
grp = ["IELTS", "B1", "A2", "Kids", "B2", "SAT"]
rows = []
for i in range(46):
    paid = _r.choice([590, 590, 400, 400, 290, 0, 590, 400]); due = _r.choice([590, 400, 400, 290])
    rows.append((i + 1, f"{_r.choice(first)} {chr(65 + _r.randrange(26))}.", _r.choice(grp), due * 1000, paid * 1000))
cw = [70, 250, 140, 200, 200]; rh = 46
sheet_w = sum(cw) + 60; sheet_h = rh * (len(rows) + 1) + 40
def sheet1():
    im = Image.new("RGBA", (sheet_w, sheet_h), (255, 255, 255, 255)); dr = ImageDraw.Draw(im); f = pf(24, False); fb = pf(24)
    hdr = ["A", "B", "C", "D", "E"]; names = ["№", "Ism", "Guruh", "Kerak", "To‘ladi"]
    x = 50
    dr.rectangle((0, 0, sheet_w, rh), fill="#E8ECEA")
    for j, w in enumerate(cw):
        dr.text((x + 10, 8), names[j], font=fb, fill="#2B3A33"); x += w
    for i, r in enumerate(rows):
        y = rh * (i + 1)
        dr.text((8, y + 9), str(i + 2), font=pf(20, False), fill="#7A8A82")
        x = 50
        for j, w in enumerate(cw):
            v_ = r[j]; s_ = f"{v_:,}".replace(",", " ") if isinstance(v_, int) and j >= 3 else str(v_)
            dr.text((x + 10, y + 9), s_, font=f, fill="#1C2A23"); x += w
        dr.line((0, y, sheet_w, y), fill="#D5DBD8", width=1)
    x = 50
    for w in cw: dr.line((x, 0, x, sheet_h), fill="#D5DBD8", width=1); x += w
    return im
S1 = sheet1()
def ex_scroll(fr, t):
    if t < T_B: off = 0
    else: off = int(min(1, (t - T_B) / (T_C - T_B)) * (S1.height - (C1[3] - C1[1]) - 10) * 0.85)
    box = C1; vw, vh = box[2] - box[0], box[3] - box[1]
    view = S1.crop((0, off, vw, off + vh)).copy()
    # highlight a row that walks down
    if T_B <= t < T_C:
        k = int((t - T_B) * 2.4); y = (k * rh * 1) % vh
        ov = Image.new("RGBA", view.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov); d.rectangle((0, y, vw, y + rh), fill=(255, 214, 0, 110), outline=(230, 170, 0, 255), width=3)
        view = Image.alpha_composite(view, ov)
    fr.alpha_composite(view, (box[0], box[1]))
dyn(ex_scroll, -1, T_C)
for k, tt in enumerate([at("adashib"), at("yana boshidan") + .3]):
    add(f'<g transform="translate({PX+PW-140 - k*260} {P1Y+200 + k*120})"><circle r="46" fill="{EXR}"/><text/></g>' + T("?", PX + PW - 140 - k * 260, P1Y + 220 + k * 120, 60, SEMI, "#fff", "middle"), tt, T_C, pop=True, dy=0, dur=.2)

# ---- EXCEL task 2: attendance grid, marks typed one by one
gn = ["Aziza S.", "Jasur R.", "Madina K.", "Sardor A.", "Nilufar T.", "Bobur O.", "Dilnoza M."]
def ex_att(fr, t):
    box = C1; vw, vh = box[2] - box[0], box[3] - box[1]
    im = Image.new("RGBA", (vw, vh), (255, 255, 255, 255)); dr = ImageDraw.Draw(im); f = pf(24, False); fb = pf(22)
    cx0, cwid = 230, 52
    dr.rectangle((0, 0, vw, 46), fill="#E8ECEA"); dr.text((12, 10), "Ism", font=fb, fill="#2B3A33")
    for d in range(12): dr.text((cx0 + d * cwid + 12, 10), str(d + 1), font=fb, fill="#2B3A33")
    total = len(gn) * 12; done = int(max(0, t - T_C - .3) * 2.2)
    for i, nm in enumerate(gn):
        y = 46 + i * 56
        dr.text((12, y + 12), nm, font=f, fill="#1C2A23"); dr.line((0, y, vw, y), fill="#D5DBD8")
        for d in range(12):
            x = cx0 + d * cwid; dr.line((x, 0, x, vh), fill="#E2E6E4")
            idx = i * 12 + d
            if idx < done:
                mark = "−" if (i * 7 + d * 3) % 11 == 0 else "+"
                dr.text((x + 16, y + 10), mark, font=pf(26), fill=EXR if mark == "−" else XLG)
            elif idx == done:
                dr.rectangle((x + 2, y + 2, x + cwid - 2, y + 54), outline="#1D6F42", width=3)
    fr.alpha_composite(im, (box[0], box[1]))
dyn(ex_att, T_C, T_D)

# ---- EXCEL task 3: broken formulas
def ex_rep(fr, t):
    box = C1; vw, vh = box[2] - box[0], box[3] - box[1]
    im = Image.new("RGBA", (vw, vh), (255, 255, 255, 255)); dr = ImageDraw.Draw(im); f = pf(24, False)
    dr.rectangle((0, 0, vw, 52), fill="#F4F6F5", outline="#D5DBD8"); dr.text((14, 12), "fx", font=pf(24), fill="#7A8A82")
    formula = "=SUMIFS(E2:E368;C2:C368;\"Chilonzor\";F2:F368;\">0\")"
    nchar = int(min(len(formula), max(0, t - T_D) * 22)); dr.text((70, 12), formula[:nchar], font=f, fill="#1C2A23")
    labels = ["Chilonzor", "Yunusobod", "Sergeli", "Jami"]
    err = t >= at("Excel'da formulalar")
    for i, lb in enumerate(labels):
        y = 80 + i * 86
        dr.text((20, y + 20), lb, font=pf(28), fill="#1C2A23")
        for j in range(3):
            x = 300 + j * 210
            dr.rectangle((x, y, x + 190, y + 70), outline="#D5DBD8", fill="#FFFFFF")
            if err and ((i + j) % 2 == 0 or i == 3):
                blink = int(t * 4) % 2 == 0
                dr.rectangle((x, y, x + 190, y + 70), fill="#FDE2DF" if blink else "#FFF1EF", outline=EXR, width=3)
                dr.text((x + 20, y + 18), "#REF!" if (i + j) % 3 else "#VALUE!", font=pf(26), fill=EXR)
            else:
                dr.text((x + 20, y + 18), f"{(i + 2) * (j + 3) * 1.7:.1f} mln", font=f, fill="#1C2A23")
    for j, h_ in enumerate(["Tushum", "Xarajat", "Foyda"]): dr.text((300 + j * 210 + 20, 52 + 6), "", font=f)
    fr.alpha_composite(im, (box[0], box[1]))
dyn(ex_rep, T_D, T_E)

# ---- MARKAZLY: tabs
tabs = ["Panel", "Qarzdorlar", "Davomat", "Hisobot"]
tab_x = []; x = C2[0] + 6
for tb in tabs:
    w = SEMI.width(tb, 28) + 50; tab_x.append((x, w)); x += w + 14
def tabrow(active):
    b = ""
    for (x, w), tb in zip(tab_x, tabs):
        on = tb == active
        b += rr(x, C2[1] + 6, w, 58, 29, MINT if on else SURF2) + T(tb, x + w / 2, C2[1] + 46, 28, SEMI, INK if on else MUTED, "middle")
    return b
tq = at("«Qarzdorlar»") + .55; td = T_C + .5; th_ = at("Markazly'da «Hisobot»") + .6
for act, a_, b_ in [("Panel", -1, tq), ("Qarzdorlar", tq, td), ("Davomat", td, th_), ("Hisobot", th_, T_E)]:
    add(tabrow(act), a_, b_, dy=0, dur=.01, fo=.01)
CY = C2[1] + 90
# panel (default) content
kp = ""; kw = (C2[2] - C2[0] - 40) / 3
for j, (lab, val, col) in enumerate([("O‘quvchi", "368", FG), ("Tushum", "184 mln", FG), ("Qarzdor", "12", BAD)]):
    kx = C2[0] + 6 + j * (kw + 14); kp += rr(kx, CY, kw, 140, 22, SURF2) + T(lab, kx + 24, CY + 46, 26, REG, MUTED) + T(val, kx + 24, CY + 110, 50, SEMI, col)
kp += rr(C2[0] + 6, CY + 160, C2[2] - C2[0] - 12, 120, 22, SURF2) + T("Bugun: 14 to‘lov · 212 / 220 darsda", C2[0] + 34, CY + 232, 30, MED, FG)
add(kp, -1, tq, dy=0, dur=.01, fo=.15)
# debtors list
debt = [("JR", "Jasur R. · IELTS", "590 000"), ("MK", "Madina K. · B1", "400 000"), ("SA", "Sardor A. · A2", "400 000"), ("NT", "Nilufar T. · Kids", "290 000")]
for i, (av, nm, sm) in enumerate(debt):
    ry = CY + i * 72
    row = rr(C2[0] + 6, ry, C2[2] - C2[0] - 12, 62, 16, "#11302A") + f'<circle cx="{C2[0]+44}" cy="{ry+31}" r="21" fill="{SURF2}"/>' + T(av, C2[0] + 44, ry + 39, 18, SEMI, MINT, "middle")
    row += T(nm, C2[0] + 80, ry + 41, 28, MED, FG) + T(sm, C2[2] - 30, ry + 41, 28, SEMI, BAD, "end")
    add(row, tq + .15 + i * .1, td, dy=20, dur=.2, fo=.15)
add(rr(C2[0] + 6, CY + 292, C2[2] - C2[0] - 12, 66, 18, "#3A1D1A", BAD, 2) + T("Jami qarz: 12 ta · 4 800 000 so‘m", C2[0] + 34, CY + 336, 32, SEMI, BAD), at("va umumiy summa"), td, pop=True, dur=.2, fo=.15)
# attendance
taps0 = at("bitta bosishda")
for i, nm in enumerate(gn[:5]):
    ry = CY + i * 60
    add(rr(C2[0] + 6, ry, C2[2] - C2[0] - 12, 52, 16, "#11302A") + T(nm, C2[0] + 34, ry + 36, 28, MED, FG) + rr(C2[2] - 196, ry + 6, 170, 40, 20, SURF2) + T("—", C2[2] - 111, ry + 35, 26, SEMI, MUTED, "middle"), td, th_, dy=10, dur=.15, fo=.15)
    ok = i != 3
    add(rr(C2[2] - 196, ry + 6, 170, 40, 20, "#123A2C" if ok else "#3A1D1A") + T("Keldi" if ok else "Kelmadi", C2[2] - 111, ry + 35, 24, SEMI, GOOD if ok else BAD, "middle"), taps0 + i * .3, th_, pop=True, dy=0, dur=.12, fo=.15)
add(rr(C2[0] + 6, CY + 304, C2[2] - C2[0] - 12, 58, 29, MINT) + ic("check", C2[0] + 30, CY + 315, 36, INK, 3) + T("Saqlandi · ota-ona kabinetida ko‘rinadi", C2[0] + 80, CY + 343, 28, SEMI, INK), at("ota-ona ham"), th_, pop=True, dur=.2, fo=.15)
# report chart
bars = [("Chilonzor", 92, 54), ("Yunusobod", 64, 41), ("Sergeli", 38, 35)]
add(T("Oktabr · filiallar", C2[0] + 10, CY + 30, 28, SEMI, FG) + rr(C2[2] - 330, CY + 2, 18, 18, 4, MINT) + T("Tushum", C2[2] - 302, CY + 20, 22, MED, MUTED) + rr(C2[2] - 180, CY + 2, 18, 18, 4, BAD) + T("Xarajat", C2[2] - 152, CY + 20, 22, MED, MUTED), th_ + .1, T_E, dy=0, dur=.15)
bw_ = 90; bx0 = C2[0] + 70
for i, (nm, inc, exp) in enumerate(bars):
    x = bx0 + i * 290; base = CY + 300
    add(T(nm, x + bw_, base + 40, 26, MED, MUTED, "middle"), th_ + .1, T_E, dy=0, dur=.15)
    def mkbar(x=x, base=base, inc=inc, exp=exp, i=i):
        def d(fr, t):
            k1 = ease((t - at("har bir filial")) / .6); k2 = ease((t - at("xarajat")) / .6)
            dr = ImageDraw.Draw(fr)
            h1 = inc * 1.9 * k1; h2 = exp * 1.9 * k2
            if h1 > 1: dr.rounded_rectangle((x, base - h1, x + bw_, base), 10, fill=(46, 229, 157))
            if h2 > 1: dr.rounded_rectangle((x + bw_ + 10, base - h2, x + 2 * bw_ + 10, base), 10, fill=(255, 122, 107))
            if k2 > .9:
                pr = inc - exp; txt = f"+{pr} mln"
                dr.text((x + 10, base - max(h1, h2) - 46), txt, font=pf(30), fill=(70, 217, 143))
        return d
    dyn(mkbar(), th_, T_E)

# ---- cursor with click ripples (Markazly side)
cur_img, _, _ = crop_el('<path d="M0 0 L0 46 L12 35 L20 54 L29 50 L21 32 L37 32 Z" fill="#fff" stroke="#0A1F17" stroke-width="3" stroke-linejoin="round"/>')
def tab_center(i): x, w = tab_x[i]; return (x + w / 2, C2[1] + 35)
keys = [(T_B, (C2[2] - 120, CY + 300)), (tq - .5, tab_center(1)), (tq + .4, tab_center(1)), (td - .5, tab_center(2)), (td + .2, tab_center(2))]
for i in range(5): keys += [(taps0 + i * .3 - .12, (C2[2] - 111, CY + i * 60 + 26)), (taps0 + i * .3 + .05, (C2[2] - 111, CY + i * 60 + 26))]
keys += [(th_ - .5, tab_center(3)), (th_ + .3, tab_center(3)), (T_E, (C2[2] - 200, CY + 200))]
clicks = [tq, td] + [taps0 + i * .3 for i in range(5)] + [th_]
def cursor(fr, t):
    if t < keys[0][0]: p = keys[0][1]
    else:
        p = keys[-1][1]
        for (a, pa), (b, pb) in zip(keys, keys[1:]):
            if a <= t < b:
                k = ease((t - a) / max(.01, b - a)); p = (pa[0] + (pb[0] - pa[0]) * k, pa[1] + (pb[1] - pa[1]) * k); break
    for c in clicks:
        if 0 <= t - c < .45:
            r = 14 + 60 * (t - c) / .45; a = int(170 * (1 - (t - c) / .45))
            ov = Image.new("RGBA", fr.size, (0, 0, 0, 0)); ImageDraw.Draw(ov).ellipse((p[0] - r, p[1] - r, p[0] + r, p[1] + r), outline=(60, 242, 168, a), width=6); fr.alpha_composite(ov)
    fr.alpha_composite(cur_img, (int(p[0]), int(p[1])))
dyn(cursor, T_B, T_E)

# ---- hook overlays: verdicts
add(rr(PX + 220, P1Y + 230, 520, 150, 40, "#3A1D1A", EXR, 4) + T("10 daqiqa", CX, P1Y + 335, 84, SEMI, BAD, "middle"), at("o‘n daqiqa") - .1, T_B, pop=True)
add(rr(PX + 220, P2Y + 230, 520, 150, 40, "#123A2C", MINT, 4) + T("3 soniya", CX, P2Y + 335, 84, SEMI, MINT, "middle"), at("uch soniya") - .1, T_B, pop=True)
add(T("Qarzdorlarni topish", CX, 250, 50, SEMI, FG, "middle"), -1, T_B, dy=0, dur=.01)
add(T("Davomat qilish", CX, 250, 50, SEMI, FG, "middle"), T_C, T_D, dy=0, dur=.2)
add(T("Oylik hisobot", CX, 250, 50, SEMI, FG, "middle"), T_D, T_E, dy=0, dur=.2)
add(T("Qarzdorlarni topish", CX, 250, 50, SEMI, FG, "middle"), T_B, T_C, dy=0, dur=.01)


# VS badge between the panels during the hook
add(f'<circle cx="{CX}" cy="{(P1Y+PH+P2Y)//2}" r="52" fill="#0D2620" stroke="#F4F8F6" stroke-width="5"/>' + T("VS", CX, (P1Y + PH + P2Y) // 2 + 15, 40, SEMI, FG, "middle"), -1, T_B, dy=0, dur=.01, pop=False)
# ---- E. result scoreboard
add(rr(90, 420, 900, 330, 44, "#3A1D1A", EXR, 4) + T("Excel", CX, 520, 50, SEMI, "#F3D6D0", "middle") + T("1 soat", CX, 670, 130, SEMI, BAD, "middle"), T_E, T_F, pop=True)
add(rr(90, 800, 900, 330, 44, "#123A2C", MINT, 4) + T("Markazly", CX, 900, 50, SEMI, FG, "middle") + T("1 daqiqa", CX, 1050, 130, SEMI, MINT, "middle"), at("Markazly'da bir daqiqa"), T_F, pop=True)

# ---- F. CTA
add('<circle cx="540" cy="760" r="480" fill="url(#halo)"/>', T_F, DUR + 1, dy=0, dur=.8)
add(T("Hoziroq", CX, 520, 76, SEMI, FG, "middle") + T("pastdagi tugmani", CX, 610, 76, SEMI, FG, "middle") + T("bosing", CX, 700, 76, SEMI, "url(#gh)", "middle"), T_F, DUR + 1)
add(rr(110, 790, 860, 210, 105, "url(#gh)") + T("7 kun bepul", CX, 892, 84, SEMI, INK, "middle") + T("sinab ko‘ring", CX, 960, 46, MED, "#0A3D27", "middle"), at("Markazly'ni 7 kun"), DUR + 1, pop=True)
add(T("markazly.onrender.com", CX, 1090, 38, MED, MUTED, "middle"), at("Markazly'ni 7 kun") + .6, DUR + 1)
arrow = f'<g transform="translate({CX-60} 1170)"><circle cx="60" cy="60" r="60" fill="#2EE59D" fill-opacity=".18"/><path d="M60 28 V92 M32 66 L60 94 L88 66" fill="none" stroke="#2EE59D" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></g>'
add(arrow, T_F + .8, DUR + 1, bob=14)
S_B, S_F = T_B, T_F
OUTNAME = 'markazly_video8_excel.mp4'; MIXNAME = 'mix_v8.m4a'; HOOK_END = at('Qarang'); FLASH = None
SAMPLES = (0.0, 1.0, 2.5, 4.0, 7.0, 10.5, 13.5, 16.5, 20.0, 23.5, 26.5, 29.5, 33.0, 36.5, 38.8, 42.5)
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
out = os.path.join(OUTDIR, OUTNAME)
ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                       "-i", os.path.join(os.path.dirname(OUTDIR), "audio", MIXNAME), "-af", "apad", "-shortest",
                       "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
samples = [int(x * FPS) for x in SAMPLES]
for i in range(n):
    t = i / FPS
    fr = BG.copy()
    for e in E: e.draw(fr, t)
    if t < HOOK_END:
        z = 1 + 0.05 * ease(t / HOOK_END)
        sh = FLASH is not None and FLASH <= t <= FLASH + .3
        if sh: z += 0.02
        cw_, ch_ = W / z, H / z
        ox = (W - cw_) / 2 + (10 * math.sin(t * 190) if sh else 0); oy = (H - ch_) / 2 + (8 * math.cos(t * 230) if sh else 0)
        fr = fr.crop((int(ox), int(oy), int(ox + cw_), int(oy + ch_))).resize((W, H), Image.BILINEAR)
        if FLASH is not None and FLASH <= t <= FLASH + .2:
            fr.alpha_composite(Image.new("RGBA", (W, H), (255, 70, 60, int(90 * (1 - (t - FLASH) / .2)))))
    ff.stdin.write(fr.convert("RGB").tobytes())
    if i in samples: fr.convert("RGB").save(os.path.join(OUTDIR, f"{OUTNAME[:-4]}_kadr_{t:04.1f}.png"))
ff.stdin.close(); ff.wait()
print("done", out)
