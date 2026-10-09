# Markazly — biznes qarorlari

## Tariflar (oylik, so‘m)

| Tarif | Faol o‘quvchi | O‘qituvchi | Narx | Asosiy imkoniyatlar |
|---|---|---|---|---|
| Start | 100 gacha | 3 gacha | 290 000 | CRM, davomat, to‘lov va qarzdorlik, tayyor landing page |
| Standart | 101–300 | 10 gacha | 590 000 | + o‘quvchi kabineti, Telegram eslatmalar, o‘z domenida sayt |
| Biznes | 301–700 | 25 gacha | 990 000 | + to‘liq sayt, xodimlar va ish haqi, 2 filial va filiallar hisoboti, texnik support, qo‘shimcha funksiyalar |
| Premium | 700+ | cheksiz | 1 690 000 dan | + cheksiz filial, o‘z brendi, shaxsiy menejer |

- "Faol o‘quvchi" — shu oyda to‘lov yoki davomati bor o‘quvchi. Lidlar soni cheklanmaydi.
- Limitdan oshsa — keyingi tarifga o‘tiladi.
- **Gamifikatsiya** (ballar, reyting, sovg‘alar) — qo‘shimcha modul, narxi alohida.
- Interfeys: o‘zbek, rus, ingliz, arab tillarida (sotishdan oldin tayyor bo‘lishi kerak).

## Shartlar

- 7 kun bepul sinov: avval sinaydi, yoqsa — keyin to‘laydi.
- To‘lov **2 oylik oldindan** olinadi.
- Yillik to‘lovda 2 oy sovg‘a (10 oy to‘laydi, 12 oy ishlatadi).
- Har bir tarifda **1 marta joyiga borib tushuntirish**.
- Texnik support va qo‘shimcha funksiya — Biznes va Premium’da. Shartnomada chegara yozilsin, masalan "oyiga 8 soatgacha qo‘shimcha ish".
- Mijoz xohlasa, ma’lumotlarini (o‘quvchilar, guruhlar, to‘lovlar) o‘zimiz yuklab beramiz.

## Raqobatchi

Modme (modme.uz) — o‘quvchi soniga qarab: 0–100 ≈ 500 000/oy, 100–300 ≈ 1 040 000/oy, 300–1000 ≈ 1 560 000/oy, 1000+ ≈ 3 000 000/oy; gamifikatsiya +150 000/oy.
Markazly farqi: tizim + sayt + kabinet bitta narxda, ~40–45% arzon, joyiga borib o‘rgatish.

## Server rejasi

- Reja: **Eskiz VPS** (ma’lumotlar O‘zbekistonda — "Shaxsga doir ma’lumotlar to‘g‘risida"gi qonun, 27-1-modda).
- Start va Standart: bitta umumiy serverda (VPS 3: 2 yadro, 4 GB) har bir markaz o‘z Docker konteyneri, o‘z bazasi (alohida baza foydalanuvchisi), o‘z domeni va o‘z Telegram boti bilan. Xavfsiz rejimda 8–10, maksimum 12–14 markaz.
- Biznes va Premium: alohida VPS.
- Server to‘lsa: yana bitta VPS 3 yoki VPS 4 (8 GB, ~20–25 markaz).
- Taxminiy xarajat (Eskiz): VPS 3 + IP + backup ≈ 265 000/oy; VPS 4 ≈ 481 000/oy.
- Render vaqtincha: bitta mijozga ≈ $13/oy (ilova $7 + baza $6). Bepul tarifda baza 30 kundan keyin o‘chiriladi — ishlatilmasin.

## Xavfsizlik ro‘yxati

- PostgreSQL internetga ochilmaydi; har markazga alohida baza foydalanuvchisi.
- Firewall: faqat 22, 80, 443. SSH faqat kalit bilan, fail2ban.
- HTTPS (Caddy), avtomatik xavfsizlik yangilanishlari.
- Kunlik backup + bir nusxasi boshqa joyda (shifrlangan); oyiga bir marta tiklashni sinash.
- Sotishdan oldin kod tekshiruvi: rollar, o‘quvchi faqat o‘zinikini ko‘rishi, login himoyasi, fayl yuklash chegaralari.
- Mijoz bilan shartnoma/oferta: ma’lumot markazniki, qayerda saqlanadi, shartnoma tugaganda qaytariladi.

## Yangi mijozni ulash

1. Domen (markaz nomiga) → A-yozuv server IP’siga.
2. Konteyner + baza + bot tokeni (markazning o‘z @BotFather boti).
3. 5 daqiqalik tekshiruv: domen va HTTPS, test o‘quvchi faqat shu markazda ko‘rinadi, bot xabari faqat shu markazdan, test ma’lumot o‘chiriladi.

## Instagram

- Ism: `Markazly | O‘quv markaz boshqaruv tizimi`
- Bio:
  ```
  O‘quv markazingizni bitta tizimdan boshqaring
  📊 Davomat · To‘lov · Hisobot
  🌐 Sayt va o‘quvchi kabineti
  ✅ 7 kun bepul sinov
  📞 +998 50 999 97 33
  ```
- Kategoriya: Dasturiy ta’minot (Software).
- Aktuallar: Tariflar · Imkoniyat · Filiallar · Sayt · Kabinet · Bepul sinov · Aloqa.

## Nom

"Ilmora" band bo‘lgani uchun **Markazly** tanlandi. Tekshirish kerak: `markazly.uz` va `markazli.uz` domenlari, `@markazly_uz`, ima.uz tovar belgisi bazasi.
