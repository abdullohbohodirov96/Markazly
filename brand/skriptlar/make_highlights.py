import os, base64
import cairosvg

D = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(D, "markazly", "aktuallar")
os.makedirs(OUT, exist_ok=True)

# 24x24 line icons (stroke), same family as the website
ICONS = {
    "1_Tariflar": '<rect x="2.5" y="5" width="19" height="14" rx="3"/><path d="M2.5 10h19M6.5 15h4"/>',
    "2_Imkoniyatlar": '<rect x="3" y="3" width="7.5" height="7.5" rx="2"/><rect x="13.5" y="3" width="7.5" height="7.5" rx="2"/><rect x="3" y="13.5" width="7.5" height="7.5" rx="2"/><rect x="13.5" y="13.5" width="7.5" height="7.5" rx="2"/>',
    "3_Filiallar": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    "4_Sayt": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.8 3 2.8 15 0 18M12 3c-2.8 3-2.8 15 0 18"/>',
    "5_Kabinet": '<rect x="6" y="2.5" width="12" height="19" rx="3"/><path d="M10.5 18.5h3"/>',
    "5b_Gamifikatsiya": '<path d="M12 3l2.6 5.6 6 .7-4.5 4.1 1.2 6L12 16.4 6.7 19.4l1.2-6L3.4 9.3l6-.7z"/>',
    "6_Bepul_sinov": '<circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.7 2.7L16 9.5"/>',
    "7_Aloqa": '<path d="M5 3.5h3.5l1.7 4.3-2.2 1.4a11 11 0 006.8 6.8l1.4-2.2 4.3 1.7V19a1.5 1.5 0 01-1.6 1.5C10.6 20 4 13.4 3.5 5.1A1.5 1.5 0 015 3.5z"/>',
}

W, H = 1080, 1920
DEFS = ('<defs><radialGradient id="bg" cx="50%" cy="50%" r="60%">'
        '<stop offset="0%" stop-color="#0C2C21"/><stop offset="60%" stop-color="#06180F"/><stop offset="100%" stop-color="#020A07"/></radialGradient>'
        '<linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#3CF2A8"/><stop offset="100%" stop-color="#1A9FC4"/></linearGradient>'
        '<radialGradient id="halo" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#2EE59D" stop-opacity=".22"/>'
        '<stop offset="100%" stop-color="#2EE59D" stop-opacity="0"/></radialGradient></defs>')

sheet = []
for name, paths in ICONS.items():
    # icon sits in the centre; Instagram crops highlight covers to a circle around the middle
    s = 18
    x, y = (W - 24 * s) / 2, (H - 24 * s) / 2
    body = (f'<rect width="{W}" height="{H}" fill="url(#bg)"/>'
            f'<circle cx="{W/2}" cy="{H/2}" r="330" fill="url(#halo)"/>'
            f'<circle cx="{W/2}" cy="{H/2}" r="300" fill="none" stroke="#1D3B2F" stroke-width="0"/>'
            f'<g transform="translate({x} {y}) scale({s})" fill="none" stroke="url(#g)" stroke-width="1.7" '
            f'stroke-linecap="round" stroke-linejoin="round">{paths}</g>')
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{DEFS}{body}</svg>'
    cairosvg.svg2png(bytestring=svg.encode(), write_to=os.path.join(OUT, f"aktual_{name}.png"))
    sheet.append(name)
print("ok", len(sheet))

# preview: circles as Instagram shows them
from PIL import Image, ImageDraw
n = len(sheet); C = 240; pad = 40
prev = Image.new("RGB", (pad + n * (C + pad), C + 2 * pad), (255, 255, 255))
mask = Image.new("L", (C, C), 0); ImageDraw.Draw(mask).ellipse((0, 0, C - 1, C - 1), fill=255)
for i, name in enumerate(sheet):
    im = Image.open(os.path.join(OUT, f"aktual_{name}.png")).convert("RGB")
    sq = im.crop((0, (H - W) // 2, W, (H - W) // 2 + W)).resize((C, C), Image.LANCZOS)
    prev.paste(sq, (pad + i * (C + pad), pad), mask)
prev.save(os.path.join(D, "markazly", "aktuallar_korinishi.png"))
