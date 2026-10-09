# Texnik topshiriq: O‘quvchi kabineti va Gamifikatsiya

Markazly tizimining ikki moduli uchun dasturchiga topshiriq. Ballar va darajalar raqamlari — boshlang‘ich qiymatlar, har bir markaz ularni sozlamalarda o‘zgartira oladi.

---

## 1. Tariflar bo‘yicha mavjudlik

| Modul | Start | Standart | Biznes | Premium |
|---|---|---|---|---|
| O‘quvchi kabineti | — | ✔ | ✔ | ✔ |
| Ota-ona akkaunti | — | ✔ | ✔ | ✔ |
| Telegram eslatmalar | — | ✔ | ✔ | ✔ |
| Gamifikatsiya | qo‘shimcha | qo‘shimcha | qo‘shimcha | qo‘shimcha |

Modul yoqilmagan markazda tegishli sahifalar va API yopiq bo‘ladi (`403`), menyuda ko‘rinmaydi.

---

## 2. Rollar

| Rol | Kim | Nimani ko‘radi |
|---|---|---|
| `student` | O‘quvchi | Faqat o‘zining jadvali, darslari, vazifalari, davomati, to‘lovlari, ballari |
| `parent` | Ota-ona | Bog‘langan farzand(lar)ining yuqoridagi ma’lumotlari; vazifa topshira olmaydi |
| `teacher` | O‘qituvchi | O‘z guruhlari: davomat, vazifa berish/baholash, ball qo‘shish (cheklangan) |
| `admin` | Administrator | Hammasi, sovg‘a buyurtmalarini tasdiqlash, ball tuzatish |
| `director` | Direktor | Hammasi + gamifikatsiya sozlamalari va hisobotlari |

**Qat’iy qoida:** har bir so‘rovda server `center_id` va foydalanuvchi huquqini tekshiradi. O‘quvchi URL’dagi ID ni o‘zgartirib boshqa o‘quvchi ma’lumotini ocholmasligi kerak (testda alohida tekshiriladi).

---

## 3. Kirish (autentifikatsiya)

- Login — **telefon raqam**. Parol o‘rniga **bir martalik kod** markazning Telegram boti orqali yuboriladi (SMS ixtiyoriy, pullik).
- Birinchi kirish: admin o‘quvchini qo‘shganda telefonni kiritadi → o‘quvchi botga `/start` bosadi va telefonini ulashadi → bot kabinetga kirish havolasini yuboradi.
- Ota-ona: o‘z telefoni bilan kiradi; admin uni bir yoki bir nechta farzandga bog‘laydi. Bitta ota-ona — bir nechta farzand, farzandlar o‘rtasida almashish tugmasi.
- Sessiya: 30 kun (telefonda qulay), "Barcha qurilmalardan chiqish" tugmasi.
- Kodni 5 marta noto‘g‘ri kiritsa — 15 daqiqaga bloklanadi.
- Kabinet o‘sha markaz domenida: `kabinet.markazdomeni.uz`.

---

## 4. O‘quvchi kabineti — sahifalar

Mobil-birinchi dizayn (asosan telefondan ochiladi). Pastda menyu: **Bosh sahifa · Darslar · Vazifalar · To‘lov · Profil**.

### 4.1 Bosh sahifa
- Salomlashish, guruh nomi va darajasi (masalan B1).
- **Bugungi dars**: vaqt, xona, o‘qituvchi. Dars bo‘lmasa — keyingi dars.
- **Uyga vazifa**: topshirilmagan vazifalar soni va eng yaqin muddat.
- **To‘lov holati**: keyingi to‘lov sanasi va summasi; qarz bo‘lsa — qizil ogohlantirish.
- **Davomat**: shu oy foizi.
- Gamifikatsiya yoqilgan bo‘lsa: ballar, daraja, guruhdagi o‘rni.

### 4.2 Dars jadvali
- Hafta ko‘rinishi; har dars: vaqt, xona, o‘qituvchi, mavzu.
- Bekor qilingan / ko‘chirilgan dars alohida belgilanadi.

### 4.3 Darslar va materiallar
- O‘tilgan darslar ro‘yxati: sana, mavzu, o‘qituvchi izohi.
- Materiallar: PDF, rasm, havola. **Video serverga yuklanmaydi** — YouTube (yopiq havola) yoki Telegram havolasi qo‘yiladi.
- Fayl cheklovi: 10 MB, turlari: pdf, jpg, png, docx.

### 4.4 Uyga vazifalar
- Ro‘yxat: vazifa, muddat, holat (berilgan / topshirilgan / baholangan / muddati o‘tgan).
- Topshirish: matn yoki fayl (rasm/PDF). Muddatdan keyin topshirish — "kechikkan" belgisi bilan.
- O‘qituvchi baho (0–100 yoki 5 ballik — markaz sozlamasi) va izoh qoldiradi.

### 4.4.1 Lug‘at
- O‘qituvchi har darsga so‘zlar qo‘shadi: so‘z, tarjima, misol gap, (ixtiyoriy) audio havolasi. Excel’dan ommaviy yuklash mumkin.
- O‘quvchi kartochkalar bilan takrorlaydi: so‘z → aylantiradi → tarjima; tugmalar **"Bilaman"** va **"Takrorlash"**.
- Takrorlash jadvali (oraliqli takrorlash): "Bilaman" bosilgan so‘z 1 → 3 → 7 → 14 → 30 kundan keyin qaytadi; "Takrorlash" — ertaga qaytadi.
- Bosh sahifada: "Bugun N ta so‘z". Kunlik takrorlash tugatilsa — gamifikatsiyada +5 ball (sozlanadi).
- O‘qituvchi guruh bo‘yicha ko‘radi: kim nechta so‘zni o‘rgangan.
- Jadvallar: `words(id, center_id, lesson_id, group_id, word, translation, example, audio_url)`, `word_reviews(student_id, word_id, box, next_review_at, last_result)`.

### 4.5 Davomat
- Oy kalendari: keldi / kelmadi / kechikdi / sababli.
- Oy bo‘yicha foiz.

### 4.6 To‘lovlar
- Har o‘quvchi **o‘zi qo‘shilgan kunda** to‘laydi (20-sanada qo‘shilgan bo‘lsa — har oyning 20-sida).
- Yangi qo‘shilgan o‘quvchi qarzdor bo‘lib ko‘rinmaydi; ortiqcha to‘lov balansga o‘tadi.
- Ko‘rinadi: keyingi to‘lov sanasi va summasi, balans, to‘lovlar tarixi (sana, summa, usul).
- Onlayn to‘lov (Payme/Click) — keyingi bosqich, hozir faqat ko‘rish.

### 4.7 Profil
- Ism, telefon, guruh(lar), til (o‘zbek / rus / ingliz / arab), Telegram ulanganmi, chiqish.

---

## 5. Telegram eslatmalar

Har markazning o‘z boti. Hammasi markaz sozlamalarida yoqiladi/o‘chiriladi.

| Hodisa | Kimga | Qachon |
|---|---|---|
| Dars eslatmasi | o‘quvchi | darsdan 2 soat oldin |
| Darsga kelmadi | ota-ona | dars boshlanib 15 daqiqa o‘tgach, "kelmadi" belgilansa |
| Yangi uyga vazifa | o‘quvchi | berilganda |
| Vazifa muddati yaqin | o‘quvchi | muddatdan 1 kun oldin |
| To‘lov sanasi yaqin | o‘quvchi + ota-ona | 3 kun oldin va shu kuni |
| Qarz | ota-ona | to‘lov kunidan 3 kun o‘tgach |
| To‘lov qabul qilindi | o‘quvchi + ota-ona | darhol |
| Ball olindi / yangi daraja / nishon | o‘quvchi | darhol (gamifikatsiya yoqilgan bo‘lsa) |

Navbat (queue) orqali yuboriladi; Telegram cheklovi: sekundiga 25 xabardan oshmasin. Xabar yuborilmasa — 3 marta qayta urinish.

---

## 6. Gamifikatsiya

Maqsad: davomat va vazifa topshirishni oshirish, o‘quvchi markazdan ketib qolmasligi.

### 6.1 Ballar (boshlang‘ich qoidalar)

| Harakat | Ball | Kim beradi |
|---|---|---|
| Darsga keldi | +10 | avtomatik (davomatdan) |
| Darsga vaqtida keldi (kechikmadi) | +2 qo‘shimcha | avtomatik |
| Uyga vazifani muddatida topshirdi | +15 | avtomatik |
| Vazifa bahosi 90% va yuqori | +10 qo‘shimcha | avtomatik |
| Test/imtihon natijasi | natija % × 0,3 (maks. +30) | avtomatik |
| To‘lovni muddatida qildi | +20 | avtomatik |
| Oyda bitta ham dars qoldirmadi | +50 | avtomatik, oy oxirida |
| Do‘stini olib keldi (shartnoma tuzilsa) | +100 | admin |
| Darsdagi faollik | +1 … +10 | o‘qituvchi (kuniga bir o‘quvchiga ko‘pi bilan 20) |
| Sababsiz kelmadi | −5 | avtomatik (markaz o‘chirib qo‘yishi mumkin) |

- Har ball yozuvi **daftarga** (ledger) tushadi: kim, qachon, nima uchun, qancha. Balans = yozuvlar yig‘indisi. Ball o‘chirilmaydi — teskari yozuv bilan tuzatiladi.
- Admin/direktor qo‘lda tuzatish kiritsa — sababi majburiy.

### 6.2 Darajalar

| Daraja | Jami ball |
|---|---|
| Boshlovchi | 0 |
| Faol | 300 |
| Bilimdon | 800 |
| Ustoz shogirdi | 1 500 |
| Chempion | 3 000 |

Darajaga jami yig‘ilgan ball hisoblanadi (sovg‘aga sarflash darajani tushirmaydi).

### 6.3 Nishonlar (badge)

| Nishon | Sharti |
|---|---|
| Temir intizom | 30 kun ketma-ket bitta dars qoldirmadi |
| Vazifa ustasi | 20 ta vazifani muddatida topshirdi |
| Oy yulduzi | oy yakunida guruhda 1-o‘rin |
| A’lochi | 5 ta test 90%+ |
| Yaxshi do‘st | do‘stini olib keldi |

### 6.4 Reyting
- **Guruh reytingi** (asosiy) va **markaz reytingi**: hafta / oy / jami.
- Oy reytingi har oy 1-sanada nolga qaytadi; jami ball saqlanadi.
- Ism ko‘rsatilishi: ism + familiyaning birinchi harfi (masalan "Aziza S.").
- O‘quvchi reytingdan yashirinishni tanlashi mumkin (ballari baribir hisoblanadi).

### 6.5 Sovg‘alar do‘koni
- Markaz o‘z sovg‘alarini qo‘shadi: nomi, rasmi, narxi (ballda), soni.
  Masalan: daftar — 300, markaz futbolkasi — 1 000, bitta bepul individual dars — 1 500, oylik to‘lovga 10% chegirma — 2 000.
- O‘quvchi buyurtma beradi → ball **band qilinadi** → admin tasdiqlaydi (ball yechiladi) yoki rad etadi (ball qaytadi).
- Sovg‘a soni tugasa — "tugagan" deb ko‘rinadi.

### 6.6 Markaz sozlamalari
- Gamifikatsiyani yoqish/o‘chirish; har bir qoida uchun ball qiymati va yoqilgan/o‘chirilgan.
- Daraja chegaralari va nomlari.
- Manfiy ballarni yoqish/o‘chirish.
- O‘qituvchi beradigan kunlik ball limiti.

### 6.7 Suiiste’molga qarshi
- Avtomatik ballar faqat bir marta (masalan bitta dars — bitta "keldi" bali). Davomat o‘zgartirilsa, ball ham qayta hisoblanadi.
- O‘qituvchi ballari limitlangan va hisobotda ko‘rinadi.
- Barcha qo‘lda o‘zgartirishlar audit jurnalida.

### 6.8 Hisobotlar (direktor)
- Gamifikatsiya yoqilgandan oldin va keyin: davomat %, vazifa topshirish %, o‘quvchi ketish darajasi.
- Eng faol o‘quvchilar va guruhlar, sarflangan sovg‘alar.

---

## 7. Ma’lumotlar bazasi (asosiy jadvallar)

Har jadvalda `center_id` (markaz) bor; hamma so‘rov shu bo‘yicha filtrlanadi.

```
students(id, center_id, full_name, phone, group_ids, joined_at, billing_day, balance, telegram_chat_id, lang, hide_from_rating)
parents(id, center_id, full_name, phone, telegram_chat_id)
parent_students(parent_id, student_id)
login_codes(id, phone, code_hash, expires_at, attempts)
sessions(id, user_type, user_id, expires_at, device)

lessons(id, center_id, group_id, starts_at, room, teacher_id, topic, status)
materials(id, center_id, lesson_id, kind, url_or_file, title)
homeworks(id, center_id, group_id, title, body, due_at, max_score)
submissions(id, homework_id, student_id, body, file, submitted_at, score, teacher_comment, late)
attendance(id, lesson_id, student_id, status, marked_at, marked_by)
payments(id, center_id, student_id, amount, paid_at, method, period_from, period_to)

point_rules(center_id, code, points, enabled)
point_ledger(id, center_id, student_id, delta, reason_code, source_id, created_by, created_at, comment)
levels(center_id, name, min_points, sort)
badges(id, center_id, code, name, icon, rule)
student_badges(student_id, badge_id, earned_at)
rewards(id, center_id, title, image, cost, stock, active)
reward_orders(id, center_id, student_id, reward_id, status, cost, created_at, decided_by, decided_at)
notifications(id, center_id, recipient_type, recipient_id, kind, payload, status, attempts, send_after)
audit_log(id, center_id, actor, action, entity, entity_id, before, after, created_at)
```

`point_ledger` da `(student_id, reason_code, source_id)` — avtomatik ballar uchun unikal, ikki marta yozilmasligi uchun.

---

## 8. API (kabinet uchun)

```
POST /api/auth/request-code      { phone }
POST /api/auth/verify            { phone, code }
GET  /api/me                     profil, bog‘langan farzandlar (ota-ona uchun)
GET  /api/students/:id/today     bosh sahifa ma’lumotlari
GET  /api/students/:id/schedule?week=
GET  /api/students/:id/lessons
GET  /api/students/:id/homeworks
POST /api/homeworks/:id/submit   (faqat student)
GET  /api/students/:id/attendance?month=
GET  /api/students/:id/payments
GET  /api/students/:id/points    balans, daraja, tarix
GET  /api/groups/:id/rating?period=week|month|all
GET  /api/rewards
POST /api/rewards/:id/order      (faqat student)
```

Admin/o‘qituvchi uchun: ball qo‘shish/tuzatish, sovg‘a qo‘shish, buyurtmani tasdiqlash, gamifikatsiya sozlamalari, eslatma sozlamalari.

---

## 9. Qabul qilish mezonlari

- [ ] O‘quvchi telefon + Telegram kodi bilan kiradi; boshqa o‘quvchining ID sini kiritsa `403`.
- [ ] Ota-ona faqat bog‘langan farzandlarini ko‘radi, vazifa topshira olmaydi.
- [ ] Hamma sahifa 380 px kenglikdagi telefonda to‘liq ishlaydi.
- [ ] Yangi qo‘shilgan o‘quvchi qarzdor bo‘lib ko‘rinmaydi; to‘lov kuni qo‘shilgan kuniga teng.
- [ ] Davomat belgilanishi bilan ball tushadi; davomat o‘zgartirilsa ball tuzatiladi; bir dars uchun ikki marta ball tushmaydi.
- [ ] Sovg‘a buyurtmasi ballni band qiladi, rad etilsa qaytaradi.
- [ ] Oy reytingi har oy 1-sanada nolga qaytadi.
- [ ] Gamifikatsiya o‘chirilgan markazda ballar sahifasi va API yopiq.
- [ ] Telegram eslatmalar sozlamalarga mos keladi, yuborilmagani qayta urinib ko‘riladi.
- [ ] Barcha qo‘lda o‘zgartirishlar audit jurnalida.

---

## 10. Bosqichlar

1. **Kabinet MVP:** kirish, bosh sahifa, jadval, davomat, to‘lovlar, ota-ona akkaunti.
2. **Darslar va vazifalar:** materiallar, vazifa topshirish va baholash, Telegram eslatmalar.
3. **Gamifikatsiya:** ballar daftari, darajalar, reyting.
4. **Sovg‘alar va nishonlar:** do‘kon, buyurtmalar, nishonlar, direktor hisobotlari.
5. **Keyingi:** onlayn to‘lov (Payme/Click), mobil ilova (PWA).
