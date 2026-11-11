# 3-dars. Pul, son va sanalarni formatlash (`Intl`)

**Fayl:** `03-pul-va-sana-formatlash.js` · **Ishga tushirish:** `node 03-pul-va-sana-formatlash.js`

## Ishda qayerda kerak
Internet-do'kon narxlari, chek, bank ilovasi, "5 daqiqa oldin" yozuvi, statistika (`1,3 mln`).
Ko'p junior dasturchilar buni qo'lda `replace` va `split` bilan yozadi — bu xato va keraksiz.
JavaScript'da tayyor **`Intl`** vositasi bor.

## Kod tahlili

### 1. Formatter bir marta yaratiladi
```js
const somFormatter = new Intl.NumberFormat('uz-UZ', {
  style: 'currency', currency: 'UZS', maximumFractionDigits: 0,
});
```
- `'uz-UZ'` — o'zbek tili, O'zbekiston qoidalari (minglik ajratgich — probel, kasr — vergul).
- `style: 'currency'` + `currency: 'UZS'` — "so'm" so'zi avtomatik qo'shiladi.
- `maximumFractionDigits: 0` — tiyinlarni ko'rsatmaslik.
- Formatterni **funksiya tashqarisida** yaratamiz: uni yaratish "qimmat", 1000 qatorli jadvalda
  har safar yangisini yaratish sekinlashtiradi.

Natija: `1 250 000 soʻm`. Valyutani `'USD'`, tilni `'en-US'` ga almashtirsangiz — `$1,250,000`.

### 2. Qisqa yozuv
```js
new Intl.NumberFormat('uz-UZ', { notation: 'compact' }).format(1250000) // "1,3 mln"
```
YouTube/Instagram'dagi "1,3 mln ko'rish" aynan shunday yasaladi.

### 3. Sana
```js
new Intl.DateTimeFormat('uz-UZ', { dateStyle: 'long' }).format(new Date('2026-11-11')) // "11-noyabr, 2026"
```
Oy nomlarini massivda qo'lda yozish shart emas.

### 4. "Qancha vaqt oldin" — `timeAgo`
```js
const diffSec = Math.round((new Date(date) - now) / 1000);
```
Ikki sanani ayirsak — **millisekundlar** farqi chiqadi. 1000 ga bo'lib, soniyaga o'tamiz.
Manfiy son — o'tmish, musbat — kelajak.

```js
for (const [unit, seconds] of UNITS) {
  if (Math.abs(diffSec) >= seconds || unit === 'second') {
    return relativeFormatter.format(Math.round(diffSec / seconds), unit);
  }
}
```
Birliklar kattadan kichikka tartiblangan. Farq qaysi birlikka birinchi "sig'sa", o'shani olamiz.
`numeric: 'auto'` tufayli `-1 day` → **"kecha"**, `1 day` → **"ertaga"**.

### 5. `now` parametri — test qilish uchun
`timeAgo(date, now = new Date())` — odatda hozirgi vaqt olinadi, lekin testda biz aniq vaqt beramiz.
Aks holda test ertaga boshqa natija beradi. Bu **"qaramlikni tashqaridan berish"** degan muhim g'oya.

## Ko'p uchraydigan xatolar
- `new Date('11.11.2026')` — bunday formatni brauzerlar turlicha tushunadi. Doim **ISO format**: `'2026-11-11'`.
- `getMonth()` 0 dan boshlanadi: yanvar = 0, dekabr = 11.
- Natijadagi bo'shliq oddiy probel emas (` ` — "tor bo'shliq"). Satrlarni taqqoslashda shuni hisobga oling (`plain` funksiyasiga qarang).

## Mashqlar
1. `formatPhone('+998901234567')` → `+998 90 123 45 67` funksiyasini yozing.
2. `formatPercent(0.857)` → `86%` (`style: 'percent'`).
3. Ikki sana orasidagi kunlar sonini hisoblovchi `daysBetween(a, b)` yozing.

## Suhbatda beriladigan savol
> "Nega `toFixed(2)` bilan pulni formatlash yetarli emas?"
