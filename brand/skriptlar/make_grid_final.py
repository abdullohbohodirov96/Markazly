"""Instagram profil to'ri uchun 3 ta postga bo'linadigan bitta katta muqova.
Har bir bo'lak 1080x1440 (3:4 — Instagram to'ri shu nisbatda ko'rsatadi)."""
import os, base64
import cairosvg
from PIL import Image

D = os.path.dirname(os.path.abspath(__file__))
# reuse fonts, text and icon helpers from the stories script (everything before the first story)
src = open(os.path.join(D, "make_stories.py")).read().split("# ───────────────────────── 1. Tariflar")[0]
exec(src)

OUTG = os.path.join(D, "markazly", "instagram_3_post")
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
b += '<circle cx="540" cy="420" r="440" fill="url(#halo1)"/>'
b += '<ellipse cx="560" cy="690" rx="280" ry="36" fill="url(#floor1)"/>'
mh = 560; mw = mh * 342 / 377
b += f'<image href="{MARK}" x="{540 - mw / 2 + 8:.1f}" y="120" width="{mw:.1f}" height="{mh}"/>'
wsz = 132
w1 = SEMI.width("Markaz", wsz); w2 = SEMI.width("ly", wsz); wx = 540 - (w1 + w2) / 2
b += T("Markaz", wx, 830, wsz, SEMI, FG) + T("ly", wx + w1, 830, wsz, SEMI, "url(#gh)")
b += T("O‘QUV MARKAZLARI UCHUN", 540, 900, 44, SEMI, MINT, "middle")
# the problem, crossed out
b += T("Endi kerak emas:", 540, 1030, 36, REG, MUTED, "middle")
probs = ["Daftar va Excel", "Yo‘qolgan qarzdorlar", "Qo‘lda davomat"]
py_ = 1070
for t in probs:
    w = MED.width(t, 38) + 120
    x_ = 540 - w / 2
    b += rr(x_, py_, w, 78, 39, "#2A1D1B", "#5A2A24", 2)
    b += f'<path d="M{x_+26} {py_+26} l26 26 M{x_+52} {py_+26} l-26 26" stroke="#FF7A6B" stroke-width="5" stroke-linecap="round"/>'
    b += T(t, x_ + 76, py_ + 52, 38, MED, "#E9C9C3")
    b += f'<line x1="{x_+72}" y1="{py_+40}" x2="{x_+w-28}" y2="{py_+40}" stroke="#FF7A6B" stroke-width="3" stroke-opacity=".8"/>'
    py_ += 96

# ── tile 2: solution
x2 = TW + 90
b += T("YECHIM", x2, 230, 34, SEMI, MINT)
b += T("Hammasi bitta", x2, 340, 96, SEMI, FG)
b += T("tizimda", x2, 448, 96, SEMI, "url(#gh)")
dx, dy, dw = x2, 510, 900
b += rr(dx, dy, dw, 460, 30, SURF, LINE, 2)
k = [("O‘quvchi", "368", FG), ("Tushum", "184 mln", FG), ("Qarzdor", "12", BAD)]
kx = dx + 26
for lab, val, col in k:
    b += rr(kx, dy + 26, 268, 136, 20, SURF2) + T(lab, kx + 24, dy + 70, 26, REG, MUTED) + T(val, kx + 24, dy + 132, 46, SEMI, col)
    kx += 268 + 13
b += T("Qarzdorlar · bugun", dx + 26, dy + 216, 28, SEMI, FG)
ry = dy + 240
for av, nm, sm in [("JR", "Jasur R. · IELTS", "590 000"), ("MK", "Madina K. · B1", "590 000")]:
    b += rr(dx + 26, ry, dw - 52, 76, 16, "#11302A")
    b += f'<circle cx="{dx+68}" cy="{ry+38}" r="22" fill="{SURF2}"/>' + T(av, dx + 68, ry + 47, 20, SEMI, MINT, "middle")
    b += T(nm, dx + 106, ry + 48, 28, MED, FG)
    p_, pw_ = pill("Qarz: " + sm, 0, 0, 22, "#3A1D1A", BAD, MED, 14, 44)
    b += f'<g transform="translate({dx + dw - 44 - pw_} {ry + 16})">{p_}</g>'
    ry += 90
cy = 1050
for t in ["Qarzdor darhol ko‘rinadi", "Davomat 1 bosishda", "Har filial foydasi aniq"]:
    b += rr(x2, cy, 64, 64, 32, "#123A2C") + ic("check", x2 + 14, cy + 14, 36, MINT, 3) + T(t, x2 + 90, cy + 47, 40, MED, FG)
    cy += 96

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

# one continuous flow line ties the three posts into a single banner: problem → solution → offer
b += ('<path d="M860 1180 C 900 1330, 1000 1350, 1180 1360 L 2080 1360 C 2200 1360, 2240 1320, 2235 1235" '
      'fill="none" stroke="url(#wave)" stroke-width="6" stroke-dasharray="2 18" stroke-linecap="round"/>')
b += '<path d="M2213 1252 L2235 1222 L2257 1252" fill="none" stroke="#2EE59D" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
for cx_, lab in [(1620, "Muammo  ·  Yechim  ·  Bepul sinov")]:
    w = MED.width(lab, 30) + 56
    b += rr(cx_ - w / 2, 1328, w, 64, 32, BOARD, "#2EE59D", 2) + T(lab, cx_, 1371, 30, MED, FG, "middle")

from PIL import ImageDraw, ImageFilter
import io
def render(body, transparent=False):
    sv = f'<svg xmlns="http://www.w3.org/2000/svg" width="{GW}" height="{GH}" viewBox="0 0 {GW} {GH}">{defs}{body}</svg>'
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=sv.encode()))).convert("RGBA")
bg_img = render(b[:BG_LEN])
# soft light beam on the floor, from the door of the mark to the right edge (blurred, fading out)
beam = Image.new("RGBA", (GW, GH), (0, 0, 0, 0))
mask = Image.new("L", (GW, GH), 0)
ImageDraw.Draw(mask).polygon([(640, 660), (GW, 860), (GW, 1060), (640, 730)], fill=255)
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
