"""shablon.html -> index.html: logolarni joylaydi va to'liq <head> qo'shadi (telefon uchun viewport, favicon, ijtimoiy tarmoq ko'rinishi).
Ishlatish: python3 sayt/build.py <markazly_belgi.png> <markazly_yozuv.png>"""
import sys, base64, os
here = os.path.dirname(os.path.abspath(__file__))
mark_png, word_png = sys.argv[1], sys.argv[2]
uri = lambda p: "data:image/png;base64," + base64.b64encode(open(p, "rb").read()).decode()
M, Wd = uri(mark_png), uri(word_png)
body = open(os.path.join(here, "shablon.html"), encoding="utf-8").read().replace("{{MARK}}", M).replace("{{WORD}}", Wd)
head = (
    '<!doctype html>\n<html lang="uz">\n<head>\n'
    '<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    '<meta name="theme-color" content="#0D2620">\n'
    '<meta name="description" content="O‘quv markazlari uchun web tizim: o‘quvchilar, davomat, to‘lovlar, filiallar, sayt va o‘quvchi kabineti. 7 kun bepul.">\n'
    '<meta property="og:title" content="Markazly — o‘quv markaz boshqaruv tizimi">\n'
    '<meta property="og:description" content="Markazingizni bitta tizimdan boshqaring. 7 kun bepul sinov.">\n'
    '<meta property="og:type" content="website">\n'
    f'<link rel="icon" type="image/png" href="{M}">\n'
)
open(os.path.join(here, "index.html"), "w", encoding="utf-8").write(head + body + "\n</html>\n")
print("index.html tayyor")
