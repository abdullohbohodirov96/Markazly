SP = 1.08
def v(t): return t / SP
DUR = 51.6
SEGS = [
    (0.00, 3.04, "O‘quv markazingiz uchun hammasi — bitta tizimda."),
    (3.28, 4.59, "Bu — Markazly."),
    (4.99, 5.94, "Boshqaruv paneli:"),
    (6.23, 9.02, "o‘quvchilar, guruhlar va o‘qituvchilar bir joyda,"),
    (9.23, 10.75, "davomat bitta bosishda,"),
    (10.98, 13.36, "to‘lov va qarzdorlar esa darhol ko‘rinadi."),
    (13.69, 15.11, "Filiallar bo‘yicha hisobot:"),
    (15.42, 16.60, "qaysi filial foyda,"),
    (16.76, 18.16, "qaysi biri zarar qilyapti —"),
    (18.41, 19.35, "aniq raqamlarda."),
    (19.69, 22.24, "Markazingizga o‘z domenida chiroyli sayt:"),
    (22.47, 25.68, "saytdan qoldirilgan ariza to‘g‘ridan-to‘g‘ri tizimga tushadi."),
    (26.04, 27.00, "O‘quvchi kabineti:"),
    (27.23, 30.06, "darslar, uyga vazifa, lug‘at kartochkalari,"),
    (30.28, 33.13, "ota-ona esa farzandining davomatini o‘zi ko‘rib turadi."),
    (33.49, 35.39, "Eng qizig‘i — gamifikatsiya:"),
    (35.63, 38.48, "o‘quvchi har bir dars va vazifa uchun ball yig‘adi,"),
    (38.65, 39.80, "reytingda ko‘tariladi"),
    (39.95, 42.05, "va ballarni sovg‘aga almashtiradi!"),
    (42.36, 44.98, "Hammasi telefonda qulay, to‘rt tilda ishlaydi."),
    (45.21, 48.93, "Ma’lumotlaringizni o‘zimiz ko‘chirib beramiz, xodimlaringizni o‘qitamiz."),
    (49.19, 53.84, "Hoziroq pastdagi tugmani bosing va Markazly'ni 7 kun bepul sinab ko‘ring."),
]
KEY = {"hammasi", "bitta", "tizimda.", "Markazly.", "davomat", "darhol", "foyda,", "aniq", "sayt:", "tizimga", "kabineti:", "gamifikatsiya:", "ball", "reytingda", "sovg‘aga", "telefonda", "to‘rt", "tilda", "o‘zimiz", "7", "kun", "bepul"}
BAD_KEY = {"zarar"}
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
SC = [v(x) for x in (0, 4.8, 13.5, 19.5, 25.85, 33.3, 42.2, 49.0)]  # scene starts A..H
S_B, S_F = SC[1], SC[7]
