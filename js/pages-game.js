/* Gamifikatsiya — interfeys.
   1) Sozlamalar → «Gamifikatsiya»: yoqish ustasi (ballar → tanga va sovg'alar → tayyor),
      yoqilgandan keyin qoidalarni tahrirlash va sovg'a so'rovlari.
   2) Guruh → «Reyting» yorlig'i: shu oy reytingi va ustoz rag'bati.
   3) Davomat oynasida: «Uy vazifasi» va «Faol» belgilari.
   4) O'quvchi kabineti → «Yutuqlarim»: daraja, XP, tanga, nishonlar, reyting, sovg'alar.

   Ballarni server hisoblaydi (server/game.js) — brauzer faqat ko'rsatadi. */
(function (global) {
  'use strict';
  var A = global.A, UI = A.UI, D = A.Data, h = UI.h;

  /* ---------- Qoidalar ro'yxati (Sozlamadagi tartib) ---------- */
  var RULES = [
    { k: 'attend', ico: '✅', t: 'Darsga keldi', d: 'Har bir darsga o‘z vaqtida kelgani uchun', def: 10 },
    { k: 'late', ico: '⏰', t: 'Kechikib keldi', d: 'Kech qolgan bo‘lsa ham kelgani uchun', def: 5 },
    { k: 'homework', ico: '📚', t: 'Uy vazifasini bajardi', d: 'Ustoz davomat oynasida «Vazifa ✓» deb belgilaydi', def: 15 },
    { k: 'active', ico: '🙋', t: 'Darsda faol bo‘ldi', d: 'Ustoz davomatda «Faol ⭐» deb belgilaydi', def: 5 },
    { k: 'quizMax', ico: '📝', t: 'Test natijasi', d: 'Foizga qarab: 100% bo‘lsa shuncha, 50% bo‘lsa yarmi', def: 10 },
    { k: 'quizPerfect', ico: '⭐', t: 'Testdan 100% — bonus', d: 'Hamma savolga to‘g‘ri javob bergani uchun qo‘shimcha', def: 10 },
    { k: 'question', ico: '💬', t: 'Ustozga savol berdi', d: 'Kabinetdan savol yozgani uchun', def: 2 },
    { k: 'onTimePay', ico: '💳', t: 'To‘lov o‘z vaqtida', d: 'Oylik to‘lovni muddatigacha to‘liq qilgani uchun', def: 15 },
    { k: 'courseLesson', ico: '🎓', t: 'Onlayn kurs darsi', d: 'Kursdagi dars testidan o‘tgani uchun', def: 30, mod: 'onlaynKurs' },
    { k: 'courseHw', ico: '🏠', t: 'Kurs vazifasi qabul qilindi', d: 'Ustoz qabul qilsa (+ baho × 2)', def: 20, mod: 'onlaynKurs' }
  ];
  var PRESETS = {
    yengil: { label: 'Yengil', attend: 5, late: 2, homework: 10, active: 3, quizMax: 10, quizPerfect: 5, question: 1, onTimePay: 10, courseLesson: 20, courseHw: 10 },
    tavsiya: { label: 'Tavsiya etilgan', attend: 10, late: 5, homework: 15, active: 5, quizMax: 10, quizPerfect: 10, question: 2, onTimePay: 15, courseLesson: 30, courseHw: 20 },
    kuchli: { label: 'Kuchli rag‘bat', attend: 15, late: 5, homework: 25, active: 10, quizMax: 20, quizPerfect: 20, question: 5, onTimePay: 25, courseLesson: 40, courseHw: 30 }
  };
  var REWARD_IDEAS = [
    { name: 'Ruchka yoki daftar', cost: 30 },
    { name: 'Markaz stikeri / brelok', cost: 50 },
    { name: 'Bitta dars bepul', cost: 300 },
    { name: 'Markaz futbolkasi', cost: 500 },
    { name: 'Oylik to‘lovdan 10% chegirma', cost: 800 }
  ];

  function gameSettings() { return (D.settings && D.settings.game) || {}; }
  function available() { return A.mod ? A.mod('gamifikatsiya') : false; }
  function enabled() { return available() && gameSettings().enabled === true; }
  function rules() { return RULES.filter(function (r) { return !r.mod || A.mod(r.mod); }); }
  function valOf(k) {
    var x = gameSettings().xp || {};
    var r = RULES.filter(function (q) { return q.k === k; })[0];
    return x[k] != null ? Number(x[k]) : (r ? r.def : 0);
  }
  function uid() { return 'rw' + Date.now().toString(36) + Math.random().toString(36).slice(2, 6); }

  /* ---------- Kichik bloklar ---------- */
  function stepper(value, onChange, min, max) {
    min = min == null ? 0 : min; max = max == null ? 500 : max;
    var inp = h('input', { type: 'number', class: 'gm-num', min: String(min), max: String(max), value: String(value) });
    function set(v) {
      v = Math.max(min, Math.min(max, Math.round(Number(v) || 0)));
      inp.value = String(v); onChange(v);
    }
    inp.addEventListener('change', function () { set(inp.value); });
    return h('div', { class: 'gm-step' }, [
      h('button', { type: 'button', class: 'gm-step-b', 'aria-label': 'Kamaytirish', onclick: function () { set(Number(inp.value) - 1); } }, '−'),
      inp,
      h('button', { type: 'button', class: 'gm-step-b', 'aria-label': 'Oshirish', onclick: function () { set(Number(inp.value) + 1); } }, '+')
    ]);
  }

  /** Ballar jadvali: har bir harakat — bitta qator */
  function rulesEditor(state) {
    var box = h('div', { class: 'gm-rules' });
    function paint() {
      UI.clear(box);
      rules().forEach(function (r) {
        box.appendChild(h('div', { class: 'gm-rule' }, [
          h('span', { class: 'gm-rule-i', 'aria-hidden': 'true' }, r.ico),
          h('div', { class: 'gm-rule-t' }, [h('b', {}, r.t), h('span', {}, r.d)]),
          stepper(state.xp[r.k], function (v) { state.xp[r.k] = v; }, 0, 500),
          h('span', { class: 'gm-rule-u' }, 'XP')
        ]));
      });
    }
    paint();
    var presets = h('div', { class: 'gm-presets' }, [h('span', { class: 'small muted' }, 'Tayyor variant:')].concat(
      Object.keys(PRESETS).map(function (id) {
        return h('button', {
          type: 'button', class: 'chip', onclick: function () {
            rules().forEach(function (r) { state.xp[r.k] = PRESETS[id][r.k]; });
            paint();
          }
        }, PRESETS[id].label);
      })));
    return h('div', {}, [presets, box]);
  }

  /** Sovg'alar ro'yxati muharriri */
  function rewardsEditor(state) {
    var box = h('div', { class: 'gm-rw-list' });
    function paint() {
      UI.clear(box);
      if (!state.rewards.length) box.appendChild(h('p', { class: 'small muted' }, 'Hozircha sovg‘a yo‘q. Pastdagi g‘oyalardan qo‘shing yoki o‘zingiz yozing.'));
      state.rewards.forEach(function (r, i) {
        var nm = h('input', { class: 'inp', value: r.name, placeholder: 'Sovg‘a nomi' });
        nm.addEventListener('input', function () { r.name = nm.value; });
        box.appendChild(h('div', { class: 'gm-rw' }, [
          h('span', { class: 'gm-rw-i', 'aria-hidden': 'true' }, '🎁'),
          nm,
          stepper(r.cost, function (v) { r.cost = v; }, 1, 100000),
          h('span', { class: 'gm-rule-u' }, 'tanga'),
          h('button', { type: 'button', class: 'btn sm ghost', 'aria-label': 'O‘chirish', onclick: function () { state.rewards.splice(i, 1); paint(); } }, '✕')
        ]));
      });
    }
    paint();
    return h('div', {}, [
      box,
      h('div', { class: 'gm-presets' }, [
        h('button', { type: 'button', class: 'btn sm', onclick: function () { state.rewards.push({ id: uid(), name: '', cost: 50 }); paint(); } }, [UI.icon('plus'), 'Sovg‘a qo‘shish'])
      ].concat(REWARD_IDEAS.map(function (x) {
        return h('button', {
          type: 'button', class: 'chip', onclick: function () {
            if (state.rewards.some(function (r) { return r.name === x.name; })) return;
            state.rewards.push({ id: uid(), name: x.name, cost: x.cost }); paint();
          }
        }, '+ ' + x.name);
      })))
    ]);
  }

  /** Taxminiy hisob: o'rtacha o'quvchi bir oyda */
  function exampleBox(state) {
    var xp = state.xp;
    var month = 12 * xp.attend + 10 * (xp.homework || 0) + 4 * (xp.active || 0) +
      4 * Math.round(0.8 * xp.quizMax) + (xp.onTimePay || 0);
    var coins = Math.floor(month / Math.max(1, state.coinRate));
    return h('div', { class: 'gm-example' }, [
      h('span', { class: 'gm-ex-i', 'aria-hidden': 'true' }, '🧮'),
      h('div', {}, [
        h('b', {}, 'Misol: oddiy o‘quvchi bir oyda ≈ ' + month + ' XP va ' + coins + ' tanga to‘playdi'),
        h('span', {}, '12 dars, 10 ta vazifa, 4 marta faol, 4 ta test (80%), to‘lov o‘z vaqtida.')
      ])
    ]);
  }

  function stateFromSettings() {
    var g = gameSettings();
    var st = { xp: {}, coinRate: Number(g.coinRate) || 10, rewards: (g.rewards || []).map(function (r) { return { id: r.id || uid(), name: r.name, cost: r.cost }; }) };
    RULES.forEach(function (r) { st.xp[r.k] = valOf(r.k); });
    return st;
  }
  async function saveGame(state, enabledFlag) {
    var rw = state.rewards.map(function (r) { return { id: r.id || uid(), name: String(r.name || '').trim(), cost: Math.max(1, Math.round(r.cost || 1)) }; })
      .filter(function (r) { return r.name; });
    await D.saveSettings(Object.assign({}, D.settings, {
      game: Object.assign({}, gameSettings(), {
        enabled: enabledFlag, xp: state.xp, coinRate: Math.max(1, Math.round(state.coinRate || 10)), rewards: rw
      })
    }));
    await A.Ops.audit(A.App ? A.App.user : null, 'Gamifikatsiya sozlandi', enabledFlag ? 'yoqildi' : 'o‘chirildi', '');
  }

  /* ================= 1. Yoqish ustasi ================= */
  function wizard(App) {
    var state = stateFromSettings();
    var step = 1;
    var body = h('div', { class: 'gm-wiz' });
    var m = UI.modal({ title: 'Gamifikatsiyani sozlash', wide: true, body: body, actions: [] });
    function nav() {
      return h('div', { class: 'gm-wiz-steps' }, ['Ballar', 'Tanga va sovg‘alar', 'Tayyor'].map(function (t, i) {
        return h('span', { class: 'gm-wiz-s' + (step === i + 1 ? ' on' : step > i + 1 ? ' done' : '') }, [h('i', {}, step > i + 1 ? '✓' : String(i + 1)), t]);
      }));
    }
    function foot(prev, next, nextLabel, nextCls) {
      return h('div', { class: 'gm-wiz-foot' }, [
        prev ? h('button', { type: 'button', class: 'btn', onclick: prev }, '← Orqaga') : h('span'),
        h('button', { type: 'button', class: 'btn ' + (nextCls || 'primary'), onclick: next }, nextLabel || 'Keyingisi →')
      ]);
    }
    function paint() {
      UI.clear(body);
      body.appendChild(nav());
      if (step === 1) {
        body.appendChild(h('p', { class: 'gm-lead' }, 'O‘quvchi qaysi harakati uchun necha ball (XP) olsin? Tayyor variantni tanlang yoki raqamlarni o‘zingiz o‘zgartiring.'));
        body.appendChild(rulesEditor(state));
        body.appendChild(foot(null, function () { step = 2; paint(); }));
      } else if (step === 2) {
        body.appendChild(h('p', { class: 'gm-lead' }, 'XP tangaga aylanadi, tangaga esa o‘quvchi sovg‘a oladi. Sovg‘a qo‘shmasangiz ham bo‘ladi — reyting va nishonlar baribir ishlaydi.'));
        body.appendChild(h('div', { class: 'gm-coin' }, [
          h('span', { class: 'gm-rule-i', 'aria-hidden': 'true' }, '🪙'),
          h('div', { class: 'gm-rule-t' }, [h('b', {}, 'Tanga kursi'), h('span', {}, 'Necha XP = 1 tanga')]),
          stepper(state.coinRate, function (v) { state.coinRate = v; }, 1, 1000),
          h('span', { class: 'gm-rule-u' }, 'XP')
        ]));
        body.appendChild(h('h3', { class: 'gm-h3' }, 'Sovg‘alar do‘koni'));
        body.appendChild(rewardsEditor(state));
        body.appendChild(foot(function () { step = 1; paint(); }, function () { step = 3; paint(); }));
      } else {
        body.appendChild(h('div', { class: 'gm-ready' }, [
          h('div', { class: 'gm-ready-i', 'aria-hidden': 'true' }, '🏆'),
          h('h3', {}, 'Hammasi tayyor!'),
          h('p', {}, 'Yoqilgandan keyin o‘quvchi kabinetida «Yutuqlarim» bo‘limi paydo bo‘ladi: daraja, XP, tanga, nishonlar va guruh reytingi. ' +
            'Ballar davomat va testlardan o‘zi hisoblanadi — o‘tgan darslar ham hisobga kiradi.')
        ]));
        body.appendChild(exampleBox(state));
        body.appendChild(h('ul', { class: 'gm-sum' }, rules().map(function (r) {
          return h('li', {}, [h('span', {}, r.ico + ' ' + r.t), h('b', {}, '+' + state.xp[r.k] + ' XP')]);
        }).concat([h('li', {}, [h('span', {}, '🪙 Tanga kursi'), h('b', {}, state.coinRate + ' XP = 1 tanga')]),
          h('li', {}, [h('span', {}, '🎁 Sovg‘alar'), h('b', {}, String(state.rewards.filter(function (r) { return r.name; }).length))])])));
        body.appendChild(foot(function () { step = 2; paint(); }, function (e) {
          UI.busy(e.currentTarget, async function () {
            try {
              await saveGame(state, true);
              m.close(true);
              UI.toast('Gamifikatsiya yoqildi! 🎉', 'ok');
              App.render();
            } catch (ex) { UI.toast(ex.message || 'Saqlanmadi', 'bad'); }
          });
        }, '🏆 Yoqish', 'gold'));
      }
    }
    paint();
  }

  /* ================= Sozlamalar sahifasi ================= */
  function settingsTab(view, App) {
    var on = enabled();
    view.appendChild(h('section', { class: 'gm-hero' + (on ? ' on' : '') }, [
      h('div', { class: 'gm-hero-t' }, [
        h('span', { class: 'gm-hero-badge' }, on ? '● Yoqilgan' : '○ O‘chiq'),
        h('h2', {}, 'Gamifikatsiya'),
        h('p', {}, 'O‘quvchilar darsga kelgani, vazifa qilgani va testlari uchun XP to‘playdi, daraja oshiradi, ' +
          'tanga yig‘ib sovg‘a oladi va guruhda reytingda bellashadi.')
      ]),
      h('div', { class: 'gm-hero-a' }, on ? [
        h('button', {
          class: 'btn on-dark', type: 'button', onclick: function () {
            UI.confirm('Gamifikatsiyani o‘chirish', 'O‘quvchilar kabinetida «Yutuqlarim» yashiriladi. Ballar o‘chmaydi — qayta yoqsangiz hammasi joyida bo‘ladi.', 'O‘chirish', true)
              .then(function (yes) {
                if (!yes) return;
                saveGame(stateFromSettings(), false).then(function () { UI.toast('O‘chirildi.', 'ok'); App.render(); });
              });
          }
        }, 'O‘chirish')
      ] : [
        h('button', { class: 'btn gold lg', type: 'button', onclick: function () { wizard(App); } }, '🏆 Sozlab yoqish')
      ])
    ]));

    if (!on) {
      view.appendChild(h('div', { class: 'gm-feats' }, [
        ['⚡', 'XP va darajalar', 'Har bir harakat uchun ball: 1-daraja «Yangi boshlovchi»dan «Afsona»gacha.'],
        ['🪙', 'Tanga va sovg‘alar', 'XP tangaga aylanadi, o‘quvchi kabinetdan sovg‘a so‘raydi, siz tasdiqlaysiz.'],
        ['🏅', 'Nishonlar va reyting', '12 xil nishon va guruh ichida oylik reyting — bellashuv motivatsiya beradi.']
      ].map(function (f) {
        return h('div', { class: 'gm-feat' }, [h('span', { 'aria-hidden': 'true' }, f[0]), h('b', {}, f[1]), h('p', {}, f[2])]);
      })));
      return;
    }

    var state = stateFromSettings();
    view.appendChild(UI.card('Ballar (XP)', [
      rulesEditor(state),
      h('div', { class: 'gm-coin', style: 'margin-top:10px' }, [
        h('span', { class: 'gm-rule-i', 'aria-hidden': 'true' }, '🪙'),
        h('div', { class: 'gm-rule-t' }, [h('b', {}, 'Tanga kursi'), h('span', {}, 'Necha XP = 1 tanga')]),
        stepper(state.coinRate, function (v) { state.coinRate = v; }, 1, 1000),
        h('span', { class: 'gm-rule-u' }, 'XP')
      ]),
      h('h3', { class: 'gm-h3' }, 'Sovg‘alar do‘koni'),
      rewardsEditor(state),
      h('div', { style: 'margin-top:14px' }, h('button', {
        class: 'btn primary', type: 'button', onclick: function (e) {
          UI.busy(e.currentTarget, async function () {
            await saveGame(state, true);
            UI.toast('Saqlandi.', 'ok');
          });
        }
      }, 'Saqlash'))
    ]));

    var ordBox = h('div', {}, h('p', { class: 'small muted' }, 'Yuklanmoqda…'));
    view.appendChild(h('div', { style: 'height:14px' }));
    view.appendChild(UI.card('Sovg‘a so‘rovlari', [ordBox]));
    function loadOrders() {
      D.api('GET', 'api/game/orders').then(function (r) {
        UI.clear(ordBox);
        var rows = r.orders || [];
        if (!rows.length) { ordBox.appendChild(UI.empty({ title: 'So‘rov yo‘q', text: 'O‘quvchi kabinetdan sovg‘a so‘rasa shu yerda chiqadi.' })); return; }
        ordBox.appendChild(UI.table([
          { label: 'O‘quvchi', render: function (o) { return o.studentName; } },
          { label: 'Sovg‘a', render: function (o) { return '🎁 ' + o.name; } },
          { label: 'Tanga', right: true, render: function (o) { return o.cost; } },
          { label: 'Sana', render: function (o) { return o.at; } },
          {
            label: 'Holat', render: function (o) {
              if (o.status !== 'kutilmoqda') return UI.pill(o.status === 'berildi' ? 'Berildi' : 'Rad etildi', o.status === 'berildi' ? 'ok' : 'bad');
              return h('div', { class: 'rowflex' }, [
                h('button', { class: 'btn sm primary', type: 'button', onclick: function () { setOrder(o, 'berildi'); } }, 'Berildi'),
                h('button', { class: 'btn sm', type: 'button', onclick: function () { setOrder(o, 'rad'); } }, 'Rad etish')
              ]);
            }
          }
        ], rows));
      }).catch(function (e) { UI.clear(ordBox); ordBox.appendChild(h('p', { class: 'err-msg' }, e.message || 'Yuklanmadi')); });
    }
    function setOrder(o, st) {
      D.api('POST', 'api/game/order/status', { id: o.id, status: st })
        .then(function () { UI.toast(st === 'berildi' ? 'Sovg‘a berildi.' : 'Rad etildi — tanga qaytdi.', 'ok'); loadOrders(); })
        .catch(function (e) { UI.toast(e.message || 'Bajarilmadi', 'bad'); });
    }
    loadOrders();
  }

  /* ================= 2. Guruh reytingi (xodim) ================= */
  var MEDAL = ['🥇', '🥈', '🥉'];
  function groupTab(view, g, App) {
    var box = h('div', {}, h('p', { class: 'small muted' }, 'Yuklanmoqda…'));
    view.appendChild(UI.card('🏆 Guruh reytingi · ' + A.monthLabel(A.thisMonth()), [
      h('p', { class: 'small muted', style: 'margin-top:0' }, 'Tartib shu oyda to‘plangan XP bo‘yicha. Ballar davomat, vazifa, test va rag‘batdan o‘zi hisoblanadi.'),
      box
    ]));
    function load() {
      D.api('GET', 'api/game/group?id=' + encodeURIComponent(g.id)).then(function (r) {
        UI.clear(box);
        var rows = r.rows || [];
        if (!rows.length) { box.appendChild(UI.empty({ title: 'Guruhda o‘quvchi yo‘q' })); return; }
        var canBonus = App.can('attendance.mark') || App.can('lesson.log');
        box.appendChild(h('div', { class: 'gm-board' }, rows.map(function (x) {
          return h('div', { class: 'gm-brow' + (x.rank <= 3 ? ' top' : '') }, [
            h('span', { class: 'gm-rank' }, MEDAL[x.rank - 1] || String(x.rank)),
            UI.avatar(x.name),
            h('div', { class: 'gm-bname' }, [h('b', {}, x.name), h('span', {}, x.level + '-daraja · jami ' + x.xp + ' XP · 🪙 ' + (x.coins || 0))]),
            h('b', { class: 'gm-bxp' }, '+' + x.monthXp + ' XP'),
            canBonus ? h('button', { class: 'btn sm', type: 'button', onclick: function () { bonusForm(x, load); } }, '⭐ Rag‘bat') : null
          ]);
        })));
      }).catch(function (e) { UI.clear(box); box.appendChild(h('p', { class: 'err-msg' }, e.message || 'Yuklanmadi')); });
    }
    load();
  }

  function bonusForm(x, done) {
    var xp = 10, reason = '';
    var reasonI = h('input', { class: 'inp', placeholder: 'Masalan: darsda eng yaxshi javob' });
    reasonI.addEventListener('input', function () { reason = reasonI.value; });
    var amtRow = h('div', { class: 'gm-presets' });
    function paintAmt() {
      UI.clear(amtRow);
      [5, 10, 20, 50, -5, -10].forEach(function (v) {
        amtRow.appendChild(h('button', {
          type: 'button', class: 'chip' + (xp === v ? ' on' : '') + (v < 0 ? ' neg' : ''),
          onclick: function () { xp = v; paintAmt(); }
        }, (v > 0 ? '+' : '') + v + ' XP'));
      });
    }
    paintAmt();
    var reasons = h('div', { class: 'gm-presets' }, ['Faol qatnashdi', 'Eng yaxshi javob', 'Qo‘shimcha topshiriq', 'Guruhga yordam berdi', 'Intizom buzildi'].map(function (t) {
      return h('button', { type: 'button', class: 'chip', onclick: function () { reasonI.value = t; reason = t; if (t === 'Intizom buzildi' && xp > 0) { xp = -5; paintAmt(); } } }, t);
    }));
    UI.modal({
      title: x.name + ' — rag‘bat',
      body: [h('label', { class: 'small muted' }, 'Ball'), amtRow, h('label', { class: 'small muted' }, 'Sababi (o‘quvchi ko‘radi)'), reasons, reasonI],
      actions: [
        { label: 'Bekor qilish' },
        {
          label: 'Berish', cls: 'primary', onClick: function (close, btn) {
            if (String(reason).trim().length < 2) { UI.toast('Sababini yozing.', 'bad'); return; }
            UI.busy(btn, async function () {
              try {
                await D.api('POST', 'api/game/bonus', { studentId: x.studentId, xp: xp, reason: reason });
                close(); UI.toast((xp > 0 ? '+' : '') + xp + ' XP berildi.', 'ok'); if (done) done();
              } catch (e) { UI.toast(e.message || 'Bajarilmadi', 'bad'); }
            });
          }
        }
      ]
    });
  }

  /* ================= 3. Davomat oynasidagi belgilar ================= */
  /** extra: { hw: 'ha'|'yoq'|undefined, faol: bool } ; onChange() */
  function attendanceMarks(extra, onChange, disabled) {
    var hwB = h('button', { type: 'button', class: 'gm-mark', disabled: !!disabled, title: 'Uy vazifasi' });
    var faolB = h('button', { type: 'button', class: 'gm-mark', disabled: !!disabled, title: 'Darsda faol' });
    function paint() {
      hwB.textContent = extra.hw === 'ha' ? '📚 ✓' : extra.hw === 'yoq' ? '📚 ✗' : '📚';
      hwB.className = 'gm-mark' + (extra.hw === 'ha' ? ' ok' : extra.hw === 'yoq' ? ' bad' : '');
      faolB.textContent = extra.faol ? '⭐ Faol' : '☆';
      faolB.className = 'gm-mark' + (extra.faol ? ' gold' : '');
    }
    hwB.addEventListener('click', function () {
      extra.hw = !extra.hw ? 'ha' : extra.hw === 'ha' ? 'yoq' : undefined; paint(); onChange();
    });
    faolB.addEventListener('click', function () { extra.faol = !extra.faol; paint(); onChange(); });
    paint();
    return h('div', { class: 'gm-marks' }, [hwB, faolB]);
  }

  /* ================= 4. O'quvchi kabineti: «Yutuqlarim» ================= */
  function portalView(el, opts) {
    var box = h('div', { class: 'gm-portal' }, h('p', { class: 'sp-muted' }, 'Yuklanmoqda…'));
    el.appendChild(box);
    D.api('GET', 'api/kabinet/game' + (opts.studentId ? '?studentId=' + encodeURIComponent(opts.studentId) : '')).then(function (g) {
      UI.clear(box);
      if (!g.enabled) { box.appendChild(h('p', { class: 'sp-muted' }, 'Yutuqlar bo‘limi hozircha yoqilmagan.')); return; }
      var L = g.level;
      box.appendChild(h('section', { class: 'gm-me' }, [
        h('div', { class: 'gm-lvl' }, [h('small', {}, 'Daraja'), h('b', {}, String(L.n))]),
        h('div', { class: 'gm-me-t' }, [
          h('b', {}, L.name),
          h('div', { class: 'gm-bar' }, h('i', { style: 'width:' + Math.max(3, L.percent) + '%' })),
          h('span', {}, L.inLevel + ' / ' + L.need + ' XP · keyingi darajagacha ' + (L.need - L.inLevel) + ' XP')
        ]),
        h('div', { class: 'gm-me-n' }, [
          h('div', {}, [h('b', {}, String(g.xp)), h('span', {}, 'jami XP')]),
          h('div', {}, [h('b', {}, '+' + g.monthXp), h('span', {}, 'shu oy')]),
          h('div', {}, [h('b', {}, '🪙 ' + g.coins), h('span', {}, 'tanga')])
        ])
      ]));

      /* Nishonlar */
      var got = g.badges.filter(function (b) { return b.got; }).length;
      box.appendChild(opts.card('Nishonlar · ' + got + ' / ' + g.badges.length, [
        h('div', { class: 'gm-badges' }, g.badges.map(function (b) {
          return h('div', { class: 'gm-badge' + (b.got ? ' got' : ''), title: b.text }, [
            h('span', { class: 'gm-badge-i' }, b.icon), h('b', {}, b.name), h('small', {}, b.text)
          ]);
        }))
      ]));

      /* Guruh reytingi */
      (g.boards || []).forEach(function (bd) {
        box.appendChild(opts.card('🏆 ' + bd.group + ' — reyting', [
          bd.myRank ? h('p', { class: 'gm-myrank' }, 'Siz ' + bd.size + ' kishi ichida ' + bd.myRank + '-o‘rindasiz' + (bd.myRank <= 3 ? ' ' + MEDAL[bd.myRank - 1] : '')) : null,
          h('div', { class: 'gm-board' }, bd.top.map(function (r) {
            return h('div', { class: 'gm-brow' + (r.me ? ' me' : '') + (r.rank <= 3 ? ' top' : '') }, [
              h('span', { class: 'gm-rank' }, MEDAL[r.rank - 1] || String(r.rank)),
              h('div', { class: 'gm-bname' }, [h('b', {}, r.name + (r.me ? ' (siz)' : '')), h('span', {}, r.level + '-daraja')]),
              h('b', { class: 'gm-bxp' }, '+' + r.monthXp + ' XP')
            ]);
          }))
        ]));
      });

      /* Sovg'alar */
      if ((g.rewards || []).length) {
        box.appendChild(opts.card('🎁 Sovg‘alar do‘koni', [
          h('div', { class: 'gm-shop' }, g.rewards.map(function (r) {
            var can = g.canOrder && g.coins >= r.cost;
            var pending = (g.orders || []).some(function (o) { return o.rewardId === r.id && o.status === 'kutilmoqda'; });
            return h('div', { class: 'gm-item' }, [
              h('span', { class: 'gm-item-i' }, '🎁'), h('b', {}, r.name), h('span', { class: 'gm-cost' }, '🪙 ' + r.cost),
              g.canOrder ? h('button', {
                type: 'button', class: 'btn sm ' + (can && !pending ? 'primary' : ''), disabled: !can || pending,
                onclick: function (e) {
                  UI.busy(e.currentTarget, async function () {
                    try { await D.kabPost('api/kabinet/game/order', { rewardId: r.id }); UI.toast('So‘rov yuborildi! Markaz tasdiqlagach sovg‘ani olasiz.', 'ok'); el.innerHTML = ''; portalView(el, opts); }
                    catch (ex) { UI.toast(ex.message || 'Bajarilmadi', 'bad'); }
                  });
                }
              }, pending ? 'Kutilmoqda' : can ? 'Olish' : (r.cost - g.coins) + ' tanga yetmaydi') : null
            ]);
          })),
          (g.orders || []).length ? h('div', { class: 'gm-orders' }, g.orders.slice(0, 5).map(function (o) {
            return h('div', { class: 'kab-line' }, [h('span', {}, '🎁 ' + o.name), h('b', {}, o.status === 'berildi' ? 'Berildi ✓' : o.status === 'rad' ? 'Rad etildi' : 'Kutilmoqda…')]);
          })) : null
        ]));
      }

      /* Qanday ball olinadi + tarix */
      var X = g.xpRules || {};
      box.appendChild(opts.card('Qanday XP olinadi', [
        h('ul', { class: 'gm-sum' }, rules().filter(function (r) { return X[r.k]; }).map(function (r) {
          return h('li', {}, [h('span', {}, r.ico + ' ' + r.t), h('b', {}, '+' + X[r.k] + ' XP')]);
        }).concat([h('li', {}, [h('span', {}, '🪙 Tanga'), h('b', {}, g.coinRate + ' XP = 1 tanga')])]))
      ]));
      if ((g.history || []).length) {
        box.appendChild(opts.card('So‘nggi ballar', [
          h('div', { class: 'gm-hist' }, g.history.map(function (e) {
            return h('div', { class: 'gm-hrow' }, [h('span', {}, e.text), h('small', {}, e.at), h('b', { class: e.xp < 0 ? 'neg' : '' }, (e.xp > 0 ? '+' : '') + e.xp)]);
          }))
        ]));
      }
    }).catch(function (e) { UI.clear(box); box.appendChild(h('p', { class: 'err-msg' }, e.message || 'Yuklanmadi.')); });
  }

  /** Kabinet bosh sahifasidagi kichik chip: "3-daraja · 420 XP · 🪙 42" */
  function homeChip(el) {
    D.api('GET', 'api/kabinet/game').then(function (g) {
      if (!g || !g.enabled) return;
      el.hidden = false;
      el.textContent = '⚡ ' + g.level.n + '-daraja · ' + g.xp + ' XP · 🪙 ' + g.coins;
    }).catch(function () { });
  }

  A.GameUI = {
    available: available, enabled: enabled, settingsTab: settingsTab, wizard: wizard,
    groupTab: groupTab, attendanceMarks: attendanceMarks, portalView: portalView, homeChip: homeChip
  };
})(typeof window !== 'undefined' ? window : globalThis);
