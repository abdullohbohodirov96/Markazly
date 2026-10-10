SP = 1.04
def v(t): return t / SP
DUR = 35.6
SEGS = [
    (0.0, 3.04, 'Hozir har bir mahallada arab tili markazi ochilyapti.'),
    (3.37, 4.84, 'Ota-ona qaysi birini tanlaydi?'),
    (5.19, 5.83, 'Albatta,'),
    (6.01, 8.26, 'zamonaviy va ishonchli ko‘ringanini.'),
    (8.65, 11.32, 'Markazly bilan markazingizning o‘z sayti bo‘ladi —'),
    (11.59, 12.92, 'o‘zbek va arab tilida,'),
    (13.12, 13.65, 'chiroyli,'),
    (13.86, 15.14, 'telefonda tez ochiladi.'),
    (15.43, 18.61, 'Saytdan qoldirilgan ariza to‘g‘ridan-to‘g‘ri tizimga tushadi,'),
    (18.79, 20.34, 'birorta mijoz yo‘qolmaydi.'),
    (20.74, 21.49, 'Ota-ona esa'),
    (21.61, 24.77, 'farzandining davomati va natijasini kabinetda ko‘rib turadi —'),
    (25.05, 26.45, 'mana shu ishonch beradi.'),
    (26.78, 28.87, 'Raqobatchilar daftar bilan ishlayotganda,'),
    (29.04, 30.68, 'siz tizim bilan ishlaysiz.'),
    (31.04, 32.69, 'Hoziroq pastdagi tugmani bosing'),
    (32.85, 33.96, "va Markazly'ni"),
    (34.08, 35.45, '7 kun bepul sinab ko‘ring.'),
]
KEY = {'tizimga', 'tizim', 'kun', 'zamonaviy', 'ishonchli', '7', 'tilida,', 'arab', 'ishonch', 'bepul', 'sayti'}
BAD_KEY = {'daftar'}
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
