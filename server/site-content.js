/* Ochiq sayt uchun YAGONA matn manbai: sarlavha, tavsif, nom variantlari,
   savol-javoblar va qidiruv tizimlari uchun statik matn.

   Shu fayldan foydalanadi:
     — build.js        → index.html (statik sayt va server uchun asos);
     — server/seo.js   → serverda sozlamalar bilan to'ldirilgan HTML;
     — js/app.js       → savol-javob sozlamada bo'sh bo'lsa (window.SITE_FAQ).
   Bitta joyda o'zgartirilsa — hamma joyda bir xil bo'ladi.

   Qoidalar: narx yozilmaydi, diniy ibora ishlatilmaydi, faqat haqiqiy
   ma'lumot (markaz o'zi aytgan: haftada 3 marta, 80 daqiqa, 10 kishigacha,
   ayollar/erkaklar/bolalar alohida, online va offline).                */
'use strict';

const M = require('./markaz').CONF;
const SAYT = M.sayt || {};

const NAME = M.nom;

/* Standart aloqa (statik sayt uchun; serverda Sozlamadagisi ishlatiladi) */
const PHONE = M.aloqa.telefon;
const LINKS = [
  { label: 'Instagram', url: M.aloqa.instagram },
  { label: 'Telegram kanal', url: M.aloqa.telegramKanal },
  { label: 'Facebook', url: M.aloqa.facebook }
];
const FACEBOOK = M.aloqa.facebook;

/* Saytda harf-harf yoziladigan shiorlar (Sozlamada o'zgartiriladi) */
const TAGLINES = (Array.isArray(SAYT.shiorlar) ? SAYT.shiorlar : []).join('\n');

/* Odamlar nomni turlicha yozadi — hammasi shu saytga olib kelsin */
const ALT_NAMES = (process.env.APP_ALT_NAMES
  ? String(process.env.APP_ALT_NAMES).split(',')
  : [NAME].concat(M.nomVariantlari))
  .map(s => s.trim()).filter(Boolean);

/* ~60 belgi: brend oldinda (nom bo'yicha qidiruv), keyin asosiy so'z */
const TITLE = String(SAYT.sarlavha || (NAME + ' — ' + M.sohasi)).slice(0, 90);

/* ~155 belgi: kim, nima, qanday, chaqiruv */
const DESC = String(SAYT.tavsif || (NAME + ' — ' + M.sohasi.toLowerCase() + '. ' +
  (SAYT.heroLead || 'Tajribali ustozlar, kichik guruhlar. Tekin darsga yoziling!'))).slice(0, 220);

const FAQ = (Array.isArray(SAYT.faq) ? SAYT.faq : [])
  .filter(f => f && f.q && f.a).map(f => ({ q: String(f.q), a: String(f.a) }));

/* JavaScript ishlatmaydigan robotlar va qidiruv tizimlari uchun matn.
   <noscript> ichida — brauzerda ko'rinmaydi, lekin HTML da o'qiladi. */
function seoText(o) {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, ch => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[ch]);
  const name = esc(o.name || NAME);
  const phone = String(o.phone || '').trim();
  const tel = phone.replace(/[^+0-9]/g, '');
  const parts = [
    '<noscript><main id="seo-prerender" style="max-width:860px;margin:24px auto;padding:28px;font:16px/1.6 system-ui,sans-serif;color:#222;background:#fff;border-radius:18px">',
    '<h1>' + name + ' — ' + esc(M.sohasi) + '</h1>',
    '<p><strong>' + name + '</strong> — ' + esc(SAYT.heroLead || M.sohasi) + '</p>',
    (Array.isArray(SAYT.natijaBosqichlar) && SAYT.natijaBosqichlar.length
      ? '<h2>' + esc(SAYT.natijaSarlavha || 'Natija yo‘li') + '</h2><ul>' +
        SAYT.natijaBosqichlar.map(b => '<li>' + esc(b.qachon) + ': ' + esc(b.nomi) + '</li>').join('') + '</ul>'
      : ''),
    '<h2>Tekin dars</h2>',
    '<p>Birinchi dars — tekin. Raqamingizni qoldiring yoki qo‘ng‘iroq qiling.</p>',
  ];
  if (FAQ.length) parts.push('<h2>Ko‘p so‘raladigan savollar</h2>');
  FAQ.forEach(f => parts.push('<h3>' + esc(f.q) + '</h3><p>' + esc(f.a) + '</p>'));
  parts.push('<h2>Bog‘lanish</h2>');
  if (phone) parts.push('<p>Telefon: <a href="tel:' + esc(tel) + '">' + esc(phone) + '</a></p>');
  if (o.address) parts.push('<p>Manzil: ' + esc(o.address) + '</p>');
  (o.links || []).filter(l => l && l.url).forEach(l => parts.push('<p><a href="' + esc(l.url) + '">' + esc(l.label) + '</a></p>'));
  parts.push('</main></noscript>');
  return parts.join('');
}

/* schema.org FAQPage — Google savol-javobni tushunadi */
function faqLd() {
  return {
    '@type': 'FAQPage',
    mainEntity: FAQ.map(f => ({
      '@type': 'Question', name: f.q,
      acceptedAnswer: { '@type': 'Answer', text: f.a }
    }))
  };
}

/* schema.org Course — markaz yo'nalishi (markaz.json dagi soha va tavsif) */
function courseLd(providerId) {
  return {
    '@type': 'Course',
    name: M.sohasi,
    description: DESC,
    inLanguage: 'uz',
    provider: { '@id': providerId }
  };
}
const CITY = M.aloqa.shahar || 'Toshkent';

module.exports = { courseLd, CITY, NAME, PHONE, LINKS, FACEBOOK, TAGLINES, ALT_NAMES, TITLE, DESC, FAQ, seoText, faqLd };
