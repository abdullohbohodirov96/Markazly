"""Markazly Instagram highlight stories, 1080x1920, vector-drawn then rasterised."""
import os, base64
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import cairosvg

D = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(D, "markazly", "storislar")
os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1920

# palette
BG1, BG2, BG3 = "#0C2C21", "#06180F", "#020A07"
SURF, SURF2, LINE = "#0E2219", "#133328", "#1D3B2F"
FG, MUTED, MINT, TEAL, INK = "#F4F8F6", "#A9C2B6", "#2EE59D", "#1FB5C8", "#04140D"
GOOD, BAD = "#46D98F", "#FF7A6B"


class Face:
    def __init__(self, p):
        f = TTFont(p); self.gs = f.getGlyphSet(); self.cmap = f.getBestCmap(); self.upm = f["head"].unitsPerEm

    def width(self, text, size):
        s = size / self.upm
        return sum(self.gs[self.cmap.get(ord(c), self.cmap[ord('?')])].width * s for c in text)

    def path(self, text, size, x, base):
        s = size / self.upm; parts = []; cx = x
        for ch in text:
            g = self.gs[self.cmap.get(ord(ch), self.cmap[ord('?')])]
            pen = SVGPathPen(self.gs); g.draw(TransformPen(pen, (s, 0, 0, -s, cx, base)))
            parts.append(pen.getCommands()); cx += g.width * s
        return " ".join(parts)


SEMI = Face(os.path.join(D, "Poppins-SemiBold.ttf"))
MED = Face(os.path.join(D, "Poppins-Medium.ttf"))
REG = Face(os.path.join(D, "Poppins-Regular.ttf"))


def T(text, x, base, size, face=REG, fill=FG, anchor="start"):
    w = face.width(text, size)
    if anchor == "middle": x -= w / 2
    elif anchor == "end": x -= w
    return f'<path d="{face.path(text, size, x, base)}" fill="{fill}"/>'


def wrap(text, size, face, maxw):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if face.width(t, size) <= maxw: cur = t
        else: lines.append(cur); cur = wd
    if cur: lines.append(cur)
    return lines


def P(text, x, base, size, maxw, face=REG, fill=MUTED, lh=1.35, anchor="start"):
    out = ""; lines = wrap(text, size, face, maxw)
    for i, ln in enumerate(lines):
        out += T(ln, x, base + i * size * lh, size, face, fill, anchor)
    return out, base + (len(lines) - 1) * size * lh


ICON = {
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "card": '<rect x="2.5" y="5" width="19" height="14" rx="3"/><path d="M2.5 10h19M6.5 15h4"/>',
    "grid": '<rect x="3" y="3" width="7.5" height="7.5" rx="2"/><rect x="13.5" y="3" width="7.5" height="7.5" rx="2"/><rect x="3" y="13.5" width="7.5" height="7.5" rx="2"/><rect x="13.5" y="13.5" width="7.5" height="7.5" rx="2"/>',
    "chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.8 3 2.8 15 0 18M12 3c-2.8 3-2.8 15 0 18"/>',
    "phone": '<rect x="6" y="2.5" width="12" height="19" rx="3"/><path d="M10.5 18.5h3"/>',
    "tick": '<circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.7 2.7L16 9.5"/>',
    "call": '<path d="M5 3.5h3.5l1.7 4.3-2.2 1.4a11 11 0 006.8 6.8l1.4-2.2 4.3 1.7V19a1.5 1.5 0 01-1.6 1.5C10.6 20 4 13.4 3.5 5.1A1.5 1.5 0 015 3.5z"/>',
    "send": '<path d="M21 3L3 10.5l7 2.5 2.5 7z"/>',
    "insta": '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r=".6"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.8-3.6 3.4-5.5 6.5-5.5s5.7 1.9 6.5 5.5"/><circle cx="17" cy="9" r="2.6"/><path d="M16.5 14.3c2.6.2 4.4 1.9 5 4.7"/>',
    "cap": '<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c3 2.5 9 2.5 12 0v-5"/>',
    "cal": '<rect x="3" y="5" width="18" height="16" rx="3"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "wallet": '<path d="M3 7.5A2.5 2.5 0 015.5 5H19v4"/><rect x="3" y="7.5" width="18" height="12" rx="2.5"/><circle cx="16.5" cy="13.5" r="1"/>',
    "lock": '<rect x="4" y="10" width="16" height="11" rx="3"/><path d="M8 10V7a4 4 0 018 0v3"/>',
    "book": '<path d="M12 6.5C10 5 6.5 4.5 3 5v13c3.5-.5 7 0 9 1.5 2-1.5 5.5-2 9-1.5V5c-3.5-.5-7 0-9 1.5z"/><path d="M12 6.5v13"/>',
    "branch": '<path d="M3 21V9l6-4 6 4v12M15 21V12l6 3v6M2 21h20M7 13h4M7 17h4"/>',
    "door": '<path d="M5 21V4.5A1.5 1.5 0 016.5 3h11A1.5 1.5 0 0119 4.5V21M3 21h18"/><circle cx="15" cy="12.5" r=".9"/>',
    "arrow": '<path d="M12 4v16M5 13l7 7 7-7"/>',
}


def ic(name, x, y, size, stroke="url(#g)", sw=1.8):
    s = size / 24
    return (f'<g transform="translate({x} {y}) scale({s})" fill="none" stroke="{stroke}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</g>')


with open(os.path.join(D, "mark_transparent.png"), "rb") as fh:
    MARK = "data:image/png;base64," + base64.b64encode(fh.read()).decode()

DEFS = (f'<defs><radialGradient id="bg" cx="50%" cy="35%" r="80%"><stop offset="0%" stop-color="{BG1}"/>'
        f'<stop offset="55%" stop-color="{BG2}"/><stop offset="100%" stop-color="{BG3}"/></radialGradient>'
        f'<linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#3CF2A8"/><stop offset="100%" stop-color="#1A9FC4"/></linearGradient>'
        f'<linearGradient id="gh" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#3CF2A8"/><stop offset="100%" stop-color="#1A9FC4"/></linearGradient>'
        f'<linearGradient id="card" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="{SURF2}"/><stop offset="100%" stop-color="{SURF}"/></linearGradient>'
        f'<linearGradient id="best" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#0F4A35"/><stop offset="100%" stop-color="{SURF}"/></linearGradient>'
        f'<radialGradient id="glow" cx="50%" cy="100%" r="70%"><stop offset="0%" stop-color="{MINT}" stop-opacity=".28"/><stop offset="100%" stop-color="{MINT}" stop-opacity="0"/></radialGradient>'
        '</defs>')


def frame(body, eyebrow):
    """Common story frame: background, glow, logo row and handle. Content area y≈330–1650."""
    logo = (f'<image href="{MARK}" x="80" y="214" width="{74*342/377:.1f}" height="74"/>'
            + T("Markaz", 80 + 74 * 342 / 377 + 22, 270, 52, SEMI, FG)
            + T("ly", 80 + 74 * 342 / 377 + 22 + SEMI.width("Markaz", 52), 270, 52, SEMI, "url(#gh)"))
    eb = T(eyebrow.upper(), W - 80, 262, 26, MED, MINT, "end")
    foot = T("@markazly_uz", W / 2, 1760, 30, MED, MUTED, "middle")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{DEFS}'
            f'<rect width="{W}" height="{H}" fill="url(#bg)"/><rect y="1300" width="{W}" height="620" fill="url(#glow)"/>'
            f'{logo}{eb}{body}{foot}</svg>')


def save(name, svg):
    open(os.path.join(OUT, name + ".svg"), "w").write(svg)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=os.path.join(OUT, name + ".png"))


def rr(x, y, w, h, r, fill, stroke=None, sw=2):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{st}/>'


def pill(text, x, y, size, fill, color, face=MED, padx=22, h=None):
    h = h or size * 1.9
    w = face.width(text, size) + 2 * padx
    return rr(x, y, w, h, h / 2, fill) + T(text, x + padx, y + h / 2 + size * 0.36, size, face, color), w


# ───────────────────────── 1. Tariflar
def s_tariflar():
    b = T("Tariflar", 80, 420, 104, SEMI, FG)
    b += T("Narx faol o‘quvchilar soniga qarab", 80, 486, 36, REG, MUTED)
    plans = [
        ("Start", "100 tagacha o‘quvchi · 3 ustoz", "290 000", "so‘m / oy", "CRM · Davomat · To‘lov · Landing", False),
        ("Standart", "101–300 o‘quvchi · 10 ustoz", "590 000", "so‘m / oy", "+ O‘quvchi kabineti · Telegram · Sayt", True),
        ("Biznes", "301–700 o‘quvchi · 25 ustoz", "990 000", "so‘m / oy", "+ Filiallar hisoboti · Support", False),
        ("Premium", "700+ o‘quvchi · cheksiz ustoz", "1 690 000", "so‘m / oydan", "+ Cheksiz filial · Shaxsiy menejer", False),
    ]
    y = 552
    for name, lim, price, unit, feat, best in plans:
        h = 236
        if best:
            b += rr(80, y, 920, h, 30, "url(#best)", MINT, 3)
        else:
            b += rr(80, y, 920, h, 30, "url(#card)", LINE, 2)
        b += T(name, 124, y + 82, 50, SEMI, FG)
        if best:
            nw = SEMI.width(name, 50)
            pp, _ = pill("TAVSIYA", 124 + nw + 20, y + 40, 22, MINT, INK, SEMI, 16, 46)
            b += pp
        b += T(lim, 124, y + 134, 30, REG, MUTED)
        b += T(price, 956, y + 90, 62, SEMI, MINT if best else FG, "end")
        b += T(unit, 956, y + 134, 28, REG, MUTED, "end")
        b += f'<line x1="124" y1="{y+164}" x2="956" y2="{y+164}" stroke="{LINE}" stroke-width="2"/>'
        b += T(feat, 124, y + 208, 30, MED, FG)
        y += h + 22
    b += T("✓".replace("✓", ""), 0, 0, 1)
    note = "7 kun bepul sinov  ·  To‘lov 2 oy oldindan  ·  Yillik to‘lovda 2 oy sovg‘a"
    b += T(note, W / 2, y + 40, 26, MED, MINT, "middle")
    save("1_Tariflar", frame(b, "Narxlar"))


# ───────────────────────── 2. Imkoniyat
def s_imkoniyat():
    b = T("Bitta tizimda", 80, 420, 92, SEMI, FG)
    b += T("hammasi", 80, 520, 92, SEMI, "url(#gh)")
    items = [("users", "Lidlar (CRM)", "Har bir ariza yoziladi"), ("cap", "Guruhlar", "Daraja, ustoz, xona"),
             ("tick", "Davomat", "Telefondan bir bosishda"), ("wallet", "To‘lov va qarz", "Qarzdor darhol ko‘rinadi"),
             ("cal", "Dars jadvali", "Xonalar to‘qnashmaydi"), ("card", "Ustozlar maoshi", "Avtomatik hisob"),
             ("chart", "Hisobotlar", "Daromad va foyda"), ("lock", "Rollar", "Har kim o‘z bo‘limini")]
    x0, y0, cw, ch, gx, gy = 80, 600, 449, 240, 22, 22
    for i, (icn, t, d) in enumerate(items):
        x = x0 + (i % 2) * (cw + gx); y = y0 + (i // 2) * (ch + gy)
        b += rr(x, y, cw, ch, 28, "url(#card)", LINE, 2)
        b += rr(x + 34, y + 34, 76, 76, 20, "#123A2C") + ic(icn, x + 50, y + 50, 44)
        b += T(t, x + 34, y + 162, 36, SEMI, FG)
        b += T(d, x + 34, y + 206, 27, REG, MUTED)
    b += T("Telefonda ham 100% ishlaydi · 4 tilda", W / 2, y0 + 4 * (ch + gy) + 30, 28, MED, MINT, "middle")
    save("2_Imkoniyat", frame(b, "Imkoniyatlar"))


# ───────────────────────── 3. Filiallar
def s_filiallar():
    b = T("Qaysi filial", 80, 420, 88, SEMI, FG)
    b += T("foydada?", 80, 516, 88, SEMI, "url(#gh)")
    b += T("Har bir filial — aniq raqamlarda", 80, 580, 34, REG, MUTED)
    # KPI tiles
    k = [("O‘quvchilar", "368", FG), ("Tushum", "184 mln", FG), ("Sof foyda", "+39,7 mln", MINT)]
    x = 80
    for lab, val, col in k:
        b += rr(x, 640, 292, 160, 24, "url(#card)", LINE, 2)
        b += T(lab, x + 28, 696, 26, REG, MUTED) + T(val, x + 28, 766, 46, SEMI, col)
        x += 292 + 22
    # branch rows
    rows = [("Chilonzor", "184 o‘quvchi", "+30,5 mln", 1.0, True), ("Yunusobod", "126 o‘quvchi", "+14,8 mln", 14.8 / 30.5, True),
            ("Sergeli", "58 o‘quvchi", "−5,6 mln", 5.6 / 30.5, False)]
    y = 840
    for nm, cnt, pr, frac, ok in rows:
        h = 210
        b += rr(80, y, 920, h, 28, "#1A1414" if not ok else "url(#card)", "#5A2A24" if not ok else LINE, 2)
        b += T(nm, 120, y + 70, 42, SEMI, FG) + T(cnt, 120, y + 116, 28, REG, MUTED)
        b += T(pr, 960, y + 74, 44, SEMI, GOOD if ok else BAD, "end")
        tag, tw = pill("Foydada" if ok else "Zararda", 0, 0, 22, "#123A2C" if ok else "#3A1D1A", GOOD if ok else BAD, MED, 16, 44)
        b += f'<g transform="translate({960 - tw} {y + 94})">{tag}</g>'
        b += rr(120, y + 160, 800, 16, 8, "#163328")
        b += rr(120, y + 160, max(800 * frac, 40), 16, 8, "url(#gh)" if ok else BAD)
        y += h + 22
    b += T("Namuna ma’lumotlar", W / 2, y + 36, 26, REG, MUTED, "middle")
    save("3_Filiallar", frame(b, "Filiallar hisoboti"))


# ───────────────────────── 4. Sayt
def s_sayt():
    b = T("Markazingizga", 80, 420, 86, SEMI, FG)
    b += T("chiroyli sayt", 80, 514, 86, SEMI, "url(#gh)")
    b += T("Nomingiz, logongiz va domeningiz bilan", 80, 578, 34, REG, MUTED)
    # browser mockup
    x, y, w = 80, 640, 920
    b += rr(x, y, w, 720, 30, "#F7FAF8") + f'<rect x="{x}" y="{y}" width="{w}" height="70" rx="30" fill="#E3ECE7"/><rect x="{x}" y="{y+40}" width="{w}" height="30" fill="#E3ECE7"/>'
    for i, c in enumerate([MINT, "#C3D3CB", "#C3D3CB"]):
        b += f'<circle cx="{x+40+i*30}" cy="{y+35}" r="9" fill="{c}"/>'
    b += rr(x + 150, y + 15, 640, 40, 20, "#F7FAF8") + ic("lock", x + 168, y + 23, 22, "#6B8478", 2) + T("markazingiz.uz", x + 200, y + 44, 24, MED, "#4A6357")
    # nav
    b += rr(x + 40, y + 100, 46, 46, 12, "#0A1F17") + T("[Markaz nomi]", x + 102, y + 134, 28, SEMI, "#0A1F17")
    b += rr(x + 650, y + 98, 230, 52, 26, "#0A1F17") + T("Ariza qoldirish", x + 765, y + 132, 24, MED, FG, "middle")
    # hero band
    b += rr(x + 40, y + 180, w - 80, 330, 26, "#0A1F17")
    pp, _ = pill("Yangi guruhlar ochildi", x + 76, y + 216, 22, "#123A2C", MINT, MED, 16, 44)
    b += pp
    hero, last = P("Chet tilini birinchi darsdan gapirib o‘rganing", x + 76, y + 300, 38, 500, SEMI, FG, 1.18)
    b += hero
    b += rr(x + 76, y + 428, 330, 58, 29, "url(#gh)") + T("Bepul darsga yozilish", x + 241, y + 466, 25, SEMI, INK, "middle")
    b += f'<circle cx="{x+740}" cy="{y+345}" r="120" fill="#123A2C"/>' + ic("cap", x + 660, y + 265, 160)
    # chips
    cx = x + 40
    for icn, t in [("globe", "Ingliz tili"), ("book", "Arab tili"), ("chart", "IELTS")]:
        cw = 260
        b += rr(cx, y + 540, cw, 130, 22, "#EAF2EE") + ic(icn, cx + 28, y + 568, 40, "#0F9A63", 2) + T(t, cx + 28, y + 645, 28, SEMI, "#0A1F17")
        cx += cw + 20
    # bullets
    yy = y + 790
    for t in ["Saytdagi ariza darhol tizimga tushadi", "Telefonda ham chiroyli ko‘rinadi", "Reklama uchun alohida landing page"]:
        b += ic("check", 80, yy - 32, 40, MINT, 2.6) + T(t, 140, yy, 34, MED, FG)
        yy += 66
    save("4_Sayt", frame(b, "Veb-sayt"))


# ───────────────────────── 5. Kabinet
def s_kabinet():
    b = T("O‘quvchi kabineti", 80, 420, 80, SEMI, FG)
    b += T("Ota-ona hammasini telefonidan ko‘radi", 80, 484, 34, REG, MUTED)
    # phone
    px, py, pw, ph = 250, 560, 580, 1000
    b += rr(px - 14, py - 14, pw + 28, ph + 28, 86, "#020806") + rr(px, py, pw, ph, 74, SURF)
    b += rr(px + pw / 2 - 90, py + 26, 180, 36, 18, "#020806")
    b += f'<circle cx="{px+70}" cy="{py+130}" r="38" fill="url(#g)"/>' + T("A", px + 70, py + 146, 38, SEMI, INK, "middle")
    b += T("Xush kelibsiz", px + 128, py + 118, 24, REG, MUTED) + T("Aziza Sobirova", px + 128, py + 156, 32, SEMI, FG)
    cards = [("cal", "Bugungi dars", "18:00 · 3-xona", False), ("book", "Uyga vazifa", "Unit 5 · 2 ta mashq", False),
             ("tick", "Keyingi to‘lov · 20-noyabr", "To‘langan", True)]
    cy = py + 210
    for icn, s1, s2, paid in cards:
        b += rr(px + 32, cy, pw - 64, 140, 30, "url(#gh)" if paid else SURF2)
        b += ic(icn, px + 66, cy + 46, 48, INK if paid else "url(#g)", 2)
        b += T(s1, px + 140, cy + 60, 24, REG, "#0B3A26" if paid else MUTED) + T(s2, px + 140, cy + 104, 32, SEMI, INK if paid else FG)
        cy += 158
    b += rr(px + 32, cy, pw - 64, 150, 30, SURF2)
    b += T("Shu oy davomati", px + 66, cy + 58, 26, REG, MUTED) + T("92%", px + pw - 66, cy + 60, 34, SEMI, FG, "end")
    b += rr(px + 66, cy + 92, pw - 132, 16, 8, LINE) + rr(px + 66, cy + 92, (pw - 132) * .92, 16, 8, MINT)
    cy += 172
    b += ic("send", px + 66, cy + 4, 30, TEAL, 2) + T("Eslatmalar Telegram orqali keladi", px + 110, cy + 30, 24, MED, MUTED)
    save("5_Kabinet", frame(b, "O‘quvchi kabineti"))


# ───────────────────────── 6. Bepul sinov
def s_sinov():
    b = T("7 kun", W / 2, 520, 220, SEMI, "url(#gh)", "middle")
    b += T("bepul sinab ko‘ring", W / 2, 616, 64, SEMI, FG, "middle")
    b += T("Yoqsa — keyin to‘laysiz", W / 2, 680, 36, REG, MUTED, "middle")
    steps = [("Tanishuv", "Markazingizga kelib, tizimni ko‘rsatamiz"),
             ("7 kun sinov", "Ma’lumotlaringizni o‘zimiz yuklaymiz"),
             ("Tarif tanlash", "Yoqsa, 2 oylik to‘lov qilasiz"),
             ("Ishga tushirish", "Sayt, bot va kabinetni ulaymiz")]
    y = 750
    for i, (t, d) in enumerate(steps):
        b += rr(80, y, 920, 150, 28, "url(#card)", LINE, 2)
        b += f'<circle cx="160" cy="{y+75}" r="40" fill="none" stroke="{MINT}" stroke-width="3"/>' + T(str(i + 1), 160, y + 90, 40, SEMI, MINT, "middle")
        b += T(t, 236, y + 66, 38, SEMI, FG) + T(d, 236, y + 112, 28, REG, MUTED)
        y += 168
    # place for the Instagram link sticker
    b += rr(190, y + 30, 700, 150, 75, "none", MINT, 3).replace('fill="none"', 'fill="#0E2B20"').replace('stroke-width="3"', 'stroke-width="3" stroke-dasharray="14 12"')
    b += ic("arrow", W / 2 - 22, y + 46, 44, MINT, 2.6)
    b += T("Bosing va ariza qoldiring", W / 2, y + 140, 32, SEMI, FG, "middle")
    save("6_Bepul_sinov", frame(b, "Bepul sinov"))


# ───────────────────────── 7. Aloqa
def s_aloqa():
    b = T("Bog‘laning", 80, 430, 104, SEMI, FG)
    b += T("Markazingizga kelib, tizimni", 80, 500, 36, REG, MUTED)
    b += T("jonli ko‘rsatamiz", 80, 548, 36, REG, MUTED)
    rows = [("call", "Telefon", "+998 50 999 97 33"), ("send", "Telegram", "@abdulloh_mrktlg"),
            ("insta", "Instagram", "@markazly_uz"), ("globe", "Sayt", "markazly.uz")]
    y = 640
    for icn, lab, val in rows:
        b += rr(80, y, 920, 190, 34, "url(#card)", LINE, 2)
        b += rr(124, y + 45, 100, 100, 28, "#123A2C") + ic(icn, 146, y + 67, 56)
        b += T(lab, 262, y + 82, 28, REG, MUTED) + T(val, 262, y + 136, 46, SEMI, FG)
        y += 212
    b += rr(80, y + 20, 920, 120, 60, "url(#gh)")
    b += T("7 kun bepul sinov — hoziroq yozing", W / 2, y + 94, 34, SEMI, INK, "middle")
    save("7_Aloqa", frame(b, "Aloqa"))


for f in (s_tariflar, s_imkoniyat, s_filiallar, s_sayt, s_kabinet, s_sinov, s_aloqa):
    f()

# contact sheet
from PIL import Image
names = ["1_Tariflar", "2_Imkoniyat", "3_Filiallar", "4_Sayt", "5_Kabinet", "6_Bepul_sinov", "7_Aloqa"]
tw, th = 360, 640
sheet = Image.new("RGB", (20 + len(names) * (tw + 20), th + 40), (237, 244, 240))
for i, n in enumerate(names):
    im = Image.open(os.path.join(OUT, n + ".png")).convert("RGB").resize((tw, th), Image.LANCZOS)
    sheet.paste(im, (20 + i * (tw + 20), 20))
sheet.save(os.path.join(D, "markazly", "storislar_korinishi.png"))
print("ok")
