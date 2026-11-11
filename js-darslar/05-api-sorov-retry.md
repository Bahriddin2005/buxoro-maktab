# 5-dars. API'ga so'rov: `async/await`, timeout, retry

**Fayl:** `05-api-sorov-retry.js` · **Ishga tushirish:** `node 05-api-sorov-retry.js`

## Ishda qayerda kerak
Deyarli har bir ilova serverdan ma'lumot oladi. Real hayotda internet uziladi, server
band bo'ladi, javob kechikadi. Yaxshi dasturchi **xato bo'lishini oldindan hisobga oladi**:
foydalanuvchi abadiy "yuklanmoqda..." ni ko'rib qolmasligi kerak.

Namoyish internetsiz ishlaydi: fayl o'zi kichik server ochadi (`/flaky` — 2 marta xato beradi,
`/slow` — 2 soniya kechikadi).

## Kod tahlili

### 1. O'z xato klassimiz
```js
class HttpError extends Error {
  constructor(status, message) { super(message); this.name = 'HttpError'; this.status = status; }
}
```
`fetch` 404 yoki 500 da **xato tashlamaydi** — u faqat tarmoq uzilganda xato beradi.
Shuning uchun `res.ok` ni o'zimiz tekshirib, `status` saqlangan xato tashlaymiz.
Keyin `catch` da `err.status === 401` bo'lsa login sahifasiga yuborish mumkin.

### 2. Qaysi xatoda qayta urinish kerak
```js
if (err.name === 'TimeoutError') return true;
if (err.name === 'TypeError') return true;
if (err instanceof HttpError) return err.status >= 500 || err.status === 429;
return false;
```
- **5xx** (server xatosi), **429** (juda ko'p so'rov), **timeout**, **tarmoq** — vaqtinchalik muammolar, qayta urinish mumkin.
- **4xx** (404 topilmadi, 400 noto'g'ri so'rov, 401 ruxsat yo'q) — necha marta urinsangiz ham natija bir xil. Qayta urinish befoyda.

### 3. Timeout
```js
fetch(url, { ...options, signal: AbortSignal.timeout(timeout) })
```
`AbortSignal.timeout(3000)` — 3 soniyadan keyin so'rovni bekor qiladi va `TimeoutError` tashlaydi.
Busiz `fetch` daqiqalab kutishi mumkin.

### 4. Retry sikli va "exponential backoff"
```js
for (let attempt = 0; ; attempt++) {
  try { ... return await res.json(); }
  catch (err) {
    if (!isRetryable(err) || attempt >= retries) throw err;
    const wait = 200 * 2 ** attempt;
    await sleep(wait);
  }
}
```
- Sikl shartsiz (`;;`) — undan faqat `return` (muvaffaqiyat) yoki `throw` (taslim bo'lish) bilan chiqiladi.
- Kutish vaqti har safar **2 baravar oshadi**: 200 → 400 → 800 ms. Server og'ir ahvolda bo'lsa,
  hamma mijoz uni bir vaqtda so'rov bilan "bombardimon" qilmasligi uchun.
- `return await res.json()` — `await` shu yerda muhim: JSON o'qishdagi xato ham shu `try` ichida ushlanadi.

### 5. `{ timeout = 3000, retries = 2, ...options } = {}`
Obyektni bo'laklash + standart qiymatlar. `...options` — qolgan hamma narsa (`method`, `headers`, `body`)
o'zgarishsiz `fetch` ga uzatiladi. `= {}` — umuman argument berilmasa ham ishlaydi.

## Ko'p uchraydigan xatolar
- `res.ok` ni tekshirmaslik: 500 xatosining HTML sahifasini JSON deb o'qishga urinish.
- `await` ni unutish: `const data = fetch(...)` → `data` ma'lumot emas, `Promise` bo'ladi.
- `try/catch` siz `async` funksiya: xato "ushlanmagan Promise" bo'lib, butun dasturni yiqitishi mumkin.
- POST (to'lov!) so'rovini o'ylamasdan qayta yuborish — pul ikki marta yechilishi mumkin.
  Bunday so'rovlarni faqat server "idempotency key" ni qo'llab-quvvatlasa qayta yuboring.

## Mashqlar
1. Kutish vaqtiga tasodifiy qo'shimcha (jitter) qo'shing: `wait + Math.random() * 100`.
2. Server `Retry-After` sarlavhasini yuborsa, aynan shuncha soniya kuting.
3. `fetchJson` ni haqiqiy ochiq API bilan sinab ko'ring (masalan, `https://jsonplaceholder.typicode.com/users`).

## Suhbatda beriladigan savol
> "`fetch` qachon reject bo'ladi va qachon bo'lmaydi? 404 kelganda `catch` ishlaydimi?"
