'use strict';
/**
 * 6-dars. Sahifalash (pagination), qidiruv va saralash — har bir ro'yxat sahifasining asosi
 * Ishga tushirish: node 06-sahifalash-qidiruv.js
 */
const assert = require('node:assert/strict');

function paginate(items, { page = 1, perPage = 10 } = {}) {
  const size = Math.min(100, Math.max(1, Math.floor(perPage) || 10)); // 1..100 oralig'ida
  const total = items.length;
  const totalPages = Math.max(1, Math.ceil(total / size));
  const current = Math.min(totalPages, Math.max(1, Math.floor(page) || 1)); // 1..totalPages
  const start = (current - 1) * size;

  return {
    data: items.slice(start, start + size),
    meta: { page: current, perPage: size, total, totalPages, hasPrev: current > 1, hasNext: current < totalPages },
  };
}

const SORTABLE = ['name', 'grade', 'score'];

function listStudents(students, { search = '', sortBy = 'name', order = 'asc', page, perPage } = {}) {
  const q = search.trim().toLowerCase();
  const filtered = q ? students.filter((s) => s.name.toLowerCase().includes(q)) : students;

  const key = SORTABLE.includes(sortBy) ? sortBy : 'name';
  const dir = order === 'desc' ? -1 : 1;
  const sorted = [...filtered].sort((a, b) => {
    const x = a[key];
    const y = b[key];
    return (typeof x === 'string' ? x.localeCompare(y, 'uz', { numeric: true }) : x - y) * dir;
  });

  return paginate(sorted, { page, perPage });
}

module.exports = { paginate, listStudents };

if (require.main === module) {
  const firstNames = ['Anvar', 'Dilnoza', 'Jasur', 'Laylo', 'Bekzod', 'Madina', 'Sardor', 'Nilufar'];
  const students = Array.from({ length: 23 }, (_, i) => ({
    id: i + 1,
    name: `${firstNames[i % firstNames.length]} ${i + 1}`,
    grade: 5 + (i % 7),
    score: (i * 37) % 100,
  }));

  const page1 = listStudents(students, { perPage: 5 });
  console.log('1-sahifa:', page1.data.map((s) => s.name), page1.meta);

  const top = listStudents(students, { sortBy: 'score', order: 'desc', perPage: 3 });
  console.log('\nEng yuqori ball:', top.data.map((s) => `${s.name} — ${s.score}`));

  const found = listStudents(students, { search: 'anv' });
  console.log('\n"anv" qidiruvi:', found.data.map((s) => s.name), `(jami ${found.meta.total})`);

  assert.equal(page1.meta.totalPages, 5);
  assert.equal(page1.data.length, 5);
  assert.equal(paginate(students, { page: 5, perPage: 5 }).data.length, 3);   // oxirgi sahifa to'liq emas
  assert.equal(paginate(students, { page: 999, perPage: 5 }).meta.page, 5);  // chegaradan tashqari
  assert.equal(paginate(students, { page: 'abc' }).meta.page, 1);            // noto'g'ri qiymat
  assert.equal(paginate([], {}).meta.totalPages, 1);                          // bo'sh ro'yxat
  assert.equal(top.data[0].score, Math.max(...students.map((s) => s.score)));
  assert.equal(listStudents(students, { sortBy: 'password' }).data[0].name, 'Anvar 1'); // ruxsat etilmagan maydon
  console.log('\n✓ Barcha tekshiruvlar o\'tdi');
}
