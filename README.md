# Markazly

**O‘quv markazlari uchun web tizim** — boshqaruv tizimi, markaz sayti va o‘quvchi kabineti bitta obunada.

- Sayt: `markazly.uz` (rejada)
- Instagram: [@markazly.uz](https://instagram.com/markazly.uz)
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

## Sayt va arizalar Telegram'ga

Saytdagi "Ariza yuborish" formasi `sayt/server.js` ga yuboriladi, server esa arizani Telegram bot orqali sizga xabar qilib jo‘natadi. Tashqi kutubxona kerak emas (Node.js 18+).

### Kerakli env o‘zgaruvchilar

| Nom | Nima | Qayerdan olinadi |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | Bot tokeni | @BotFather → `/newbot` → token |
| `TELEGRAM_CHAT_ID` | Arizalar keladigan chat | Pastdagi qadamlar |
| `PORT` | Server porti | Render o‘zi beradi, qo‘lda yozmang |

**Chat ID ni olish:**
1. Yangi botingizga Telegram'da `/start` deb yozing (guruhga yuborilsin desangiz — botni guruhga qo‘shib, guruhda biror xabar yozing).
2. Brauzerda oching: `https://api.telegram.org/bot<TOKEN>/getUpdates`
3. Javobdagi `"chat":{"id": ... }` raqami — shu `TELEGRAM_CHAT_ID`. Guruh ID minus bilan boshlanadi.

### Render'ga joylash

1. Render → **New → Web Service** → shu repozitoriy.
2. **Root Directory:** `sayt` · **Build command:** bo‘sh · **Start command:** `npm start`
3. **Environment** bo‘limiga `TELEGRAM_BOT_TOKEN` va `TELEGRAM_CHAT_ID` ni qo‘shing.
4. Domen: Settings → Custom Domains → `markazly.uz`.

Mahalliy sinash: `cd sayt && TELEGRAM_BOT_TOKEN=... TELEGRAM_CHAT_ID=... npm start` → http://localhost:3000

Himoya: yashirin "honeypot" maydon (botlar uchun), bir IP dan 10 daqiqada 5 tadan ko‘p ariza qabul qilinmaydi. Server ishlamasa, forma arizani Telegram orqali qo‘lda yuborishni taklif qiladi.

> `index.html` ni tahrirlamang — `shablon.html` ni o‘zgartiring, keyin logolarni `{{MARK}}`/`{{WORD}}` o‘rniga qo‘yib `index.html` ni qayta yig‘ing.

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
