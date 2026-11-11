'use strict';
/**
 * 5-dars. API'ga so'rov: async/await, timeout, xatolarni ushlash, qayta urinish (retry)
 * Ishga tushirish: node 05-api-sorov-retry.js
 * (Internet shart emas — namoyish uchun shu faylning o'zi kichik server ishga tushiradi.)
 */
const http = require('node:http');
const assert = require('node:assert/strict');

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

class HttpError extends Error {
  constructor(status, message) {
    super(message);
    this.name = 'HttpError';
    this.status = status;
  }
}

function isRetryable(err) {
  if (err.name === 'TimeoutError') return true;          // server javob bermadi
  if (err.name === 'TypeError') return true;             // tarmoq xatosi (internet uzildi)
  if (err instanceof HttpError) return err.status >= 500 || err.status === 429;
  return false;                                          // 400, 404 va h.k. — qayta urinish befoyda
}

async function fetchJson(url, { timeout = 3000, retries = 2, ...options } = {}) {
  for (let attempt = 0; ; attempt++) {
    try {
      const res = await fetch(url, { ...options, signal: AbortSignal.timeout(timeout) });
      if (!res.ok) throw new HttpError(res.status, `Server ${res.status} qaytardi`);
      return await res.json();
    } catch (err) {
      if (!isRetryable(err) || attempt >= retries) throw err;
      const wait = 200 * 2 ** attempt;                   // 200, 400, 800 ms ...
      console.log(`    ${attempt + 1}-urinish xato (${err.message}). ${wait} ms dan keyin qayta...`);
      await sleep(wait);
    }
  }
}

module.exports = { fetchJson, HttpError };

// ---- Namoyish uchun soxta server ----
function startFakeServer() {
  let flakyCalls = 0;
  const server = http.createServer((req, res) => {
    const json = (status, body) => {
      res.writeHead(status, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(body));
    };
    if (req.url === '/flaky') {
      flakyCalls++;
      return flakyCalls <= 2 ? json(503, { error: 'band' }) : json(200, { students: 28 });
    }
    if (req.url === '/slow') return setTimeout(() => json(200, { ok: true }), 2000);
    return json(404, { error: 'topilmadi' });
  });
  return new Promise((resolve) => server.listen(0, () => resolve(server)));
}

async function demo() {
  const server = await startFakeServer();
  const base = `http://localhost:${server.address().port}`;

  console.log('1) Server 2 marta xato beradi, 3-sida ishlaydi:');
  const data = await fetchJson(`${base}/flaky`);
  console.log('    natija:', data);
  assert.deepEqual(data, { students: 28 });

  console.log('\n2) 404 — qayta urinmaymiz, darhol xato:');
  await assert.rejects(fetchJson(`${base}/yoq`), (err) => {
    console.log(`    ushlandi: ${err.name}, status ${err.status}`);
    return err.status === 404;
  });

  console.log('\n3) Server juda sekin — timeout:');
  await assert.rejects(fetchJson(`${base}/slow`, { timeout: 300, retries: 1 }), (err) => {
    console.log(`    ushlandi: ${err.name}`);
    return err.name === 'TimeoutError';
  });

  server.closeAllConnections();
  server.close();
  console.log('\n✓ Barcha tekshiruvlar o\'tdi');
}

if (require.main === module) demo();
