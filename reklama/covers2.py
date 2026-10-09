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


# ───────── one shared template: same brand row, same visual card, same headline block, same badge
def cover(num, tag, lines, visual, name, red_glow=False):
    b = '<circle cx="540" cy="620" r="560" fill="url(#%s)"/>' % ("rd" if red_glow else "halo")
    b += brand(270)
    # series number + topic tag
    tw = SEMI.width(tag, 30) + 60
    b += rr(CX - tw / 2 - 40, 378, tw + 80, 60, 30, "#0F3A2C", MINT, 2) + T(f"{num:02d}", CX - tw / 2 - 6, 418, 30, SEMI, MINT, "middle") + T(tag, CX - tw / 2 + 30, 418, 30, SEMI, FG)
    # visual card
    b += rr(110, 470, 860, 420, 40, SURF, LINE, 2) + visual(110, 470, 860, 420)
    # headline (3 lines, last one in brand gradient)
    for i, (t) in enumerate(lines):
        size = 104
        while SEMI.width(t, size) > 900: size -= 4
        b += T(t, CX, 1035 + i * 122, size, SEMI, "url(#gh)" if i == len(lines) - 1 else FG, "middle")
    b += badge(1360)
    save(b, name)

def v_admin(x, y, w, h):
    o = rr(x + 40, y + 70, w - 80, 270, 34, "#F4F8F6") + f'<circle cx="{x+112}" cy="{y+138}" r="38" fill="url(#g)"/>' + T("A", x + 112, y + 152, 38, SEMI, INK, "middle")
    o += T("Admin", x + 168, y + 132, 34, SEMI, INK) + T("hozir · Telegram", x + 168, y + 168, 22, REG, "#5C7268")
    o += T("Bugungi tushum:", x + 76, y + 240, 30, MED, "#3F5A4D") + T("? ??? ??? so‘m", x + 76, y + 300, 58, SEMI, BAD)
    o += f'<g transform="translate({x+w-70} {y+70}) rotate(12)"><circle r="54" fill="{BAD}"/><path d="M0 -26 V8" stroke="#fff" stroke-width="11" stroke-linecap="round"/><circle cy="28" r="7" fill="#fff"/></g>'
    return o
def v_loss(x, y, w, h):
    o = T("HAR OY", x + w / 2, y + 80, 36, SEMI, BAD, "middle") + T("−4 000 000", x + w / 2, y + 210, 126, SEMI, BAD, "middle") + T("so‘m", x + w / 2, y + 268, 40, MED, "#F3D6D0", "middle")
    import random as _r; _r.seed(5); red = set(_r.sample(range(60), 6)); g = 36; x0 = x + w / 2 - 19 * g / 2
    for i in range(60):
        cx_ = x0 + (i % 20) * g; cy_ = y + 318 + (i // 20) * g
        o += f'<circle cx="{cx_:.0f}" cy="{cy_}" r="{15 if i in red else 11}" fill="{BAD if i in red else "#2EE59D"}" fill-opacity="{1 if i in red else .5}"/>'
    return o
def v_system(x, y, w, h):
    o = ""; kw = (w - 80 - 30) / 3; kx = x + 40
    for lab, val, col in [("O‘quvchi", "368", FG), ("Tushum", "184 mln", FG), ("Qarzdor", "12", BAD)]:
        o += rr(kx, y + 40, kw, 130, 22, SURF2) + T(lab, kx + 22, y + 84, 26, REG, MUTED) + T(val, kx + 22, y + 146, 46, SEMI, col); kx += kw + 15
    for i, (icn, t) in enumerate([("users", "Davomat"), ("wallet", "To‘lovlar"), ("branch", "Filiallar"), ("globe", "Sayt"), ("cap", "Kabinet")]):
        cx_ = x + 40 + i * ((w - 80) / 5) + (w - 80) / 10
        o += f'<circle cx="{cx_:.0f}" cy="{y+260}" r="50" fill="#123A2C"/>' + ic(icn, cx_ - 26, y + 234, 52, MINT, 2) + T(t, cx_, y + 350, 24, MED, MUTED, "middle")
    return o
def v_branch(x, y, w, h):
    o = ""
    for i, (nm, val, pct, col) in enumerate([("1-filial · Chilonzor", "+ 18 mln", .82, GOOD), ("2-filial · Yunusobod", "− 6 mln", .34, BAD)]):
        yy = y + 70 + i * 160
        o += T(nm, x + 50, yy + 10, 34, SEMI, FG) + T(val, x + w - 50, yy + 10, 40, SEMI, col, "end")
        o += rr(x + 50, yy + 40, w - 100, 40, 20, LINE) + rr(x + 50, yy + 40, (w - 100) * pct, 40, 20, col)
    return o
def v_parent(x, y, w, h):
    o = rr(x + 40, y + 60, 620, 120, 34, "#16392D") + T("Assalomu alaykum, bolam", x + 76, y + 112, 32, MED, FG) + T("bugun darsga keldimi?", x + 76, y + 154, 32, MED, FG)
    o += T("Ota-ona · 19:42", x + 40, y + 216, 22, REG, MUTED)
    o += rr(x + w - 520, y + 250, 480, 110, 34, "url(#gh)") + ic("tick", x + w - 494, y + 280, 50, INK, 2.4) + T("Keldi · 18:00", x + w - 430, y + 318, 34, SEMI, INK)
    return o
def v_trial(x, y, w, h):
    o = T("7", x + 200, y + 300, 300, SEMI, "url(#gh)", "middle") + T("kun", x + 200, y + 370, 50, SEMI, FG, "middle")
    for i, t in enumerate(["3 daqiqada boshlaysiz", "Ma’lumotni o‘zimiz ko‘chiramiz", "Yoqmasa — to‘lamaysiz"]):
        yy = y + 110 + i * 100
        o += f'<circle cx="{x+410}" cy="{yy}" r="30" fill="#123A2C"/>' + ic("check", x + 394, yy - 16, 32, MINT, 3) + T(t, x + 460, yy + 11, 28, MED, FG)
    return o

def v_all(x, y, w, h):
    o = ""
    tiles = [("Boshqaruv", "users"), ("Filiallar", "branch"), ("Sayt", "globe"), ("Kabinet", "cap"), ("Reyting", "chart"), ("To‘lovlar", "wallet")]
    tw, th = (w - 80 - 40) / 3, (h - 80 - 20) / 2
    for k, (nm, icn) in enumerate(tiles):
        tx = x + 40 + (k % 3) * (tw + 20); ty = y + 40 + (k // 3) * (th + 20)
        o += rr(tx, ty, tw, th, 24, SURF2) + f'<circle cx="{tx+tw/2:.0f}" cy="{ty+70}" r="44" fill="#123A2C"/>' + ic(icn, tx + tw / 2 - 24, ty + 46, 48, MINT, 2) + T(nm, tx + tw / 2, ty + 150, 28, SEMI, FG, "middle")
    return o
cover(1, "Hisobot", ["Admin", "hisobotiga", "ishonasizmi?"], v_admin, "cover_01_admin.png", True)
cover(2, "Markazly", ["Markazingiz", "bitta tizimda", "to‘liq"], v_system, "cover_02_tizim.png")
cover(3, "Qarzdorlar", ["Har oy", "qancha pul", "yo‘qotyapsiz?"], v_loss, "cover_03_yoqotish.png", True)
cover(4, "Filiallar", ["Qaysi filialingiz", "zarar", "qilyapti?"], v_branch, "cover_04_filiallar.png", True)
cover(5, "Ota-onalar", ["“Bolam darsga", "keldimi?”", "Javob tayyor"], v_parent, "cover_05_ota_ona.png")
cover(7, "Umumiy", ["Hammasi", "bitta", "tizimda"], v_all, "cover_07_umumiy.png")
cover(6, "Bepul sinov", ["Avval sinang,", "yoqsa", "keyin to‘lang"], v_trial, "cover_06_sinov.png")

# profile grid preview (3:4 centre crops, newest first = 6..1)
names = ["cover_06_sinov", "cover_05_ota_ona", "cover_04_filiallar", "cover_03_yoqotish", "cover_02_tizim", "cover_01_admin"]
g = Image.new("RGB", (3 * 360 + 8, 2 * 480 + 4), "white")
for i, n in enumerate(names):
    g.paste(Image.open(os.path.join(OUTDIR, n + "_tor.png")), ((i % 3) * 364, (i // 3) * 484))
g.save(os.path.join(OUTDIR, "coverlar_profilda.png"))
print("ok")
