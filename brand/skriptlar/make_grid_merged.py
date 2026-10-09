"""Instagram profil to'ri uchun 3 ta postga bo'linadigan bitta katta muqova.
Har bir bo'lak 1080x1440 (3:4 — Instagram to'ri shu nisbatda ko'rsatadi)."""
import os, base64
import cairosvg
from PIL import Image

D = os.path.dirname(os.path.abspath(__file__))
# reuse fonts, text and icon helpers from the stories script (everything before the first story)
src = open(os.path.join(D, "make_stories.py")).read().split("# ───────────────────────── 1. Tariflar")[0]
exec(src)

OUTG = os.path.join(D, "markazly", "instagram_3_post_v3")
os.makedirs(OUTG, exist_ok=True)
GW, GH, TW = 3240, 1440, 1080
BOARD, BOARD2 = "#0D2620", "#112E27"
AMB = "#F6C76B"

grid_lines = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{GH}" stroke="#E8F5EF" stroke-opacity=".045" stroke-width="2"/>' for x in range(0, GW + 1, 40))
grid_lines += "".join(f'<line x1="0" y1="{y}" x2="{GW}" y2="{y}" stroke="#E8F5EF" stroke-opacity=".045" stroke-width="2"/>' for y in range(0, GH + 1, 40))

defs = DEFS.replace("</defs>",
    '<radialGradient id="l1" cx="18%" cy="40%" r="35%"><stop offset="0%" stop-color="#2EE59D" stop-opacity=".22"/><stop offset="100%" stop-color="#2EE59D" stop-opacity="0"/></radialGradient>'
    '<radialGradient id="l3" cx="82%" cy="60%" r="35%"><stop offset="0%" stop-color="#1FB5C8" stop-opacity=".2"/><stop offset="100%" stop-color="#1FB5C8" stop-opacity="0"/></radialGradient>'
    '<linearGradient id="wave" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#2EE59D" stop-opacity="0"/><stop offset="20%" stop-color="#2EE59D"/><stop offset="80%" stop-color="#1FB5C8"/><stop offset="100%" stop-color="#1FB5C8" stop-opacity="0"/></linearGradient>'
    '</defs>')

b = f'<rect width="{GW}" height="{GH}" fill="{BOARD}"/>{grid_lines}'
b += f'<rect width="{GW}" height="{GH}" fill="url(#l1)"/><rect width="{GW}" height="{GH}" fill="url(#l3)"/>'
# notebook margin line (left tile) and a light wave running through all three tiles
b += f'<line x1="150" y1="0" x2="150" y2="{GH}" stroke="#FF7A6B" stroke-opacity=".35" stroke-width="3"/>'
BG_LEN = len(b)
# ── tile 1: brand (big mark, as in v1) + the problem, crossed out (as in v2)
b += ('<defs><radialGradient id="halo1" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#2EE59D" stop-opacity=".38"/>'
      '<stop offset="55%" stop-color="#1FB5C8" stop-opacity=".10"/><stop offset="100%" stop-color="#1FB5C8" stop-opacity="0"/></radialGradient>'
      '<radialGradient id="floor1" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#3CF2A8" stop-opacity=".55"/><stop offset="100%" stop-color="#3CF2A8" stop-opacity="0"/></radialGradient>'
      '<linearGradient id="track" gradientUnits="userSpaceOnUse" x1="70" y1="0" x2="3170" y2="0"><stop offset="0%" stop-color="#FF7A6B"/><stop offset="30%" stop-color="#2EE59D"/><stop offset="100%" stop-color="#1FB5C8"/></linearGradient></defs>')
b += '<circle cx="540" cy="440" r="470" fill="url(#halo1)"/>'
mh = 640; mw = mh * 342 / 377
b += f'<ellipse cx="560" cy="{110+mh-10}" rx="300" ry="38" fill="url(#floor1)"/>'
b += f'<image href="{MARK}" x="{540 - mw / 2 + 8:.1f}" y="110" width="{mw:.1f}" height="{mh}"/>'
wsz = 140
w1 = SEMI.width("Markaz", wsz); w2 = SEMI.width("ly", wsz); wx = 540 - (w1 + w2) / 2
b += T("Markaz", wx, 900, wsz, SEMI, FG) + T("ly", wx + w1, 900, wsz, SEMI, "url(#gh)")
b += T("O‘QUV MARKAZLARI UCHUN", 540, 970, 44, SEMI, MINT, "middle")
b += T("Endi kerak emas:", 540, 1052, 34, REG, MUTED, "middle")
py_ = 1078
for t in ["Daftar va Excel", "Yo‘qolgan qarzdorlar", "Qo‘lda davomat"]:
    w = MED.width(t, 34) + 110
    x_ = 540 - w / 2
    b += rr(x_, py_, w, 66, 33, "#2A1D1B", "#5A2A24", 2)
    b += f'<path d="M{x_+24} {py_+22} l22 22 M{x_+46} {py_+22} l-22 22" stroke="#FF7A6B" stroke-width="5" stroke-linecap="round"/>'
    b += T(t, x_ + 68, py_ + 45, 34, MED, "#E9C9C3")
    b += f'<line x1="{x_+64}" y1="{py_+34}" x2="{x_+w-24}" y2="{py_+34}" stroke="#FF7A6B" stroke-width="3" stroke-opacity=".8"/>'
    py_ += 82

# ── tile 2: v1 headline + v2 dashboard
x2 = TW + 90
lines = [("Daftar, Excel va", FG), ("qarzdorlarsiz", FG), ("boshqaring", "url(#gh)")]
hs = 104
while max(SEMI.width(t, hs) for t, _ in lines) > 900:
    hs -= 2
b += T("YECHIM · O‘QUV MARKAZINGIZNI", x2, 200, 32, SEMI, MINT)
y = 200 + hs * 1.15
for t, c in lines:
    b += T(t, x2, y, hs, SEMI, c); y += hs * 1.1
dx, dy, dw = x2, int(y - hs * 1.1 + 60), 800
b += rr(dx, dy, dw, 400, 30, SURF, LINE, 2)
kw = (dw - 52 - 26) / 3
kx = dx + 26
for lab, val, col in [("O‘quvchi", "368", FG), ("Tushum", "184 mln", FG), ("Qarzdor", "12", BAD)]:
    b += rr(kx, dy + 26, kw, 130, 20, SURF2) + T(lab, kx + 22, dy + 68, 26, REG, MUTED) + T(val, kx + 22, dy + 128, 44, SEMI, col)
    kx += kw + 13
b += T("Qarzdorlar · bugun", dx + 26, dy + 206, 28, SEMI, FG)
ry = dy + 228
for av, nm, sm in [("JR", "Jasur R. · IELTS", "590 000"), ("MK", "Madina K. · B1", "590 000")]:
    b += rr(dx + 26, ry, dw - 52, 70, 16, "#11302A")
    b += f'<circle cx="{dx+66}" cy="{ry+35}" r="21" fill="{SURF2}"/>' + T(av, dx + 66, ry + 44, 19, SEMI, MINT, "middle")
    b += T(nm, dx + 102, ry + 45, 27, MED, FG)
    p_, pw_ = pill("Qarz: " + sm, 0, 0, 21, "#3A1D1A", BAD, MED, 14, 42)
    b += f'<g transform="translate({dx + dw - 42 - pw_} {ry + 14})">{p_}</g>'
    ry += 82
cy = dy + 450
for t in ["Qarzdor darhol ko‘rinadi", "Davomat 1 bosishda", "Har filial foydasi aniq"]:
    b += rr(x2, cy, 60, 60, 30, "#123A2C") + ic("check", x2 + 13, cy + 13, 34, MINT, 3) + T(t, x2 + 84, cy + 44, 38, MED, FG)
    cy += 84
CHECK_END = cy

# ── tile 3: phone + offer
px, py, pw = 2 * TW + 290, 300, 500
b += T("Sayt + o‘quvchi kabineti", 2 * TW + 540, 200, 46, SEMI, FG, "middle")
b += rr(px - 12, py - 12, pw + 24, 834, 70, "#020806") + rr(px, py, pw, 810, 58, SURF)
b += rr(px + pw / 2 - 75, py + 20, 150, 28, 14, "#020806")
b += f'<circle cx="{px+60}" cy="{py+104}" r="30" fill="url(#g)"/>' + T("A", px + 60, py + 117, 30, SEMI, INK, "middle")
b += T("B1 guruh", px + 106, py + 94, 22, REG, MUTED) + T("Aziza Sobirova", px + 106, py + 128, 28, SEMI, FG)
cy = py + 168
for icn, s1, s2, paid in [("cal", "Bugungi dars", "18:00 · 3-xona", False), ("cap", "Lug‘at · bugun", "12 ta yangi so‘z", False),
                          ("tick", "Keyingi to‘lov", "To‘langan", True)]:
    b += rr(px + 24, cy, pw - 48, 124, 24, "url(#gh)" if paid else SURF2)
    b += ic(icn, px + 48, cy + 40, 44, INK if paid else "url(#g)", 2)
    b += T(s1, px + 110, cy + 52, 22, REG, "#0B3A26" if paid else MUTED) + T(s2, px + 110, cy + 90, 28, SEMI, INK if paid else FG)
    cy += 138
b += rr(px + 24, cy + 4, pw - 48, 110, 24, SURF2)
b += T("Shu oy davomati", px + 48, cy + 50, 24, REG, MUTED) + T("92%", px + pw - 48, cy + 52, 30, SEMI, FG, "end")
b += rr(px + 48, cy + 74, pw - 96, 14, 7, LINE) + rr(px + 48, cy + 74, (pw - 96) * .92, 14, 7, MINT)
b += rr(2 * TW + 120, 1040, 840, 170, 85, "url(#gh)")
b += T("7 kun bepul", 2 * TW + 540, 1118, 62, SEMI, INK, "middle")
b += T("3 daqiqada boshlang", 2 * TW + 540, 1174, 36, MED, "#0A3D27", "middle")
b += T("@markazly.uz", 2 * TW + 540, 1275, 34, MED, FG, "middle")

# ── connectors that physically cross the seams
# toast: icon sits in post 2, text in post 3 — one card split by the seam
tx, ty = 2 * TW - 130, 640
b += rr(tx, ty, 430, 108, 24, FG) + rr(tx + 22, ty + 22, 64, 64, 18, MINT) + ic("check", tx + 38, ty + 38, 32, INK, 3)
b += T("To‘lov qabul", 2 * TW + 30, ty + 50, 26, SEMI, INK) + T("590 000 so‘m", 2 * TW + 30, ty + 86, 24, REG, "#3F5A4D")
# one solid track: red (problem) → mint (solution) → teal (offer), 3 numbered stops, arrows on the seams
LY = 1378
b += f'<line x1="70" y1="{LY}" x2="{GW-70}" y2="{LY}" stroke="url(#track)" stroke-width="26" stroke-opacity=".18" stroke-linecap="round"/>'
b += f'<line x1="70" y1="{LY}" x2="{GW-70}" y2="{LY}" stroke="url(#track)" stroke-width="8" stroke-linecap="round"/>'
b += f'<path d="M{GW-96} {LY-20} L{GW-66} {LY} L{GW-96} {LY+20}" fill="none" stroke="#1FB5C8" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>'
for sx, col in [(TW, "#2EE59D"), (2 * TW, "#1FB5C8")]:
    b += f'<circle cx="{sx}" cy="{LY}" r="34" fill="{BOARD}" stroke="{col}" stroke-width="5"/>'
    b += f'<path d="M{sx-8} {LY-14} L{sx+8} {LY} L{sx-8} {LY+14}" fill="none" stroke="{col}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
for i, (num, lab, fill, tcol) in enumerate([("1", "Muammo", "#FF7A6B", "#2A0E0A"), ("2", "Yechim", "#2EE59D", INK), ("3", "Bepul sinov", "#1FB5C8", INK)]):
    w = SEMI.width(lab, 30) + 100
    x_ = i * TW + 540 - w / 2
    b += rr(x_, LY - 32, w, 64, 32, BOARD, fill, 3)
    b += f'<circle cx="{x_+32}" cy="{LY}" r="22" fill="{fill}"/>' + T(num, x_ + 32, LY + 10, 26, SEMI, tcol, "middle")
    b += T(lab, x_ + 66, LY + 11, 30, SEMI, FG)

from PIL import ImageDraw, ImageFilter
import io
def render(body, transparent=False):
    sv = f'<svg xmlns="http://www.w3.org/2000/svg" width="{GW}" height="{GH}" viewBox="0 0 {GW} {GH}">{defs}{body}</svg>'
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=sv.encode()))).convert("RGBA")
bg_img = render(b[:BG_LEN])
# soft light beam on the floor, from the door of the mark to the right edge (blurred, fading out)
beam = Image.new("RGBA", (GW, GH), (0, 0, 0, 0))
mask = Image.new("L", (GW, GH), 0)
ImageDraw.Draw(mask).polygon([(660, 700), (GW, 900), (GW, 1100), (660, 770)], fill=255)
fade = Image.linear_gradient("L").rotate(90, expand=True).resize((GW, GH)).transpose(Image.FLIP_LEFT_RIGHT)  # 255 at left → 0 at right
fade = fade.point(lambda v: int(v * 0.55))
mask = Image.composite(fade, Image.new("L", (GW, GH), 0), mask).filter(ImageFilter.GaussianBlur(38))
beam.paste((60, 242, 168, 255), (0, 0, GW, GH)); beam.putalpha(mask)
bg_img = Image.alpha_composite(bg_img, beam)
fg_img = render(b[BG_LEN:], True)
full_img = Image.alpha_composite(bg_img, fg_img).convert("RGB")
full = os.path.join(OUTG, "toliq_panorama.png")
full_img.save(full)
im = Image.open(full).convert("RGB")
names = ["1_chap", "2_orta", "3_ong"]
for i, n in enumerate(names):
    im.crop((i * TW, 0, (i + 1) * TW, GH)).save(os.path.join(OUTG, f"post_{n}.png"))

# how it looks on the profile (3 tiles with Instagram's thin gaps)
gap = 6; scale = 0.4
pw_, ph_ = int(TW * scale), int(GH * scale)
prev = Image.new("RGB", (3 * pw_ + 2 * gap, ph_), (255, 255, 255))
for i, n in enumerate(names):
    prev.paste(Image.open(os.path.join(OUTG, f"post_{n}.png")).resize((pw_, ph_), Image.LANCZOS), (i * (pw_ + gap), 0))
prev.save(os.path.join(OUTG, "profilda_korinishi.png"))
print("ok")
