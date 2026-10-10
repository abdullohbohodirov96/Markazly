SP = 1.06
def v(t): return t / SP
DUR = 39.0
SEGS = [
    (0.13, 1.66, 'Arab tili markazingiz bormi?'),
    (2.07, 4.15, 'Unda bu video aynan siz uchun.'),
    (4.5, 5.13, 'Arab tilida eng qiyini —'),
    (5.27, 5.99, 'so‘z yodlash:'),
    (6.21, 7.08, 'o‘quvchi darsda tushunadi,'),
    (7.35, 8.64, 'uyga borib esa unutadi.'),
    (8.88, 10.28, "Markazly'da har bir o‘quvchining"),
    (10.67, 13.41, 'shaxsiy kabineti bor: harakatlari bilan lug‘at kartochkalari,'),
    (13.65, 15.52, 'uyga vazifa va baholar.'),
    (15.76, 17.4, 'O‘quvchi har bir yodlangan so‘z uchun'),
    (17.73, 22.33, 'ball oladi va guruhda reytingda ko‘tariladi —'),
    (22.61, 23.14, 'shunda'),
    (23.28, 24.87, 'o‘qish musobaqaga aylanadi!'),
    (25.22, 27.4, 'Siz esa kim qancha so‘z yodlagani,'),
    (27.54, 30.47, 'kim darsga kelmagani va kim to‘lamaganini'),
    (30.6, 31.65, 'bitta panelda ko‘rasiz.'),
    (31.92, 34.92, 'Ota-ona ham farzandining natijasini o‘zi kuzatib boradi.'),
    (35.28, 37.06, 'Hoziroq pastdagi tugmani bosing'),
    (37.19, 38.29, "va Markazly'ni"),
    (38.43, 39.81, '7 kun bepul sinab ko‘ring.'),
]
KEY = {'panelda', 'kun', 'yodlash:', '7', 'bitta', 'Arab', 'reytingda', 'bepul', 'kabineti', 'aylanadi!', 'ball', 'musobaqaga'}
BAD_KEY = {'qiyini', 'unutadi.'}
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
