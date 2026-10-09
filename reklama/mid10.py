T_B, T_C, T_D, T_E, T_F, T_G = at("Keling"), at("Birinchi"), at("Ikkinchi"), at("Uchinchi"), at("Va eng muhimi"), at("Hoziroq")
# ── A. hook: the two fears
add(T("Yangi tizimga", CX, 440, 84, SEMI, FG, "middle") + T("o‘tishdan qo‘rqasizmi?", CX, 540, 84, SEMI, BAD, "middle"), -1, T_C, dy=0, dur=.01)
fears = [("Ma’lumotlarim yo‘qolib", "qolmaydimi?", at("«Ma’lumotlarim"), 640, 110), ("Xodimlarim o‘rgana", "oladimi?", at("xodimlarim o‘rgana"), 860, 260)]
for l1, l2, tt, y, x in fears:
    add(rr(x, y, 720, 180, 40, "#2A1D1B", "#5A2A24", 3) + f'<path d="M{x+60} {y+178} l20 40 l30 -40 Z" fill="#2A1D1B"/>' + T(l1, x + 40, y + 76, 44, SEMI, "#F3D6D0") + T(l2, x + 40, y + 136, 44, SEMI, "#F3D6D0"), -1 if tt < .5 else tt, T_C, pop=True)
for l1, l2, tt, y, x in fears:
    add(f'<circle cx="{x+700}" cy="{y+20}" r="44" fill="{MINT}"/>' + ic("check", x + 680, y, 40, INK, 3.2), T_B + .6 + (y - 640) / 900, T_C, pop=True)
add(T("Hammasiga javob:", CX, 1230, 56, SEMI, MINT, "middle"), T_B + .2, T_C)
def step(n, title, sub, t0, t1):
    add(rr(CX - 60, 380, 120, 120, 60, "url(#gh)") + T(str(n), CX, 470, 76, SEMI, INK, "middle"), t0, t1, pop=True)
    add(T(title, CX, 610, 72, SEMI, FG, "middle"), t0 + .2, t1)
    add(T(sub, CX, 680, 38, MED, MUTED, "middle"), t0 + .4, t1)
# ── C. migration
step(1, "O‘zimiz ko‘chiramiz", "Excel, daftar — qaysi bo‘lsa ham", T_C, T_D)
xl = rr(150, 790, 220, 270, 24, "#F2F4F3") + rr(150, 790, 220, 60, 24, "#1D6F42") + T("X", 260, 836, 40, SEMI, "#fff", "middle") + "".join(rr(175, 880 + i * 40, 170, 18, 6, "#C9D3CE") for i in range(4))
nb = rr(420, 790, 220, 270, 24, "#F6C76B") + "".join(f'<line x1="440" y1="{860 + i*36}" x2="620" y2="{860 + i*36}" stroke="#8A6A2A" stroke-width="3"/>' for i in range(5)) + rr(420, 790, 30, 270, 12, "#E8873D")
add(xl, at("Excel'dami"), T_D, pop=True); add(nb, at("Excel'dami") + .5, T_D, pop=True)
def flow(fr, t):
    from PIL import ImageDraw
    k = (t - at("o‘zimiz tizimga")) * 1.6; dr = ImageDraw.Draw(fr)
    for j in range(5):
        p = (k + j * .2) % 1
        x = 650 + p * 160; y = 925
        dr.ellipse((x - 9, y - 9, x + 9, y + 9), fill=(46, 229, 157, int(255 * (1 - abs(p - .5) * 2))))
dyn(flow, at("o‘zimiz tizimga"), T_D)
db = f'<image href="{MARK}" x="840" y="840" width="{150*342/377:.0f}" height="150"/>'
add(rr(810, 790, 220, 270, 24, SURF, MINT, 3) + db + T("Markazly", 920, 1030, 28, SEMI, FG, "middle"), at("o‘zimiz tizimga"), T_D, pop=True)
# ── D. separate databases
step(2, "Har bir markaz — alohida", "Ma’lumotlaringizni faqat siz ko‘rasiz", T_D, T_E)
for i, (nm, mine) in enumerate([("A markaz", False), ("Sizning markaz", True), ("B markaz", False)]):
    x = 100 + i * 300
    add(rr(x, 800, 280, 300, 30, "#123A2C" if mine else SURF, MINT if mine else LINE, 4 if mine else 2) + ic("lock", x + 100, 850, 80, MINT if mine else MUTED, 2.2)
        + T(nm.split()[0], x + 140, 1000, 32, SEMI, FG if mine else MUTED, "middle") + T(" ".join(nm.split()[1:]), x + 140, 1042, 28, MED, FG if mine else MUTED, "middle"), at("har bir markazning") + i * .25, T_E, pop=True)
add(rr(250, 1130, 580, 70, 35, "#123A2C", MINT, 2) + T("Boshqa hech kim ko‘rmaydi", CX, 1177, 34, SEMI, MINT, "middle"), at("ma’lumotlaringizni sizdan"), T_E, pop=True)
# ── E. training
step(3, "O‘zimiz o‘qitamiz", "Markazingizga borib, xodimlaringizga", T_E, T_F)
board = rr(240, 790, 600, 330, 26, "#F4F8F6") + rr(270, 820, 540, 230, 14, SURF) + f'<image href="{MARK}" x="300" y="850" width="{90*342/377:.0f}" height="90"/>' + "".join(rr(410, 860 + i * 40, 360 - i * 80, 20, 8, MINT if i == 0 else LINE) for i in range(3))
add(board, at("markazingizga o‘zimiz"), T_F, pop=True)
for i in range(3):
    x = 330 + i * 210
    add(f'<circle cx="{x}" cy="1180" r="38" fill="{SURF2}"/><path d="M{x-60} 1290 Q{x} 1200 {x+60} 1290 Z" fill="{SURF2}"/>', at("xodimlaringizni") + i * .15, T_F, pop=True)
# ── F. guarantee
add(T("Va eng muhimi", CX, 440, 60, SEMI, MUTED, "middle"), T_F, T_G)
add(T("7", 300, 800, 330, SEMI, "url(#gh)", "middle") + T("kun bepul", 300, 880, 48, SEMI, FG, "middle"), at("avval 7 kun"), T_G, pop=True)
add(rr(520, 560, 460, 180, 36, "#123A2C", MINT, 3) + T("Yoqmasa —", 560, 630, 40, SEMI, FG) + T("0 so‘m", 560, 712, 72, SEMI, MINT), at("yoqmasa"), T_G, pop=True)
add(rr(520, 770, 460, 120, 36, SURF, LINE, 2) + T("Hech qanday shart yo‘q", 560, 845, 32, MED, FG), at("hech narsa"), T_G, pop=True)
# ── G. CTA
add('<circle cx="540" cy="760" r="480" fill="url(#halo)"/>', T_G, DUR + 1, dy=0, dur=.8)
add(T("Hoziroq", CX, 520, 76, SEMI, FG, "middle") + T("pastdagi tugmani", CX, 610, 76, SEMI, FG, "middle") + T("bosing", CX, 700, 76, SEMI, "url(#gh)", "middle"), T_G, DUR + 1)
add(rr(110, 790, 860, 210, 105, "url(#gh)") + T("7 kun bepul", CX, 892, 84, SEMI, INK, "middle") + T("sinab ko‘ring", CX, 960, 46, MED, "#0A3D27", "middle"), at("Markazly'ni 7 kun"), DUR + 1, pop=True)
add(T("markazly.onrender.com", CX, 1090, 38, MED, MUTED, "middle"), at("Markazly'ni 7 kun") + .5, DUR + 1)
arrow = f'<g transform="translate({CX-60} 1170)"><circle cx="60" cy="60" r="60" fill="#2EE59D" fill-opacity=".18"/><path d="M60 28 V92 M32 66 L60 94 L88 66" fill="none" stroke="#2EE59D" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></g>'
add(arrow, T_G + .8, DUR + 1, bob=14)
S_B, S_F = T_B, T_G
