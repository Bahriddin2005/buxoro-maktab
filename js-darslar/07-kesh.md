# 7-dars. Kesh (cache)

**Fayl:** `07-kesh.js` · **Ishga tushirish:** `node 07-kesh.js`

## Ishda qayerda kerak
Valyuta kursi, ob-havo, kategoriyalar ro'yxati, foydalanuvchi profili — tez-tez o'zgarmaydigan,
lekin tez-tez so'raladigan ma'lumotlar. Kesh ilovani **tezlashtiradi** va pullik API'larda **pul tejaydi**.

## Kod tahlili

### 1. `Map` — kesh uchun to'g'ri tuzilma
```js
#store = new Map();
```
- `Map` kalit sifatida istalgan qiymatni qabul qiladi va tez ishlaydi.
- `#store` — **xususiy (private) maydon**. Klassdan tashqarida `cache.#store` ga murojaat qilib bo'lmaydi —
  hamma faqat `get/set/delete` orqali ishlaydi.

### 2. TTL — "yashash muddati"
```js
set(key, value) { this.#store.set(key, { value, expiresAt: Date.now() + this.ttlMs }); }

get(key) {
  ...
  if (Date.now() > entry.expiresAt) { this.#store.delete(key); return undefined; }
```
Har bir yozuv bilan birga uning "yaroqlilik muddati" saqlanadi. Muddati o'tgan yozuv o'qilganda o'chiriladi.
Aks holda foydalanuvchi kechagi valyuta kursini ko'rib qoladi.

### 3. Asosiy hiyla: Promise'ni keshlash
```js
const promise = fn(key).catch(...);
cache.set(key, promise);
return promise;
```
Agar biz natija kelgandan **keyin** keshga yozsak, bir vaqtda kelgan 3 ta so'rov keshni bo'sh ko'radi
va serverga 3 ta so'rov ketadi. Biz esa so'rov boshlanishi bilanoq **Promise'ning o'zini** saqlaymiz —
qolgan 2 ta chaqiruvchi o'sha Promise'ni kutadi. Namoyishda: 3 ta chaqiruv → 1 ta haqiqiy so'rov.

### 4. Xatoni keshlamaslik
```js
fn(key).catch((err) => { cache.delete(key); throw err; });
```
Server bir lahza ishlamay qolsa, xatoni 5 daqiqa keshlab qo'ysak — hamma 5 daqiqa xato ko'radi.
Shuning uchun xatoda yozuv o'chiriladi va xato **qayta tashlanadi** (`throw err`), chaqiruvchi uni bilishi kerak.

### 5. `hit !== undefined`
`if (hit)` yozilsa, `0`, `''`, `false` kabi to'g'ri qiymatlar ham "yo'q" deb hisoblanardi.

## Ko'p uchraydigan xatolar
- Muddatsiz kesh: ma'lumot eskiradi va xotira cheksiz o'sadi.
- Har bir foydalanuvchiga xos ma'lumotni umumiy kalit bilan keshlash — bir odam boshqasining ma'lumotini ko'rib qoladi!
  Kalitga foydalanuvchi ID sini qo'shing: `profile:${userId}`.
- Ma'lumot o'zgarganda keshni tozalashni unutish (masalan, profil tahrirlangandan keyin).

## Mashqlar
1. `TTLCache` ga `maxSize` qo'shing: limitdan oshsa, eng eski yozuvni o'chirsin (`Map` qo'shilish tartibini saqlaydi — `map.keys().next().value`).
2. `cachedAsync` bir nechta argument bilan ishlasin (kalit: `JSON.stringify(args)`).
3. `cache.clear()` va `cache.size` qo'shing.

## Suhbatda beriladigan savol
> "Kompyuter fanidagi ikki eng qiyin narsa: keshni yangilash va nom qo'yish. Keshni qachon tozalash kerakligini qanday aniqlaysiz?"
