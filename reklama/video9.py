TIMING = 'timing9'
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
T_B, T_C, T_D, T_E, T_F = at("Markazly'ning oylik"), at("Endi solishtiring"), at("Markazly esa"), at("Ya'ni tizim"), at("Hoziroq")
# ── A. hook: price of one lunch
add('<circle cx="540" cy="700" r="460" fill="url(#halo)"/>', -1, T_B, dy=0, dur=.01)
add(T("KUNIGA", CX, 470, 48, SEMI, MINT, "middle") + T("10 000", CX, 650, 200, SEMI, "url(#gh)", "middle") + T("so‘m", CX, 740, 60, MED, FG, "middle"), -1, T_B, dy=0, dur=.01)
bowl = (f'<g transform="translate({CX} 930)"><ellipse cx="0" cy="40" rx="150" ry="22" fill="#000" fill-opacity=".25"/>'
        f'<path d="M-140 -10 H140 A140 120 0 0 1 -140 -10 Z" fill="#F6C76B"/><path d="M-120 -10 Q0 -90 120 -10 Z" fill="#F4F8F6"/>'
        f'<circle cx="-40" cy="-40" r="12" fill="#E8873D"/><circle cx="20" cy="-48" r="10" fill="#E8873D"/><circle cx="60" cy="-30" r="9" fill="#46D98F"/></g>')
add(bowl, at("bu bitta tushlikdan") - .1, T_B, pop=True)
add(T("= bitta tushlikdan arzon", CX, 1150, 54, SEMI, FG, "middle"), at("bu bitta tushlikdan") + .3, T_B)
# ── B. price breakdown
def pcard(y, top, big, col, sub=""):
    return rr(110, y, 860, 190, 40, SURF, LINE, 2) + T(top, 160, y + 66, 34, MED, MUTED) + T(big, 160, y + 156, 84, SEMI, col) + (T(sub, 930, y + 156, 36, MED, MUTED, "end") if sub else "")
add(pcard(450, "Markazly · Start tarifi", "290 000", FG, "so‘m / oy"), at("Markazly'ning oylik"), T_C, dy=40)
add(T("÷ 30 kun", CX, 730, 60, SEMI, MUTED, "middle"), at("290 ming"), T_C, pop=True)
add(rr(110, 790, 860, 210, 44, "url(#gh)") + T("9 700 so‘m", CX, 905, 100, SEMI, INK, "middle") + T("kuniga", CX, 966, 40, MED, "#0A3D27", "middle"), at("9 700"), T_C, pop=True)
# ── C. compare: tiny daily price vs real losses
add(T("Endi solishtiring", CX, 430, 66, SEMI, FG, "middle"), T_C, T_D)
add(rr(110, 490, 860, 150, 36, "#123A2C", MINT, 3) + T("Markazly", 160, 550, 34, MED, MUTED) + T("9 700 so‘m / kun", 160, 612, 56, SEMI, MINT), T_C + .2, T_D, dy=30)
add(rr(110, 670, 860, 200, 36, "#3A1D1A", BAD, 3) + T("1 ta unutilgan to‘lov", 160, 736, 34, MED, "#F3D6D0") + T("−400 000 so‘m", 160, 830, 80, SEMI, BAD), at("bitta o‘quvchi to‘lovni"), T_D, pop=True, jit=(at("400 ming"), at("400 ming") + .3))
add(rr(110, 900, 860, 200, 36, "#3A1D1A", BAD, 3) + T("1 ta javobsiz ariza", 160, 966, 34, MED, "#F3D6D0") + T("−1 o‘quvchi", 160, 1060, 80, SEMI, BAD), at("Bitta javobsiz"), T_D, pop=True)
# ── D. one place
add(T("Hammasi bitta joyda", CX, 430, 66, SEMI, FG, "middle"), T_D, T_E)
add(rr(90, 480, 900, 620, 44, SURF, MINT, 3), T_D + .1, T_E, dy=40)
for i, (icn, nm, sub, tt) in enumerate([("wallet", "Qarzdorlar", "12 ta · 4,8 mln so‘m", "Markazly esa"), ("users", "Arizalar", "Bugun 5 ta yangi", "arizalarni ham"), ("cal", "Davomat", "212 / 220 darsda", "davomatni ham")]):
    y = 520 + i * 185
    add(rr(130, y, 820, 160, 30, SURF2) + f'<circle cx="220" cy="{y+80}" r="52" fill="#123A2C"/>' + ic(icn, 192, y + 52, 56, MINT, 2) + T(nm, 300, y + 72, 44, SEMI, FG) + T(sub, 300, y + 122, 30, MED, MUTED)
        + f'<circle cx="890" cy="{y+80}" r="28" fill="{MINT}"/>' + ic("check", 874, y + 64, 32, INK, 3), at(tt), T_E, pop=True)
# ── E. pays for itself
add(T("O‘z pulini", CX, 450, 80, SEMI, FG, "middle") + T("1-oydayoq qaytaradi", CX, 550, 80, SEMI, "url(#gh)", "middle"), T_E, T_F)
add(rr(110, 620, 860, 470, 40, SURF, LINE, 2) + T("Foyda", 150, 680, 30, MED, MUTED) + "".join(T(f"{m}-oy", 210 + i * 230, 1060, 28, MED, MUTED, "middle") for i, m in enumerate([1, 2, 3, 4])), T_E + .2, T_F, dy=40)
def growth(fr, t):
    from PIL import ImageDraw
    k = ease((t - T_E - .4) / 1.8)
    pts = [(210, 1000), (440, 900), (670, 790), (900, 680)]
    n = 1 + k * 3; dr = ImageDraw.Draw(fr)
    cur = []
    for i in range(int(n)): cur.append(pts[i])
    if int(n) < 4:
        a, b = pts[int(n) - 1], pts[int(n)]; f = n - int(n); cur.append((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f))
    if len(cur) > 1: dr.line(cur, fill=(46, 229, 157), width=12, joint="curve")
    for p in cur[:-1]: dr.ellipse((p[0] - 14, p[1] - 14, p[0] + 14, p[1] + 14), fill=(46, 229, 157))
    dr.line((150, 1010, 950, 1010), fill=(60, 90, 80), width=3)
dyn(growth, T_E + .3, T_F)
add(rr(620, 700, 300, 70, 35, "#123A2C", MINT, 2) + T("+ foydangiz", 770, 747, 34, SEMI, MINT, "middle"), at("qolgani sizning"), T_F, pop=True)
# ── F. CTA
add('<circle cx="540" cy="760" r="480" fill="url(#halo)"/>', T_F, DUR + 1, dy=0, dur=.8)
add(T("Hoziroq", CX, 520, 76, SEMI, FG, "middle") + T("pastdagi tugmani", CX, 610, 76, SEMI, FG, "middle") + T("bosing", CX, 700, 76, SEMI, "url(#gh)", "middle"), T_F, DUR + 1)
add(rr(110, 790, 860, 210, 105, "url(#gh)") + T("7 kun bepul", CX, 892, 84, SEMI, INK, "middle") + T("yoqmasa — 0 so‘m", CX, 960, 46, MED, "#0A3D27", "middle"), at("Markazly'ni 7 kun"), DUR + 1, pop=True)
add(T("markazly.uz", CX, 1090, 38, MED, MUTED, "middle"), at("yoqmasa"), DUR + 1)
arrow = f'<g transform="translate({CX-60} 1170)"><circle cx="60" cy="60" r="60" fill="#2EE59D" fill-opacity=".18"/><path d="M60 28 V92 M32 66 L60 94 L88 66" fill="none" stroke="#2EE59D" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></g>'
add(arrow, T_F + .8, DUR + 1, bob=14)
S_B, S_F = T_B, T_F
OUTNAME = 'markazly_video9_narx.mp4'; MIXNAME = 'mix_v9.m4a'; HOOK_END = at('Markazly\'ning oylik'); FLASH = None
SAMPLES = (0.0, 1.5, 3.0, 5.5, 8.4, 10.5, 12.5, 15.5, 19.5, 22.5, 25.5, 28.0, 31.0, 34.0)
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
