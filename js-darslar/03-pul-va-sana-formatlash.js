'use strict';
/**
 * 3-dars. Pul, son va sanalarni foydalanuvchiga chiroyli ko'rsatish (Intl)
 * Ishga tushirish: node 03-pul-va-sana-formatlash.js
 */
const assert = require('node:assert/strict');

const LOCALE = 'uz-UZ';

const somFormatter = new Intl.NumberFormat(LOCALE, {
  style: 'currency',
  currency: 'UZS',
  maximumFractionDigits: 0,
});
const compactFormatter = new Intl.NumberFormat(LOCALE, { notation: 'compact' });
const dateFormatter = new Intl.DateTimeFormat(LOCALE, { dateStyle: 'long' });
const relativeFormatter = new Intl.RelativeTimeFormat('uz', { numeric: 'auto' });

const formatSom = (amount) => somFormatter.format(amount);
const formatCompact = (n) => compactFormatter.format(n);
const formatDate = (date) => dateFormatter.format(new Date(date));

const UNITS = [
  ['year', 365 * 24 * 3600],
  ['month', 30 * 24 * 3600],
  ['week', 7 * 24 * 3600],
  ['day', 24 * 3600],
  ['hour', 3600],
  ['minute', 60],
  ['second', 1],
];

/** "3 kun oldin", "kecha", "2 soatdan keyin" */
function timeAgo(date, now = new Date()) {
  const diffSec = Math.round((new Date(date) - now) / 1000);
  for (const [unit, seconds] of UNITS) {
    if (Math.abs(diffSec) >= seconds || unit === 'second') {
      return relativeFormatter.format(Math.round(diffSec / seconds), unit);
    }
  }
}

/** Ekranda ko'rinadigan bo'shliqlarni oddiy probelga almashtirish (taqqoslash uchun) */
const plain = (s) => s.replace(/[  ]/g, ' ');

module.exports = { formatSom, formatCompact, formatDate, timeAgo };

if (require.main === module) {
  const now = new Date('2026-11-11T12:00:00');
  console.log(formatSom(1250000));
  console.log(formatCompact(1250000), "ko'rish");
  console.log(formatDate('2026-11-11'));
  console.log(timeAgo('2026-11-08T12:00:00', now));
  console.log(timeAgo('2026-11-10T11:00:00', now));
  console.log(timeAgo('2026-11-11T11:55:00', now));
  console.log(timeAgo('2026-11-11T14:00:00', now));

  assert.equal(plain(formatSom(1250000)), "1 250 000 soʻm");
  assert.equal(plain(formatDate('2026-11-11')), '11-noyabr, 2026');
  assert.equal(timeAgo('2026-11-08T12:00:00', now), '3 kun oldin');
  assert.equal(timeAgo('2026-11-10T11:00:00', now), 'kecha');
  assert.equal(timeAgo('2026-11-11T11:55:00', now), '5 daqiqa oldin');
  console.log('\n✓ Barcha tekshiruvlar o\'tdi');
}
