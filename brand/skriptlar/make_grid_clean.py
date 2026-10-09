"""Instagram: 3 ta postli toza banner — logo | chiroyli matn | telefon + taklif, to'lqin chiziqlar bilan ulangan."""
import os, io, math
import cairosvg
from PIL import Image, ImageDraw, ImageFilter

D = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(D, "make_stories.py")).read().split("# ───────────────────────── 1. Tariflar")[0])

OUTG = os.path.join(D, "markazly", "instagram_3_post_v4")
os.makedirs(OUTG, exist_ok=True)
GW, GH, TW = 3240, 1440, 1080
BOARD = "#0D2620"

grid = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{GH}" stroke="#E8F5EF" stroke-opacity=".04" stroke-width="2"/>' for x in range(0, GW + 1, 40))
grid += "".join(f'<line x1="0" y1="{y}" x2="{GW}" y2="{y}" stroke="#E8F5EF" stroke-opacity=".04" stroke-width="2"/>' for y in range(0, GH + 1, 40))
defs = DEFS.replace("</defs>",
    '<radialGradient id="l1" cx="17%" cy="38%" r="30%"><stop offset="0%" stop-color="#2EE59D" stop-opacity=".20"/><stop offset="100%" stop-color="#2EE59D" stop-opacity="0"/></radialGradient>'
    '<radialGradient id="l2" cx="50%" cy="45%" r="28%"><stop offset="0%" stop-color="#1FB5C8" stop-opacity=".08"/><stop offset="100%" stop-color="#1FB5C8" stop-opacity="0"/></radialGradient>'
    '<radialGradient id="l3" cx="84%" cy="45%" r="30%"><stop offset="0%" stop-color="#1FB5C8" stop-opacity=".18"/><stop offset="100%" stop-color="#1FB5C8" stop-opacity="0"/></radialGradient>'
    '<linearGradient id="wv" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="2400" y2="0"><stop offset="0%" stop-color="#2EE59D" stop-opacity="0"/><stop offset="12%" stop-color="#2EE59D"/><stop offset="100%" stop-color="#7FE8F2"/></linearGradient>'
    '<radialGradient id="halo1" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#2EE59D" stop-opacity=".30"/><stop offset="60%" stop-color="#1FB5C8" stop-opacity=".07"/><stop offset="100%" stop-color="#1FB5C8" stop-opacity="0"/></radialGradient>'
    '<radialGradient id="floor1" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#3CF2A8" stop-opacity=".5"/><stop offset="100%" stop-color="#3CF2A8" stop-opacity="0"/></radialGradient>'
    '</defs>')

bg = f'<rect width="{GW}" height="{GH}" fill="{BOARD}"/>{grid}'
bg += ''.join(f'<rect width="{GW}" height="{GH}" fill="url(#{i})"/>' for i in ("l1", "l2", "l3"))
bg += f'<line x1="150" y1="0" x2="150" y2="{GH}" stroke="#E8F5EF" stroke-opacity=".10" stroke-width="2"/>'

# ── waves: three lines start loose on the left and converge into the "7 kun bepul" badge
END_X, END_Y = 2 * TW + 150, 1050
def ease_at(x):
    t = min(1, max(0, (x - 1.45 * TW) / (END_X - 1.45 * TW)))
    return t * t * (3 - 2 * t)
def wy(x, off, amp, ph):
    e = ease_at(x)
    return 1290 + (END_Y - 1290) * e + (off + amp * math.sin(x / 330 + ph)) * (1 - e)
def wave(off, amp, ph):
    return "M" + " L".join(f"{x},{wy(x, off, amp, ph):.1f}" for x in range(-20, END_X + 1, 12))
waves = ""
for off, amp, ph, sw, op in [(0, 34, 0.0, 5, .95), (46, 40, 1.3, 3, .45), (-50, 28, 2.4, 3, .3)]:
    d = wave(off, amp, ph)
    waves += f'<path d="{d}" fill="none" stroke="url(#wv)" stroke-width="{sw*5}" stroke-opacity="{op*.12}" stroke-linecap="round"/>'
    waves += f'<path d="{d}" fill="none" stroke="url(#wv)" stroke-width="{sw}" stroke-opacity="{op}" stroke-linecap="round"/>'
# small glowing dots riding the main wave at each post
for x in (540, TW + 540):
    y = wy(x, 0, 34, 0.0)
    waves += f'<circle cx="{x}" cy="{y:.1f}" r="22" fill="#2EE59D" fill-opacity=".18"/><circle cx="{x}" cy="{y:.1f}" r="9" fill="#BFFFE4"/>'
fg = waves
# ── post 1: brand
fg += '<circle cx="540" cy="520" r="420" fill="url(#halo1)"/>'
mh = 540; mw = mh * 342 / 377; my = 250
fg += f'<ellipse cx="560" cy="{my+mh-8}" rx="250" ry="30" fill="url(#floor1)"/>'
fg += f'<image href="{MARK}" x="{540 - mw / 2 + 8:.1f}" y="{my}" width="{mw:.1f}" height="{mh}"/>'
wsz = 160
w1 = SEMI.width("Markaz", wsz); w2 = SEMI.width("ly", wsz); wx = 540 - (w1 + w2) / 2
fg += T("Markaz", wx, 1000, wsz, SEMI, FG) + T("ly", wx + w1, 1000, wsz, SEMI, "url(#gh)")
fg += T("O‘quv markaz boshqaruv tizimi", 540, 1075, 40, REG, MUTED, "middle")

# ── post 2: the headline
x2 = TW + 100
ey = "O‘QUV MARKAZLARI UCHUN"
ew = SEMI.width(ey, 28) + 64
fg += rr(x2, 268, ew, 58, 29, "#0F3A2C", "#2EE59D", 2)
fg += f'<circle cx="{x2+28}" cy="297" r="7" fill="#2EE59D"/>' + T(ey, x2 + 46, 307, 28, SEMI, MINT)
hs = 124
L1, L2a, L2b, L3 = "Markazingizni", "bitta", " tizimdan", "boshqaring"
while max(SEMI.width(L1, hs), SEMI.width(L2a + L2b, hs), SEMI.width(L3, hs)) > 880:
    hs -= 2
lh = hs * 1.08
b1 = 330 + hs * 1.08
fg += T(L1, x2, b1, hs, SEMI, FG)
# "bitta" sits on a soft mint marker stroke
bw = SEMI.width(L2a, hs)
fg += rr(x2 - 8, b1 + lh - hs * .36, bw + 16, hs * .40, 12, "#2EE59D").replace('fill="#2EE59D"', 'fill="#2EE59D" fill-opacity=".22"')
fg += T(L2a, x2, b1 + lh, hs, SEMI, MINT) + T(L2b, x2 + bw, b1 + lh, hs, SEMI, FG)
fg += T(L3, x2, b1 + 2 * lh, hs, SEMI, "url(#gh)")
# hand-drawn swoosh under "boshqaring"
w3 = SEMI.width(L3, hs); uy = b1 + 2 * lh + 34
fg += f'<path d="M{x2+6} {uy+8} C{x2+w3*.3} {uy-10}, {x2+w3*.7} {uy-8}, {x2+w3-4} {uy+4}" fill="none" stroke="url(#gh)" stroke-width="9" stroke-linecap="round"/>'
fg += f'<path d="M{x2+w3*.18} {uy+26} C{x2+w3*.45} {uy+14}, {x2+w3*.7} {uy+16}, {x2+w3*.86} {uy+22}" fill="none" stroke="#1FB5C8" stroke-opacity=".6" stroke-width="5" stroke-linecap="round"/>'
sy = uy + 92
fg += T("Daftar va Excelsiz — hammasi bir joyda.", x2, sy, 36, REG, MUTED)
cy = sy + 50
for icn, t in [("tick", "Davomat va to‘lovlar"), ("chart", "Filiallar hisoboti"), ("globe", "Sayt + o‘quvchi kabineti")]:
    w = MED.width(t, 34) + 104
    fg += rr(x2, cy, w, 70, 35, "#112E27", "#24493D", 2) + ic(icn, x2 + 22, cy + 17, 36, MINT, 2) + T(t, x2 + 76, cy + 47, 34, MED, FG)
    cy += 86

# ── post 3: phone + offer
px, py, pw, ph = 2 * TW + 300, 150, 480, 800
fg += rr(px - 12, py - 12, pw + 24, ph + 24, 70, "#020806") + rr(px, py, pw, ph, 58, SURF)
fg += rr(px + pw / 2 - 72, py + 20, 144, 28, 14, "#020806")
fg += f'<circle cx="{px+58}" cy="{py+104}" r="30" fill="url(#g)"/>' + T("A", px + 58, py + 117, 30, SEMI, INK, "middle")
fg += T("B1 guruh", px + 104, py + 94, 22, REG, MUTED) + T("Aziza Sobirova", px + 104, py + 128, 28, SEMI, FG)
cy = py + 168
for icn, s1, s2, paid in [("cal", "Bugungi dars", "18:00 · 3-xona", False), ("cap", "Lug‘at · bugun", "12 ta yangi so‘z", False),
                          ("tick", "Keyingi to‘lov", "To‘langan", True)]:
    fg += rr(px + 22, cy, pw - 44, 120, 24, "url(#gh)" if paid else SURF2)
    fg += ic(icn, px + 46, cy + 38, 44, INK if paid else "url(#g)", 2)
    fg += T(s1, px + 106, cy + 50, 22, REG, "#0B3A26" if paid else MUTED) + T(s2, px + 106, cy + 88, 28, SEMI, INK if paid else FG)
    cy += 134
fg += rr(px + 22, cy + 4, pw - 44, 106, 24, SURF2)
fg += T("Shu oy davomati", px + 46, cy + 48, 24, REG, MUTED) + T("92%", px + pw - 46, cy + 50, 30, SEMI, FG, "end")
fg += rr(px + 46, cy + 72, pw - 92, 14, 7, LINE) + rr(px + 46, cy + 72, (pw - 92) * .92, 14, 7, MINT)
tx, ty = 2 * TW + 70, 560
fg += rr(tx, ty, 330, 108, 24, FG) + rr(tx + 20, ty + 22, 64, 64, 18, MINT) + ic("check", tx + 36, ty + 38, 32, INK, 3)
fg += T("To‘lov qabul", tx + 102, ty + 50, 26, SEMI, INK) + T("590 000 so‘m", tx + 102, ty + 86, 24, REG, "#3F5A4D")
# offer — the waves end here
bx, by, bw_, bh = 2 * TW + 110, 975, 870, 150
fg += rr(bx - 8, by - 8, bw_ + 16, bh + 16, (bh + 16) / 2, "#2EE59D", None) .replace('fill="#2EE59D"', 'fill="#2EE59D" fill-opacity=".18"')
fg += rr(bx, by, bw_, bh, bh / 2, "url(#gh)")
fg += T("7 kun bepul sinov", bx + bw_ / 2, by + 72, 58, SEMI, INK, "middle")
fg += T("3 daqiqada boshlang", bx + bw_ / 2, by + 118, 32, MED, "#0A3D27", "middle")
fg += T("@markazly.uz", 2 * TW + 545, 1250, 38, MED, FG, "middle")


def render(body):
    sv = f'<svg xmlns="http://www.w3.org/2000/svg" width="{GW}" height="{GH}" viewBox="0 0 {GW} {GH}">{defs}{body}</svg>'
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=sv.encode()))).convert("RGBA")

img = Image.alpha_composite(render(bg), render(fg)).convert("RGB")
img.save(os.path.join(OUTG, "toliq_panorama.png"))
names = ["1_chap", "2_orta", "3_ong"]
for i, n in enumerate(names):
    img.crop((i * TW, 0, (i + 1) * TW, GH)).save(os.path.join(OUTG, f"post_{n}.png"))
gap, s = 6, 0.4
w_, h_ = int(TW * s), int(GH * s)
prev = Image.new("RGB", (3 * w_ + 2 * gap, h_), (255, 255, 255))
for i, n in enumerate(names):
    prev.paste(Image.open(os.path.join(OUTG, f"post_{n}.png")).resize((w_, h_), Image.LANCZOS), (i * (w_ + gap), 0))
prev.save(os.path.join(OUTG, "profilda_korinishi.png"))
print("ok", hs)
