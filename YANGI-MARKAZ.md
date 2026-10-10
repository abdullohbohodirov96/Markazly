# Yangi markazni ishga tushirish

Shablon bitta. Har bir yangi markaz uchun kod o‘zgarmaydi. Faqat quyidagilar to‘ldiriladi:

1. `markaz.json`: nom, aloqa, sayt matnlari, rang va modullar.
2. `assets/`: logotip. `python3 scripts/ikonlar.py logo.png` buyrug‘i logodan barcha ikonlarni yasaydi.
3. Render’dagi muhit o‘zgaruvchilari: baza, direktor paroli va bot tokeni.

Har bir markazning serveri va bazasi alohida bo‘ladi. Ma’lumotlar hech qachon aralashmaydi.

---

## 1-qadam. Markaz egasidan so‘raladigan savollar (anketa)

### A. Asosiy ma’lumot
| # | Savol | `markaz.json` dagi joyi |
|---|---|---|
| 1 | Markazning to‘liq nomi? Qisqa nomi bormi (telefon ekranida chiqadi)? | `nom`, `qisqaNom` |
| 2 | Odamlar nomni yana qanday yozib qidiradi (ruscha, qisqartma)? | `nomVariantlari` |
| 3 | Markaz turi: til markazi, IT, matematika, maktabgacha…? Asosiy fan qaysi? | `sohasi`, `fan` |
| 4 | Telefon, manzil, shahar? | `aloqa.telefon`, `aloqa.manzil`, `aloqa.shahar` |
| 5 | Instagram, Telegram kanal, qabul uchun Telegram, Facebook? | `aloqa.*` |
| 6 | Telegram bot bormi? Bo‘lmasa @BotFather’da yaratamiz. | `aloqa.botUsername` + `.env` token |
| 7 | Domen bormi (masalan markaz.uz)? | `sayt.url` |
| 8 | Logotip (PNG, kvadrat, kamida 512px) va asosiy rang? | `assets/`, `rang.asosiy` |

### B. Ish tartibi
| # | Savol | Joyi |
|---|---|---|
| 9 | Ish vaqti (boshlanish va tugash)? | `ish.boshlanish`, `ish.tugash` |
| 10 | Bitta dars necha daqiqa? | `ish.darsDaqiqa` |
| 11 | Oylik to‘lov qachon olinadi: hamma uchun bir kunda yoki har o‘quvchi qo‘shilgan kunida? | `ish.tolovKuni` (qo‘shilgan kun avtomatik ishlaydi) |
| 12 | Chek raqami oldidan qanday harflar yozilsin (masalan `ALB`, `IT`)? | `ish.chekPrefiksi` |
| 13 | Interfeys qaysi tillarda bo‘lsin (uz, ru, en, ar)? | `ish.tillar` |
| 14 | Filiallar bormi? Nechta, nomlari? | ⚠️ Shablonda hozircha filiallar bo‘yicha alohida hisob yo‘q (saytda 2 ta qabul manzili bor). Filiallar kerak bo‘lsa, AlBayan versiyasidan ko‘chiriladi |
| 15 | Kurslar va narxlar; guruhlar, ustozlar, xonalar? | ERP’da kiritiladi (Excel’dan import ham bor) |
| 16 | Xodimlar va rollari: direktor, administrator, ustoz, buxgalter. Kimga nima ko‘rinsin? | ERP → Sozlamalar → Foydalanuvchilar |
| 17 | Ustoz maoshi: belgilangan summami yoki foizmi? | ERP → Xodimlar |
| 18 | Hozir ma’lumotlar qayerda (Excel, daftar, boshqa dastur)? Ko‘chirib beramiz. | Import |

### C. Modullar: kerak yoki kerak emas
| Modul | Nima qiladi | Kalit |
|---|---|---|
| Sayt | Markazning ochiq sayti: ariza formasi, ustozlar, narx, savol-javob | `sayt` |
| O‘quvchi kabineti | O‘quvchi davomati, to‘lovi, vazifasi, testlari va jadvali | `kabinet` |
| Ota-ona kabineti | Ota-ona farzandining davomati va to‘lovini ko‘radi | `otaOna` |
| Gamifikatsiya | XP, daraja, tanga, nishon, reyting va sovg‘alar. Sozlamalarda yoqiladi va ballar o‘sha yerda so‘raladi | `gamifikatsiya` |
| Telegram bot | Davomat va to‘lov xabarlari, e’lonlar, bepul darsga yozilish | `telegramBot` |
| Karta orqali to‘lov boti | O‘quvchi botda «To‘lov qilish»ni bosadi, bank xabari kelgach to‘lov avtomatik tasdiqlanadi | `tolovBoti` |
| Daraja testi | Saytda bepul daraja testi. Savollar bazasi hozircha faqat **arab tili** uchun | `darajaTesti` |
| Onlayn kurs | A1 video-darslik. Mazmuni hozircha faqat **arab tili** uchun | `onlaynKurs` |
| Kanal viktorinasi | Telegram kanalga kuniga test-savollar. Hozircha **arab tili** uchun | `kanalViktorina` |

> Arab tilidan boshqa fan uchun daraja testi, onlayn kurs yoki viktorina kerak bo‘lsa, ularga alohida mazmun yoziladi. Bu qo‘shimcha ish.

### D. Sayt matnlari (sayt yoqilgan bo‘lsa)
Yangi markaz uchun quyidagi matnlar yoziladi. Har birini `{ "uz": "…", "ru": "…", "en": "…", "ar": "…" }` ko‘rinishida 4 tilda berish mumkin.

| Matn | Kalit |
|---|---|
| Bosh ekrandagi ustki qator va tavsif | `heroEyebrow`, `heroLead` |
| Doskadagi so‘z va dars nomi | `heroDoska` |
| Shiorlar | `shiorlar` |
| «Natija yo‘li»: 4 bosqich | `natijaBosqichlar` |
| «3 qadam» | `qadamlar` |
| «Nega biz»: sarlavha, matn, 6 band | `negaBiz*` |
| Darajalar, ustozlar va dars haqida izohlar | `darajalarIzoh`, `ustozlarIzoh`, `darsIzoh` |
| Arizadagi «Hozirgi darajangiz» savoli va variantlari | `darajaSavoli`, `darajaVariantlari` |
| Ko‘p so‘raladigan savollar | `faq` |
| Google uchun sarlavha va tavsif | `sarlavha`, `tavsif`, `kursNomi`, `kursTavsifi` |

Tayyor misol: `namunalar/sabo-academy.json` (arab tili markazi).

### E. Gamifikatsiya (modul yoqilgan bo‘lsa)
- Qaysi harakat uchun necha ball beriladi? Bular so‘raladi: darsga kelgani, kechikib kelgani, uy vazifasi, darsda faollik, test natijasi, test 100%, ustozga savol, o‘z vaqtida to‘lov.
- Necha XP 1 tangaga teng bo‘lsin?
- Tangaga qanday sovg‘alar beriladi (ruchka, futbolka, bepul dars, chegirma…)?

Bularni markaz egasining o‘zi **ERP → Sozlamalar → 🏆 Gamifikatsiya → «Sozlab yoqish»** orqali kiritadi.

---

## 2-qadam. Fayllarni tayyorlash

```bash
git clone <shablon> markaz-nomi && cd markaz-nomi
# markaz.json ni anketaga qarab to'ldiring
python3 scripts/ikonlar.py ~/Downloads/logo.png   # logo bo'lmasa: argumentsiz (nom harflaridan chizadi)
npm install && node build.js
SEED_DIRECTOR_PASSWORD='VaqtinchaParol2026' npm start   # http://localhost:3000 — tekshirib ko'ring
bash scripts/test-all.sh                                 # hamma testlar
```

## 3-qadam. Serverga chiqarish (Render)

1. GitHub’da markaz uchun yangi repo oching va kodni yuklang.
2. Neon’da yangi PostgreSQL baza oching va `DATABASE_URL` ni oling.
3. Render → New → Blueprint → shu repo (`render.yaml`). Muhit o‘zgaruvchilarini to‘ldiring:
   - `DATABASE_URL`: Neon manzili.
   - `SEED_DIRECTOR_PASSWORD`: kuchli parol. Uni markaz egasiga bering va birinchi kirishda almashtirtiring.
   - `TELEGRAM_BOT_TOKEN`, `TELEGRAM_BOT_USERNAME`: bot yoqilgan bo‘lsa.
   - `SITE_URL`: domen. Domen bo‘lmasa Render manzili yoziladi.
4. Domen: Render → Settings → Custom Domain. DNS’da CNAME yozuvi qo‘shiladi.
5. Tekshiruv ro‘yxati:
   - Sayt ochiladi.
   - Ariza yuborilsa ERP → Murojaatlar’ga tushadi.
   - Direktor kiradi.
   - O‘quvchi kodi bilan kabinet ochiladi.
   - Bot `/start` ga javob beradi.

## 4-qadam. Topshirish
- Ma’lumotlarni Excel’dan import qilish: Sozlamalar → Ma’lumotlar.
- Joyiga borib xodimlarni o‘qitish: `QOLLANMA.md`.
- 7 kunlik bepul sinov. Sinov davomida chiqqan kamchiliklar shu davrda tuzatiladi.
