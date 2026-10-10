/* Gamifikatsiya: XP, daraja, tanga, nishonlar va reyting.

   ASOSIY QOIDA: ball HECH QACHON mijozdan kelmaydi va alohida "hisoblagich"
   sifatida saqlanmaydi. Har safar markazning haqiqiy ma'lumotidan qayta
   hisoblanadi: davomat, test natijalari, onlayn kurs, o'z vaqtida to'lov,
   ustoz rag'bati. Shuning uchun uni soxtalashtirib bo'lmaydi — davomatni
   o'zgartirgan odam (ustoz) bilan ball ham o'zgaradi, tarix ham qoladi.

   Saqlanadigan yagona narsalar:
     gamebonus/<id>  — ustoz rag'bati { studentId, xp, reason, by, byName, at }
     gameorder/<id>  — sovg'a so'rovi { studentId, rewardId, name, cost, status, at }
   Sozlama: meta/settings.game { xp: {...}, coinRate, rewards: [{id,name,cost}] } */
'use strict';

const DEFAULT_XP = {
  attend: 10,        // darsga keldi
  late: 5,           // kechikib keldi
  homework: 15,      // uy vazifasini bajargan (ustoz davomatda belgilaydi)
  active: 5,         // darsda faol qatnashdi (ustoz belgilaydi)
  quizMax: 10,       // test: foizga qarab 0..10
  quizPerfect: 10,   // 100% uchun qo'shimcha
  courseLesson: 30,  // onlayn kurs: dars testi o'tildi
  courseHw: 20,      // onlayn kurs: vazifa qabul qilindi (+baho*2)
  question: 2,       // ustozga savol berdi
  onTimePay: 15      // hisob muddatida to'landi
};
const BONUS_MAX = 50;

const LEVEL_NAMES = ['Yangi boshlovchi', 'Izlanuvchi', 'Faol', 'Bilimdon', 'Ilg‘or', 'Chempion', 'Ustoz shogirdi', 'Afsona'];
/** L-darajaga yetish uchun kerak XP: 0, 100, 300, 600, 1000, 1500 … */
function levelStart(L) { return 50 * L * (L - 1); }
function levelOf(xp) {
  let L = 1;
  while (xp >= levelStart(L + 1)) L++;
  const from = levelStart(L), to = levelStart(L + 1);
  return {
    n: L, name: LEVEL_NAMES[Math.min(L - 1, LEVEL_NAMES.length - 1)],
    from, to, inLevel: xp - from, need: to - from,
    percent: Math.round((xp - from) * 100 / (to - from))
  };
}

const BADGES = [
  { id: 'birinchi', icon: '🎯', name: 'Birinchi qadam', text: 'Birinchi darsga keldi' },
  { id: 'intizom10', icon: '🔥', name: 'Intizomli', text: 'Ketma-ket 10 ta darsni qoldirmadi' },
  { id: 'intizom30', icon: '🏅', name: 'Temir intizom', text: 'Ketma-ket 30 ta darsni qoldirmadi' },
  { id: 'vazifa10', icon: '📚', name: 'Tirishqoq', text: '10 ta uy vazifasini bajardi' },
  { id: 'faol10', icon: '🙋', name: 'Faol', text: 'Darsda 10 marta faol bo‘ldi' },
  { id: 'alochi', icon: '⭐', name: 'A’lochi', text: 'Testdan 100% oldi' },
  { id: 'alochi5', icon: '🌟', name: 'Yulduz', text: '5 ta testdan 100% oldi' },
  { id: 'qiziquvchan', icon: '💡', name: 'Qiziquvchan', text: 'Ustozga 5 ta savol berdi' },
  { id: 'masul', icon: '🤝', name: 'Mas’uliyatli', text: '3 oy to‘lovni o‘z vaqtida qildi' },
  { id: 'xp500', icon: '🚀', name: '500 XP', text: '500 XP to‘pladi' },
  { id: 'xp1500', icon: '👑', name: '1500 XP', text: '1500 XP to‘pladi' },
  { id: 'kurs5', icon: '📘', name: 'Kitobxon', text: 'Onlayn kursda 5 ta darsni tugatdi' }
];

function conf(settings) {
  const g = (settings && settings.game) || {};
  const xp = Object.assign({}, DEFAULT_XP);
  Object.keys(DEFAULT_XP).forEach(k => {
    const v = Number(g.xp && g.xp[k]);
    if (Number.isFinite(v) && v >= 0 && v <= 500) xp[k] = Math.round(v);
  });
  const coinRate = Math.max(1, Math.min(1000, Math.round(Number(g.coinRate) || 10)));
  const rewards = (Array.isArray(g.rewards) ? g.rewards : []).slice(0, 30)
    .map(r => ({ id: String(r.id || '').slice(0, 40), name: String(r.name || '').slice(0, 80), cost: Math.max(1, Math.round(Number(r.cost) || 0)) }))
    .filter(r => r.id && r.name && r.cost);
  /* Gamifikatsiya Sozlamalarda yoqiladi (sukut bo'yicha o'chiq) */
  return { xp, coinRate, rewards, enabled: g.enabled === true };
}

async function listCol(store, prefix) {
  return (await store.list(prefix)).filter(r => r.path.split('/').length === 2).map(r => r.data).filter(Boolean);
}

/** Bir nechta o'quvchi uchun kerakli ma'lumotni BIR MARTA yuklash */
async function loadCtx(store, opts) {
  const settings = (await store.get('meta/settings')) || {};
  const all = await store.all();
  const ctx = {
    conf: conf(settings),
    course: !!(opts && opts.course),
    memberships: [], lessons: [], quizres: [], questions: [], bonuses: [], orders: [],
    invoices: [], payments: [], courseprog: {}, students: {}
  };
  for (const { path: p, data } of all) {
    if (!data) continue;
    const seg = p.split('/');
    const col = seg[0];
    if (col === 'lessons') ctx.lessons.push({ gid: String(seg[1] || '').split('__')[0], doc: data });
    else if (seg.length !== 2) continue;
    else if (col === 'memberships') ctx.memberships.push(data);
    else if (col === 'quizres') ctx.quizres.push(data);
    else if (col === 'questions') ctx.questions.push(data);
    else if (col === 'gamebonus') ctx.bonuses.push(data);
    else if (col === 'gameorder') ctx.orders.push(data);
    else if (col === 'invoices') ctx.invoices.push(data);
    else if (col === 'payments') ctx.payments.push(data);
    else if (col === 'courseprog') ctx.courseprog[seg[1]] = data;
    else if (col === 'students') ctx.students[data.id] = data;
  }
  return ctx;
}

/** Bitta o'quvchining barcha XP hodisalari (eng yangisi birinchi) */
function eventsOf(ctx, sid) {
  const X = ctx.conf.xp;
  const ev = [];
  const mids = {};
  ctx.memberships.filter(m => String(m.studentId) === String(sid)).forEach(m => { mids[m.id] = m.groupId; });

  /* Davomat */
  const att = [];
  ctx.lessons.forEach(({ gid, doc }) => {
    const items = doc.items || {};
    Object.keys(items).forEach(date => {
      const day = items[date] || {};
      if (day.status === 'bekor') return;
      Object.keys(mids).forEach(mid => {
        if (mids[mid] !== gid) return;
        const v = (day.attendance || {})[mid];
        const st = String((v && v.status) || v || '');
        if (st) att.push({ date, st, hw: v && v.hw, faol: !!(v && v.faol) });
      });
    });
  });
  att.sort((a, b) => a.date.localeCompare(b.date));
  let streak = 0, bestStreak = 0, attended = 0, hwDone = 0, activeN = 0;
  att.forEach(a => {
    if (a.st === 'keldi' || a.st === 'kechikdi') {
      attended++; streak++; bestStreak = Math.max(bestStreak, streak);
      ev.push({ at: a.date, xp: a.st === 'keldi' ? X.attend : X.late, kind: 'davomat', text: a.st === 'keldi' ? 'Darsga keldi' : 'Darsga kechikib keldi' });
    } else if (a.st === 'kelmadi') {
      streak = 0;
    }   // 'sababli' seriyani uzmaydi
    if (a.hw === 'ha') { hwDone++; ev.push({ at: a.date, xp: X.homework, kind: 'vazifa', text: 'Uy vazifasini bajardi' }); }
    if (a.faol) { activeN++; ev.push({ at: a.date, xp: X.active, kind: 'faol', text: 'Darsda faol qatnashdi' }); }
  });

  /* Testlar */
  let perfect = 0;
  ctx.quizres.filter(r => String(r.studentId) === String(sid)).forEach(r => {
    const pct = r.total ? Math.round((Number(r.score) || 0) * 100 / r.total) : 0;
    let xp = Math.round(pct * X.quizMax / 100);
    if (pct === 100) { xp += X.quizPerfect; perfect++; }
    ev.push({ at: String(r.at || '').slice(0, 10), xp, kind: 'test', text: 'Test: ' + pct + '%' });
  });

  /* Savollar */
  const asked = ctx.questions.filter(q => String(q.studentId) === String(sid));
  asked.forEach(q => ev.push({ at: String(q.at || '').slice(0, 10), xp: X.question, kind: 'savol', text: 'Ustozga savol berdi' }));

  /* Onlayn kurs */
  let courseDone = 0;
  if (ctx.course && ctx.courseprog[sid]) {
    const ls = ctx.courseprog[sid].lessons || {};
    Object.keys(ls).forEach(lid => {
      const p = ls[lid] || {};
      if (p.steps && p.steps.test) {
        courseDone++;
        ev.push({ at: String(p.steps.test).slice(0, 10), xp: X.courseLesson, kind: 'kurs', text: 'Kurs darsi o‘tildi' });
      }
      if (p.hw && p.hw.status === 'qabul') {
        ev.push({ at: String(p.hw.submittedAt || '').slice(0, 10), xp: X.courseHw + 2 * (Number(p.hw.grade) || 0), kind: 'kurs', text: 'Vazifa qabul qilindi' + (p.hw.grade ? ' (baho ' + p.hw.grade + ')' : '') });
      }
    });
  }

  /* O'z vaqtida to'lov: hisob muddatigacha to'liq yopilgan */
  let onTime = 0;
  const myInv = ctx.invoices.filter(i => String(i.studentId) === String(sid) && !i.voided && Number(i.final) > 0 && i.dueDate);
  if (myInv.length) {
    const paidBy = {};
    ctx.payments.filter(p => String(p.studentId) === String(sid) && !p.voided && p.type !== 'refund').forEach(p => {
      (p.allocations || []).forEach(a => {
        (paidBy[a.invoiceId] = paidBy[a.invoiceId] || []).push({ date: String(p.date || ''), amount: Number(a.amount) || 0 });
      });
    });
    myInv.forEach(inv => {
      const sum = (paidBy[inv.id] || []).filter(x => x.date && x.date <= inv.dueDate).reduce((n, x) => n + x.amount, 0);
      if (sum >= Number(inv.final)) {
        onTime++;
        ev.push({ at: inv.dueDate, xp: X.onTimePay, kind: 'tolov', text: 'To‘lov o‘z vaqtida' });
      }
    });
  }

  /* Ustoz rag'bati */
  ctx.bonuses.filter(b => String(b.studentId) === String(sid)).forEach(b => {
    ev.push({ at: String(b.at || '').slice(0, 10), xp: Number(b.xp) || 0, kind: 'ragbat', text: (b.xp >= 0 ? 'Rag‘bat: ' : 'Jarima: ') + (b.reason || '') + (b.byName ? ' — ' + b.byName : '') });
  });

  ev.sort((a, b) => String(b.at).localeCompare(String(a.at)));
  return { ev, meta: { attended, bestStreak, perfect, asked: asked.length, onTime, courseDone, hwDone, activeN } };
}

function statsFrom(ctx, sid, ym) {
  const { ev, meta } = eventsOf(ctx, sid);
  const xp = Math.max(0, ev.reduce((n, e) => n + e.xp, 0));
  const monthXp = Math.max(0, ev.filter(e => String(e.at).slice(0, 7) === ym).reduce((n, e) => n + e.xp, 0));
  const spent = ctx.orders.filter(o => String(o.studentId) === String(sid) && o.status !== 'rad')
    .reduce((n, o) => n + (Number(o.cost) || 0), 0);
  const coins = Math.max(0, Math.floor(xp / ctx.conf.coinRate) - spent);
  const has = {
    birinchi: meta.attended >= 1, intizom10: meta.bestStreak >= 10, intizom30: meta.bestStreak >= 30,
    alochi: meta.perfect >= 1, alochi5: meta.perfect >= 5, qiziquvchan: meta.asked >= 5,
    masul: meta.onTime >= 3, vazifa10: meta.hwDone >= 10, faol10: meta.activeN >= 10, xp500: xp >= 500, xp1500: xp >= 1500, kurs5: meta.courseDone >= 5
  };
  const badges = BADGES.filter(b => b.id !== 'kurs5' || ctx.course).map(b => Object.assign({ got: !!has[b.id] }, b));
  return { xp, monthXp, level: levelOf(xp), coins, spent, badges, streak: meta.bestStreak, history: ev.slice(0, 25) };
}

/** Ism + familiyaning bosh harfi (reytingda boshqalarga to'liq ism ko'rsatilmaydi) */
function shortName(st) {
  if (!st) return '—';
  const ln = String(st.lastName || '').trim();
  return (String(st.firstName || '').trim() + (ln ? ' ' + ln[0] + '.' : '')).trim() || '—';
}

/** Guruh reytingi: { rows: [{studentId, name, xp, monthXp, level}], } */
function boardFrom(ctx, gid, ym, meId, full) {
  const sids = {};
  ctx.memberships.filter(m => m.groupId === gid && m.status !== 'chiqdi' && m.status !== 'arxiv').forEach(m => { sids[m.studentId] = 1; });
  const rows = Object.keys(sids).map(sid => {
    const s = statsFrom(ctx, sid, ym);
    const st = ctx.students[sid];
    return {
      studentId: sid, me: sid === String(meId || ''),
      name: full ? ((st ? ((st.lastName || '') + ' ' + (st.firstName || '')).trim() : sid)) : shortName(st),
      xp: s.xp, monthXp: s.monthXp, level: s.level.n, coins: full ? s.coins : undefined
    };
  });
  rows.sort((a, b) => (b.monthXp - a.monthXp) || (b.xp - a.xp) || a.name.localeCompare(b.name));
  /* Teng ball — teng o'rin */
  rows.forEach((r, i) => {
    const prev = rows[i - 1];
    r.rank = (prev && prev.monthXp === r.monthXp && prev.xp === r.xp) ? prev.rank : i + 1;
  });
  return rows;
}

/** O'quvchi kabineti uchun to'liq ma'lumot */
async function forStudent(store, sid, opts) {
  const ctx = await loadCtx(store, opts);
  const ym = (opts && opts.ym) || '';
  const me = statsFrom(ctx, sid, ym);
  const gids = {};
  ctx.memberships.filter(m => String(m.studentId) === String(sid) && m.status !== 'chiqdi').forEach(m => { gids[m.groupId] = 1; });
  const boards = [];
  for (const gid of Object.keys(gids)) {
    const g = await store.get('groups/' + gid);
    const rows = boardFrom(ctx, gid, ym, sid, false);
    const mine = rows.find(r => r.me);
    boards.push({
      groupId: gid, group: g ? g.name : '', size: rows.length, myRank: mine ? mine.rank : null,
      top: rows.slice(0, 10).map(r => ({ rank: r.rank, name: r.name, monthXp: r.monthXp, level: r.level, me: r.me }))
    });
  }
  const myOrders = ctx.orders.filter(o => String(o.studentId) === String(sid))
    .sort((a, b) => String(b.at).localeCompare(String(a.at))).slice(0, 20);
  return Object.assign(me, { boards, rewards: ctx.conf.rewards, orders: myOrders, coinRate: ctx.conf.coinRate, xpRules: ctx.conf.xp });
}

/** Xodim uchun: guruh reytingi (to'liq ism bilan) */
async function forGroup(store, gid, opts) {
  const ctx = await loadCtx(store, opts);
  return { rows: boardFrom(ctx, gid, (opts && opts.ym) || '', null, true) };
}

/** Xodim uchun: bitta o'quvchi */
async function studentStats(store, sid, opts) {
  const ctx = await loadCtx(store, opts);
  return statsFrom(ctx, sid, (opts && opts.ym) || '');
}

/** Ustoz rag'bati (yoki jarimasi): -50..+50 */
async function addBonus(store, data, opts) {
  const sid = String((data && data.studentId) || '').slice(0, 60);
  const xp = Math.round(Number(data && data.xp));
  const reason = String((data && data.reason) || '').trim().slice(0, 120);
  if (!sid || !(await store.get('students/' + sid))) return { ok: false, reason: 'oquvchi' };
  if (!Number.isFinite(xp) || xp === 0 || Math.abs(xp) > BONUS_MAX) return { ok: false, reason: 'xp' };
  if (reason.length < 2) return { ok: false, reason: 'sabab' };
  const id = 'gb_' + Date.now().toString(36) + require('crypto').randomBytes(3).toString('hex');
  const rec = { id, studentId: sid, xp, reason, by: String(opts.byUserId || ''), byName: String(opts.byName || ''), at: opts.stamp() };
  await store.set('gamebonus/' + id, rec);
  return { ok: true, rec };
}

/** O'quvchi sovg'a so'raydi: tanga yetarli bo'lsa — kutilmoqda */
async function order(store, sid, rewardId, opts) {
  const ctx = await loadCtx(store, opts);
  const r = ctx.conf.rewards.find(x => x.id === String(rewardId || ''));
  if (!r) return { ok: false, reason: 'topilmadi' };
  const s = statsFrom(ctx, sid, '');
  if (s.coins < r.cost) return { ok: false, reason: 'tanga' };
  if (ctx.orders.some(o => String(o.studentId) === String(sid) && o.status === 'kutilmoqda' && o.rewardId === r.id)) {
    return { ok: false, reason: 'takror' };
  }
  const id = 'go_' + Date.now().toString(36) + require('crypto').randomBytes(3).toString('hex');
  const rec = { id, studentId: String(sid), rewardId: r.id, name: r.name, cost: r.cost, status: 'kutilmoqda', at: opts.stamp() };
  await store.set('gameorder/' + id, rec);
  return { ok: true, rec };
}

module.exports = {
  DEFAULT_XP, BONUS_MAX, BADGES, LEVEL_NAMES, levelOf, levelStart, conf,
  forStudent, forGroup, studentStats, addBonus, order, shortName
};
