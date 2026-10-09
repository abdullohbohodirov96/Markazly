T_B, T_C, T_D, T_E, T_F = at("Markazly'ning oylik"), at("Endi solishtiring"), at("Markazly esa"), at("Ya'ni tizim"), at("Hoziroq")
# ── A. hook: price of one lunch
add('<circle cx="540" cy="700" r="460" fill="url(#halo)"/>', -1, T_B, dy=0, dur=.01)
add(T("KUNIGA", CX, 470, 48, SEMI, MINT, "middle") + T("10 000", CX, 650, 200, SEMI, "url(#gh)", "middle") + T("so‘m", CX, 740, 60, MED, FG, "middle"), -1, T_B, dy=0, dur=.01)
bowl = (f'<g transform="translate({CX} 930)"><ellipse cx="0" cy="40" rx="150" ry="22" fill="#000" fill-opacity=".25"/>'
        f'<path d="M-140 -10 H140 A140 120 0 0 1 -140 -10 Z" fill="#F6C76B"/><path d="M-120 -10 Q0 -90 120 -10 Z" fill="#F4F8F6"/>'
        f'<circle cx="-40" cy="-40" r="12" fill="#E8873D"/><circle cx="20" cy="-48" r="10" fill="#E8873D"/><circle cx="60" cy="-30" r="9" fill="#46D98F"/></g>')
add(bowl, at("bu bitta tushlikdan") - .1, T_B, pop=True)
add(T("= bitta tushlikdan arzon", CX, 1150, 54, SEMI, FG, "middle"), at("bu bitta tushlikdan") + .3, T_B)
# ── B. price breakdown
def pcard(y, top, big, col, sub=""):
    return rr(110, y, 860, 190, 40, SURF, LINE, 2) + T(top, 160, y + 66, 34, MED, MUTED) + T(big, 160, y + 156, 84, SEMI, col) + (T(sub, 930, y + 156, 36, MED, MUTED, "end") if sub else "")
add(pcard(450, "Markazly · Start tarifi", "290 000", FG, "so‘m / oy"), at("Markazly'ning oylik"), T_C, dy=40)
add(T("÷ 30 kun", CX, 730, 60, SEMI, MUTED, "middle"), at("290 ming"), T_C, pop=True)
add(rr(110, 790, 860, 210, 44, "url(#gh)") + T("9 700 so‘m", CX, 905, 100, SEMI, INK, "middle") + T("kuniga", CX, 966, 40, MED, "#0A3D27", "middle"), at("9 700"), T_C, pop=True)
# ── C. compare: tiny daily price vs real losses
add(T("Endi solishtiring", CX, 430, 66, SEMI, FG, "middle"), T_C, T_D)
add(rr(110, 490, 860, 150, 36, "#123A2C", MINT, 3) + T("Markazly", 160, 550, 34, MED, MUTED) + T("9 700 so‘m / kun", 160, 612, 56, SEMI, MINT), T_C + .2, T_D, dy=30)
add(rr(110, 670, 860, 200, 36, "#3A1D1A", BAD, 3) + T("1 ta unutilgan to‘lov", 160, 736, 34, MED, "#F3D6D0") + T("−400 000 so‘m", 160, 830, 80, SEMI, BAD), at("bitta o‘quvchi to‘lovni"), T_D, pop=True, jit=(at("400 ming"), at("400 ming") + .3))
add(rr(110, 900, 860, 200, 36, "#3A1D1A", BAD, 3) + T("1 ta javobsiz ariza", 160, 966, 34, MED, "#F3D6D0") + T("−1 o‘quvchi", 160, 1060, 80, SEMI, BAD), at("Bitta javobsiz"), T_D, pop=True)
# ── D. one place
add(T("Hammasi bitta joyda", CX, 430, 66, SEMI, FG, "middle"), T_D, T_E)
add(rr(90, 480, 900, 620, 44, SURF, MINT, 3), T_D + .1, T_E, dy=40)
for i, (icn, nm, sub, tt) in enumerate([("wallet", "Qarzdorlar", "12 ta · 4,8 mln so‘m", "Markazly esa"), ("users", "Arizalar", "Bugun 5 ta yangi", "arizalarni ham"), ("cal", "Davomat", "212 / 220 darsda", "davomatni ham")]):
    y = 520 + i * 185
    add(rr(130, y, 820, 160, 30, SURF2) + f'<circle cx="220" cy="{y+80}" r="52" fill="#123A2C"/>' + ic(icn, 192, y + 52, 56, MINT, 2) + T(nm, 300, y + 72, 44, SEMI, FG) + T(sub, 300, y + 122, 30, MED, MUTED)
        + f'<circle cx="890" cy="{y+80}" r="28" fill="{MINT}"/>' + ic("check", 874, y + 64, 32, INK, 3), at(tt), T_E, pop=True)
# ── E. pays for itself
add(T("O‘z pulini", CX, 450, 80, SEMI, FG, "middle") + T("1-oydayoq qaytaradi", CX, 550, 80, SEMI, "url(#gh)", "middle"), T_E, T_F)
add(rr(110, 620, 860, 470, 40, SURF, LINE, 2) + T("Foyda", 150, 680, 30, MED, MUTED) + "".join(T(f"{m}-oy", 210 + i * 230, 1060, 28, MED, MUTED, "middle") for i, m in enumerate([1, 2, 3, 4])), T_E + .2, T_F, dy=40)
def growth(fr, t):
    from PIL import ImageDraw
    k = ease((t - T_E - .4) / 1.8)
    pts = [(210, 1000), (440, 900), (670, 790), (900, 680)]
    n = 1 + k * 3; dr = ImageDraw.Draw(fr)
    cur = []
    for i in range(int(n)): cur.append(pts[i])
    if int(n) < 4:
        a, b = pts[int(n) - 1], pts[int(n)]; f = n - int(n); cur.append((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f))
    if len(cur) > 1: dr.line(cur, fill=(46, 229, 157), width=12, joint="curve")
    for p in cur[:-1]: dr.ellipse((p[0] - 14, p[1] - 14, p[0] + 14, p[1] + 14), fill=(46, 229, 157))
    dr.line((150, 1010, 950, 1010), fill=(60, 90, 80), width=3)
dyn(growth, T_E + .3, T_F)
add(rr(620, 700, 300, 70, 35, "#123A2C", MINT, 2) + T("+ foydangiz", 770, 747, 34, SEMI, MINT, "middle"), at("qolgani sizning"), T_F, pop=True)
# ── F. CTA
add('<circle cx="540" cy="760" r="480" fill="url(#halo)"/>', T_F, DUR + 1, dy=0, dur=.8)
add(T("Hoziroq", CX, 520, 76, SEMI, FG, "middle") + T("pastdagi tugmani", CX, 610, 76, SEMI, FG, "middle") + T("bosing", CX, 700, 76, SEMI, "url(#gh)", "middle"), T_F, DUR + 1)
add(rr(110, 790, 860, 210, 105, "url(#gh)") + T("7 kun bepul", CX, 892, 84, SEMI, INK, "middle") + T("yoqmasa — 0 so‘m", CX, 960, 46, MED, "#0A3D27", "middle"), at("Markazly'ni 7 kun"), DUR + 1, pop=True)
add(T("markazly.onrender.com", CX, 1090, 38, MED, MUTED, "middle"), at("yoqmasa"), DUR + 1)
arrow = f'<g transform="translate({CX-60} 1170)"><circle cx="60" cy="60" r="60" fill="#2EE59D" fill-opacity=".18"/><path d="M60 28 V92 M32 66 L60 94 L88 66" fill="none" stroke="#2EE59D" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></g>'
add(arrow, T_F + .8, DUR + 1, bob=14)
S_B, S_F = T_B, T_F
