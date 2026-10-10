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
    nom: CONF.nom, qisqaNom: CONF.qisqaNom, sohasi: CONF.sohasi, logoMatn: CONF.logoMatn,
    aloqa: CONF.aloqa, sayt: CONF.sayt, rang: CONF.rang,
    ish: { darsDaqiqa: CONF.ish.darsDaqiqa, tillar: CONF.ish.tillar, chekPrefiksi: CONF.ish.chekPrefiksi },
    modullar: CONF.modullar
  };
}

module.exports = { CONF, on, publicConf, normalize, FILE };
