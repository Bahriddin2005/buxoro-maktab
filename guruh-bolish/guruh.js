#!/usr/bin/env node
'use strict';
/*
 * Guruhga bo'lish — terminal dasturi.
 *
 *   node guruh.js bol    <fayl> <guruhlar soni>
 *   node guruh.js bol    <fayl> --hajm <guruhdagi odam soni>
 *   node guruh.js chaqir <fayl>
 *   node guruh.js yangila <fayl>
 */
const fs = require('fs');
const path = require('path');
const { parseNames, splitIntoGroups, pickNext, groupsToText } = require('./logic');

const HELP = `
Guruhga bo'lish — sinfni adolatli guruhlarga bo'lish va o'quvchini takrorlanmasdan chaqirish.

Foydalanish:
  node guruh.js bol <fayl> <son>            <son> ta guruhga bo'lish
  node guruh.js bol <fayl> --hajm <son>     har guruhda taxminan <son> kishi
  node guruh.js chaqir <fayl>               tasodifiy o'quvchini chaqirish (takrorlanmaydi)
  node guruh.js yangila <fayl>              chaqirilganlar ro'yxatini tozalash

<fayl> — har qatorida bitta ism yozilgan matn fayli (masalan, sinf.txt).

Misollar:
  node guruh.js bol sinf.txt 4
  node guruh.js bol sinf.txt --hajm 3
  node guruh.js chaqir sinf.txt
`.trim();

function fail(message) {
  console.error(`Xato: ${message}`);
  process.exit(1);
}

function readNames(file) {
  if (!file) fail("Fayl ko'rsatilmadi. Yordam uchun: node guruh.js --yordam");
  let text;
  try {
    text = fs.readFileSync(file, 'utf8');
  } catch (_) {
    fail(`"${file}" faylini o'qib bo'lmadi.`);
  }
  const names = parseNames(text);
  if (names.length === 0) fail(`"${file}" faylida birorta ham ism topilmadi.`);
  return names;
}

// Chaqirilganlar har bir sinf fayli yonida alohida saqlanadi: sinf.txt → .sinf.txt.chaqirilgan.json
function stateFile(file) {
  return path.join(path.dirname(file), `.${path.basename(file)}.chaqirilgan.json`);
}

function loadCalled(file) {
  try {
    const data = JSON.parse(fs.readFileSync(stateFile(file), 'utf8'));
    return Array.isArray(data) ? data : [];
  } catch (_) {
    return [];
  }
}

function cmdSplit(args) {
  const [file, ...rest] = args;
  const names = readNames(file);
  const sizeIdx = rest.indexOf('--hajm');
  const mode = sizeIdx >= 0 ? 'size' : 'count';
  const value = sizeIdx >= 0 ? rest[sizeIdx + 1] : rest[0];
  if (value === undefined) fail("Son ko'rsatilmadi. Masalan: node guruh.js bol sinf.txt 4");

  try {
    const groups = splitIntoGroups(names, mode, value);
    console.log(`${names.length} ta o'quvchi → ${groups.length} ta guruh\n`);
    console.log(groupsToText(groups));
  } catch (e) {
    fail(e.message);
  }
}

function cmdPick(args) {
  const [file] = args;
  const names = readNames(file);
  const result = pickNext(names, loadCalled(file));
  fs.writeFileSync(stateFile(file), JSON.stringify(result.called, null, 2));

  if (result.newRound) console.log('(Hamma chaqirilgan edi — yangi aylana boshlandi)\n');
  console.log(`  ➜  ${result.name}\n`);
  console.log(result.left === 0
    ? "Hamma bir martadan chaqirildi. Keyingisi yangi aylanadan bo'ladi."
    : `Hali chaqirilmagan: ${result.left} kishi`);
}

function cmdReset(args) {
  const [file] = args;
  if (!file) fail("Fayl ko'rsatilmadi.");
  fs.rmSync(stateFile(file), { force: true });
  console.log("Chaqirilganlar ro'yxati tozalandi.");
}

const [command, ...args] = process.argv.slice(2);
switch (command) {
  case 'bol': cmdSplit(args); break;
  case 'chaqir': cmdPick(args); break;
  case 'yangila': cmdReset(args); break;
  case undefined:
  case '-h':
  case '--help':
  case '--yordam':
    console.log(HELP); break;
  default:
    fail(`Noma'lum buyruq: "${command}". Yordam uchun: node guruh.js --yordam`);
}
