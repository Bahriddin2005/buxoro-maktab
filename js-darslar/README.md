# JavaScript: ishda kerak bo'ladigan real kod bo'laklari

O'quvchilar uchun 8 ta kichik dars. Har biri — real loyihalarda har kuni uchraydigan bitta vazifa.
Har bir `.js` fayl mustaqil: o'zi namoyish qiladi va natijani `assert` bilan o'zi tekshiradi.
Yonidagi `.md` faylda — kodning qadamma-qadam tahlili, keng tarqalgan xatolar, mashqlar va intervyu savoli.

**Talab:** faqat Node.js 18+ (kutubxona o'rnatish shart emas, internet ham kerak emas).

| # | Dars | Qayerda ishlatiladi | Asosiy mavzular |
|---|------|---------------------|-----------------|
| 1 | [Forma tekshirish](01-forma-tekshirish.md) | Ro'yxatdan o'tish, buyurtma formasi | `trim`, regex, normallashtirish, `Object.entries` |
| 2 | [Ma'lumotdan hisobot](02-malumot-hisobot.md) | Dashboard, admin panel | `filter`, `map`, `reduce`, `sort`, guruhlash |
| 3 | [Pul va sana formatlash](03-pul-va-sana-formatlash.md) | Narxlar, chek, "5 daqiqa oldin" | `Intl.NumberFormat`, `Intl.RelativeTimeFormat` |
| 4 | [Debounce va throttle](04-debounce-throttle.md) | Qidiruv maydoni, scroll | closure, `setTimeout`, `this` |
| 5 | [API so'rov, timeout, retry](05-api-sorov-retry.md) | Serverdan ma'lumot olish | `async/await`, `fetch`, xato klasslari |
| 6 | [Sahifalash va qidiruv](06-sahifalash-qidiruv.md) | Katalog, jadvallar | chegaralash, whitelist, saralash |
| 7 | [Kesh](07-kesh.md) | Valyuta kursi, ob-havo, profil | `Map`, TTL, Promise keshlash, `#private` |
| 8 | [REST API server](08-rest-api-server.md) | Backend | `http`, routing, status kodlar, validatsiya |

## Ishga tushirish

```bash
cd js-darslar
node 01-forma-tekshirish.js
node 08-rest-api-server.js --demo
```

Hammasini birdaniga tekshirish:

```bash
for f in 0*.js; do node "$f" --demo > /dev/null && echo "✓ $f"; done
```

## O'qitish bo'yicha tavsiya
1. Avval `.js` faylni ishga tushiring — o'quvchilar natijani ko'rsin.
2. `.md` dagi tahlilni birga o'qib, kodni qatorma-qator muhokama qiling.
3. "Ko'p uchraydigan xatolar" bo'limidagi xatoni ataylab kodga kiritib, nima buzilishini ko'rsating.
4. Mashqlarni uy vazifasi qilib bering. Fayl oxiridagi `assert` lar o'quvchi o'zgartirishi hech narsani buzmaganini tekshiradi.
