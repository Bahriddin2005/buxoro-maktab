'use strict';
/**
 * 7-dars. Kesh (cache): bir xil so'rovni qayta-qayta yubormaslik
 * Ishga tushirish: node 07-kesh.js
 */
const assert = require('node:assert/strict');

class TTLCache {
  #store = new Map();

  constructor(ttlMs) {
    this.ttlMs = ttlMs;
  }

  get(key) {
    const entry = this.#store.get(key);
    if (!entry) return undefined;
    if (Date.now() > entry.expiresAt) {
      this.#store.delete(key); // muddati o'tgan — o'chiramiz
      return undefined;
    }
    return entry.value;
  }

  set(key, value) {
    this.#store.set(key, { value, expiresAt: Date.now() + this.ttlMs });
  }

  delete(key) {
    this.#store.delete(key);
  }
}

/** Async funksiyani keshlab qo'yadi. Bir vaqtdagi bir xil so'rovlar ham bitta bo'ladi. */
function cachedAsync(fn, ttlMs) {
  const cache = new TTLCache(ttlMs);
  return function (key) {
    const hit = cache.get(key);
    if (hit !== undefined) return hit;

    const promise = fn(key).catch((err) => {
      cache.delete(key); // xatoni keshlamaymiz
      throw err;
    });
    cache.set(key, promise); // natijani emas, Promise'ning o'zini saqlaymiz
    return promise;
  };
}

module.exports = { TTLCache, cachedAsync };

// ---- Namoyish ----
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function demo() {
  let realCalls = 0;
  async function getWeather(city) {
    realCalls++;
    console.log(`  (haqiqiy so'rov #${realCalls}: ${city})`);
    await sleep(200); // sekin API
    if (city === 'Xato') throw new Error('API ishlamayapti');
    return { city, temp: 14 };
  }
  const getWeatherCached = cachedAsync(getWeather, 500);

  console.log('1) Bir vaqtda 3 ta bir xil so\'rov:');
  const results = await Promise.all([
    getWeatherCached('Buxoro'),
    getWeatherCached('Buxoro'),
    getWeatherCached('Buxoro'),
  ]);
  console.log('  natija:', results[0]);
  assert.equal(realCalls, 1);

  console.log('\n2) Darhol yana so\'raymiz — keshdan:');
  const t = Date.now();
  await getWeatherCached('Buxoro');
  console.log(`  ${Date.now() - t} ms (200 ms emas)`);
  assert.equal(realCalls, 1);

  console.log('\n3) Kesh muddati (500 ms) o\'tgach — yangi so\'rov:');
  await sleep(600);
  await getWeatherCached('Buxoro');
  assert.equal(realCalls, 2);

  console.log('\n4) Xato keshlanmaydi — keyingi urinish yana serverga boradi:');
  await assert.rejects(getWeatherCached('Xato'));
  await assert.rejects(getWeatherCached('Xato'));
  assert.equal(realCalls, 4);

  console.log('\n✓ Barcha tekshiruvlar o\'tdi');
}

if (require.main === module) demo();
