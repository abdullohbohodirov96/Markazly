SP = 1.06
def v(t): return t / SP
DUR = 36.2
SEGS = [
    (0.15, 1.97, 'Yangi tizimga o‘tishdan qo‘rqasizmi?'),
    (2.43, 4.1, '«Ma’lumotlarim yo‘qolib qolmaydimi,'),
    (4.4, 5.82, 'xodimlarim o‘rgana oladimi?»'),
    (6.03, 6.8, 'deb o‘ylaysizmi?'),
    (7.25, 7.53, 'Keling,'),
    (7.76, 9.04, 'hammasiga javob beraman.'),
    (9.47, 10.06, 'Birinchi:'),
    (10.39, 11.75, 'eski ma’lumotlaringizni —'),
    (11.98, 13.76, "Excel'dami, daftardami —"),
    (13.89, 15.54, 'o‘zimiz tizimga ko‘chirib beramiz.'),
    (15.96, 16.52, 'Ikkinchi:'),
    (16.85, 18.86, 'har bir markazning bazasi alohida,'),
    (19.09, 21.81, 'ma’lumotlaringizni sizdan boshqa hech kim ko‘rmaydi.'),
    (22.3, 22.81, 'Uchinchi:'),
    (23.13, 24.6, 'markazingizga o‘zimiz borib,'),
    (24.6, 26.12, 'xodimlaringizni o‘qitamiz.'),
    (26.41, 27.4, 'Va eng muhimi —'),
    (27.7, 29.92, 'avval 7 kun bepul ishlatib ko‘rasiz,'),
    (30.14, 30.67, 'yoqmasa,'),
    (30.8, 32.02, 'hech narsa to‘lamaysiz.'),
    (32.4, 35.29, 'Hoziroq pastdagi tugmani bosing va'),
    (35.41, 36.77, "Markazly'ni 7 kun bepul sinab ko‘ring."),
]
KEY = {'kim', 'kun', '7', 'alohida,', 'hech', 'Uchinchi:', 'Ikkinchi:', 'Birinchi:', 'o‘zimiz', 'o‘qitamiz.', 'bepul'}
BAD_KEY = {'qo‘rqasizmi?', 'yo‘qolib'}
def word_times():
    out = []
    for a, b, txt in SEGS:
        ws = txt.split(); L = sum(len(w) + 1 for w in ws); t = a
        for w in ws:
            d = (b - a) * (len(w) + 1) / L; out.append((v(t), v(t + d), w)); t += d
    return out
def chunks(maxw=3, maxc=22):
    res = []
    wt = word_times()
    for a, b, txt in SEGS:
        ws = [w for w in wt if a / SP - 1e-6 <= w[0] < b / SP - 1e-6]; cur = []
        for w in ws:
            if cur and (len(cur) >= maxw or sum(len(x[2]) + 1 for x in cur) + len(w[2]) > maxc or cur[-1][2].endswith((",", "—", ":", "!", "?", "."))):
                res.append(cur); cur = []
            if w[2] == "—":
                if cur: cur.append(w)
                continue
            cur.append(w)
        if cur: res.append(cur)
    return [(c[0][0], c[-1][1], c) for c in res]
def at(sub, end=False):
    for a, b, t in SEGS:
        if sub in t: return v(b) if end else v(a)
    raise KeyError(sub)
