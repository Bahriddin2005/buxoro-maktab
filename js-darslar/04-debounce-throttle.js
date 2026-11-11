'use strict';
/**
 * 4-dars. Debounce va throttle — tez-tez sodir bo'ladigan hodisalarni jilovlash
 * Ishga tushirish: node 04-debounce-throttle.js
 */
const assert = require('node:assert/strict');

/** Oxirgi chaqiruvdan keyin `delay` ms jimlik bo'lsagina fn ishlaydi. */
function debounce(fn, delay) {
  let timer = null;
  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}

/** fn ko'pi bilan har `interval` ms da bir marta ishlaydi. */
function throttle(fn, interval) {
  let last = 0;
  return function (...args) {
    const now = Date.now();
    if (now - last >= interval) {
      last = now;
      fn.apply(this, args);
    }
  };
}

module.exports = { debounce, throttle };

// ---- Namoyish ----
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function demo() {
  // 1) Qidiruv: foydalanuvchi "maktab" so'zini har 100 ms da bitta harfdan yozadi
  const searches = [];
  const search = debounce((text) => {
    searches.push(text);
    console.log(`  → serverga so'rov: "${text}"`);
  }, 300);

  console.log('Debounce (qidiruv maydoni):');
  let typed = '';
  for (const letter of 'maktab') {
    typed += letter;
    console.log(`  yozildi: ${typed}`);
    search(typed);
    await sleep(100);
  }
  await sleep(400);
  assert.deepEqual(searches, ['maktab']); // 6 ta emas, faqat 1 ta so'rov

  // 2) Scroll: 1 soniya davomida har 20 ms da hodisa (≈50 ta)
  let events = 0;
  let handled = 0;
  const onScroll = throttle(() => handled++, 250);
  console.log('\nThrottle (sahifani aylantirish):');
  const end = Date.now() + 1000;
  while (Date.now() < end) {
    events++;
    onScroll();
    await sleep(20);
  }
  console.log(`  ${events} ta hodisa keldi, faqat ${handled} tasi qayta ishlandi`);
  assert.ok(handled >= 3 && handled <= 5);

  console.log('\n✓ Barcha tekshiruvlar o\'tdi');
}

if (require.main === module) demo();
