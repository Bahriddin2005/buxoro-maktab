# 6-dars. Sahifalash, qidiruv va saralash

**Fayl:** `06-sahifalash-qidiruv.js` · **Ishga tushirish:** `node 06-sahifalash-qidiruv.js`

## Ishda qayerda kerak
Mahsulotlar katalogi, foydalanuvchilar jadvali, buyurtmalar tarixi, admin panel —
**ro'yxat bor joyning hammasida**. 10 000 ta yozuvni bitta sahifada ko'rsatib bo'lmaydi.

## Kod tahlili

### 1. Kiruvchi qiymatlarni "chegaralash" (clamp)
```js
const size = Math.min(100, Math.max(1, Math.floor(perPage) || 10));
const current = Math.min(totalPages, Math.max(1, Math.floor(page) || 1));
```
Bu qiymatlar odatda URL'dan keladi (`?page=3&perPage=20`), ya'ni foydalanuvchi **istalgan narsani** yozishi mumkin:
- `Math.floor('abc')` → `NaN`, `NaN || 1` → `1`. Noto'g'ri qiymat standart qiymatga aylanadi.
- `Math.max(1, ...)` — 0 yoki manfiy sahifa bo'lmaydi.
- `Math.min(totalPages, ...)` — `?page=999` oxirgi sahifani beradi.
- `perPage` ning yuqori chegarasi 100 — aks holda kimdir `?perPage=1000000` yozib serverni og'irlashtiradi.

### 2. Kesib olish
```js
const start = (current - 1) * size;
items.slice(start, start + size);
```
3-sahifa, 5 tadan: `start = 10`, elementlar `10..14`. `slice` massiv chegarasidan chiqsa ham xato bermaydi.

### 3. `meta` — frontend uchun
```js
meta: { page, perPage, total, totalPages, hasPrev, hasNext }
```
Frontend "Oldingi/Keyingi" tugmalarini yoqish/o'chirish va "23 tadan 1–5" yozuvi uchun aynan shularni so'raydi.
Bu shakl ko'p real API'larda deyarli bir xil.

### 4. Qidiruv
```js
const q = search.trim().toLowerCase();
const filtered = q ? students.filter((s) => s.name.toLowerCase().includes(q)) : students;
```
Katta-kichik harfga qaramaydigan qidiruv. Qidiruv bo'sh bo'lsa — filtrlash umuman bajarilmaydi.

### 5. Xavfsiz saralash
```js
const key = SORTABLE.includes(sortBy) ? sortBy : 'name';
```
**Oq ro'yxat (whitelist):** faqat ruxsat etilgan maydonlar bo'yicha saralash. Real loyihada `sortBy`
to'g'ridan-to'g'ri SQL so'roviga qo'yilsa — bu **SQL injection** xavfi.

```js
return (typeof x === 'string' ? x.localeCompare(y, 'uz', { numeric: true }) : x - y) * dir;
```
- Satrlar `localeCompare` bilan solishtiriladi (harflar alifbo bo'yicha to'g'ri tartiblanadi).
- `{ numeric: true }` — satr ichidagi raqamlarni son sifatida solishtiradi. Busiz tartib
  `Anvar 1, Anvar 17, Anvar 9` bo'lib qoladi, u bilan esa `Anvar 1, Anvar 9, Anvar 17`.
  (Fayl nomlari, `7-A sinf` / `10-A sinf` kabi qiymatlarda juda muhim.)
- Sonlar — ayirish bilan.
- `* dir` — `-1` ga ko'paytirish tartibni teskari qiladi. Ikkita alohida funksiya yozish shart emas.
- `[...filtered]` — asl massivni buzmaslik uchun nusxa.

### 6. Tartib muhim: qidiruv → saralash → sahifalash
Agar avval sahifalab, keyin qidirsak — faqat 1-sahifadan qidirgan bo'lamiz. Bu juda keng tarqalgan xato.

## Ko'p uchraydigan xatolar
- Sahifani 0 dan boshlash (frontend 1 dan, backend 0 dan — "bitta sahifa siljib ketdi" xatosi).
- URL'dan kelgan `page` ni satr ekanini unutish: `'2' + 1 === '21'`.
- Haqiqiy loyihada hamma ma'lumotni bazadan olib, keyin JS'da kesish. Ma'lumot ko'p bo'lsa,
  sahifalash **bazaning o'zida** qilinadi (`LIMIT 10 OFFSET 20`). Bu yerdagi mantiq esa bir xil.

## Mashqlar
1. `pageNumbers(current, totalPages)` yozing: `1 … 4 5 [6] 7 8 … 20` ko'rinishidagi tugmalar ro'yxatini qaytarsin.
2. `grade` bo'yicha filtr qo'shing (`{ grade: 7 }`).
3. Ikki maydon bo'yicha saralash: avval sinf, keyin ism.

## Suhbatda beriladigan savol
> "Offset sahifalash va cursor sahifalashning farqi nima? Cheksiz lentada qaysi biri yaxshi?"
