sys.path.insert(0, os.path.dirname(OUTDIR))
from arabic import TA, AR, AR6
def ar(t, x, y, s, col=FG, anchor="middle", face=None): return TA(t, x, y, s, face or AR, col, anchor)
T_B, T_C, T_D, T_E = at("ماركازلي نظامٌ"), at("موقعٌ"), at("النظام يعمل"), at("اضغط")
# ── A. hook
add('<circle cx="540" cy="760" r="540" fill="url(#rd)"/>', -1, T_B, dy=0, dur=.01)
add(ar("هل تعرف حقاً", CX, 520, 96) + ar("ما يحدث في مركزك؟", CX, 650, 96, "url(#gh)"), -1, T_B, dy=0, dur=.01)
for i, (t, key) in enumerate([("من دفع الرسوم؟", "من دفع"), ("من تأخّر؟", "ومن تأخّر"), ("من غاب عن الدرس؟", "ومن غاب")]):
    y = 760 + i * 160
    add(rr(140, y, 800, 130, 34, "#2A1D1B", "#5A2A24", 3) + f'<circle cx="868" cy="{y+65}" r="38" fill="{BAD}"/>' + T("?", 868, y + 86, 54, SEMI, "#2A0E0A", "middle") + ar(t, 800, y + 86, 52, "#F3D6D0", "right"), at(key), T_B, pop=True)
# ── B. one system: panel, attendance, payments, branches
add('<circle cx="540" cy="430" r="300" fill="url(#halo)"/>', T_B, T_C, dy=0, dur=.5)
mh = 170; mw = mh * 342 / 377
add(f'<image href="{MARK}" x="{CX - mw/2 + 3:.0f}" y="300" width="{mw:.0f}" height="{mh}"/>', T_B, T_C, pop=True)
add(ar("نظامٌ واحد لكلّ شيء", CX, 560, 66, "url(#gh)"), T_B + .3, T_C)
dx, dw = 110, 860
k = rr(dx, 610, dw, 170, 30, SURF, LINE, 2); kw = (dw - 60) / 3
for j, (lab, val, col) in enumerate([("الطلاب", "368", FG), ("الإيرادات", "184M", FG), ("المتأخّرون", "12", BAD)]):
    kx = dx + dw - 20 - (j + 1) * kw - j * 10
    k += rr(kx, 630, kw, 130, 20, SURF2) + ar(lab, kx + kw - 22, 680, 30, MUTED, "right") + T(val, kx + kw - 22, 745, 48, SEMI, col, "end")
add(k, at("الحضور"), T_C, dy=40)
att = rr(dx, 800, dw, 300, 30, SURF, LINE, 2) + ar("الحضور · مجموعة A1", dx + dw - 30, 860, 34, FG, "right")
nm = ["أحمد", "فاطمة", "يوسف", "مريم"]
for j, n_ in enumerate(nm): att += ar(n_, dx + dw - 30, 920 + j * 50, 32, FG, "right")
add(att, at("الحضور") + .2, T_C, dy=40)
for j in range(4):
    ok = j != 2
    add(rr(dx + 30, 892 + j * 50, 170, 40, 20, "#123A2C" if ok else "#3A1D1A") + ar("حاضر" if ok else "غائب", dx + 115, 922 + j * 50, 28, GOOD if ok else BAD), at("الحضور") + .5 + j * .15, T_C, pop=True, dur=.15)
add(rr(dx, 1120, dw, 110, 30, "#3A1D1A", BAD, 2) + ar("متأخّرون عن الدفع: ١٢ طالباً", dx + dw - 30, 1190, 38, BAD, "right"), at("والمدفوعات"), T_C, pop=True)
br = rr(dx, 1250, dw, 0, 0, "none")
for j, (n_, pct, col) in enumerate([("فرع ١", .85, GOOD), ("فرع ٢", .35, BAD)]):
    y = 1250 + j * 0
add(rr(dx, 1250, 420, 110, 26, SURF, LINE, 2) + ar("فرع ١ · ربح", dx + 390, 1300, 30, GOOD, "right") + rr(dx + 30, 1320, 360, 18, 9, GOOD), at("وتقارير"), T_C, pop=True)
add(rr(dx + 440, 1250, 420, 110, 26, SURF, LINE, 2) + ar("فرع ٢ · خسارة", dx + 830, 1300, 30, BAD, "right") + rr(dx + 470, 1320, 140, 18, 9, BAD), at("وتقارير") + .3, T_C, pop=True)
# ── C. website + student account + points
x, y, w = 110, 330, 860
s_ = rr(x, y, w, 470, 30, "#071510", LINE, 2) + f'<path d="M{x} {y+30} Q{x} {y} {x+30} {y} H{x+w-30} Q{x+w} {y} {x+w} {y+30} V{y+62} H{x} Z" fill="#0B1D16"/>'
s_ += "".join(f'<circle cx="{x+w-34-j*26}" cy="{y+31}" r="8" fill="{c}"/>' for j, c in enumerate([MINT, LINE, LINE]))
s_ += rr(x + 130, y + 13, 600, 38, 19, "#06120D", LINE, 2) + T("alnoor-academy.uz", x + 430, y + 40, 22, MED, FG, "middle")
s_ += ar("أكاديمية النور", x + w - 40, y + 130, 40, FG, "right") + ar("تعلّم العربية", x + w - 40, y + 240, 70, "url(#gh)", "right") + ar("من الدرس الأوّل", x + w - 40, y + 320, 52, FG, "right")
s_ += rr(x + w - 360, y + 360, 320, 70, 35, "url(#gh)") + ar("سجّل الآن", x + w - 200, y + 406, 34, INK)
s_ += rr(x + 40, y + 120, 260, 300, 26, "#12281F", LINE, 2) + ic("book", x + 100, y + 200, 140, MINT, 1.5)
add(s_, T_C, T_D, dy=60)
add(rr(110, 830, 420, 380, 30, "url(#best)", MINT, 2) + ar("بطاقة الكلمات", 500, 890, 30, MUTED, "right") + ar("كِتَاب", 320, 1040, 110, FG) + T("kitob", 320, 1110, 40, MED, MUTED, "middle"), at("وحسابٌ"), T_D, pop=True)
lb = rr(550, 830, 420, 380, 30, SURF, LINE, 2) + ar("الترتيب", 940, 890, 30, MUTED, "right")
for j, (n_, p) in enumerate([("أحمد", "1248"), ("فاطمة", "1190"), ("يوسف", "1052")]):
    yy = 920 + j * 90
    lb += rr(570, yy, 380, 74, 16, "#2A2412" if j == 0 else "#11302A") + ar(n_, 930, yy + 50, 34, FG, "right") + T(p, 600, yy + 50, 32, SEMI, AMB if j == 0 else MUTED)
add(lb, at("مع نقاطٍ"), T_D, dy=40)
add(rr(330, 1240, 420, 90, 45, "#2A2412", AMB, 2) + ar("+١٠ نقاط", CX, 1300, 44, AMB), at("مع نقاطٍ") + .6, T_D, pop=True)
# ── D. 4 languages, migration, training
add(ar("يعمل بأربع لغات", CX, 440, 76, FG), T_D, T_E)
for j, lg in enumerate(["العربية", "الأوزبكية", "الروسية", "الإنجليزية"]):
    xx = 110 + (j % 2) * 440; yy = 500 + (j // 2) * 130
    add(rr(xx, yy, 420, 110, 30, "#123A2C" if j == 0 else SURF, MINT if j == 0 else LINE, 2) + ic("globe", xx + 330, yy + 31, 48, MINT, 2) + ar(lg, xx + 300, yy + 72, 42, FG, "right"), at("النظام يعمل") + .3 + j * .2, T_E, pop=True, dur=.2)
for j, (t, tt) in enumerate([("ننقل بياناتك بأنفسنا", "وننقل"), ("وندرّب موظفيك مجاناً", "وننقل")]):
    yy = 820 + j * 130
    add(rr(110, yy, 860, 110, 30, "#123A2C", MINT, 2) + f'<circle cx="900" cy="{yy+55}" r="34" fill="{MINT}"/>' + ic("check", 882, yy + 37, 36, INK, 3) + ar(t, 840, yy + 72, 42, FG, "right"), at(tt) + j * 1.3, T_E, dy=30)
# ── E. CTA
add('<circle cx="540" cy="760" r="480" fill="url(#halo)"/>', T_E, DUR + 1, dy=0, dur=.8)
add(ar("اضغط الزرّ", CX, 530, 90) + ar("في الأسفل الآن", CX, 650, 90, "url(#gh)"), T_E, DUR + 1)
add(rr(110, 740, 860, 220, 110, "url(#gh)") + ar("جرّب ٧ أيام مجاناً", CX, 870, 74, INK), at("وجرّب"), DUR + 1, pop=True)
add(T("markazly.onrender.com", CX, 1040, 38, MED, MUTED, "middle"), at("وجرّب") + .6, DUR + 1)
arrow = f'<g transform="translate({CX-60} 1120)"><circle cx="60" cy="60" r="60" fill="#2EE59D" fill-opacity=".18"/><path d="M60 28 V92 M32 66 L60 94 L88 66" fill="none" stroke="#2EE59D" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></g>'
add(arrow, T_E + .6, DUR + 1, bob=14)
S_B, S_F = T_B, T_E
