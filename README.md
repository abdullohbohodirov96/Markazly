# Markazly

**O‘quv markazlari uchun web tizim** — boshqaruv tizimi, markaz sayti va o‘quvchi kabineti bitta obunada.

- Sayt: `markazly.uz` (rejada)
- Instagram: [@markazly_uz](https://instagram.com/markazly_uz)
- Aloqa: +998 50 999 97 33 · Telegram [@abdulloh_mrktlg](https://t.me/abdulloh_mrktlg)

## Papkalar

| Papka | Ichida nima bor |
|---|---|
| `sayt/` | Sotuv sayti. `index.html` — tayyor, bitta fayl (logolar ichiga joylangan), domenga to‘g‘ridan-to‘g‘ri qo‘yiladi. `shablon.html` — tahrirlash uchun manba (`{{MARK}}`, `{{WORD}}` o‘rniga logo qo‘yiladi). |
| `brand/logo/` | Logo: post (1080×1080), gorizontal (qora fon va shaffof), faqat yozuv, faqat belgi. PNG, SVG va PDF (vektor) formatlarda. |
| `brand/instagram/` | Profil rasmlari, 7 ta aktual muqovasi va 7 ta aktual storisi (1080×1920). |
| `brand/manba/` | Logoning asl rasmi. |
| `brand/skriptlar/` | Logo, aktual va storislarni qayta yasaydigan Python skriptlar. |
| `prezentatsiya/` | Mijozlarga ko‘rsatiladigan prezentatsiya slaydlari (14 ta) va tartibi (`deck.json`). |
| `docs/` | Tariflar, shartlar, xarajatlar, server va xavfsizlik bo‘yicha qarorlar. |

## Brend

| Rang | Kod | Qayerda |
|---|---|---|
| Qora-yashil fon | `#0A1F17` / `#050E0B` | Asosiy fon |
| Yalpiz | `#2EE59D` | Urg‘u, tugmalar |
| Moviy | `#1FB5C8` | Gradientning ikkinchi rangi |
| Oq | `#F4F8F6` | Matn |

- Logo yozuvi: **Poppins SemiBold**, "Markaz" oq, "ly" yalpiz→moviy gradientda.
- Belgi: ochiq eshikdan kirib kelayotgan odam — "markazga kirish".
- Sayt shriftlari: Sora (sarlavha), Golos Text (matn), IBM Plex Mono (raqam va yorliqlar).

## Skriptlarni ishga tushirish

```bash
pip install cairosvg fonttools pillow
# Poppins-SemiBold/Medium/Regular.ttf va markazly_belgi_shaffof.png (mark_transparent.png nomi bilan)
# skript bilan bir papkada bo‘lishi kerak
python3 make_markazly.py     # logo
python3 make_highlights.py   # aktual muqovalari
python3 make_stories.py      # aktual storislari
```
