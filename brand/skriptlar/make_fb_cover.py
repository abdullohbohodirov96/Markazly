"""Facebook cover 1640x624. Asosiy narsalar markaziy xavfsiz zonada (telefonda yon tomonlar kesiladi)."""
import os, io, math
import cairosvg
from PIL import Image, ImageDraw

D = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(D, "make_stories.py")).read().split("# ───────────────────────── 1. Tariflar")[0])
OUT = os.path.join(D, "markazly", "facebook")
os.makedirs(OUT, exist_ok=True)
W, H = 1640, 624
BOARD = "#0D2620"
grid = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="#E8F5EF" stroke-opacity=".045" stroke-width="1.5"/>' for x in range(0, W + 1, 32))
grid += "".join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="#E8F5EF" stroke-opacity=".045" stroke-width="1.5"/>' for y in range(0, H + 1, 32))
defs = DEFS.replace("</defs>",
    '<radialGradient id="l1" cx="20%" cy="45%" r="40%"><stop offset="0%" stop-color="#2EE59D" stop-opacity=".16"/><stop offset="100%" stop-color="#2EE59D" stop-opacity="0"/></radialGradient>'
    '<radialGradient id="l3" cx="72%" cy="40%" r="35%"><stop offset="0%" stop-color="#1FB5C8" stop-opacity=".20"/><stop offset="100%" stop-color="#1FB5C8" stop-opacity="0"/></radialGradient>'
    '<linearGradient id="wv" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="1640" y2="0"><stop offset="0%" stop-color="#2EE59D" stop-opacity="0"/><stop offset="15%" stop-color="#2EE59D"/><stop offset="100%" stop-color="#7FE8F2"/></linearGradient>'
    '<radialGradient id="halo" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#2EE59D" stop-opacity=".28"/><stop offset="100%" stop-color="#2EE59D" stop-opacity="0"/></radialGradient>'
    '</defs>')
b = f'<rect width="{W}" height="{H}" fill="{BOARD}"/>{grid}<rect width="{W}" height="{H}" fill="url(#l1)"/><rect width="{W}" height="{H}" fill="url(#l3)"/>'

# waves along the bottom, flowing to the right
def wy(x, off, amp, ph):
    return 596 + off + amp * math.sin(x / 210 + ph) - 50 * (x / W) ** 2
for off, amp, ph, sw, op in [(0, 16, 0, 3.5, .9), (18, 20, 1.3, 2, .45), (-20, 14, 2.4, 2, .3)]:
    d = "M" + " L".join(f"{x},{wy(x, off, amp, ph):.1f}" for x in range(-10, W + 11, 8))
    b += f'<path d="{d}" fill="none" stroke="url(#wv)" stroke-width="{sw*5}" stroke-opacity="{op*.12}"/><path d="{d}" fill="none" stroke="url(#wv)" stroke-width="{sw}" stroke-opacity="{op}"/>'

# big faint mark on the far left (decor, outside the mobile safe zone)
mh = 520; mw = mh * 342 / 377
b += f'<circle cx="120" cy="300" r="300" fill="url(#halo)"/>'
b += f'<image href="{MARK}" x="{120-mw/2:.0f}" y="{300-mh/2}" width="{mw:.0f}" height="{mh}" opacity=".16"/>'

# ── left block: brand + headline + actions
X = 300
mk = 64; mkw = mk * 342 / 377
b += f'<image href="{MARK}" x="{X}" y="62" width="{mkw:.0f}" height="{mk}"/>'
b += T("Markaz", X + mkw + 14, 114, 50, SEMI, FG) + T("ly", X + mkw + 14 + SEMI.width("Markaz", 50), 114, 50, SEMI, "url(#gh)")
ey = "O‘QUV MARKAZLARI UCHUN"
ex = X + mkw + 14 + SEMI.width("Markazly", 50) + 26
b += rr(ex, 78, SEMI.width(ey, 17) + 44, 36, 18, "#0F3A2C", "#2EE59D", 1.5) + f'<circle cx="{ex+19}" cy="96" r="4.5" fill="#2EE59D"/>' + T(ey, ex + 31, 102, 17, SEMI, MINT)
hs, lh, y0 = 72, 80, 222
b += T("Markazingizni", X, y0, hs, SEMI, FG)
bw = SEMI.width("bitta", hs)
b += rr(X - 6, y0 + lh - hs * .36, bw + 12, hs * .40, 8, "#2EE59D").replace('fill="#2EE59D"', 'fill="#2EE59D" fill-opacity=".22"')
b += T("bitta", X, y0 + lh, hs, SEMI, MINT) + T(" tizimdan", X + bw, y0 + lh, hs, SEMI, FG)
b += T("boshqaring", X, y0 + 2 * lh, hs, SEMI, "url(#gh)")
w3 = SEMI.width("boshqaring", hs); uy = y0 + 2 * lh + 22
b += f'<path d="M{X+4} {uy+5} C{X+w3*.3} {uy-6}, {X+w3*.7} {uy-5}, {X+w3-3} {uy+3}" fill="none" stroke="url(#gh)" stroke-width="6" stroke-linecap="round"/>'
b += f'<path d="M{X+w3*.2} {uy+17} C{X+w3*.45} {uy+9}, {X+w3*.7} {uy+10}, {X+w3*.86} {uy+14}" fill="none" stroke="#1FB5C8" stroke-opacity=".6" stroke-width="3.5" stroke-linecap="round"/>'
ry = 448
bt = "7 kun bepul sinov"
bwid = SEMI.width(bt, 28) + 64
b += rr(X, ry, bwid, 62, 31, "url(#gh)") + T(bt, X + bwid / 2, ry + 41, 28, SEMI, INK, "middle")
num = "+998 50 999 97 33"
nx = X + bwid + 16; nw = SEMI.width(num, 28) + 86
b += rr(nx, ry, nw, 62, 31, "#112E27", "#2EE59D", 2) + f'<circle cx="{nx+32}" cy="{ry+31}" r="20" fill="#2EE59D"/>' + ic("call", nx + 20, ry + 19, 24, INK, 2.2) + T(num, nx + 64, ry + 41, 28, SEMI, FG)
b += T("Davomat · To‘lovlar · Filiallar · Sayt · O‘quvchi kabineti", X, 548, 20, MED, MUTED)

# ── right block: phone (scaled copy of the post mock) + toast
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
S = 0.62; PX, PY = 1060, 58
b += f'<g transform="translate({PX} {PY}) scale({S})">{p}</g>'
tx, ty = 872, 318
b += rr(tx, ty, 230, 76, 18, FG) + rr(tx + 14, ty + 15, 46, 46, 13, MINT) + ic("check", tx + 25, ty + 26, 24, INK, 3)
b += T("To‘lov qabul", tx + 74, ty + 34, 19, SEMI, INK) + T("590 000 so‘m", tx + 74, ty + 60, 17, REG, "#3F5A4D")
# small KPI card on the other side of the phone
kx, ky = 1180, 408
b += rr(kx, ky, 176, 92, 18, SURF, LINE, 1.5) + T("Tushum · oy", kx + 18, ky + 34, 16, REG, MUTED) + T("184 mln", kx + 18, ky + 72, 30, SEMI, FG)

sv = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{defs}{b}</svg>'
img = Image.open(io.BytesIO(cairosvg.svg2png(bytestring=sv.encode()))).convert("RGB")
img.save(os.path.join(OUT, "markazly_facebook_cover.png"))
img.save(os.path.join(OUT, "markazly_facebook_cover.jpg"), quality=95)

# previews: desktop (851x315 crop of full width) and mobile (640x360 -> center crop)
dh = int(W * 315 / 851); dy = (H - dh) // 2
img.crop((0, dy, W, dy + dh)).resize((851, 315), Image.LANCZOS).save(os.path.join(OUT, "korinishi_kompyuter.png"))
mw_ = int(H * 640 / 360); mx = (W - mw_) // 2
img.crop((mx, 0, mx + mw_, H)).resize((640, 360), Image.LANCZOS).save(os.path.join(OUT, "korinishi_telefon.png"))
print("ok", mx, mx + mw_)
