SP = 1.04
def v(t): return t / SP
DUR = 37.4
SEGS = [
    (0.0, 2.81, 'هل تعرف حقاً ما يحدث في مركزك التعليمي؟'),
    (3.21, 5.14, 'من دفع الرسوم،'),
    (5.33, 6.49, 'ومن تأخّر،'),
    (6.84, 7.53, 'ومن غاب عن الدرس؟'),
    (7.79, 9.87, 'ماركازلي نظامٌ واحد يجمع كلّ شيء:'),
    (10.21, 11.71, 'الحضور بضغطةٍ واحدة،'),
    (11.99, 14.58, 'والمدفوعات والمتأخّرون يظهرون فوراً،'),
    (14.94, 17.58, 'وتقارير كلّ فرعٍ بالأرقام الدقيقة.'),
    (17.86, 20.2, 'موقعٌ إلكترونيّ جميل لمركزك،'),
    (20.37, 22.13, 'وحسابٌ خاصّ لكلّ طالب،'),
    (22.47, 25.78, 'مع نقاطٍ وترتيبٍ يحفّزان الطلاب على التعلّم.'),
    (26.16, 28.89, 'النظام يعمل بأربع لغات منها العربية،'),
    (29.16, 32.39, 'وننقل بياناتك وندرّب موظفيك بأنفسنا.'),
    (32.76, 34.35, 'اضغط الزرّ في الأسفل الآن،'),
    (34.49, 37.14, 'وجرّب ماركازلي سبعة أيام مجاناً.'),
]
KEY = {'سبعة', 'بضغطةٍ', 'مجاناً.', 'فوراً،', 'ماركازلي', 'العربية،', 'أيام'}
BAD_KEY = {'تأخّر،', 'غاب'}
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
