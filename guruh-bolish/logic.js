'use strict';
/*
 * Guruhga bo'lish — asosiy mantiq.
 * Fayl, terminal va boshqa narsalarga bog'liq emas, shuning uchun oson test qilinadi.
 */

/**
 * Matndan ismlar ro'yxatini ajratadi.
 * Har bir qator (yoki vergul / nuqta-vergul bilan ajratilgan qism) — bitta ism.
 * "1." / "2)" kabi raqamlar, bo'sh qatorlar va takroriy ismlar olib tashlanadi.
 */
function parseNames(text) {
  const seen = new Set();
  const result = [];
  for (const raw of String(text || '').split(/[\n,;]+/)) {
    const name = raw.replace(/^\s*\d+[.)]\s*/, '').replace(/\s+/g, ' ').trim();
    const key = name.toLowerCase();
    if (name && !seen.has(key)) {
      seen.add(key);
      result.push(name);
    }
  }
  return result;
}

/** Fisher–Yates aralashtirish. Asl massivni o'zgartirmaydi. */
function shuffle(items, rand = Math.random) {
  const arr = items.slice();
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(rand() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

/**
 * O'quvchilarni guruhlarga bo'ladi.
 * mode = 'count' — nechta guruh kerak; mode = 'size' — har guruhda necha kishi.
 * Guruhlar hajmi bir-biridan ko'pi bilan 1 taga farq qiladi
 * (masalan, 25 kishi / 4 guruh → 7, 6, 6, 6 — hech kim yolg'iz qolmaydi).
 */
function splitIntoGroups(names, mode, value, rand = Math.random) {
  const n = names.length;
  const v = Math.floor(Number(value));
  if (n === 0) throw new Error("Ro'yxat bo'sh. Avval o'quvchilar ismini kiriting.");
  if (!Number.isFinite(v) || v < 1) throw new Error("Son 1 dan katta yoki teng bo'lishi kerak.");

  const groupCount = mode === 'size' ? Math.ceil(n / v) : v;
  if (groupCount > n) {
    throw new Error(`${n} ta o'quvchini ${groupCount} ta guruhga bo'lib bo'lmaydi.`);
  }

  const groups = Array.from({ length: groupCount }, () => []);
  shuffle(names, rand).forEach((name, i) => groups[i % groupCount].push(name));
  return groups;
}

/**
 * Takrorlanmas tanlov: hamma bir martadan chaqirilmaguncha hech kim
 * ikkinchi marta chiqmaydi. `called` — avval chaqirilganlar ro'yxati.
 * Natija: { name, called, round } — yangi holat qaytariladi, asl massiv o'zgarmaydi.
 */
function pickNext(names, called = [], rand = Math.random) {
  if (names.length === 0) throw new Error("Ro'yxat bo'sh. Avval o'quvchilar ismini kiriting.");
  const calledSet = new Set(called);
  let pool = names.filter((n) => !calledSet.has(n));
  let newRound = false;
  if (pool.length === 0) {
    pool = names.slice();
    called = [];
    newRound = true;
  }
  const name = pool[Math.floor(rand() * pool.length)];
  const nextCalled = [...called.filter((n) => names.includes(n)), name];
  return { name, called: nextCalled, left: names.length - nextCalled.length, newRound };
}

/** Guruhlarni chiroyli matnga aylantiradi. */
function groupsToText(groups) {
  return groups
    .map((g, i) => `${i + 1}-guruh (${g.length} kishi):\n` + g.map((n) => `  • ${n}`).join('\n'))
    .join('\n\n');
}

module.exports = { parseNames, shuffle, splitIntoGroups, pickNext, groupsToText };
