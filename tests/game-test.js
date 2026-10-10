/* Gamifikatsiya — server tomoni.
   Tekshiriladi: sozlamada yoqish/o'chirish, davomat + vazifa + faollikdan XP,
   ustoz rag'bati (faqat o'z o'quvchisiga, chegarali), tanga va sovg'a so'rovi,
   reyting, mijoz ballni o'zi yoza olmasligi.
   Sinov o'zi alohida server ko'taradi:  node tests/game-test.js            */
'use strict';
const fs = require('fs'), os = require('os'), path = require('path');
const { spawn } = require('child_process');

const PASS = 'Albyana2026!';
const PORT = 4100 + Math.floor(Math.random() * 80);
const BASE = 'http://localhost:' + PORT;
const DIR = fs.mkdtempSync(path.join(os.tmpdir(), 'markaz-game-'));
let srv = null;

async function boot() {
  srv = spawn(process.execPath, [path.join(__dirname, '..', 'server', 'index.js')], {
    env: Object.assign({}, process.env, {
      DATA_DIR: DIR, PORT: String(PORT), DATABASE_URL: '', BACKUP_DIR: path.join(DIR, 'bk'),
      FILES_DIR: path.join(DIR, 'files'), SEED_DIRECTOR_PASSWORD: PASS, TELEGRAM_BOT_TOKEN: '',
      MARKAZ_FILE: process.env.MARKAZ_FILE || path.join(__dirname, 'markaz.test.json')
    }),
    stdio: 'ignore'
  });
  for (let i = 0; i < 80; i++) {
    if (await fetch(BASE + '/api/health').then(r => r.status).catch(() => 0) === 200) return true;
    await new Promise(r => setTimeout(r, 300));
  }
  return false;
}
function stop() { try { srv && srv.kill(); } catch (e) { } try { fs.rmSync(DIR, { recursive: true, force: true }); } catch (e) { } }

let pass = 0, fail = 0; const out = [];
function ok(n, c, e) { if (c) { pass++; out.push('  ✓ ' + n); } else { fail++; out.push('  ✗ ' + n + (e ? '  → ' + String(e).slice(0, 220) : '')); } }
function eq(n, got, want) { ok(n, got === want, 'kutilgan ' + JSON.stringify(want) + ', olindi ' + JSON.stringify(got)); }
function section(t) { out.push('\n' + t); }
async function req(p, o = {}) {
  const r = await fetch(BASE + p, {
    method: o.method || (o.body ? 'POST' : 'GET'),
    headers: Object.assign(o.body ? { 'Content-Type': 'application/json' } : {}, o.cookie ? { Cookie: o.cookie } : {}, o.csrf ? { 'X-Kab-Csrf': o.csrf } : {}),
    body: o.body ? JSON.stringify(o.body) : undefined
  });
  const t = await r.text(); let j = null; try { j = JSON.parse(t); } catch (e) { }
  return { status: r.status, json: j, text: t, cookie: (r.headers.get('set-cookie') || '').split(';')[0] };
}
const login = (l, p) => req('/api/login', { body: { login: l, password: p } }).then(r => r.cookie);
const put = (p, data, cookie, extra) => req('/api/doc?path=' + encodeURIComponent(p), { method: 'PUT', cookie, body: Object.assign({ data }, extra || {}) });
const get = (p, cookie) => req('/api/doc?path=' + encodeURIComponent(p), { cookie });

(async () => {
  if (!await boot()) { stop(); console.error('Server ko‘tarilmadi'); process.exit(1); }
  const dir = await login('admin', PASS);
  ok('Direktor kirdi', !!dir);
  const ym = new Date(Date.now() + 5 * 3600e3).toISOString().slice(0, 7);
  const d1 = ym + '-02', d2 = ym + '-04';

  await put('staff/t1', { id: 't1', name: 'Ustoz', status: 'faol' }, dir);
  await put('staff/t2', { id: 't2', name: 'Begona', status: 'faol' }, dir);
  await put('groups/g1', { id: 'g1', name: 'A guruh', teacherId: 't1', days: [1, 3], startTime: '10:00', endTime: '11:30', startDate: ym + '-01', fee: 300000, status: 'faol' }, dir);
  await put('groups/g2', { id: 'g2', name: 'B guruh', teacherId: 't2', days: [2, 4], startTime: '10:00', endTime: '11:30', startDate: ym + '-01', fee: 300000, status: 'faol' }, dir);
  for (const [s, g, fn] of [['s1', 'g1', 'Ali'], ['s2', 'g1', 'Vali'], ['s3', 'g2', 'Soli']]) {
    await put('students/' + s, { id: s, firstName: fn, lastName: 'Karimov', phone: '+99890111223' + s.slice(-1), status: 'faol' }, dir);
    await put('memberships/m' + s, { id: 'm' + s, studentId: s, groupId: g, status: 'faol', joinedAt: ym + '-01' }, dir);
  }
  await put('users/u1', { id: 'u1', login: 'ustoz1', name: 'Ustoz', role: 'oqituvchi', staffId: 't1', active: true }, dir, { password: 'Ustoz12345x' });
  const teach = await login('ustoz1', 'Ustoz12345x');
  ok('Ustoz kirdi', !!teach);
  const s1 = (await get('students/s1', dir)).json.data;
  const kab = await req('/api/kabinet', { body: { code: s1.code } });
  eq('O‘quvchi kabinetga kirdi', kab.status, 200);

  section('1. Sukut bo‘yicha o‘chiq');
  const off = await req('/api/kabinet/game', { cookie: kab.cookie });
  eq('Kabinet: yoqilmagan', off.json && off.json.enabled, false);
  eq('kabinet/me: gameOn yo‘q', (await req('/api/kabinet/me', { cookie: kab.cookie })).json.gameOn, false);

  section('2. Sozlamada yoqiladi va ballar beriladi');
  const st = (await get('meta/settings', dir)).json.data;
  st.game = { enabled: true, xp: { attend: 10, late: 5, homework: 15, active: 5, quizMax: 10, quizPerfect: 10, question: 2, onTimePay: 15 }, coinRate: 10, rewards: [{ id: 'r1', name: 'Ruchka', cost: 2 }] };
  eq('Sozlama saqlandi', (await put('meta/settings', st, dir)).status, 200);
  eq('Ustoz sozlamani o‘zgartira olmaydi', (await put('meta/settings', Object.assign({}, st, { game: { enabled: false } }), teach)).status, 403);

  const lesson = { items: {} };
  lesson.items[d1] = { status: 'otkazildi', attendance: { ms1: { status: 'keldi', hw: 'ha', faol: true }, ms2: { status: 'kechikdi', hw: 'xato-qiymat' } } };
  lesson.items[d2] = { status: 'otkazildi', attendance: { ms1: { status: 'kelmadi' }, ms2: { status: 'keldi', hw: 'yoq' } } };
  eq('Ustoz davomatni vazifa/faollik bilan saqladi', (await put('lessons/g1__' + ym, lesson, teach)).status, 200);
  const saved = (await get('lessons/g1__' + ym, dir)).json.data;
  ok('Noto‘g‘ri vazifa qiymati olib tashlandi', saved.items[d1].attendance.ms2.hw === undefined, JSON.stringify(saved.items[d1].attendance.ms2));

  const g1 = await req('/api/kabinet/game', { cookie: kab.cookie });
  eq('Kabinet: yoqilgan', g1.json.enabled, true);
  eq('XP = keldi 10 + vazifa 15 + faol 5', g1.json.xp, 30);
  eq('Shu oy XP', g1.json.monthXp, 30);
  eq('Tanga = 30/10', g1.json.coins, 3);
  eq('1-daraja', g1.json.level.n, 1);
  ok('“Birinchi qadam” nishoni olindi', g1.json.badges.some(b => b.id === 'birinchi' && b.got));
  ok('Tarixda vazifa bor', g1.json.history.some(e => /vazifa/i.test(e.text)));
  eq('kabinet/me: gameOn', (await req('/api/kabinet/me', { cookie: kab.cookie })).json.gameOn, true);

  section('2b. Soxta davomat bilan ball yig‘ib bo‘lmaydi');
  eq('Noto‘g‘ri manzilli davomat hujjati rad etildi', (await put('lessons/g1__soxta', { items: { [d1]: { attendance: { ms1: { status: 'keldi' } } } } }, teach)).status, 403);
  eq('Boshqa oy sanasi rad etildi', (await put('lessons/g1__' + ym, { items: { '2020-01-01': { attendance: { ms1: { status: 'keldi' } } } } }, teach)).status, 403);
  const fut = new Date(Date.now() + 5 * 3600e3 + 40 * 864e5).toISOString().slice(0, 10);
  eq('Kelajakdagi darsga davomat — yo‘q', (await put('lessons/g1__' + fut.slice(0, 7), { items: { [fut]: { attendance: { ms1: { status: 'keldi', hw: 'ha' } } } } }, teach)).status, 403);
  const l2 = (await get('lessons/g1__' + ym, dir)).json.data;
  ok('Kelmagan o‘quvchiga vazifa belgisi yo‘q', l2.items[d2].attendance.ms1.hw === undefined);
  {
    const cp = await get('courseprog/s3', teach);
    ok('Ustoz begona o‘quvchi kurs yozuvini o‘qiy olmaydi', cp.status === 403 || (cp.json && cp.json.data == null), cp.status);
  }

  section('3. Ustoz rag‘bati');
  eq('O‘z o‘quvchisiga +10', (await req('/api/game/bonus', { cookie: teach, body: { studentId: 's1', xp: 10, reason: 'Faol qatnashdi' } })).status, 200);
  eq('Begona guruh o‘quvchisiga — yo‘q', (await req('/api/game/bonus', { cookie: teach, body: { studentId: 's3', xp: 10, reason: 'x x' } })).status, 403);
  eq('Chegaradan katta ball — yo‘q', (await req('/api/game/bonus', { cookie: teach, body: { studentId: 's1', xp: 999, reason: 'ko‘p' } })).status, 400);
  eq('Sababsiz — yo‘q', (await req('/api/game/bonus', { cookie: teach, body: { studentId: 's1', xp: 5, reason: '' } })).status, 400);
  eq('Rag‘bat yozuvini qo‘lda yozib bo‘lmaydi', (await put('gamebonus/x1', { id: 'x1', studentId: 's1', xp: 500 }, dir)).status, 403);
  const g2 = await req('/api/kabinet/game', { cookie: kab.cookie });
  eq('XP 40 bo‘ldi', g2.json.xp, 40);

  section('4. Reyting');
  const board = await req('/api/game/group?id=g1', { cookie: teach });
  eq('Ustoz guruh reytingini ko‘radi', board.status, 200);
  eq('1-o‘rinda Ali', board.json.rows[0].studentId, 's1');
  eq('Ustoz begona guruh reytingini ko‘rmaydi', (await req('/api/game/group?id=g2', { cookie: teach })).status, 403);
  const myBoard = g2.json.boards[0];
  ok('Kabinetda boshqalarning familiyasi qisqartirilgan', myBoard.top.every(r => /^[^ ]+( [A-ZА-Я]\.)?$/.test(r.name)), JSON.stringify(myBoard.top));
  eq('Mening o‘rnim 1', myBoard.myRank, 1);

  section('5. Tanga va sovg‘a');
  const o1 = await req('/api/kabinet/game/order', { cookie: kab.cookie, csrf: kab.json.csrf, body: { rewardId: 'r1' } });
  eq('Sovg‘a so‘raldi', o1.status, 200);
  eq('Takror so‘rov — yo‘q', (await req('/api/kabinet/game/order', { cookie: kab.cookie, csrf: kab.json.csrf, body: { rewardId: 'r1' } })).status, 400);
  eq('CSRFsiz — yo‘q', (await req('/api/kabinet/game/order', { cookie: kab.cookie, body: { rewardId: 'r1' } })).status, 403);
  eq('Tanga kamaydi (4 − 2)', (await req('/api/kabinet/game', { cookie: kab.cookie })).json.coins, 2);
  const ol = await req('/api/game/orders', { cookie: dir });
  eq('Direktor so‘rovni ko‘radi', ol.json.orders.length, 1);
  eq('Ustoz so‘rovlarni ko‘rmaydi', (await req('/api/game/orders', { cookie: teach })).status, 403);
  eq('Berildi', (await req('/api/game/order/status', { cookie: dir, body: { id: o1.json.order.id, status: 'berildi' } })).status, 200);
  eq('Qayta o‘zgartirib bo‘lmaydi', (await req('/api/game/order/status', { cookie: dir, body: { id: o1.json.order.id, status: 'rad' } })).status, 400);
  eq('Qimmat sovg‘a — tanga yetmaydi', await (async () => {
    st.game.rewards.push({ id: 'r2', name: 'Futbolka', cost: 999 }); await put('meta/settings', st, dir);
    return (await req('/api/kabinet/game/order', { cookie: kab.cookie, csrf: kab.json.csrf, body: { rewardId: 'r2' } })).status;
  })(), 400);

  section('6. O‘chirilsa kabinetda yashirinadi');
  st.game.enabled = false; await put('meta/settings', st, dir);
  eq('Kabinet: yoqilmagan', (await req('/api/kabinet/game', { cookie: kab.cookie })).json.enabled, false);
  eq('Sovg‘a so‘rab bo‘lmaydi', (await req('/api/kabinet/game/order', { cookie: kab.cookie, csrf: kab.json.csrf, body: { rewardId: 'r1' } })).status, 404);

  stop();
  console.log(out.join('\n'));
  console.log('\n' + '─'.repeat(52));
  console.log((fail === 0 ? '✓ HAMMASI O’TDI' : '✗ XATOLAR BOR') + ` — ${pass} ta o'tdi, ${fail} ta xato`);
  process.exit(fail ? 1 : 0);
})().catch(e => { stop(); console.error(e); process.exit(1); });
