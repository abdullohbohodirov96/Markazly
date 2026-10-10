TIMING = 'timing12'
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
import sys
sys.path.insert(0, os.path.dirname(OUTDIR))
from arabic import TA, AR
def ar(t, x, y, s, col=FG, anchor="middle"): return TA(t, x, y, s, AR, col, anchor)
T_B, T_C, T_D, T_E, T_F, T_G = at("Arab tilida eng"), at("Markazly'da har bir"), at("O‘quvchi har bir"), at("Siz esa kim"), at("Ota-ona ham"), at("Hoziroq")
# ── A. hook
add(ar("العربية", CX, 640, 260, "#2EE59D").replace('fill="#2EE59D"', 'fill="#2EE59D" fill-opacity=".10"'), -1, T_B, dy=0, dur=.01)
add(T("Arab tili", CX, 560, 120, SEMI, "url(#gh)", "middle") + T("markazingiz bormi?", CX, 690, 92, SEMI, FG, "middle"), -1, T_B, dy=0, dur=.01)
add(rr(240, 800, 600, 100, 50, "#123A2C", MINT, 2) + T("Bu video siz uchun", CX, 866, 44, SEMI, MINT, "middle"), at("Unda bu video"), T_B, pop=True)
# ── B. the problem: words are forgotten
add(T("Eng qiyini —", CX, 440, 70, SEMI, FG, "middle") + T("so‘z yodlash", CX, 540, 84, SEMI, "url(#gh)", "middle"), T_B, T_C)
add(rr(190, 620, 700, 440, 40, "url(#best)", MINT, 3) + ar("كِتَاب", CX, 840, 150) + T("kitob", CX, 940, 48, MED, MUTED, "middle"), at("so‘z yodlash"), at("uyga borib"), pop=True)
add(rr(190, 620, 700, 440, 40, "#1A1F1D", "#5A2A24", 3) + ar("؟ ؟ ؟", CX, 860, 150, "#5A6B63") + T("esdan chiqdi", CX, 960, 48, SEMI, BAD, "middle"), at("uyga borib"), T_C, pop=True)
add(T("Darsda tushundi…", CX, 1150, 46, MED, MUTED, "middle"), at("o‘quvchi darsda"), T_C)
# ── C. cabinet with flashcards
add(T("O‘quvchi kabineti", CX, 420, 72, SEMI, FG, "middle"), T_C, T_D)
px, py, pw, ph = 300, 470, 480, 780
p = rr(px - 12, py - 12, pw + 24, ph + 24, 70, "#020806") + rr(px, py, pw, ph, 58, SURF) + rr(px + pw / 2 - 72, py + 20, 144, 28, 14, "#020806")
p += f'<circle cx="{px+58}" cy="{py+104}" r="30" fill="url(#g)"/>' + T("A", px + 58, py + 117, 30, SEMI, INK, "middle") + T("Arab tili · A1", px + 104, py + 94, 22, REG, MUTED) + T("Aziza Sobirova", px + 104, py + 128, 28, SEMI, FG)
add(p, T_C, T_D, dy=80, dur=.4)
cards = [("كِتَاب", "kitob"), ("قَلَم", "qalam"), ("مَدْرَسَة", "maktab")]
for i, (a, u) in enumerate(cards):
    y = py + 170 + i * 150
    add(rr(px + 22, y, pw - 44, 132, 24, "url(#best)" if i == 0 else SURF2, MINT if i == 0 else None) + ar(a, px + pw - 60, y + 86, 60, FG, "right") + T(u, px + 50, y + 82, 30, MED, MUTED), at("shaxsiy kabineti") + .4 + i * .35, T_D, pop=True, dur=.2)
add(rr(px + 22, py + 640, pw - 44, 110, 24, SURF2) + ic("book", px + 46, py + 672, 44, "url(#g)", 2) + T("Uyga vazifa", px + 106, py + 686, 22, REG, MUTED) + T("92 / 100", px + 106, py + 724, 28, SEMI, GOOD), at("uyga vazifa va baholar"), T_D, pop=True)
# ── D. gamification
add('<circle cx="540" cy="760" r="480" fill="url(#halo)"/>', T_D, T_E, dy=0, dur=.5)
add(T("Har bir so‘z — ball", CX, 420, 72, SEMI, FG, "middle"), T_D, T_E)
for j, (tt, x, y, w_) in enumerate([(0.3, 150, 480, "كِتَاب"), (0.9, 600, 470, "قَلَم"), (1.5, 380, 590, "بَيْت")]):
    add(rr(x, y, 320, 90, 45, "#2A2412", AMB, 2) + ar(w_, x + 230, y + 62, 46, FG) + T("+10", x + 70, y + 60, 40, SEMI, AMB, "middle"), T_D + tt, T_E, pop=True, dur=.2)
lb = rr(110, 720, 860, 400, 36, SURF, LINE, 2) + T("Reyting · Arab tili A1", 150, 780, 32, SEMI, FG)
for j, (nm, pts) in enumerate([("Aziza S.", "1 248"), ("Jasur R.", "1 190"), ("Madina K.", "1 052"), ("Sardor A.", "860")]):
    yy = 810 + j * 74
    lb += rr(140, yy, 800, 62, 14, "#2A2412" if j == 0 else "#11302A") + T(str(j + 1), 176, yy + 43, 30, SEMI, AMB if j == 0 else FG, "middle") + T(nm, 220, yy + 43, 30, MED, FG) + T(pts, 910, yy + 43, 30, SEMI, AMB if j == 0 else MUTED, "end")
add(lb, at("ball oladi"), T_E, dy=40)
add(f'<g transform="translate(860 1170)"><path d="M-50 -60 H50 V-20 A50 50 0 0 1 -50 -20 Z" fill="url(#amb)"/><rect x="-10" y="28" width="20" height="30" fill="#E8873D"/><rect x="-36" y="56" width="72" height="16" rx="6" fill="#E8873D"/></g>'
    + rr(130, 1150, 560, 80, 40, "#2A2412", AMB, 2) + T("O‘qish = musobaqa", 410, 1203, 38, SEMI, AMB, "middle"), at("o‘qish musobaqaga"), T_E, pop=True)
# ── E. director panel
add(T("Siz bitta panelda ko‘rasiz", CX, 430, 60, SEMI, FG, "middle"), T_E, T_F)
tb = rr(90, 480, 900, 640, 36, SURF, LINE, 2) + T("O‘quvchi", 130, 540, 26, SEMI, MUTED) + T("So‘zlar", 520, 540, 26, SEMI, MUTED) + T("Davomat", 680, 540, 26, SEMI, MUTED) + T("To‘lov", 850, 540, 26, SEMI, MUTED)
add(tb, T_E, T_F, dy=40)
rows = [("Aziza S.", "124", "100%", "✓", GOOD), ("Jasur R.", "98", "96%", "✓", GOOD), ("Madina K.", "45", "71%", "qarz", BAD), ("Sardor A.", "86", "92%", "✓", GOOD), ("Nilufar T.", "12", "40%", "qarz", BAD)]
for j, (nm, w_, d, pay, col) in enumerate(rows):
    yy = 570 + j * 104
    bad = col == BAD
    r = rr(110, yy, 860, 90, 18, "#2A1D1B" if bad else "#11302A") + T(nm, 130, yy + 58, 30, MED, FG) + T(w_, 520, yy + 58, 34, SEMI, BAD if int(w_) < 50 else MINT) + T(d, 680, yy + 58, 30, SEMI, BAD if bad else FG)
    r += (T("qarz", 850, yy + 58, 28, SEMI, BAD) if pay == "qarz" else ic("check", 856, yy + 28, 34, GOOD, 3))
    add(r, at("Siz esa kim") + .3 + j * .2, T_F, dy=20, dur=.25)
# ── F. parents
add(T("Ota-ona ham ko‘radi", CX, 430, 66, SEMI, FG, "middle"), T_F, T_G)
add(rr(110, 520, 860, 300, 40, FG) + T("Aziza · bu hafta", 160, 600, 34, MED, "#3F5A4D") + T("+35 ta yangi so‘z", 160, 690, 64, SEMI, "#0A7A50") + T("Darsga keldi: 3 / 3", 160, 770, 36, SEMI, INK), T_F + .2, T_G, pop=True)
# ── G. CTA
add('<circle cx="540" cy="760" r="480" fill="url(#halo)"/>', T_G, DUR + 1, dy=0, dur=.8)
add(T("Hoziroq", CX, 520, 76, SEMI, FG, "middle") + T("pastdagi tugmani", CX, 610, 76, SEMI, FG, "middle") + T("bosing", CX, 700, 76, SEMI, "url(#gh)", "middle"), T_G, DUR + 1)
add(rr(110, 790, 860, 210, 105, "url(#gh)") + T("7 kun bepul", CX, 892, 84, SEMI, INK, "middle") + T("sinab ko‘ring", CX, 960, 46, MED, "#0A3D27", "middle"), at("7 kun bepul"), DUR + 1, pop=True)
add(T("markazly.onrender.com", CX, 1090, 38, MED, MUTED, "middle"), at("7 kun bepul") + .5, DUR + 1)
arrow = f'<g transform="translate({CX-60} 1170)"><circle cx="60" cy="60" r="60" fill="#2EE59D" fill-opacity=".18"/><path d="M60 28 V92 M32 66 L60 94 L88 66" fill="none" stroke="#2EE59D" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></g>'
add(arrow, T_G + .6, DUR + 1, bob=14)
S_B, S_F = T_B, T_G
OUTNAME = 'markazly_video12_arab_lugat.mp4'; MIXNAME = 'mix_v12.m4a'; HOOK_END = at('Arab tilida eng'); FLASH = None
SAMPLES = (0.0, 2.5, 5.0, 7.0, 10.0, 13.0, 16.5, 19.5, 23.0, 26.0, 29.5, 31.5, 34.5)
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
