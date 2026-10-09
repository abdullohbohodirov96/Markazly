SP = 1.06
def v(t): return t / SP
DUR = 36.6
SEGS = [
    (0.0, 1.22, 'Kuniga 10 ming so‘m —'),
    (1.45, 3.22, 'bu bitta tushlikdan ham arzon.'),
    (3.59, 5.15, "Markazly'ning oylik narxi"),
    (5.28, 6.46, '290 ming so‘m,'),
    (6.69, 8.0, "ya'ni kuniga atigi"),
    (8.17, 9.3, '9 700 so‘m.'),
    (9.73, 10.52, 'Endi solishtiring:'),
    (10.82, 12.57, 'bitta o‘quvchi to‘lovni unutsa —'),
    (12.79, 14.25, '400 ming so‘m yo‘qotasiz.'),
    (14.5, 16.3, 'Bitta javobsiz qolgan ariza —'),
    (16.48, 19.1, 'yana bitta o‘quvchi boshqa markazga ketdi degani.'),
    (19.46, 21.2, 'Markazly esa qarzdorlarni ham,'),
    (21.2, 22.4, 'arizalarni ham,'),
    (22.4, 23.72, 'davomatni ham'),
    (23.86, 25.62, 'bitta joyda ushlab turadi.'),
    (25.77, 28.28, "Ya'ni tizim o‘z pulini birinchi oydayoq qaytaradi —"),
    (28.55, 30.27, 'qolgani sizning foydangiz.'),
    (30.59, 33.44, 'Hoziroq pastdagi tugmani bosing va'),
    (33.58, 34.96, "Markazly'ni 7 kun bepul sinab ko‘ring —"),
    (35.26, 35.82, 'yoqmasa,'),
    (35.95, 37.22, 'hech narsa to‘lamaysiz.'),
]
KEY = {'birinchi', 'arzon.', '9', 'kun', '7', '700', '290', '10', 'foydangiz.', 'oydayoq', 'bepul'}
BAD_KEY = {'unutsa', 'yo‘qotasiz.', '400', 'ketdi', 'javobsiz'}
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
