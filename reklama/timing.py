# All times in seconds of the FINAL video (Sardor take 2, sped up 1.05x).
SP = 1.05
def v(t): return t / SP
DUR = 35.6
# spoken segments (original take times) -> text
SEGS = [
    (0.00, 3.09, "Administratoringiz hisobotni to‘g‘ri qilyaptimi yoki yo‘q —"),
    (3.32, 4.43, "siz buni bilmaysiz-ku!"),
    (4.73, 6.30, "Har kecha admin raqam tashlaydi:"),
    (6.49, 7.45, "bugun shuncha to‘lov,"),
    (7.59, 8.40, "shuncha o‘quvchi —"),
    (8.68, 9.64, "siz esa ishonasiz,"),
    (9.79, 11.02, "chunki boshqa iloji yo‘q!"),
    (11.34, 15.21, "Raqamni kim o‘zgartirdi, kim to‘lamay qoldi, qaysi guruh bo‘sh qoldi —"),
    (15.43, 17.01, "buni faqat admin aytsa bilasiz."),
    (17.34, 22.16, "Markazly'da esa har bir to‘lov, davomat, har bir qarz — hammasi tizimga yoziladi:"),
    (22.40, 25.04, "kim, qachon, qancha — hammasi ko‘rinib turadi,"),
    (25.30, 28.49, "siz esa buni telefoningizdan, xohlagan paytda o‘zingiz ko‘rasiz,"),
    (28.69, 29.93, "hisobot so‘rab o‘tirmaysiz!"),
    (30.20, 34.22, "Hoziroq pastdagi tugmani bosing va Markazly'ni 7 kun bepul sinab ko‘ring!"),
]
# words highlighted in mint inside captions
KEY = {"bilmaysiz-ku!", "ishonasiz,", "iloji", "yo‘q!", "Markazly'da", "tizimga", "telefoningizdan,", "o‘tirmaysiz!", "7", "kun", "bepul", "o‘zgartirdi,", "to‘lamay", "bo‘sh"}
BAD_KEY = {"bilmaysiz-ku!", "o‘zgartirdi,", "to‘lamay", "bo‘sh", "yo‘q!"}

def word_times():
    """Split each segment into words with times proportional to character length."""
    out = []
    for a, b, txt in SEGS:
        ws = txt.split()
        L = sum(len(w) + 1 for w in ws)
        t = a
        for w in ws:
            d = (b - a) * (len(w) + 1) / L
            out.append((v(t), v(t + d), w))
            t += d
    return out

def chunks(maxw=3, maxc=22):
    """Group words into short caption chunks (2-3 words), never across segments."""
    res = []
    for a, b, txt in SEGS:
        ws = [w for w in word_times() if a / SP - 1e-6 <= w[0] < b / SP - 1e-6]
        cur = []
        for w in ws:
            if cur and (len(cur) >= maxw or sum(len(x[2]) + 1 for x in cur) + len(w[2]) > maxc or cur[-1][2].endswith((",", "—", ":", "!", "?", "."))):
                res.append(cur); cur = []
            if w[2] == "—":
                if cur: cur.append(w)
                continue
            cur.append(w)
        if cur: res.append(cur)
    return [(c[0][0], c[-1][1], c) for c in res]

# scene starts (final-video seconds)
S_B, S_C, S_D, S_E, S_F = v(4.6), v(11.2), v(17.2), v(25.2), v(30.1)
