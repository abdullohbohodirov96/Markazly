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
b += (f'<path d="M0 1250 C 600 1150, 1000 1350, 1620 1240 S 2700 1120, {GW} 1220" fill="none" stroke="url(#wave)" stroke-width="5" opacity=".9"/>'
      f'<path d="M0 1290 C 620 1200, 1020 1390, 1620 1285 S 2700 1170, {GW} 1265" fill="none" stroke="url(#wave)" stroke-width="2" opacity=".45"/>')

# ── tile 1: logo
mh = 430; mw = mh * 342 / 377
b += f'<image href="{MARK}" x="{540 - mw / 2:.1f}" y="260" width="{mw:.1f}" height="{mh}"/>'
wsz = 148
w1 = SEMI.width("Markaz", wsz); w2 = SEMI.width("ly", wsz); wx = 540 - (w1 + w2) / 2
b += T("Markaz", wx, 900, wsz, SEMI, FG) + T("ly", wx + w1, 900, wsz, SEMI, "url(#gh)")
b += T("O‘quv markaz boshqaruv tizimi", 540, 985, 40, REG, MUTED, "middle")

# ── tile 2: headline
x2 = TW + 90
b += T("O‘QUV MARKAZLARI UCHUN", x2, 360, 34, SEMI, MINT)
b += T("Markazingizni", x2, 500, 112, SEMI, FG)
b += T("bitta tizimdan", x2, 630, 112, SEMI, FG)
b += T("boshqaring", x2, 760, 112, SEMI, "url(#gh)")
chips = [("tick", "Davomat va to‘lovlar"), ("chart", "Filiallar hisoboti"), ("globe", "Sayt + o‘quvchi kabineti")]
cy = 850
for icn, t in chips:
    w = REG.width(t, 38) + 110
    b += rr(x2, cy, w, 82, 41, BOARD2, LINE, 2) + ic(icn, x2 + 26, cy + 21, 40) + T(t, x2 + 82, cy + 54, 38, MED, FG)
    cy += 104

# ── tile 3: phone + offer
px, py, pw = 2 * TW + 290, 230, 500
b += rr(px - 12, py - 12, pw + 24, 904, 70, "#020806") + rr(px, py, pw, 880, 58, SURF)
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
b += rr(2 * TW + 140, 1000, 800, 150, 75, "url(#gh)")
b += T("7 kun bepul sinov", 2 * TW + 540, 1095, 54, SEMI, INK, "middle")
b += T("@markazly.uz", 2 * TW + 540, 1225, 36, MED, FG, "middle")
# toast across the 2→3 seam? keep text off seams: place it fully inside tile 3
b += rr(2 * TW + 40, 560, 330, 108, 24, FG) + rr(2 * TW + 60, 582, 64, 64, 18, MINT) + ic("check", 2 * TW + 76, 598, 32, INK, 3)
b += T("To‘lov qabul", 2 * TW + 140, 610, 26, SEMI, INK) + T("590 000 so‘m", 2 * TW + 140, 646, 24, REG, "#3F5A4D")

svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{GW}" height="{GH}" viewBox="0 0 {GW} {GH}">{defs}{b}</svg>'
full = os.path.join(OUTG, "toliq_panorama.png")
cairosvg.svg2png(bytestring=svg.encode(), write_to=full)

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
