'use strict';
// Ishga tushirish: node --test   (yoki: node test.js)
const test = require('node:test');
const assert = require('node:assert/strict');
const { parseNames, shuffle, splitIntoGroups, pickNext } = require('./logic');

const names = Array.from({ length: 25 }, (_, i) => `O'quvchi ${i + 1}`);

test("parseNames: bo'sh qator, raqam va takrorni olib tashlaydi", () => {
  const text = '1. Anvar\n\n2) Dilnoza\nanvar\n  Jasur   Rahimov , Laylo';
  assert.deepEqual(parseNames(text), ['Anvar', 'Dilnoza', 'Jasur Rahimov', 'Laylo']);
});

test("shuffle: hech kim yo'qolmaydi va asl massiv o'zgarmaydi", () => {
  const copy = names.slice();
  const out = shuffle(names);
  assert.deepEqual(names, copy);
  assert.deepEqual(out.slice().sort(), copy.slice().sort());
});

test("splitIntoGroups: guruhlar soni bo'yicha, farq ko'pi bilan 1", () => {
  const groups = splitIntoGroups(names, 'count', 4);
  assert.equal(groups.length, 4);
  const sizes = groups.map((g) => g.length);
  assert.ok(Math.max(...sizes) - Math.min(...sizes) <= 1);
  assert.equal(groups.flat().length, 25);
  assert.equal(new Set(groups.flat()).size, 25);
});

test("splitIntoGroups: hajm bo'yicha — hech kim yolg'iz qolmaydi", () => {
  const groups = splitIntoGroups(names, 'size', 4); // 25 / 4 → 7 guruh
  assert.equal(groups.length, 7);
  assert.ok(groups.every((g) => g.length >= 3 && g.length <= 4));
});

test("splitIntoGroups: noto'g'ri qiymatlarda xato beradi", () => {
  assert.throws(() => splitIntoGroups([], 'count', 2));
  assert.throws(() => splitIntoGroups(names, 'count', 0));
  assert.throws(() => splitIntoGroups(names, 'count', 30));
});

test('pickNext: aylana tugaguncha hech kim takrorlanmaydi', () => {
  let called = [];
  const seen = new Set();
  for (let i = 0; i < names.length; i++) {
    const r = pickNext(names, called);
    assert.ok(!seen.has(r.name), `${r.name} ikki marta chiqdi`);
    seen.add(r.name);
    called = r.called;
  }
  assert.equal(seen.size, names.length);
  const next = pickNext(names, called);
  assert.equal(next.newRound, true);
  assert.equal(next.called.length, 1);
});

test("pickNext: ro'yxatdan o'chirilgan ism hisobga olinmaydi", () => {
  const r = pickNext(['A', 'B'], ['A', 'Eski'], () => 0);
  assert.equal(r.name, 'B');
  assert.deepEqual(r.called, ['A', 'B']);
  assert.equal(r.left, 0);
});
