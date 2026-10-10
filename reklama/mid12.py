sys.path.insert(0, os.path.dirname(OUTDIR))
from arabic import TA, AR
def ar(t, x, y, s, col=FG, anchor="middle"): return TA(t, x, y, s, AR, col, anchor)
T_B, T_C, T_D, T_E, T_F, T_G = at("Arab tilida eng"), at("Markazly'da har bir"), at("O‘quvchi har bir"), at("Siz esa kim"), at("Ota-ona ham"), at("Hoziroq")
# ── A. hook
add(ar("العربية", CX, 640, 260, "#2EE59D").replace('fill="#2EE59D"', 'fill="#2EE59D" fill-opacity=".10"'), -1, T_B, dy=0, dur=.01)
add(T("Arab tili", CX, 560, 120, SEMI, "url(#gh)", "middle") + T("markazingiz bormi?", CX, 690, 92, SEMI, FG, "middle"), -1, T_B, dy=0, dur=.01)
add(rr(240, 800, 600, 100, 50, "#123A2C", MINT, 2) + T("Bu video siz uchun", CX, 866, 44, SEMI, MINT, "middle"), at("Unda bu video"), T_B, pop=True)
# ── B. the problem: words are forgotten
add(T("Eng qiyini —", CX, 440, 70, SEMI, FG, "middle") + T("so‘z yodlash", CX, 540, 84, SEMI, "url(#gh)", "middle"), T_B, T_C)
add(rr(190, 620, 700, 440, 40, "url(#best)", MINT, 3) + ar("كِتَاب", CX, 840, 150) + T("kitob", CX, 940, 48, MED, MUTED, "middle"), at("so‘z yodlash"), at("uyga borib"), pop=True)
add(rr(190, 620, 700, 440, 40, "#1A1F1D", "#5A2A24", 3) + ar("؟ ؟ ؟", CX, 860, 150, "#5A6B63") + T("esdan chiqdi", CX, 960, 48, SEMI, BAD, "middle"), at("uyga borib"), T_C, pop=True)
add(T("Darsda tushundi…", CX, 1150, 46, MED, MUTED, "middle"), at("o‘quvchi darsda"), T_C)
# ── C. cabinet with flashcards
add(T("O‘quvchi kabineti", CX, 420, 72, SEMI, FG, "middle"), T_C, T_D)
px, py, pw, ph = 300, 470, 480, 780
p = rr(px - 12, py - 12, pw + 24, ph + 24, 70, "#020806") + rr(px, py, pw, ph, 58, SURF) + rr(px + pw / 2 - 72, py + 20, 144, 28, 14, "#020806")
p += f'<circle cx="{px+58}" cy="{py+104}" r="30" fill="url(#g)"/>' + T("A", px + 58, py + 117, 30, SEMI, INK, "middle") + T("Arab tili · A1", px + 104, py + 94, 22, REG, MUTED) + T("Aziza Sobirova", px + 104, py + 128, 28, SEMI, FG)
add(p, T_C, T_D, dy=80, dur=.4)
cards = [("كِتَاب", "kitob"), ("قَلَم", "qalam"), ("مَدْرَسَة", "maktab")]
for i, (a, u) in enumerate(cards):
    y = py + 170 + i * 150
    add(rr(px + 22, y, pw - 44, 132, 24, "url(#best)" if i == 0 else SURF2, MINT if i == 0 else None) + ar(a, px + pw - 60, y + 86, 60, FG, "right") + T(u, px + 50, y + 82, 30, MED, MUTED), at("shaxsiy kabineti") + .4 + i * .35, T_D, pop=True, dur=.2)
add(rr(px + 22, py + 640, pw - 44, 110, 24, SURF2) + ic("book", px + 46, py + 672, 44, "url(#g)", 2) + T("Uyga vazifa", px + 106, py + 686, 22, REG, MUTED) + T("92 / 100", px + 106, py + 724, 28, SEMI, GOOD), at("uyga vazifa va baholar"), T_D, pop=True)
# ── D. gamification
add('<circle cx="540" cy="760" r="480" fill="url(#halo)"/>', T_D, T_E, dy=0, dur=.5)
add(T("Har bir so‘z — ball", CX, 420, 72, SEMI, FG, "middle"), T_D, T_E)
for j, (tt, x, y, w_) in enumerate([(0.3, 150, 480, "كِتَاب"), (0.9, 600, 470, "قَلَم"), (1.5, 380, 590, "بَيْت")]):
    add(rr(x, y, 320, 90, 45, "#2A2412", AMB, 2) + ar(w_, x + 230, y + 62, 46, FG) + T("+10", x + 70, y + 60, 40, SEMI, AMB, "middle"), T_D + tt, T_E, pop=True, dur=.2)
lb = rr(110, 720, 860, 400, 36, SURF, LINE, 2) + T("Reyting · Arab tili A1", 150, 780, 32, SEMI, FG)
for j, (nm, pts) in enumerate([("Aziza S.", "1 248"), ("Jasur R.", "1 190"), ("Madina K.", "1 052"), ("Sardor A.", "860")]):
    yy = 810 + j * 74
    lb += rr(140, yy, 800, 62, 14, "#2A2412" if j == 0 else "#11302A") + T(str(j + 1), 176, yy + 43, 30, SEMI, AMB if j == 0 else FG, "middle") + T(nm, 220, yy + 43, 30, MED, FG) + T(pts, 910, yy + 43, 30, SEMI, AMB if j == 0 else MUTED, "end")
add(lb, at("ball oladi"), T_E, dy=40)
add(f'<g transform="translate(860 1170)"><path d="M-50 -60 H50 V-20 A50 50 0 0 1 -50 -20 Z" fill="url(#amb)"/><rect x="-10" y="28" width="20" height="30" fill="#E8873D"/><rect x="-36" y="56" width="72" height="16" rx="6" fill="#E8873D"/></g>'
    + rr(130, 1150, 560, 80, 40, "#2A2412", AMB, 2) + T("O‘qish = musobaqa", 410, 1203, 38, SEMI, AMB, "middle"), at("o‘qish musobaqaga"), T_E, pop=True)
# ── E. director panel
add(T("Siz bitta panelda ko‘rasiz", CX, 430, 60, SEMI, FG, "middle"), T_E, T_F)
tb = rr(90, 480, 900, 640, 36, SURF, LINE, 2) + T("O‘quvchi", 130, 540, 26, SEMI, MUTED) + T("So‘zlar", 520, 540, 26, SEMI, MUTED) + T("Davomat", 680, 540, 26, SEMI, MUTED) + T("To‘lov", 850, 540, 26, SEMI, MUTED)
add(tb, T_E, T_F, dy=40)
rows = [("Aziza S.", "124", "100%", "✓", GOOD), ("Jasur R.", "98", "96%", "✓", GOOD), ("Madina K.", "45", "71%", "qarz", BAD), ("Sardor A.", "86", "92%", "✓", GOOD), ("Nilufar T.", "12", "40%", "qarz", BAD)]
for j, (nm, w_, d, pay, col) in enumerate(rows):
    yy = 570 + j * 104
    bad = col == BAD
    r = rr(110, yy, 860, 90, 18, "#2A1D1B" if bad else "#11302A") + T(nm, 130, yy + 58, 30, MED, FG) + T(w_, 520, yy + 58, 34, SEMI, BAD if int(w_) < 50 else MINT) + T(d, 680, yy + 58, 30, SEMI, BAD if bad else FG)
    r += (T("qarz", 850, yy + 58, 28, SEMI, BAD) if pay == "qarz" else ic("check", 856, yy + 28, 34, GOOD, 3))
    add(r, at("Siz esa kim") + .3 + j * .2, T_F, dy=20, dur=.25)
# ── F. parents
add(T("Ota-ona ham ko‘radi", CX, 430, 66, SEMI, FG, "middle"), T_F, T_G)
add(rr(110, 520, 860, 300, 40, FG) + T("Aziza · bu hafta", 160, 600, 34, MED, "#3F5A4D") + T("+35 ta yangi so‘z", 160, 690, 64, SEMI, "#0A7A50") + T("Darsga keldi: 3 / 3", 160, 770, 36, SEMI, INK), T_F + .2, T_G, pop=True)
# ── G. CTA
add('<circle cx="540" cy="760" r="480" fill="url(#halo)"/>', T_G, DUR + 1, dy=0, dur=.8)
add(T("Hoziroq", CX, 520, 76, SEMI, FG, "middle") + T("pastdagi tugmani", CX, 610, 76, SEMI, FG, "middle") + T("bosing", CX, 700, 76, SEMI, "url(#gh)", "middle"), T_G, DUR + 1)
add(rr(110, 790, 860, 210, 105, "url(#gh)") + T("7 kun bepul", CX, 892, 84, SEMI, INK, "middle") + T("sinab ko‘ring", CX, 960, 46, MED, "#0A3D27", "middle"), at("7 kun bepul"), DUR + 1, pop=True)
add(T("markazly.onrender.com", CX, 1090, 38, MED, MUTED, "middle"), at("7 kun bepul") + .5, DUR + 1)
arrow = f'<g transform="translate({CX-60} 1170)"><circle cx="60" cy="60" r="60" fill="#2EE59D" fill-opacity=".18"/><path d="M60 28 V92 M32 66 L60 94 L88 66" fill="none" stroke="#2EE59D" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></g>'
add(arrow, T_G + .6, DUR + 1, bob=14)
S_B, S_F = T_B, T_G
