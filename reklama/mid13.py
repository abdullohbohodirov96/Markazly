sys.path.insert(0, os.path.dirname(OUTDIR))
from arabic import TA, AR
def ar(t, x, y, s, col=FG, anchor="middle"): return TA(t, x, y, s, AR, col, anchor)
T_B, T_C, T_D, T_E, T_F, T_G = at("Ota-ona qaysi"), at("Markazly bilan"), at("Saytdan"), at("Ota-ona esa"), at("Raqobatchilar"), at("Hoziroq")
# ── A. hook: centres pop up everywhere
add(T("Har mahallada —", CX, 440, 72, SEMI, FG, "middle") + T("arab tili markazi", CX, 540, 80, SEMI, "url(#gh)", "middle"), -1, T_B, dy=0, dur=.01)
import random as _r
_r.seed(4)
spots = [(x, y) for y in range(640, 1260, 150) for x in range(150, 1000, 190)]
_r.shuffle(spots)
for k, (x, y) in enumerate(spots[:18]):
    x += _r.randint(-20, 20); y += _r.randint(-20, 20)
    add(f'<g transform="translate({x} {y})"><path d="M-46 30 V-10 L0 -44 L46 -10 V30 Z" fill="{SURF2}" stroke="{MINT if k % 5 == 0 else LINE}" stroke-width="3"/><rect x="-12" y="4" width="24" height="26" fill="#0D2620"/></g>'
        + (ar("مركز", x, y + 76, 26, MUTED) if k % 3 == 0 else ""), -0.6 + k * .14, T_B, pop=True, dur=.15)
# ── B. parent chooses the modern one
add(T("Ota-ona qaysi birini tanlaydi?", CX, 440, 56, SEMI, FG, "middle"), T_B, T_C)
old = rr(100, 520, 420, 520, 36, "#1A1F1D", "#3A4A43", 3) + rr(160, 600, 300, 230, 12, "#F6C76B") + "".join(f'<line x1="180" y1="{640 + i*36}" x2="440" y2="{640 + i*36}" stroke="#8A6A2A" stroke-width="3"/>' for i in range(5)) + T("Daftar", 310, 910, 44, SEMI, MUTED, "middle") + T("eski usul", 310, 970, 30, MED, MUTED, "middle")
new = rr(560, 520, 420, 520, 36, "#123A2C", MINT, 4) + rr(680, 580, 180, 300, 30, "#020806") + rr(692, 592, 156, 276, 22, SURF) + f'<image href="{MARK}" x="{770-45*342/377/2:.0f}" y="650" width="{45*342/377:.0f}" height="45"/>' + "".join(rr(708, 720 + i * 40, 124, 24, 8, MINT if i == 0 else LINE) for i in range(3)) + T("Zamonaviy", 770, 950, 44, SEMI, FG, "middle") + T("sayt + tizim", 770, 1005, 30, MED, MINT, "middle")
add(old, T_B + .2, T_C, pop=True); add(new, T_B + .5, T_C, pop=True)
add(f'<circle cx="940" cy="540" r="50" fill="{MINT}"/>' + ic("check", 918, 518, 44, INK, 3.4), at("zamonaviy va"), T_C, pop=True)
add(f'<path d="M140 560 L480 1000 M480 560 L140 1000" stroke="{BAD}" stroke-width="10" stroke-linecap="round" stroke-opacity=".8"/>', at("zamonaviy va") + .3, T_C, dy=0, dur=.2)
# ── C. bilingual site
add(T("O‘z saytingiz — 2 tilda", CX, 420, 64, SEMI, FG, "middle"), T_C, T_D)
x, y, w = 110, 470, 860
s_ = rr(x, y, w, 620, 30, "#071510", LINE, 2) + f'<path d="M{x} {y+30} Q{x} {y} {x+30} {y} H{x+w-30} Q{x+w} {y} {x+w} {y+30} V{y+62} H{x} Z" fill="#0B1D16"/>'
s_ += "".join(f'<circle cx="{x+34+j*26}" cy="{y+31}" r="8" fill="{c}"/>' for j, c in enumerate([MINT, LINE, LINE]))
s_ += rr(x + 130, y + 13, 560, 38, 19, "#06120D", LINE, 2) + ic("lock", x + 148, y + 21, 20, MUTED, 2) + T("alnoor.uz", x + 178, y + 40, 22, MED, FG)
s_ += rr(x + 640, y + 90, 190, 54, 27, MINT) + T("UZ", x + 690, y + 126, 26, SEMI, INK, "middle") + ar("عربي", x + 780, y + 128, 28, INK)
s_ += T("Al-Noor Academy", x + 40, y + 126, 32, SEMI, FG)
s_ += ar("تعلّم العربية", x + w - 40, y + 270, 78, "url(#gh)", "right") + T("Arab tilini birinchi darsdan", x + 40, y + 360, 42, SEMI, FG) + T("o‘rganing", x + 40, y + 414, 42, SEMI, FG)
s_ += rr(x + 40, y + 460, 330, 70, 35, "url(#gh)") + T("Bepul darsga yozilish", x + 205, y + 505, 26, SEMI, INK, "middle")
s_ += rr(x + 600, y + 300, 220, 230, 28, "#12281F", LINE, 2) + ic("book", x + 640, y + 340, 140, MINT, 1.5)
add(s_, T_C + .1, T_D, dy=60, dur=.4)
add(rr(640, 1120, 330, 90, 45, "#123A2C", MINT, 2) + ic("phone", 670, 1142, 46, MINT, 2) + T("0,8 soniya", 840, 1180, 34, SEMI, MINT, "middle"), at("telefonda tez"), T_D, pop=True)
# ── D. lead lands in the system
add(T("Ariza — darhol tizimda", CX, 420, 64, SEMI, FG, "middle"), T_D, T_E)
crm = rr(110, 600, 860, 520, 36, SURF, LINE, 2) + T("Arizalar", 150, 670, 36, SEMI, FG)
for j, (nm, g) in enumerate([("Dilshod · Arab tili A1", "kecha"), ("Mohira · Arab tili Kids", "kecha"), ("Bekzod · Arab tili B1", "2 kun")]):
    yy = 830 + j * 92
    crm += rr(140, yy, 800, 76, 16, "#11302A") + T(nm, 170, yy + 49, 30, MED, FG) + T(g, 910, yy + 49, 24, REG, MUTED, "end")
add(crm, T_D + .1, T_E, dy=40)
add(rr(140, 710, 800, 100, 22, FG) + rr(160, 728, 64, 64, 18, MINT) + ic("users", 172, 740, 40, INK, 2.4) + T("Yangi ariza: Ali · Arab tili A2", 246, 758, 30, SEMI, INK) + T("saytdan · hozir", 246, 794, 24, REG, "#3F5A4D"), at("Saytdan") + .8, T_E, pop=True)
add(T("Birorta mijoz yo‘qolmaydi", CX, 1200, 40, SEMI, MINT, "middle"), at("birorta mijoz"), T_E)
# ── E. parent trust
add(T("Ota-onaga ishonch", CX, 420, 66, SEMI, FG, "middle"), T_E, T_F)
add(rr(110, 500, 860, 560, 40, FG) + T("Farzandingiz: Ali", 160, 580, 36, SEMI, INK) + T("Arab tili · A2", 160, 626, 28, MED, "#3F5A4D")
    + rr(160, 670, 360, 160, 24, "#E6F4EE") + T("Davomat", 190, 720, 28, MED, "#3F5A4D") + T("96%", 190, 800, 66, SEMI, "#0A7A50")
    + rr(560, 670, 360, 160, 24, "#E6F4EE") + T("Lug‘at", 590, 720, 28, MED, "#3F5A4D") + T("120 so‘z", 590, 800, 60, SEMI, "#0A7A50")
    + rr(160, 860, 760, 150, 24, "#FFF7E6") + T("Ustoz izohi:", 190, 910, 26, MED, "#8A6A2A") + T("Talaffuzi yaxshilandi, barakalla!", 190, 965, 32, SEMI, "#5A4416"), T_E + .2, T_F, pop=True)
# ── F. you vs competitors
add(T("Siz va raqobatchilar", CX, 420, 66, SEMI, FG, "middle"), T_F, T_G)
add(rr(110, 500, 860, 230, 40, "#2A1D1B", "#5A2A24", 3) + T("Raqobatchilar", 160, 590, 38, SEMI, "#F3D6D0") + T("daftar va Excel", 160, 670, 52, SEMI, BAD), T_F + .1, T_G, pop=True)
add(rr(110, 760, 860, 230, 40, "#123A2C", MINT, 4) + T("Siz", 160, 850, 38, SEMI, FG) + T("Markazly tizimi", 160, 930, 56, SEMI, MINT) + f'<circle cx="880" cy="875" r="50" fill="{MINT}"/>' + ic("check", 858, 853, 44, INK, 3.4), at("siz tizim"), T_G, pop=True)
# ── G. CTA
add('<circle cx="540" cy="760" r="480" fill="url(#halo)"/>', T_G, DUR + 1, dy=0, dur=.8)
add(T("Hoziroq", CX, 520, 76, SEMI, FG, "middle") + T("pastdagi tugmani", CX, 610, 76, SEMI, FG, "middle") + T("bosing", CX, 700, 76, SEMI, "url(#gh)", "middle"), T_G, DUR + 1)
add(rr(110, 790, 860, 210, 105, "url(#gh)") + T("7 kun bepul", CX, 892, 84, SEMI, INK, "middle") + T("sinab ko‘ring", CX, 960, 46, MED, "#0A3D27", "middle"), at("7 kun bepul"), DUR + 1, pop=True)
add(T("markazly.onrender.com", CX, 1090, 38, MED, MUTED, "middle"), at("7 kun bepul") + .5, DUR + 1)
arrow = f'<g transform="translate({CX-60} 1170)"><circle cx="60" cy="60" r="60" fill="#2EE59D" fill-opacity=".18"/><path d="M60 28 V92 M32 66 L60 94 L88 66" fill="none" stroke="#2EE59D" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></g>'
add(arrow, T_G + .6, DUR + 1, bob=14)
S_B, S_F = T_B, T_G
