"""Instagram to'rining 2-qatori: YECHIM — 3 ta post (tizim, sayt, kabinet). Har biri 1080x1440."""
import os, io
import cairosvg
from PIL import Image, ImageDraw, ImageFilter

D = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(D, "make_stories.py")).read().split("# ───────────────────────── 1. Tariflar")[0])

OUTG = os.path.join(D, "markazly", "instagram_to'r_2")
os.makedirs(OUTG, exist_ok=True)
GW, GH, TW = 3240, 1440, 1080
BOARD, BOARD2, AMB = "#0D2620", "#112E27", "#F6C76B"

grid = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{GH}" stroke="#E8F5EF" stroke-opacity=".045" stroke-width="2"/>' for x in range(0, GW + 1, 40))
grid += "".join(f'<line x1="0" y1="{y}" x2="{GW}" y2="{y}" stroke="#E8F5EF" stroke-opacity=".045" stroke-width="2"/>' for y in range(0, GH + 1, 40))
defs = DEFS.replace("</defs>",
    '<linearGradient id="amb" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#F6C76B"/><stop offset="100%" stop-color="#E8873D"/></linearGradient>'
    '<radialGradient id="lA" cx="50%" cy="45%" r="45%"><stop offset="0%" stop-color="#2EE59D" stop-opacity=".14"/><stop offset="100%" stop-color="#2EE59D" stop-opacity="0"/></radialGradient>'
    '</defs>')

bg = f'<rect width="{GW}" height="{GH}" fill="{BOARD}"/>{grid}'
for i in range(3):
    bg += f'<rect x="{i*TW}" width="{TW}" height="{GH}" fill="url(#lA)"/>'

fg = ""


def header(i, eyebrow, l1, l2):
    x = i * TW + 90
    out = T(eyebrow, x, 250, 32, SEMI, MINT)
    out += T(l1, x, 352, 84, SEMI, FG) + T(l2, x, 448, 84, SEMI, "url(#gh)")
    return out


def bullets(i, items, y=1150):
    x = i * TW + 90; out = ""
    for t in items:
        out += rr(x, y - 50, 64, 64, 32, "#123A2C") + ic("check", x + 14, y - 36, 36, MINT, 3) + T(t, x + 90, y, 40, MED, FG)
        y += 92
    return out


# ── 1. Boshqaruv tizimi
fg += header(0, "YECHIM · BITTA OBUNADA", "Boshqaruv", "tizimi")
x0, y0, w0 = 90, 520, 900
fg += rr(x0, y0, w0, 520, 30, SURF, LINE, 2)
k = [("O‘quvchi", "368", FG), ("Tushum", "184 mln", FG), ("Qarzdor", "12", BAD)]
kx = x0 + 28
for lab, val, col in k:
    fg += rr(kx, y0 + 28, 266, 140, 20, SURF2) + T(lab, kx + 24, y0 + 74, 26, REG, MUTED) + T(val, kx + 24, y0 + 136, 46, SEMI, col)
    kx += 266 + 13
fg += T("Qarzdorlar", x0 + 28, y0 + 224, 30, SEMI, FG) + T("bugun", x0 + w0 - 28, y0 + 224, 24, REG, MUTED, "end")
rows = [("JR", "Jasur R. · IELTS", "590 000"), ("MK", "Madina K. · B1", "590 000"), ("SA", "Sardor A. · A2", "290 000")]
ry = y0 + 250
for av, nm, sm in rows:
    fg += rr(x0 + 28, ry, w0 - 56, 74, 16, "#11302A")
    fg += f'<circle cx="{x0+70}" cy="{ry+37}" r="22" fill="{SURF2}"/>' + T(av, x0 + 70, ry + 46, 20, SEMI, MINT, "middle")
    fg += T(nm, x0 + 108, ry + 47, 28, MED, FG)
    p_, pw_ = pill("Qarz: " + sm, 0, 0, 22, "#3A1D1A", BAD, MED, 14, 44)
    fg += f'<g transform="translate({x0 + w0 - 46 - pw_} {ry + 15})">{p_}</g>'
    ry += 86
fg += bullets(0, ["Qarzdorlar avtomatik ro‘yxatda", "Davomat — 1 bosishda", "Har filial foydasi aniq"])

# ── 2. Markaz sayti
fg += header(1, "YECHIM", "Markazingizga", "o‘z sayti")
x, y, w = TW + 90, 520, 900
fg += rr(x, y, w, 520, 30, "#071510", LINE, 2)
fg += f'<path d="M{x} {y+30} Q{x} {y} {x+30} {y} H{x+w-30} Q{x+w} {y} {x+w} {y+30} V{y+62} H{x} Z" fill="#0B1D16"/>'
for j, c in enumerate([MINT, LINE, LINE]):
    fg += f'<circle cx="{x+34+j*26}" cy="{y+31}" r="8" fill="{c}"/>'
fg += rr(x + 130, y + 13, 640, 38, 19, "#06120D", LINE, 2) + ic("lock", x + 148, y + 21, 20, MUTED, 2) + T("nuracademy.uz", x + 178, y + 40, 22, MED, FG)
fg += rr(x + 32, y + 86, 46, 46, 12, "url(#amb)") + T("N", x + 55, y + 119, 24, SEMI, "#2A1400", "middle") + T("Nur Academy", x + 92, y + 120, 28, SEMI, FG)
fg += rr(x + 744, y + 88, 124, 44, 22, FG) + T("Ariza", x + 806, y + 118, 22, SEMI, INK, "middle")
pp, _ = pill("Yangi guruhlar ochildi", x + 32, y + 166, 20, "#2A2412", AMB, MED, 14, 40)
fg += pp
hero, _ = P("Ingliz tilida birinchi darsdan gapiring", x + 32, y + 260, 40, 500, SEMI, FG, 1.15)
fg += hero
fg += rr(x + 32, y + 360, 300, 56, 28, "url(#amb)") + T("Bepul darsga yozilish", x + 182, y + 396, 22, SEMI, "#2A1400", "middle")
fg += rr(x + 620, y + 170, 240, 240, 28, "#12281F", LINE, 2) + ic("cap", x + 670, y + 220, 140, AMB, 1.5)
cx = x + 32
for g, t in [("url(#amb)", "General English"), ("url(#gh)", "IELTS"), ("#7B86FF", "Bolalar uchun")]:
    fg += rr(cx, y + 440, 266, 56, 16, "#0C1F18", LINE, 2) + rr(cx + 16, y + 462, 12, 12, 6, g) + T(t, cx + 40, y + 477, 22, SEMI, FG)
    cx += 280
fg += bullets(1, ["O‘z domenida, o‘z logosi bilan", "Ariza o‘zi tizimga tushadi", "Telefonda tez va chiroyli"])

# ── 3. O'quvchi kabineti
fg += header(2, "YECHIM", "O‘quvchi", "kabineti")
x, y = 2 * TW + 90, 520
# flashcard
fg += rr(x, y, 900, 250, 30, "url(#best)", MINT, 2)
fg += T("Lug‘at · 12 tadan 5-so‘z", x + 36, y + 58, 26, REG, MUTED)
fg += T("achieve", x + 36, y + 140, 72, SEMI, FG) + T("erishmoq · I achieved my goal.", x + 36, y + 196, 28, REG, MUTED)
fg += rr(x + 620, y + 160, 120, 56, 16, SURF2, LINE, 2) + T("Yana", x + 680, y + 197, 24, SEMI, FG, "middle")
fg += rr(x + 754, y + 160, 120, 56, 16, MINT) + T("Bilaman", x + 814, y + 197, 24, SEMI, INK, "middle")
# homework + points
fg += rr(x, y + 272, 440, 248, 30, SURF, LINE, 2)
fg += ic("book", x + 32, y + 304, 44) + T("Uyga vazifa", x + 32, y + 400, 32, SEMI, FG)
p_, _ = pill("92 / 100", x + 32, y + 430, 24, "#123A2C", GOOD, SEMI, 16, 48)
fg += p_
fg += rr(x + 460, y + 272, 440, 248, 30, SURF, LINE, 2)
fg += ic("chart", x + 492, y + 304, 44) + T("Ballar", x + 492, y + 400, 32, SEMI, FG)
fg += T("1 248", x + 492, y + 470, 48, SEMI, MINT) + T("· Bilimdon", x + 492 + SEMI.width("1 248", 48) + 12, y + 468, 26, REG, MUTED)
fg += bullets(2, ["Darslar va uyga vazifa", "Lug‘at — kartochkalar bilan", "Ballar, reyting va sovg‘alar"])


def render(body):
    sv = f'<svg xmlns="http://www.w3.org/2000/svg" width="{GW}" height="{GH}" viewBox="0 0 {GW} {GH}">{defs}{body}</svg>'
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=sv.encode()))).convert("RGBA")


bg_img = render(bg)
# soft light band continuing the first row's beam across the bottom
mask = Image.new("L", (GW, GH), 0)
ImageDraw.Draw(mask).polygon([(0, 1360), (GW, 1300), (GW, 1420), (0, 1440)], fill=110)
mask = mask.filter(ImageFilter.GaussianBlur(36))
band = Image.new("RGBA", (GW, GH), (46, 229, 157, 255)); band.putalpha(mask)
img = Image.alpha_composite(Image.alpha_composite(bg_img, band), render(fg)).convert("RGB")
img.save(os.path.join(OUTG, "toliq_panorama.png"))
names = ["4_tizim_chap", "5_sayt_orta", "6_kabinet_ong"]
for i, n in enumerate(names):
    img.crop((i * TW, 0, (i + 1) * TW, GH)).save(os.path.join(OUTG, f"post_{n}.png"))

# preview: both rows as on the profile (row 1 = cover on top, row 2 = solution)
row1 = os.path.join(D, "markazly", "instagram_to'r")
s_, gap = 0.36, 6
tw_, th_ = int(TW * s_), int(GH * s_)
prev = Image.new("RGB", (3 * tw_ + 2 * gap, 2 * th_ + gap), (255, 255, 255))
for i, n in enumerate(["1_chap", "2_orta", "3_ong"]):
    prev.paste(Image.open(os.path.join(row1, f"post_{n}.png")).resize((tw_, th_), Image.LANCZOS), (i * (tw_ + gap), 0))
for i, n in enumerate(names):
    prev.paste(Image.open(os.path.join(OUTG, f"post_{n}.png")).resize((tw_, th_), Image.LANCZOS), (i * (tw_ + gap), th_ + gap))
prev.save(os.path.join(OUTG, "profil_2_qator.png"))
print("ok")
