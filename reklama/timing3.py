SP = 1.05
def v(t): return t / SP
DUR = 36.9
SEGS = [
    (0.00, 3.04, "Markazingiz har oy millionlab so‘m yo‘qotyapti —"),
    (3.27, 4.81, "va siz buni sezmayapsiz ham."),
    (5.27, 6.57, "Keling, hisoblab ko‘ramiz:"),
    (6.94, 8.60, "markazda 300 ta o‘quvchi bor,"),
    (8.89, 11.44, "shulardan atigi 10 tasi to‘lovni kechiktirdi-yu,"),
    (11.67, 12.61, "esdan chiqib ketdi."),
    (13.02, 15.28, "Bir oylik to‘lov 400 ming so‘m bo‘lsa —"),
    (15.56, 16.86, "bu oyiga 4 million,"),
    (17.13, 19.62, "yiliga esa 48 million so‘m degani!"),
    (20.03, 21.06, "Bu pul yo‘qolmagan,"),
    (21.36, 23.43, "shunchaki hech kim vaqtida eslatmagan."),
    (23.96, 27.11, "Markazly'da esa qarzdorlar o‘zi alohida ro‘yxatga tushadi,"),
    (27.44, 30.24, "kim qancha to‘lashi kerakligi har kuni ko‘rinib turadi —"),
    (30.57, 32.28, "birorta to‘lov ham unutilmaydi."),
    (32.70, 37.03, "Hoziroq pastdagi tugmani bosing va Markazly'ni 7 kun bepul sinab ko‘ring."),
]
KEY = {"millionlab", "300", "10", "4", "48", "million,", "million", "Markazly'da", "alohida", "har", "kuni", "unutilmaydi.", "7", "kun", "bepul"}
BAD_KEY = {"yo‘qotyapti", "sezmayapsiz", "kechiktirdi-yu,", "chiqib", "ketdi.", "eslatmagan."}
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
S_B, S_C, S_D, S_E, S_F = v(5.1), v(12.85), v(19.85), v(23.75), v(32.5)
