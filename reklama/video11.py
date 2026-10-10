TIMING = 'timing11'
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
from arabic import TA, AR, AR6
def ar(t, x, y, s, col=FG, anchor="middle", face=None): return TA(t, x, y, s, face or AR, col, anchor)
T_B, T_C, T_D, T_E = at("ماركازلي نظامٌ"), at("موقعٌ"), at("النظام يعمل"), at("اضغط")
# ── A. hook
add('<circle cx="540" cy="760" r="540" fill="url(#rd)"/>', -1, T_B, dy=0, dur=.01)
add(ar("هل تعرف حقاً", CX, 520, 96) + ar("ما يحدث في مركزك؟", CX, 650, 96, "url(#gh)"), -1, T_B, dy=0, dur=.01)
for i, (t, key) in enumerate([("من دفع الرسوم؟", "من دفع"), ("من تأخّر؟", "ومن تأخّر"), ("من غاب عن الدرس؟", "ومن غاب")]):
    y = 760 + i * 160
    add(rr(140, y, 800, 130, 34, "#2A1D1B", "#5A2A24", 3) + f'<circle cx="868" cy="{y+65}" r="38" fill="{BAD}"/>' + T("?", 868, y + 86, 54, SEMI, "#2A0E0A", "middle") + ar(t, 800, y + 86, 52, "#F3D6D0", "right"), at(key), T_B, pop=True)
# ── B. one system: panel, attendance, payments, branches
add('<circle cx="540" cy="430" r="300" fill="url(#halo)"/>', T_B, T_C, dy=0, dur=.5)
mh = 170; mw = mh * 342 / 377
add(f'<image href="{MARK}" x="{CX - mw/2 + 3:.0f}" y="300" width="{mw:.0f}" height="{mh}"/>', T_B, T_C, pop=True)
add(ar("نظامٌ واحد لكلّ شيء", CX, 560, 66, "url(#gh)"), T_B + .3, T_C)
dx, dw = 110, 860
k = rr(dx, 610, dw, 170, 30, SURF, LINE, 2); kw = (dw - 60) / 3
for j, (lab, val, col) in enumerate([("الطلاب", "368", FG), ("الإيرادات", "184M", FG), ("المتأخّرون", "12", BAD)]):
    kx = dx + dw - 20 - (j + 1) * kw - j * 10
    k += rr(kx, 630, kw, 130, 20, SURF2) + ar(lab, kx + kw - 22, 680, 30, MUTED, "right") + T(val, kx + kw - 22, 745, 48, SEMI, col, "end")
add(k, at("الحضور"), T_C, dy=40)
att = rr(dx, 800, dw, 300, 30, SURF, LINE, 2) + ar("الحضور · المجموعة الأولى", dx + dw - 30, 860, 34, FG, "right")
nm = ["أحمد", "فاطمة", "يوسف", "مريم"]
for j, n_ in enumerate(nm): att += ar(n_, dx + dw - 30, 920 + j * 50, 32, FG, "right")
add(att, at("الحضور") + .2, T_C, dy=40)
for j in range(4):
    ok = j != 2
    add(rr(dx + 30, 892 + j * 50, 170, 40, 20, "#123A2C" if ok else "#3A1D1A") + ar("حاضر" if ok else "غائب", dx + 115, 922 + j * 50, 28, GOOD if ok else BAD), at("الحضور") + .5 + j * .15, T_C, pop=True, dur=.15)
add(rr(dx, 1120, dw, 110, 30, "#3A1D1A", BAD, 2) + ar("متأخّرون عن الدفع: اثنا عشر طالباً", dx + dw - 30, 1190, 38, BAD, "right"), at("والمدفوعات"), T_C, pop=True)
br = rr(dx, 1250, dw, 0, 0, "none")
for j, (n_, pct, col) in enumerate([("فرع ١", .85, GOOD), ("فرع ٢", .35, BAD)]):
    y = 1250 + j * 0
add(rr(dx, 1250, 420, 110, 26, SURF, LINE, 2) + ar("الفرع الأول · ربح", dx + 390, 1300, 30, GOOD, "right") + rr(dx + 30, 1320, 360, 18, 9, GOOD), at("وتقارير"), T_C, pop=True)
add(rr(dx + 440, 1250, 420, 110, 26, SURF, LINE, 2) + ar("الفرع الثاني · خسارة", dx + 830, 1300, 30, BAD, "right") + rr(dx + 470, 1320, 140, 18, 9, BAD), at("وتقارير") + .3, T_C, pop=True)
# ── C. website + student account + points
x, y, w = 110, 330, 860
s_ = rr(x, y, w, 470, 30, "#071510", LINE, 2) + f'<path d="M{x} {y+30} Q{x} {y} {x+30} {y} H{x+w-30} Q{x+w} {y} {x+w} {y+30} V{y+62} H{x} Z" fill="#0B1D16"/>'
s_ += "".join(f'<circle cx="{x+w-34-j*26}" cy="{y+31}" r="8" fill="{c}"/>' for j, c in enumerate([MINT, LINE, LINE]))
s_ += rr(x + 130, y + 13, 600, 38, 19, "#06120D", LINE, 2) + T("alnoor-academy.uz", x + 430, y + 40, 22, MED, FG, "middle")
s_ += ar("أكاديمية النور", x + w - 40, y + 130, 40, FG, "right") + ar("تعلّم العربية", x + w - 40, y + 240, 70, "url(#gh)", "right") + ar("من الدرس الأوّل", x + w - 40, y + 320, 52, FG, "right")
s_ += rr(x + w - 360, y + 360, 320, 70, 35, "url(#gh)") + ar("سجّل الآن", x + w - 200, y + 406, 34, INK)
s_ += rr(x + 40, y + 120, 260, 300, 26, "#12281F", LINE, 2) + ic("book", x + 100, y + 200, 140, MINT, 1.5)
add(s_, T_C, T_D, dy=60)
add(rr(110, 830, 420, 380, 30, "url(#best)", MINT, 2) + ar("بطاقة الكلمات", 500, 890, 30, MUTED, "right") + ar("كِتَاب", 320, 1040, 110, FG) + T("kitob", 320, 1110, 40, MED, MUTED, "middle"), at("وحسابٌ"), T_D, pop=True)
lb = rr(550, 830, 420, 380, 30, SURF, LINE, 2) + ar("الترتيب", 940, 890, 30, MUTED, "right")
for j, (n_, p) in enumerate([("أحمد", "1248"), ("فاطمة", "1190"), ("يوسف", "1052")]):
    yy = 920 + j * 90
    lb += rr(570, yy, 380, 74, 16, "#2A2412" if j == 0 else "#11302A") + ar(n_, 930, yy + 50, 34, FG, "right") + T(p, 600, yy + 50, 32, SEMI, AMB if j == 0 else MUTED)
add(lb, at("مع نقاطٍ"), T_D, dy=40)
add(rr(330, 1240, 420, 90, 45, "#2A2412", AMB, 2) + T("+10", 630, 1300, 44, SEMI, AMB, "middle") + ar("نقاط", 470, 1300, 44, AMB), at("مع نقاطٍ") + .6, T_D, pop=True)
# ── D. 4 languages, migration, training
add(ar("يعمل بأربع لغات", CX, 440, 76, FG), T_D, T_E)
for j, lg in enumerate(["العربية", "الأوزبكية", "الروسية", "الإنجليزية"]):
    xx = 110 + (j % 2) * 440; yy = 500 + (j // 2) * 130
    add(rr(xx, yy, 420, 110, 30, "#123A2C" if j == 0 else SURF, MINT if j == 0 else LINE, 2) + ic("globe", xx + 330, yy + 31, 48, MINT, 2) + ar(lg, xx + 300, yy + 72, 42, FG, "right"), at("النظام يعمل") + .3 + j * .2, T_E, pop=True, dur=.2)
for j, (t, tt) in enumerate([("ننقل بياناتك بأنفسنا", "وننقل"), ("وندرّب موظفيك مجاناً", "وننقل")]):
    yy = 820 + j * 130
    add(rr(110, yy, 860, 110, 30, "#123A2C", MINT, 2) + f'<circle cx="900" cy="{yy+55}" r="34" fill="{MINT}"/>' + ic("check", 882, yy + 37, 36, INK, 3) + ar(t, 840, yy + 72, 42, FG, "right"), at(tt) + j * 1.3, T_E, dy=30)
# ── E. CTA
add('<circle cx="540" cy="760" r="480" fill="url(#halo)"/>', T_E, DUR + 1, dy=0, dur=.8)
add(ar("اضغط الزرّ", CX, 530, 90) + ar("في الأسفل الآن", CX, 650, 90, "url(#gh)"), T_E, DUR + 1)
add(rr(110, 740, 860, 220, 110, "url(#gh)") + ar("جرّب ٧ أيام مجاناً", CX, 870, 74, INK), at("وجرّب"), DUR + 1, pop=True)
add(T("markazly.uz", CX, 1040, 38, MED, MUTED, "middle"), at("وجرّب") + .6, DUR + 1)
arrow = f'<g transform="translate({CX-60} 1120)"><circle cx="60" cy="60" r="60" fill="#2EE59D" fill-opacity=".18"/><path d="M60 28 V92 M32 66 L60 94 L88 66" fill="none" stroke="#2EE59D" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></g>'
add(arrow, T_E + .6, DUR + 1, bob=14)
S_B, S_F = T_B, T_E
OUTNAME = 'markazly_video11_arabcha.mp4'; MIXNAME = 'mix_v11.m4a'; HOOK_END = at('ماركازلي نظامٌ'); FLASH = None
SAMPLES = (0.0, 2.5, 4.5, 6.8, 9.0, 12.0, 15.0, 19.0, 22.5, 26.0, 29.0, 33.0, 35.5)
# ── Arabic captions: words placed right-to-left, key words coloured
for a_, b_, ws in chunks():
    if a_ < S_B - .1 or a_ >= S_F - .05: continue
    words = [w[2] for w in ws if w[2] != "—"]
    size = 64
    widths = [AR.width(w, size) for w in words]; sp = size * .3
    tw = sum(widths) + sp * (len(words) - 1)
    if tw > 900:
        k = 900 / tw; size = int(size * k); widths = [AR.width(w, size) for w in words]; sp = size * .3; tw = sum(widths) + sp * (len(words) - 1)
    yb = 1530; x = CX + tw / 2
    cap = rr(CX - tw / 2 - 34, yb - size - 22, tw + 68, size + 60, 26, "#04140D").replace('fill="#04140D"', 'fill="#04140D" fill-opacity=".78"')
    for w, wd in zip(words, widths):
        col = BAD if w in BAD_KEY else (MINT if w in KEY else FG)
        cap += TA(w, x - wd, yb, size, AR, col, "start"); x -= wd + sp
    add(cap, a_, b_ + .02, dy=0, dur=.1, pop=True, fo=.04)


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
