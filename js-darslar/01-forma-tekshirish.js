'use strict';
/**
 * 1-dars. Forma ma'lumotlarini tekshirish (validatsiya)
 * Ishga tushirish: node 01-forma-tekshirish.js
 */
const assert = require('node:assert/strict');

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

function validateEmail(input) {
  const email = String(input ?? '').trim().toLowerCase();
  if (email === '') return { error: 'Email kiritilmagan' };
  if (!EMAIL_RE.test(email)) return { error: "Email formati noto'g'ri" };
  return { value: email };
}

function validatePhone(input) {
  const digits = String(input ?? '').replace(/\D/g, ''); // raqamdan boshqa hamma narsani olib tashlaymiz
  let local;
  if (digits.length === 9) local = digits;
  else if (digits.length === 12 && digits.startsWith('998')) local = digits.slice(3);
  else return { error: "Telefon noto'g'ri (masalan: +998 90 123 45 67)" };
  return { value: '+998' + local };
}

function validatePassword(input) {
  const password = String(input ?? '');
  const rules = [
    [password.length >= 8, 'kamida 8 ta belgi'],
    [/[A-Z]/.test(password), 'kamida bitta katta harf'],
    [/[0-9]/.test(password), 'kamida bitta raqam'],
  ];
  const missing = rules.filter(([ok]) => !ok).map(([, text]) => text);
  if (missing.length > 0) return { error: `Parolda ${missing.join(', ')} bo'lishi kerak` };
  return { value: password };
}

function validateForm(form) {
  const checks = {
    email: validateEmail(form.email),
    phone: validatePhone(form.phone),
    password: validatePassword(form.password),
  };
  const errors = {};
  const data = {};
  for (const [field, result] of Object.entries(checks)) {
    if (result.error) errors[field] = result.error;
    else data[field] = result.value;
  }
  return { ok: Object.keys(errors).length === 0, errors, data };
}

module.exports = { validateEmail, validatePhone, validatePassword, validateForm };

// ---- Namoyish (fayl to'g'ridan-to'g'ri ishga tushirilganda) ----
if (require.main === module) {
  const good = validateForm({ email: '  Anvar@Maktab.UZ ', phone: '90 123-45-67', password: 'Maktab2026' });
  const bad = validateForm({ email: 'anvar@', phone: '12345', password: 'abc' });
  console.log("To'g'ri forma:", good);
  console.log("Xato forma:", bad);

  assert.equal(good.ok, true);
  assert.equal(good.data.email, 'anvar@maktab.uz');
  assert.equal(good.data.phone, '+998901234567');
  assert.equal(validatePhone('+998 (90) 123-45-67').value, '+998901234567');
  assert.equal(bad.ok, false);
  assert.deepEqual(Object.keys(bad.errors), ['email', 'phone', 'password']);
  console.log('\n✓ Barcha tekshiruvlar o\'tdi');
}
