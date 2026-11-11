'use strict';
/**
 * 8-dars. Kutubxonasiz kichik REST API: vazifalar (todo) CRUD
 *   node 08-rest-api-server.js          — server 3000-portda ishlaydi
 *   node 08-rest-api-server.js --demo   — server ochiladi, so'rovlar yuboriladi, yopiladi
 */
const http = require('node:http');
const assert = require('node:assert/strict');

class ApiError extends Error {
  constructor(status, message) {
    super(message);
    this.status = status;
  }
}

let tasks = [];
let nextId = 1;

function send(res, status, body) {
  res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8' });
  res.end(body === undefined ? '' : JSON.stringify(body));
}

async function readJson(req) {
  let raw = '';
  for await (const chunk of req) {
    raw += chunk;
    if (raw.length > 1e6) throw new ApiError(413, "So'rov juda katta");
  }
  if (!raw) return {};
  try {
    return JSON.parse(raw);
  } catch {
    throw new ApiError(400, "JSON noto'g'ri");
  }
}

function validateTask(body, { partial = false } = {}) {
  const out = {};
  if (!partial || body.title !== undefined) {
    if (typeof body.title !== 'string' || body.title.trim() === '') {
      throw new ApiError(400, "'title' bo'sh bo'lmagan matn bo'lishi kerak");
    }
    out.title = body.title.trim();
  }
  if (body.done !== undefined) {
    if (typeof body.done !== 'boolean') throw new ApiError(400, "'done' true yoki false bo'lishi kerak");
    out.done = body.done;
  }
  return out; // faqat ruxsat etilgan maydonlar
}

async function handle(req, res) {
  const { pathname } = new URL(req.url, 'http://localhost');
  const match = pathname.match(/^\/tasks(?:\/(\d+))?$/);
  if (!match) throw new ApiError(404, 'Bunday manzil yo\'q');

  if (!match[1]) {
    if (req.method === 'GET') return send(res, 200, tasks);
    if (req.method === 'POST') {
      const data = validateTask(await readJson(req));
      const task = { id: nextId++, done: false, ...data, createdAt: new Date().toISOString() };
      tasks.push(task);
      return send(res, 201, task);
    }
  } else {
    const id = Number(match[1]);
    const task = tasks.find((t) => t.id === id);
    if (!task) throw new ApiError(404, `${id}-vazifa topilmadi`);
    if (req.method === 'GET') return send(res, 200, task);
    if (req.method === 'PATCH') {
      Object.assign(task, validateTask(await readJson(req), { partial: true }));
      return send(res, 200, task);
    }
    if (req.method === 'DELETE') {
      tasks = tasks.filter((t) => t.id !== id);
      return send(res, 204);
    }
  }
  throw new ApiError(405, "Bu usul qo'llab-quvvatlanmaydi");
}

const server = http.createServer((req, res) => {
  handle(req, res).catch((err) => {
    const status = err.status ?? 500;
    if (status === 500) console.error(err); // kutilmagan xato — logga yozamiz
    send(res, status, { error: status === 500 ? 'Serverda xatolik' : err.message });
  });
});

module.exports = { server };

// ---- Namoyish ----
async function demo() {
  await new Promise((resolve) => server.listen(0, resolve));
  const base = `http://localhost:${server.address().port}`;
  const call = async (method, path, body) => {
    const res = await fetch(base + path, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: body === undefined ? undefined : typeof body === 'string' ? body : JSON.stringify(body),
    });
    const text = await res.text();
    const json = text ? JSON.parse(text) : null;
    console.log(`${method.padEnd(6)} ${path.padEnd(10)} → ${res.status}`, json ?? '');
    return { status: res.status, json };
  };

  const a = await call('POST', '/tasks', { title: 'Uy vazifasini tekshirish' });
  await call('POST', '/tasks', { title: 'Test tuzish', id: 999 });           // id ni o'zgartira olmaydi
  await call('GET', '/tasks');
  const p = await call('PATCH', `/tasks/${a.json.id}`, { done: true });
  const bad = await call('POST', '/tasks', { title: '   ' });
  const broken = await call('POST', '/tasks', '{ buzilgan json');
  const d = await call('DELETE', `/tasks/${a.json.id}`);
  const missing = await call('GET', `/tasks/${a.json.id}`);
  const list = await call('GET', '/tasks');

  assert.equal(a.status, 201);
  assert.equal(p.json.done, true);
  assert.equal(bad.status, 400);
  assert.equal(broken.status, 400);
  assert.equal(d.status, 204);
  assert.equal(missing.status, 404);
  assert.deepEqual(list.json.map((t) => t.id), [2]);
  server.close();
  console.log('\n✓ Barcha tekshiruvlar o\'tdi');
}

if (require.main === module) {
  if (process.argv.includes('--demo')) {
    demo();
  } else {
    const port = Number(process.env.PORT) || 3000;
    server.listen(port, () => {
      console.log(`Server ishlayapti: http://localhost:${port}/tasks`);
      console.log(`Sinab ko'ring:  curl -X POST localhost:${port}/tasks -H "Content-Type: application/json" -d '{"title":"Dars"}'`);
    });
  }
}
