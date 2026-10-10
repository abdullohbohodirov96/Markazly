/* Markaz sozlamasi (markaz.json) — shablonning YAGONA manbai.

   Yangi markaz uchun kod o'zgarmaydi: nom, aloqa, sayt matnlari, rang,
   ish tartibi va qaysi modullar yoqilgani shu fayldan o'qiladi.
   Boshqa faylni ko'rsatish mumkin: MARKAZ_FILE=/yo'l/markaz.json

   Bu modul brauzerda ham ishlatiladigan OCHIQ qismni ham beradi
   (publicConf) — unda maxfiy narsa yo'q.                              */
'use strict';
const fs = require('fs');
const path = require('path');

const FILE = process.env.MARKAZ_FILE || path.join(__dirname, '..', 'markaz.json');

const DEFAULT_MODULES = {
  sayt: true, darajaTesti: false, kabinet: true, otaOna: true, gamifikatsiya: true,
  onlaynKurs: false, telegramBot: true, tolovBoti: false, kanalViktorina: false
};

function read() {
  let raw = {};
  try { raw = JSON.parse(fs.readFileSync(FILE, 'utf8')); }
  catch (e) {
    if (e.code !== 'ENOENT') throw new Error('markaz.json o‘qilmadi: ' + e.message);
  }
  return normalize(raw);
}

function str(v, max) { return String(v == null ? '' : v).trim().slice(0, max || 300); }

function normalize(raw) {
  const r = raw || {};
  const al = r.aloqa || {};
  const ish = r.ish || {};
  const mods = Object.assign({}, DEFAULT_MODULES);
  Object.keys(r.modullar || {}).forEach(k => { if (k in DEFAULT_MODULES) mods[k] = r.modullar[k] === true; });
  const nom = str(process.env.APP_NAME || r.nom, 80) || 'O‘quv markazi';
  const color = /^#[0-9a-f]{6}$/i.test(String((r.rang || {}).asosiy || '')) ? String(r.rang.asosiy).toLowerCase() : '#16705f';
  const prefix = str(ish.chekPrefiksi, 6).toUpperCase().replace(/[^A-Z0-9]/g, '') || 'MRK';
  const langs = (Array.isArray(ish.tillar) ? ish.tillar : ['uz', 'ru', 'en', 'ar'])
    .filter(l => ['uz', 'ru', 'en', 'ar'].indexOf(l) >= 0);
  if (langs.indexOf('uz') < 0) langs.unshift('uz');
  return {
    nom,
    qisqaNom: str(r.qisqaNom, 30) || nom,
    nomVariantlari: (Array.isArray(r.nomVariantlari) ? r.nomVariantlari : []).map(s => str(s, 80)).filter(Boolean),
    sohasi: str(r.sohasi, 80) || 'O‘quv markazi',
    fan: str(r.fan, 80),
    logoMatn: str(r.logoMatn, 20),
    aloqa: {
      telefon: str(process.env.SITE_PHONE || al.telefon, 30),
      manzil: str(al.manzil, 200),
      shahar: str(al.shahar, 60),
      instagram: str(al.instagram, 200),
      telegramKanal: str(al.telegramKanal, 200),
      telegramQabul: str(al.telegramQabul, 200),
      facebook: str(al.facebook, 200),
      botUsername: str(process.env.TELEGRAM_BOT_USERNAME || al.botUsername, 60).replace(/^@/, '')
    },
    sayt: Object.assign({}, r.sayt || {}, {
      url: str(process.env.SITE_URL || (r.sayt || {}).url, 200).replace(/\/+$/, '')
    }),
    rang: { asosiy: color },
    ish: {
      boshlanish: /^\d{2}:\d{2}$/.test(ish.boshlanish) ? ish.boshlanish : '08:00',
      tugash: /^\d{2}:\d{2}$/.test(ish.tugash) ? ish.tugash : '22:00',
      darsDaqiqa: Math.max(30, Math.min(240, Number(ish.darsDaqiqa) || 80)),
      tolovKuni: Math.max(1, Math.min(31, Number(ish.tolovKuni) || 5)),
      chekPrefiksi: prefix,
      tillar: langs
    },
    modullar: mods
  };
}

const CONF = read();

/** Modul yoqilganmi */
function on(name) { return CONF.modullar[name] === true; }

/** Brauzerga beriladigan ochiq qism (index.html ichiga yoziladi) */
function publicConf() {
  return {
    nom: CONF.nom, qisqaNom: CONF.qisqaNom, sohasi: CONF.sohasi, fan: CONF.fan, logoMatn: CONF.logoMatn,
    aloqa: CONF.aloqa, sayt: CONF.sayt, rang: CONF.rang,
    ish: { darsDaqiqa: CONF.ish.darsDaqiqa, tillar: CONF.ish.tillar, chekPrefiksi: CONF.ish.chekPrefiksi },
    modullar: CONF.modullar
  };
}

/* ---------------- Rang palitrasi (bitta asosiy rangdan) ---------------- */
function hexToRgb(h) { const n = parseInt(h.slice(1), 16); return [n >> 16 & 255, n >> 8 & 255, n & 255]; }
function rgbToHex(r) { return '#' + r.map(v => Math.max(0, Math.min(255, Math.round(v))).toString(16).padStart(2, '0')).join(''); }
function mix(h, to, t) { const a = hexToRgb(h), b = hexToRgb(to); return rgbToHex(a.map((v, i) => v + (b[i] - v) * t)); }
function palette() {
  const B = CONF.rang.asosiy;
  return {
    brand: B, deep: mix(B, '#000000', 0.35), light: mix(B, '#ffffff', 0.18), soft: mix(B, '#ffffff', 0.88),
    dBrand: mix(B, '#ffffff', 0.38), dDeep: mix(B, '#ffffff', 0.55), dLight: mix(B, '#ffffff', 0.46),
    dSoft: mix(B, '#151b27', 0.78), dActive: mix(B, '#151b27', 0.45)
  };
}
function colorTag() {
  const P = palette();
  const dark = `--brand:${P.dBrand};--brand-deep:${P.dDeep};--brand-light:${P.dLight};--brand-soft:${P.dSoft};--side-active-bg:${P.dActive}`;
  return `<style id="markaz-rang">
:root{--brand:${P.brand};--brand-deep:${P.deep};--brand-light:${P.light};--brand-soft:${P.soft};--side-bg:${P.deep};--side-active-ink:${P.deep}}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){${dark}}}
:root[data-theme="dark"]{${dark}}
</style>`;
}
/** Brauzer uchun ochiq sozlama (inline skript; '<' ekranlanadi) */
function markazTag() {
  return '<script>window.MARKAZ = ' + JSON.stringify(publicConf()).replace(/</g, '\\u003c') + ';</script>';
}
/** index.html dagi eski teglarni joriy markaz.json bilan almashtirish */
function injectInto(html) {
  return String(html)
    .replace(/<style id="markaz-rang">[\s\S]*?<\/style>/, () => colorTag())
    .replace(/<script>window\.MARKAZ = [\s\S]*?<\/script>/, () => markazTag());
}

module.exports = { CONF, on, publicConf, normalize, FILE, palette, colorTag, markazTag, injectInto };
