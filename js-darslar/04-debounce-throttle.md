# 4-dars. Debounce va throttle

**Fayl:** `04-debounce-throttle.js` · **Ishga tushirish:** `node 04-debounce-throttle.js`

## Ishda qayerda kerak
- **Debounce** — qidiruv maydoni: foydalanuvchi yozib bo'lgach bitta so'rov yuboriladi,
  har bir harf uchun emas. Shuningdek: formani avtomatik saqlash, oyna o'lchami o'zgarganda qayta hisoblash.
- **Throttle** — scroll, sichqoncha harakati, "cheksiz lenta" (pastga yetganda yangi postlar yuklash).

Bu **frontend intervyularida eng ko'p so'raladigan** vazifalardan biri.

## Farqi — oddiy misolda
Liftni tasavvur qiling:
- **Debounce:** eshik har kim kirganda qaytadan 5 soniya kutadi. Odamlar kelishdan to'xtagandagina yuradi.
- **Throttle:** lift har 5 daqiqada bir marta jo'naydi, kim kelgan bo'lsa olib ketadi.

## Kod tahlili

### Debounce
```js
function debounce(fn, delay) {
  let timer = null;
  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}
```
1. `debounce` **yangi funksiya qaytaradi**. Biz aslida o'shani chaqiramiz.
2. `timer` o'zgaruvchisi tashqi funksiyada, lekin ichki funksiya uni "eslab qoladi" — bu **closure (yopilish)**.
   Har bir chaqiruv o'sha bitta `timer` ni ko'radi.
3. Har chaqiruvda: eski taymer bekor qilinadi (`clearTimeout`) va yangisi qo'yiladi.
   Demak, `delay` ms davomida yangi chaqiruv bo'lmasagina `fn` ishlaydi.
4. `...args` — barcha argumentlarni massivga yig'adi; `fn.apply(this, args)` — ularni va `this` ni
   asl funksiyaga uzatadi. Shuning uchun ichki funksiya `function` bilan yozilgan, arrow emas.

Namoyishda: 6 ta harf yozildi → serverga **faqat 1 ta** so'rov: `"maktab"`.

### Throttle
```js
let last = 0;
...
if (now - last >= interval) { last = now; fn.apply(this, args); }
```
Oxirgi ishlagan vaqtni eslab qolamiz. Yetarli vaqt o'tmagan bo'lsa — chaqiruvni shunchaki e'tiborsiz qoldiramiz.
Namoyishda: ~50 ta hodisadan faqat ~4 tasi ishlanadi.

## Ko'p uchraydigan xatolar
- Debounce'ni **har renderda qayta yaratish** (React'da): har safar yangi `timer` paydo bo'ladi va hech narsa ishlamaydi.
  React'da `useMemo`/`useRef` bilan bir marta yaratiladi.
- Komponent yopilganda taymerni tozalamaslik — yo'qolgan sahifa uchun so'rov ketadi.
- Debounce va throttle'ni adashtirish: qidiruvga throttle qo'yilsa, oxirgi harf yo'qolishi mumkin.

## Mashqlar
1. Debounce'ga `cancel()` metodini qo'shing (`debounced.cancel()` kutilayotgan chaqiruvni bekor qilsin).
2. Throttle oxirgi chaqiruvni ham bajarsin ("trailing" rejim): interval tugaganda eng so'nggi argumentlar bilan bir marta ishlasin.
3. HTML sahifada `<input>` ga ulang va natijani konsolda kuzating.

## Suhbatda beriladigan savol
> "Debounce funksiyasini qog'ozda yozib bering va unda closure qayerda ekanini tushuntiring."
