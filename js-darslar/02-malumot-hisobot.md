# 2-dars. Ma'lumotlardan hisobot: `filter`, `map`, `reduce`, `sort`

**Fayl:** `02-malumot-hisobot.js` · **Ishga tushirish:** `node 02-malumot-hisobot.js`

## Ishda qayerda kerak
Admin panel, dashboard, "oylik savdo", "eng faol mijozlar", Excel'ga eksport — serverdan
massiv keladi va uni kerakli ko'rinishga keltirish kerak. Bu dasturchining **eng ko'p
qiladigan ishi**.

## Kod tahlili

### 1. Kichik yordamchi funksiyalar
```js
const isPaid = (order) => order.status === 'paid';
const orderTotal = (order) => order.price * order.qty;
```
Shartni bir joyda yozamiz va hamma joyda ishlatamiz. Ertaga "to'langan" holatiga
`'delivered'` ham qo'shilsa — faqat bitta qator o'zgaradi.

### 2. `reduce` — massivni bitta qiymatga "yig'ish"
```js
list.filter(isPaid).reduce((sum, order) => sum + orderTotal(order), 0);
```
- `filter` — faqat to'langanlar qoladi.
- `reduce((sum, order) => ..., 0)` — `sum` 0 dan boshlanadi, har buyurtmada qo'shilib boradi.
- **`0` ni yozish shart:** busiz bo'sh massivda `reduce` xato beradi.

### 3. `groupBy` — guruhlash
```js
(groups[key] ||= []).push(item);
```
`||=` — "agar `groups[key]` hali yo'q bo'lsa, `[]` ga teng qil". Keyin unga element qo'shamiz.
Natija: `{ Anvar: [...], Dilnoza: [...] }`.
> Node 21+ va zamonaviy brauzerlarda tayyor `Object.groupBy(items, fn)` ham bor.

### 4. Zanjir (chaining): `Object.entries → map → sort`
```js
Object.entries(groups)              // [['Anvar', [...]], ['Dilnoza', [...]]]
  .map(([customer, items]) => ({ customer, orders: items.length, total: ... }))
  .sort((a, b) => b.total - a.total);
```
- `Object.entries` obyektni `[kalit, qiymat]` juftliklari massiviga aylantiradi.
- `map` har juftlikdan jadval qatoriga mos obyekt yasaydi.
- `sort((a, b) => b.total - a.total)` — kamayish tartibida. `a - b` bo'lsa — o'sish tartibida.

### 5. `topProduct` — oddiy `for...of` ham yaxshi
Har doim `reduce` yozish shart emas. O'qishga oson bo'lsa, oddiy sikl ham professional kod.
`?? [null, 0]` — ro'yxat bo'sh bo'lsa ham dastur qulamaydi.

### 6. `countByStatus` — o'zgarmas (immutable) uslub
```js
({ ...acc, [o.status]: (acc[o.status] ?? 0) + 1 })
```
`...acc` — eski obyektni nusxalash, `[o.status]` — kalit nomi o'zgaruvchidan olinadi.
React/Redux'da aynan shu uslub talab qilinadi.

## Ko'p uchraydigan xatolar
- `sort()` ni solishtirish funksiyasiz chaqirish: `[10, 9, 100].sort()` → `[10, 100, 9]` (satr kabi saralaydi!).
- `sort()` **asl massivni o'zgartiradi**. Asl ro'yxat kerak bo'lsa: `[...arr].sort(...)` yoki `arr.toSorted(...)`.
- `reduce` ga boshlang'ich qiymat bermaslik.
- Pulni `0.1 + 0.2` kabi kasr sonlarda hisoblash. So'mda butun son, dollarda **tiyin/sentda** saqlang.

## Mashqlar
1. Har bir mahsulot bo'yicha tushumni hisoblang (`{ Daftar: 80000, ... }`).
2. O'rtacha chek (bitta to'langan buyurtmaning o'rtacha summasi)ni toping.
3. Buyurtmalarga `date` qo'shib, oylar bo'yicha guruhlang.

## Suhbatda beriladigan savol
> "`map`, `filter`, `forEach` va `reduce` ning farqi nima? Qaysi biri yangi massiv qaytaradi?"
