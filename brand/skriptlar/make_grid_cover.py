"""Instagram profil to'ri uchun 3 ta postga bo'linadigan bitta katta muqova.
Har bir bo'lak 1080x1440 (3:4 — Instagram to'ri shu nisbatda ko'rsatadi)."""
import os, base64
import cairosvg
from PIL import Image

D = os.path.dirname(os.path.abspath(__file__))
# reuse fonts, text and icon helpers from the stories script (everything before the first story)
src = open(os.path.join(D, "make_stories.py")).read().split("# ───────────────────────── 1. Tariflar")[0]
exec(src)

OUTG = os.path.join(D, "markazly", "instagram_to'r")
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
# ── tile 1: big glowing mark; the door's light spills right across all three tiles
b += ('<defs><radialGradient id="halo1" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#2EE59D" stop-opacity=".38"/>'
      '<stop offset="55%" stop-color="#1FB5C8" stop-opacity=".10"/><stop offset="100%" stop-color="#1FB5C8" stop-opacity="0"/></radialGradient>'
      '<linearGradient id="beam" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#3CF2A8" stop-opacity=".45"/>'
      '<stop offset="45%" stop-color="#2EE59D" stop-opacity=".16"/><stop offset="100%" stop-color="#1FB5C8" stop-opacity="0"/></linearGradient>'
      '<filter id="soft" x="-20%" y="-60%" width="140%" height="220%"><feGaussianBlur stdDeviation="28"/></filter>'
      '<radialGradient id="floor1" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#3CF2A8" stop-opacity=".55"/><stop offset="100%" stop-color="#3CF2A8" stop-opacity="0"/></radialGradient></defs>')
b += '<circle cx="540" cy="560" r="520" fill="url(#halo1)"/>'
b += '<ellipse cx="560" cy="950" rx="360" ry="46" fill="url(#floor1)"/>'
mh = 780; mw = mh * 342 / 377
b += f'<image href="{MARK}" x="{540 - mw / 2 + 10:.1f}" y="170" width="{mw:.1f}" height="{mh}"/>'
wsz = 150
w1 = SEMI.width("Markaz", wsz); w2 = SEMI.width("ly", wsz); wx = 540 - (w1 + w2) / 2
b += T("Markaz", wx, 1145, wsz, SEMI, FG) + T("ly", wx + w1, 1145, wsz, SEMI, "url(#gh)")
b += T("O‘QUV MARKAZLARI UCHUN", 540, 1235, 50, SEMI, MINT, "middle")

# ── tile 2: problem → result
x2 = TW + 90
maxw = TW - 180
lines = [("Daftar, Excel va", FG), ("qarzdorlarsiz", FG), ("boshqaring", "url(#gh)")]
hs = 112
while max(SEMI.width(t, hs) for t, _ in lines) > maxw:
    hs -= 2
b += T("O‘QUV MARKAZINGIZNI", x2, 330, 34, SEMI, MINT)
y = 330 + hs * 1.18
for t, c in lines:
    b += T(t, x2, y, hs, SEMI, c); y += hs * 1.14
cy = y + 10
for t in ["Qarzdor darhol ko‘rinadi", "Davomat 1 bosishda", "Har filial foydasi aniq"]:
    w = MED.width(t, 40) + 120
    b += rr(x2, cy, w, 88, 44, BOARD2, LINE, 2) + rr(x2 + 16, cy + 16, 56, 56, 28, "#123A2C") + ic("check", x2 + 28, cy + 28, 32, MINT, 3) + T(t, x2 + 90, cy + 58, 40, MED, FG)
    cy += 108

# ── tile 3: phone + offer
px, py, pw = 2 * TW + 290, 300, 500
b += T("Sayt + o‘quvchi kabineti", 2 * TW + 540, 200, 46, SEMI, FG, "middle")
b += rr(px - 12, py - 12, pw + 24, 834, 70, "#020806") + rr(px, py, pw, 810, 58, SURF)
b += rr(px + pw / 2 - 75, py + 20, 150, 28, 14, "#020806")
b += f'<circle cx="{px+60}" cy="{py+104}" r="30" fill="url(#g)"/>' + T("A", px + 60, py + 117, 30, SEMI, INK, "middle")
b += T("B1 guruh", px + 106, py + 94, 22, REG, MUTED) + T("Aziza Sobirova", px + 106, py + 128, 28, SEMI, FG)
cards = [("cal", "Bugungi dars", "18:00 · 3-xona", False), ("cap", "Lug‘at · bugun", "12 ta yangi so‘z", False),
         ("tick", "Keyingi to‘lov", "To‘langan", True)]
cy = py + 168
for icn, s1, s2, paid in cards:
    b += rr(px + 24, cy, pw - 48, 124, 24, "url(#gh)" if paid else SURF2)
    b += ic(icn, px + 48, cy + 40, 44, INK if paid else "url(#g)", 2)
    b += T(s1, px + 110, cy + 52, 22, REG, "#0B3A26" if paid else MUTED) + T(s2, px + 110, cy + 90, 28, SEMI, INK if paid else FG)
    cy += 138
b += rr(px + 24, cy + 4, pw - 48, 110, 24, SURF2)
b += T("Shu oy davomati", px + 48, cy + 50, 24, REG, MUTED) + T("92%", px + pw - 48, cy + 52, 30, SEMI, FG, "end")
b += rr(px + 48, cy + 74, pw - 96, 14, 7, LINE) + rr(px + 48, cy + 74, (pw - 96) * .92, 14, 7, MINT)
# offer badge overlapping the phone
b += rr(2 * TW + 120, 1040, 840, 170, 85, "url(#gh)")
b += T("7 kun bepul", 2 * TW + 540, 1118, 62, SEMI, INK, "middle")
b += T("3 daqiqada boshlang", 2 * TW + 540, 1174, 36, MED, "#0A3D27", "middle")
b += T("@markazly.uz", 2 * TW + 540, 1290, 36, MED, FG, "middle")
# toast across the 2→3 seam? keep text off seams: place it fully inside tile 3
b += rr(2 * TW + 40, 600, 330, 108, 24, FG) + rr(2 * TW + 60, 622, 64, 64, 18, MINT) + ic("check", 2 * TW + 76, 638, 32, INK, 3)
b += T("To‘lov qabul", 2 * TW + 140, 650, 26, SEMI, INK) + T("590 000 so‘m", 2 * TW + 140, 686, 24, REG, "#3F5A4D")

from PIL import ImageDraw, ImageFilter
import io
def render(body, transparent=False):
    sv = f'<svg xmlns="http://www.w3.org/2000/svg" width="{GW}" height="{GH}" viewBox="0 0 {GW} {GH}">{defs}{body}</svg>'
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=sv.encode()))).convert("RGBA")
bg_img = render(b[:BG_LEN])
# soft light beam on the floor, from the door of the mark to the right edge (blurred, fading out)
beam = Image.new("RGBA", (GW, GH), (0, 0, 0, 0))
mask = Image.new("L", (GW, GH), 0)
ImageDraw.Draw(mask).polygon([(650, 905), (GW, 1060), (GW, 1250), (650, 985)], fill=255)
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
