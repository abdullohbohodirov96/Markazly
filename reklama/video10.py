TIMING = 'timing10'
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
T_B, T_C, T_D, T_E, T_F, T_G = at("Keling"), at("Birinchi"), at("Ikkinchi"), at("Uchinchi"), at("Va eng muhimi"), at("Hoziroq")
# ── A. hook: the two fears
add(T("Yangi tizimga", CX, 440, 84, SEMI, FG, "middle") + T("o‘tishdan qo‘rqasizmi?", CX, 540, 84, SEMI, BAD, "middle"), -1, T_C, dy=0, dur=.01)
fears = [("Ma’lumotlarim yo‘qolib", "qolmaydimi?", at("«Ma’lumotlarim"), 640, 110), ("Xodimlarim o‘rgana", "oladimi?", at("xodimlarim o‘rgana"), 860, 260)]
for l1, l2, tt, y, x in fears:
    add(rr(x, y, 720, 180, 40, "#2A1D1B", "#5A2A24", 3) + f'<path d="M{x+60} {y+178} l20 40 l30 -40 Z" fill="#2A1D1B"/>' + T(l1, x + 40, y + 76, 44, SEMI, "#F3D6D0") + T(l2, x + 40, y + 136, 44, SEMI, "#F3D6D0"), -1 if tt < .5 else tt, T_C, pop=True)
for l1, l2, tt, y, x in fears:
    add(f'<circle cx="{x+700}" cy="{y+20}" r="44" fill="{MINT}"/>' + ic("check", x + 680, y, 40, INK, 3.2), T_B + .6 + (y - 640) / 900, T_C, pop=True)
add(T("Hammasiga javob:", CX, 1230, 56, SEMI, MINT, "middle"), T_B + .2, T_C)
def step(n, title, sub, t0, t1):
    add(rr(CX - 60, 380, 120, 120, 60, "url(#gh)") + T(str(n), CX, 470, 76, SEMI, INK, "middle"), t0, t1, pop=True)
    add(T(title, CX, 610, 72, SEMI, FG, "middle"), t0 + .2, t1)
    add(T(sub, CX, 680, 38, MED, MUTED, "middle"), t0 + .4, t1)
# ── C. migration
step(1, "O‘zimiz ko‘chiramiz", "Excel, daftar — qaysi bo‘lsa ham", T_C, T_D)
xl = rr(150, 790, 220, 270, 24, "#F2F4F3") + rr(150, 790, 220, 60, 24, "#1D6F42") + T("X", 260, 836, 40, SEMI, "#fff", "middle") + "".join(rr(175, 880 + i * 40, 170, 18, 6, "#C9D3CE") for i in range(4))
nb = rr(420, 790, 220, 270, 24, "#F6C76B") + "".join(f'<line x1="440" y1="{860 + i*36}" x2="620" y2="{860 + i*36}" stroke="#8A6A2A" stroke-width="3"/>' for i in range(5)) + rr(420, 790, 30, 270, 12, "#E8873D")
add(xl, at("Excel'dami"), T_D, pop=True); add(nb, at("Excel'dami") + .5, T_D, pop=True)
def flow(fr, t):
    from PIL import ImageDraw
    k = (t - at("o‘zimiz tizimga")) * 1.6; dr = ImageDraw.Draw(fr)
    for j in range(5):
        p = (k + j * .2) % 1
        x = 650 + p * 160; y = 925
        dr.ellipse((x - 9, y - 9, x + 9, y + 9), fill=(46, 229, 157, int(255 * (1 - abs(p - .5) * 2))))
dyn(flow, at("o‘zimiz tizimga"), T_D)
db = f'<image href="{MARK}" x="840" y="840" width="{150*342/377:.0f}" height="150"/>'
add(rr(810, 790, 220, 270, 24, SURF, MINT, 3) + db + T("Markazly", 920, 1030, 28, SEMI, FG, "middle"), at("o‘zimiz tizimga"), T_D, pop=True)
# ── D. separate databases
step(2, "Har bir markaz — alohida", "Ma’lumotlaringizni faqat siz ko‘rasiz", T_D, T_E)
for i, (nm, mine) in enumerate([("A markaz", False), ("Sizning markaz", True), ("B markaz", False)]):
    x = 100 + i * 300
    add(rr(x, 800, 280, 300, 30, "#123A2C" if mine else SURF, MINT if mine else LINE, 4 if mine else 2) + ic("lock", x + 100, 850, 80, MINT if mine else MUTED, 2.2)
        + T(nm.split()[0], x + 140, 1000, 32, SEMI, FG if mine else MUTED, "middle") + T(" ".join(nm.split()[1:]), x + 140, 1042, 28, MED, FG if mine else MUTED, "middle"), at("har bir markazning") + i * .25, T_E, pop=True)
add(rr(250, 1130, 580, 70, 35, "#123A2C", MINT, 2) + T("Boshqa hech kim ko‘rmaydi", CX, 1177, 34, SEMI, MINT, "middle"), at("ma’lumotlaringizni sizdan"), T_E, pop=True)
# ── E. training
step(3, "O‘zimiz o‘qitamiz", "Markazingizga borib, xodimlaringizga", T_E, T_F)
board = rr(240, 790, 600, 330, 26, "#F4F8F6") + rr(270, 820, 540, 230, 14, SURF) + f'<image href="{MARK}" x="300" y="850" width="{90*342/377:.0f}" height="90"/>' + "".join(rr(410, 860 + i * 40, 360 - i * 80, 20, 8, MINT if i == 0 else LINE) for i in range(3))
add(board, at("markazingizga o‘zimiz"), T_F, pop=True)
for i in range(3):
    x = 330 + i * 210
    add(f'<circle cx="{x}" cy="1180" r="38" fill="{SURF2}"/><path d="M{x-60} 1290 Q{x} 1200 {x+60} 1290 Z" fill="{SURF2}"/>', at("xodimlaringizni") + i * .15, T_F, pop=True)
# ── F. guarantee
add(T("Va eng muhimi", CX, 440, 60, SEMI, MUTED, "middle"), T_F, T_G)
add(T("7", 300, 800, 330, SEMI, "url(#gh)", "middle") + T("kun bepul", 300, 880, 48, SEMI, FG, "middle"), at("avval 7 kun"), T_G, pop=True)
add(rr(520, 560, 460, 180, 36, "#123A2C", MINT, 3) + T("Yoqmasa —", 560, 630, 40, SEMI, FG) + T("0 so‘m", 560, 712, 72, SEMI, MINT), at("yoqmasa"), T_G, pop=True)
add(rr(520, 770, 460, 120, 36, SURF, LINE, 2) + T("Hech qanday shart yo‘q", 560, 845, 32, MED, FG), at("hech narsa"), T_G, pop=True)
# ── G. CTA
add('<circle cx="540" cy="760" r="480" fill="url(#halo)"/>', T_G, DUR + 1, dy=0, dur=.8)
add(T("Hoziroq", CX, 520, 76, SEMI, FG, "middle") + T("pastdagi tugmani", CX, 610, 76, SEMI, FG, "middle") + T("bosing", CX, 700, 76, SEMI, "url(#gh)", "middle"), T_G, DUR + 1)
add(rr(110, 790, 860, 210, 105, "url(#gh)") + T("7 kun bepul", CX, 892, 84, SEMI, INK, "middle") + T("sinab ko‘ring", CX, 960, 46, MED, "#0A3D27", "middle"), at("Markazly'ni 7 kun"), DUR + 1, pop=True)
add(T("markazly.onrender.com", CX, 1090, 38, MED, MUTED, "middle"), at("Markazly'ni 7 kun") + .5, DUR + 1)
arrow = f'<g transform="translate({CX-60} 1170)"><circle cx="60" cy="60" r="60" fill="#2EE59D" fill-opacity=".18"/><path d="M60 28 V92 M32 66 L60 94 L88 66" fill="none" stroke="#2EE59D" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></g>'
add(arrow, T_G + .8, DUR + 1, bob=14)
S_B, S_F = T_B, T_G
OUTNAME = 'markazly_video10_etirozlar.mp4'; MIXNAME = 'mix_v10.m4a'; HOOK_END = at('Keling'); FLASH = None
SAMPLES = (0.0, 1.8, 4.5, 7.5, 11.0, 13.6, 17.0, 20.0, 23.0, 25.0, 27.5, 29.5, 32.5)
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
