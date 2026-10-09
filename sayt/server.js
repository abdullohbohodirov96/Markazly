// Markazly sayti: index.html ni beradi va formadagi arizani Telegram'ga yuboradi.
// Tashqi kutubxona kerak emas (Node.js 18+).
const http = require("http");
const fs = require("fs");
const path = require("path");

const PORT = process.env.PORT || 3000;
const BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
const CHAT_ID = process.env.TELEGRAM_CHAT_ID;

if (!BOT_TOKEN || !CHAT_ID) {
  console.warn("Diqqat: TELEGRAM_BOT_TOKEN yoki TELEGRAM_CHAT_ID berilmagan — arizalar Telegram'ga bormaydi.");
}

const INDEX = path.join(__dirname, "index.html");

// Bir IP dan 10 daqiqada 5 tadan ko'p ariza qabul qilinmaydi (spamdan himoya)
const hits = new Map();
function tooMany(ip) {
  const now = Date.now();
  const list = (hits.get(ip) || []).filter((t) => now - t < 10 * 60 * 1000);
  list.push(now);
  hits.set(ip, list);
  return list.length > 5;
}

const esc = (s) => String(s).replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
const clip = (s, n) => String(s || "").trim().slice(0, n);

function readBody(req) {
  return new Promise((resolve, reject) => {
    let data = "";
    req.on("data", (chunk) => {
      data += chunk;
      if (data.length > 10_000) { reject(new Error("too large")); req.destroy(); }
    });
    req.on("end", () => resolve(data));
    req.on("error", reject);
  });
}

function send(res, code, body, type = "application/json; charset=utf-8") {
  res.writeHead(code, { "Content-Type": type });
  res.end(typeof body === "string" ? body : JSON.stringify(body));
}

async function handleLead(req, res) {
  const ip = (req.headers["x-forwarded-for"] || req.socket.remoteAddress || "").split(",")[0].trim();
  if (tooMany(ip)) return send(res, 429, { ok: false, error: "Juda ko'p urinish. Birozdan keyin qayta yuboring." });

  let f;
  try { f = JSON.parse(await readBody(req)); } catch { return send(res, 400, { ok: false, error: "Noto'g'ri so'rov." }); }

  if (f.website) return send(res, 200, { ok: true }); // bot to'ldiradigan yashirin maydon

  const lead = {
    name: clip(f.name, 80),
    phone: clip(f.phone, 30),
    center: clip(f.center, 120),
    size: clip(f.size, 40),
    plan: clip(f.plan, 40),
    source: clip(f.source, 40) || "Ariza formasi",
  };
  if (!lead.name || lead.phone.replace(/\D/g, "").length < 9) {
    return send(res, 400, { ok: false, error: "Ism va telefon raqamini to'ldiring." });
  }
  if (!BOT_TOKEN || !CHAT_ID) return send(res, 500, { ok: false, error: "Server sozlanmagan." });

  const text =
    `🆕 <b>Yangi ariza — 7 kunlik bepul sinov</b>\n\n` +
    `👤 <b>Ism:</b> ${esc(lead.name)}\n` +
    `📞 <b>Telefon:</b> ${esc(lead.phone)}\n` +
    `🏫 <b>Markaz:</b> ${esc(lead.center || "ko'rsatilmagan")}\n` +
    `👥 <b>O'quvchilar:</b> ${esc(lead.size || "—")}\n` +
    `💳 <b>Tarif:</b> ${esc(lead.plan || "—")}\n` +
    `📍 <b>Qayerdan:</b> ${esc(lead.source)}\n\n` +
    `🕒 ${new Date().toLocaleString("uz-UZ", { timeZone: "Asia/Tashkent" })}`;

  try {
    const r = await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ chat_id: CHAT_ID, text, parse_mode: "HTML" }),
    });
    const j = await r.json();
    if (!j.ok) throw new Error(j.description || "telegram error");
    return send(res, 200, { ok: true });
  } catch (e) {
    console.error("Telegram xatosi:", e.message);
    return send(res, 502, { ok: false, error: "Ariza yuborilmadi. Iltimos, telefon orqali bog'laning." });
  }
}

http
  .createServer(async (req, res) => {
    if (req.method === "POST" && req.url === "/api/lead") return handleLead(req, res);
    if (req.method === "GET" && req.url === "/health") return send(res, 200, { ok: true });
    if (req.method === "GET") {
      return fs.readFile(INDEX, (err, html) =>
        err ? send(res, 500, "index.html topilmadi", "text/plain") : send(res, 200, html, "text/html; charset=utf-8")
      );
    }
    send(res, 405, { ok: false });
  })
  .listen(PORT, () => console.log(`Markazly sayti ${PORT}-portda ishlayapti`));
