"""Facebook cover 1640x624. Asosiy narsalar markaziy xavfsiz zonada (telefonda yon tomonlar kesiladi)."""
import os, io, math
import cairosvg
from PIL import Image, ImageDraw

D = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(D, "make_stories.py")).read().split("# ───────────────────────── 1. Tariflar")[0])
OUT = os.path.join(D, "markazly", "instagram_post")
os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1350
BOARD = "#0D2620"
grid = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="#E8F5EF" stroke-opacity=".045" stroke-width="1.5"/>' for x in range(0, W + 1, 32))
grid += "".join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="#E8F5EF" stroke-opacity=".045" stroke-width="1.5"/>' for y in range(0, H + 1, 32))
defs = DEFS.replace("</defs>",
    '<radialGradient id="l1" cx="15%" cy="25%" r="45%"><stop offset="0%" stop-color="#2EE59D" stop-opacity=".16"/><stop offset="100%" stop-color="#2EE59D" stop-opacity="0"/></radialGradient>'
    '<radialGradient id="l3" cx="80%" cy="65%" r="40%"><stop offset="0%" stop-color="#1FB5C8" stop-opacity=".20"/><stop offset="100%" stop-color="#1FB5C8" stop-opacity="0"/></radialGradient>'
    '<linearGradient id="wv" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="1080" y2="0"><stop offset="0%" stop-color="#2EE59D" stop-opacity="0"/><stop offset="15%" stop-color="#2EE59D"/><stop offset="100%" stop-color="#7FE8F2"/></linearGradient>'
    '<radialGradient id="halo" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#2EE59D" stop-opacity=".28"/><stop offset="100%" stop-color="#2EE59D" stop-opacity="0"/></radialGradient>'
    '</defs>')
b = f'<rect width="{W}" height="{H}" fill="{BOARD}"/>{grid}<rect width="{W}" height="{H}" fill="url(#l1)"/><rect width="{W}" height="{H}" fill="url(#l3)"/>'


def wy(x, off, amp, ph):
    return 1300 + off + amp * math.sin(x / 200 + ph) - 70 * (x / W) ** 2
for off, amp, ph, sw, op in [(0, 18, 0, 4, .9), (20, 22, 1.3, 2.5, .45), (-22, 16, 2.4, 2.5, .3)]:
    d = "M" + " L".join(f"{x},{wy(x, off, amp, ph):.1f}" for x in range(-10, W + 11, 8))
    b += f'<path d="{d}" fill="none" stroke="url(#wv)" stroke-width="{sw*5}" stroke-opacity="{op*.12}"/><path d="{d}" fill="none" stroke="url(#wv)" stroke-width="{sw}" stroke-opacity="{op}"/>'

X = 90
mk = 80; mkw = mk * 342 / 377
b += f'<circle cx="{X+40}" cy="120" r="160" fill="url(#halo)"/>'
b += f'<image href="{MARK}" x="{X}" y="80" width="{mkw:.0f}" height="{mk}"/>'
b += T("Markaz", X + mkw + 16, 144, 62, SEMI, FG) + T("ly", X + mkw + 16 + SEMI.width("Markaz", 62), 144, 62, SEMI, "url(#gh)")
ey = "O‘QUV MARKAZLARI UCHUN"
ew = SEMI.width(ey, 22) + 54
b += rr(W - 90 - ew, 96, ew, 46, 23, "#0F3A2C", "#2EE59D", 2) + f'<circle cx="{W-90-ew+23}" cy="119" r="6" fill="#2EE59D"/>' + T(ey, W - 90 - ew + 38, 127, 22, SEMI, MINT)

hs, lh, y0 = 124, 132, 338
b += T("Markazingizni", X, y0, hs, SEMI, FG)
bw = SEMI.width("bitta", hs)
b += rr(X - 8, y0 + lh - hs * .36, bw + 16, hs * .40, 12, "#2EE59D").replace('fill="#2EE59D"', 'fill="#2EE59D" fill-opacity=".22"')
b += T("bitta", X, y0 + lh, hs, SEMI, MINT) + T(" tizimdan", X + bw, y0 + lh, hs, SEMI, FG)
b += T("boshqaring", X, y0 + 2 * lh, hs, SEMI, "url(#gh)")
w3 = SEMI.width("boshqaring", hs); uy = y0 + 2 * lh + 34
b += f'<path d="M{X+6} {uy+8} C{X+w3*.3} {uy-10}, {X+w3*.7} {uy-8}, {X+w3-4} {uy+4}" fill="none" stroke="url(#gh)" stroke-width="9" stroke-linecap="round"/>'
b += f'<path d="M{X+w3*.18} {uy+26} C{X+w3*.45} {uy+14}, {X+w3*.7} {uy+16}, {X+w3*.86} {uy+22}" fill="none" stroke="#1FB5C8" stroke-opacity=".6" stroke-width="5" stroke-linecap="round"/>'

# left column: subtitle + features
sy = 760
b += T("Daftar va Excelsiz —", X, sy, 36, REG, MUTED) + T("hammasi bir joyda.", X, sy + 46, 36, REG, MUTED)
cy = sy + 86
for icn, t in [("tick", "Davomat va to‘lovlar"), ("chart", "Filiallar hisoboti"), ("globe", "Sayt + o‘quvchi kabineti")]:
    w = MED.width(t, 32) + 100
    b += rr(X, cy, w, 66, 33, "#112E27", "#24493D", 2) + ic(icn, X + 20, cy + 16, 34, MINT, 2) + T(t, X + 72, cy + 44, 32, MED, FG)
    cy += 80
px, py, pw, ph = 0, 0, 480, 800
p = rr(px - 12, py - 12, pw + 24, ph + 24, 70, "#020806") + rr(px, py, pw, ph, 58, SURF) + rr(pw / 2 - 72, 20, 144, 28, 14, "#020806")
p += f'<circle cx="58" cy="104" r="30" fill="url(#g)"/>' + T("A", 58, 117, 30, SEMI, INK, "middle")
p += T("B1 guruh", 104, 94, 22, REG, MUTED) + T("Aziza Sobirova", 104, 128, 28, SEMI, FG)
cy = 168
for icn, s1, s2, paid in [("cal", "Bugungi dars", "18:00 · 3-xona", False), ("cap", "Lug‘at · bugun", "12 ta yangi so‘z", False), ("tick", "Keyingi to‘lov", "To‘langan", True)]:
    p += rr(22, cy, pw - 44, 120, 24, "url(#gh)" if paid else SURF2) + ic(icn, 46, cy + 38, 44, INK if paid else "url(#g)", 2)
    p += T(s1, 106, cy + 50, 22, REG, "#0B3A26" if paid else MUTED) + T(s2, 106, cy + 88, 28, SEMI, INK if paid else FG)
    cy += 134
p += rr(22, cy + 4, pw - 44, 106, 24, SURF2) + T("Shu oy davomati", 46, cy + 48, 24, REG, MUTED) + T("92%", pw - 46, cy + 50, 30, SEMI, FG, "end")
p += rr(46, cy + 72, pw - 92, 14, 7, LINE) + rr(46, cy + 72, (pw - 92) * .92, 14, 7, MINT)

S = 0.66; PX, PY = 650, 690
b += f'<g transform="translate({PX} {PY}) scale({S})">{p}</g>'

ry = 1146
bt = "7 kun bepul sinov"
bwid = SEMI.width(bt, 32) + 70
b += rr(X - 6, ry - 6, bwid + 12, 82, 41, "#2EE59D").replace('fill="#2EE59D"', 'fill="#2EE59D" fill-opacity=".18"')
b += rr(X, ry, bwid, 70, 35, "url(#gh)") + T(bt, X + bwid / 2, ry + 46, 32, SEMI, INK, "middle")
num = "+998 50 999 97 33"
nx = X + bwid + 18; nw = SEMI.width(num, 32) + 96
b += rr(nx, ry, nw, 70, 35, "#112E27", "#2EE59D", 2) + f'<circle cx="{nx+36}" cy="{ry+35}" r="23" fill="#2EE59D"/>' + ic("call", nx + 22, ry + 21, 28, INK, 2.2) + T(num, nx + 72, ry + 46, 32, SEMI, FG)
b += T("@markazly.uz", X, 1262, 30, MED, MUTED)

sv = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{defs}{b}</svg>'
img = Image.open(io.BytesIO(cairosvg.svg2png(bytestring=sv.encode()))).convert("RGB")
img.save(os.path.join(OUT, "markazly_post_1080x1350.png"))
img.save(os.path.join(OUT, "markazly_post_1080x1350.jpg"), quality=95)
print("ok", nx + nw)
