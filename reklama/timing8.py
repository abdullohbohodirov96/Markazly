SP = 1.08
def v(t): return t / SP
DUR = 46.4
SEGS = [
    (0.13, 1.85, "Excel'da qarzdorlarni topish —"),
    (1.98, 2.7, 'o‘n daqiqa.'),
    (3.03, 3.83, "Markazly'da —"),
    (4.08, 4.69, 'uch soniya.'),
    (5.23, 5.52, 'Qarang:'),
    (5.98, 8.49, "Excel'da har bir qatorni ko‘z bilan tekshirasiz,"),
    (8.72, 9.57, 'adashib ketasiz,'),
    (9.71, 11.02, 'yana boshidan boshlaysiz.'),
    (11.45, 12.4, "Markazly'da esa"),
    (12.64, 14.33, '«Qarzdorlar» tugmasini bosasiz —'),
    (14.66, 14.99, 'kim,'),
    (15.19, 16.24, 'qancha qarzdorligi'),
    (16.39, 18.35, 'va umumiy summa darhol chiqadi.'),
    (18.83, 19.76, 'Davomat ham shunday:'),
    (20.21, 22.81, "Excel'da har bir katakka qo‘lda belgi qo‘yasiz,"),
    (23.13, 24.05, "Markazly'da esa"),
    (24.2, 25.69, 'bitta bosishda belgilaysiz —'),
    (25.98, 28.11, 'ota-ona ham kabinetida darhol ko‘radi.'),
    (28.69, 30.11, 'Oy oxiridagi hisobot-chi?'),
    (30.61, 32.29, "Excel'da formulalar buziladi,"),
    (32.46, 33.73, 'raqamlar to‘g‘ri chiqmaydi.'),
    (34.19, 36.32, "Markazly'da «Hisobot»ni bosasiz —"),
    (36.61, 38.22, 'har bir filial bo‘yicha tushum,'),
    (38.4, 40.1, 'xarajat va foyda tayyor.'),
    (40.53, 41.61, "Excel'da bir soat,"),
    (41.88, 43.55, "Markazly'da bir daqiqa."),
    (43.95, 47.04, 'Hoziroq pastdagi tugmani bosing va'),
    (47.18, 48.63, "Markazly'ni 7 kun bepul sinab ko‘ring."),
]
KEY = {'bosishda', '«Qarzdorlar»', "Markazly'da", 'tayyor.', '«Hisobot»ni', 'kun', '7', 'daqiqa.', 'darhol', 'bitta', 'foyda', 'soniya.', 'bepul'}
BAD_KEY = {'buziladi,', 'chiqmaydi.', 'adashib', 'boshidan', 'qo‘lda'}
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
