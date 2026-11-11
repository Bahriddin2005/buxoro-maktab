# 8-dars. Kutubxonasiz kichik REST API (CRUD)

**Fayl:** `08-rest-api-server.js`
- `node 08-rest-api-server.js --demo` — server ochiladi, o'zi so'rovlar yuboradi va natijani ko'rsatadi.
- `node 08-rest-api-server.js` — server `http://localhost:3000/tasks` da ishlaydi (brauzer yoki `curl` bilan sinang).

## Ishda qayerda kerak
Backend dasturchining asosiy ishi — API yozish. Ishda odatda Express, Fastify yoki NestJS ishlatiladi,
lekin ularning **ichida aynan shu narsa** bo'ladi. Buni kutubxonasiz bir marta yozgan o'quvchi
har qanday freymvorkni tez o'rganadi.

| Usul | Manzil | Vazifasi | Javob kodi |
|------|--------|----------|-----------|
| GET | `/tasks` | Hamma vazifalar | 200 |
| POST | `/tasks` | Yangi vazifa | 201 |
| GET | `/tasks/1` | Bitta vazifa | 200 / 404 |
| PATCH | `/tasks/1` | Qisman o'zgartirish | 200 / 400 / 404 |
| DELETE | `/tasks/1` | O'chirish | 204 / 404 |

## Kod tahlili

### 1. Javob yuborish — bitta joyda
```js
function send(res, status, body) {
  res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8' });
  res.end(body === undefined ? '' : JSON.stringify(body));
}
```
`charset=utf-8` — o'zbekcha `oʻ`, `gʻ` harflari buzilmasligi uchun. 204 (No Content) javobida tana bo'lmaydi.

### 2. So'rov tanasini o'qish
```js
for await (const chunk of req) {
  raw += chunk;
  if (raw.length > 1e6) throw new ApiError(413, "So'rov juda katta");
}
```
So'rov tanasi bo'laklab keladi. `for await` ularni birma-bir o'qiydi.
**1 MB chegara** — kimdir 10 GB yuborib serverni to'xtatib qo'ymasligi uchun.
`JSON.parse` xatosi `try/catch` bilan ushlanib, 400 xatoga aylantiriladi (500 emas — bu mijozning xatosi).

### 3. Validatsiya va "mass assignment" himoyasi
```js
return out; // faqat ruxsat etilgan maydonlar
...
const task = { id: nextId++, done: false, ...data, createdAt: ... };
```
`validateTask` faqat `title` va `done` ni qaytaradi. Shuning uchun mijoz `{ "id": 999, "isAdmin": true }`
yuborsa ham, ular obyektga **tushmaydi**. Agar `...body` ni to'g'ridan-to'g'ri yoyganimizda —
mijoz istalgan maydonni o'zgartira olardi. Bu real hayotda uchraydigan xavfsizlik zaifligi.

`partial: true` — PATCH uchun: `title` yuborilmasa, uni tekshirmaymiz (faqat `done` ni o'zgartirish mumkin).

### 4. Marshrutlash (routing) regex bilan
```js
const match = pathname.match(/^\/tasks(?:\/(\d+))?$/);
```
- `/tasks` → `match[1]` bo'sh (ro'yxat bilan ishlash).
- `/tasks/5` → `match[1] === '5'` (bitta vazifa).
- `(?: ... )?` — ixtiyoriy guruh, `(\d+)` — faqat raqamlarni ushlaydi. `/tasks/abc` → 404.

Express'dagi `app.get('/tasks/:id', ...)` ichida xuddi shunday narsa ishlaydi.

### 5. Xatolarni markazlashgan holda ushlash
```js
handle(req, res).catch((err) => {
  const status = err.status ?? 500;
  if (status === 500) console.error(err);
  send(res, status, { error: status === 500 ? 'Serverda xatolik' : err.message });
});
```
- Kod ichida istalgan joyda `throw new ApiError(404, '...')` qilish kifoya — javob shu yerda bir xil shaklda yuboriladi.
- **Kutilmagan** xato (500) tafsilotlari mijozga ko'rsatilmaydi (ular ichki ma'lumot, hakerga yordam beradi),
  faqat logga yoziladi.

### 6. HTTP status kodlari
`200` OK · `201` yaratildi · `204` tanasiz muvaffaqiyat · `400` noto'g'ri so'rov · `404` topilmadi ·
`405` usul ruxsat etilmagan · `413` juda katta · `500` server xatosi. To'g'ri kod qaytarish —
API sifatining asosiy belgisi.

## Ko'p uchraydigan xatolar
- Hamma narsaga `200` qaytarish va xatoni tanada yozish.
- Mijoz yuborgan obyektni tekshirmasdan bazaga yozish.
- `async` handler'dagi xatoni ushlamaslik — server qulaydi.
- Ma'lumotni o'zgaruvchida saqlash (bu yerdagidek) — server qayta ishga tushsa, hammasi o'chadi.
  Real loyihada baza (PostgreSQL, MongoDB) ishlatiladi.

## Mashqlar
1. `GET /tasks?done=true` filtri qo'shing (`new URL(...).searchParams.get('done')`).
2. 6-darsdagi `paginate` ni ulang: `GET /tasks?page=2&perPage=5`.
3. Vazifalarni `tasks.json` fayliga saqlang (`fs.writeFileSync`), server qayta yonganda o'qib olsin.
4. Xuddi shu API'ni Express bilan qayta yozing va farqni solishtiring.

## Suhbatda beriladigan savol
> "PUT va PATCH ning farqi nima? DELETE so'rovi muvaffaqiyatli bo'lsa qaysi status qaytariladi?"
