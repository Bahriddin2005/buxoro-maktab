# 1-dars. Forma ma'lumotlarini tekshirish (validatsiya)

**Fayl:** `01-forma-tekshirish.js` · **Ishga tushirish:** `node 01-forma-tekshirish.js`

## Ishda qayerda kerak
Ro'yxatdan o'tish, buyurtma berish, profilni tahrirlash — foydalanuvchi biror narsa
kiritadigan har bir joyda. Frontendda (darhol xato ko'rsatish uchun) va backendda
(ishonchli himoya uchun) **ikkalasida ham** tekshiriladi.

## Kod tahlili

### 1. Email
```js
const email = String(input ?? '').trim().toLowerCase();
```
- `input ?? ''` — agar `input` `null` yoki `undefined` bo'lsa, bo'sh satr olinadi.
  Bu dastur `undefined.trim()` degan xato bilan qulamasligi uchun.
- `String(...)` — raqam yoki boshqa tur kelsa ham satrga aylantiradi.
- `.trim()` — boshidagi va oxiridagi bo'sh joylarni olib tashlaydi (foydalanuvchilar ko'pincha probel qo'shib yuborishadi).
- `.toLowerCase()` — `Anvar@Maktab.UZ` va `anvar@maktab.uz` bitta email deb hisoblanadi.

```js
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
```
Regex qismlari: `^` — boshi, `[^\s@]+` — probel va `@` bo'lmagan 1+ belgi, `@`,
yana shunday belgilar, `\.` — nuqta, `{2,}` — kamida 2 harfli domen (`uz`, `com`), `$` — oxiri.
Bu "mukammal" email tekshiruvi emas — haqiqiy tekshiruv emailga xat yuborib tasdiqlatishdir.

### 2. Telefon — *normallashtirish*
```js
const digits = String(input ?? '').replace(/\D/g, '');
```
`\D` — "raqam bo'lmagan har qanday belgi", `g` — hammasini. Natijada `+998 (90) 123-45-67`
→ `998901234567`. Keyin uzunlikka qarab yagona formatga keltiramiz: `+998901234567`.

**Muhim g'oya:** ma'lumotni bazaga **bitta formatda** saqlash. Aks holda bitta odam
uch xil yozuvda uch marta ro'yxatdan o'tib ketadi.

### 3. Parol — qoidalar jadvali
```js
const rules = [
  [password.length >= 8, 'kamida 8 ta belgi'],
  ...
];
const missing = rules.filter(([ok]) => !ok).map(([, text]) => text);
```
Har bir qoida `[shart, matn]` juftligi. `filter` bajarilmaganlarni ajratadi,
`map` faqat matnni oladi (`[, text]` — birinchi elementni tashlab, ikkinchisini olish).
Yangi qoida qo'shish uchun `if` yozish shart emas — massivga bitta qator qo'shiladi.

### 4. Butun forma
Har bir funksiya bir xil shaklda javob qaytaradi: `{ value }` yoki `{ error }`.
Shuning uchun `validateForm` hammasini bitta sikl bilan yig'adi va natija beradi:
```js
{ ok: false, errors: { email: '...', phone: '...' }, data: {...} }
```
Bu shakl frontendga qulay: `errors.email` ni email maydoni ostida ko'rsatish kifoya.

### 5. `require.main === module`
Fayl `node 01-...js` bilan ishga tushirilsa — namoyish ishlaydi. Boshqa fayl
`require('./01-...')` qilsa — faqat funksiyalar olinadi, namoyish ishlamaydi.

## Ko'p uchraydigan xatolar
- Faqat frontendda tekshirish. Brauzer tekshiruvini aylanib o'tish oson — **server ham tekshirishi shart**.
- Birinchi xatoda to'xtash. Foydalanuvchiga hamma xatoni birdaniga ko'rsatgan yaxshi.
- `trim()` qilmaslik — `"anvar@mail.uz "` bazaga probel bilan tushadi.

## Mashqlar
1. `validateName` qo'shing: kamida 2 harf, faqat harflar, probel va `'` belgisi.
2. Parolga "kamida bitta maxsus belgi (`!@#$...`)" qoidasini qo'shing.
3. Faqat Uzbekiston operatorlari kodlarini (`90, 91, 93, 94, 95, 97, 98, 99, 33, 88, 77, 50`) qabul qiling.

## Suhbatda (intervyuda) beriladigan savol
> "Nega validatsiya ham frontendda, ham backendda bo'lishi kerak?"
