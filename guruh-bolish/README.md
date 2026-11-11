# Guruhga bo'lish

O'qituvchilar uchun kichik JavaScript (Node.js) dastur.

**Muammo:** darsda sinfni guruhlarga bo'lishga vaqt ketadi, guruhlar teng chiqmaydi
(bitta-ikkita o'quvchi "ortib qoladi"), doskaga chaqirganda esa ba'zilar qayta-qayta
chiqadi, ba'zilar umuman chiqmaydi.

**Yechim:**
- `bol` — o'quvchilarni tasodifiy, lekin **teng** guruhlarga bo'ladi (hajmlar farqi ko'pi bilan 1).
- `chaqir` — o'quvchini tasodifiy chaqiradi, **hamma bir martadan chiqmaguncha hech kim takrorlanmaydi**.
  Holat fayl yonida saqlanadi, shuning uchun keyingi darsda ham davom etadi.

Hech qanday kutubxona kerak emas — faqat Node.js 18+.

## Ishlatish

`sinf.txt` fayliga har qatorga bitta ism yozing (namuna fayl bor), so'ng:

```bash
node guruh.js bol sinf.txt 4            # 4 ta guruhga bo'lish
node guruh.js bol sinf.txt --hajm 3     # har guruhda ~3 kishi
node guruh.js chaqir sinf.txt           # kimni chaqiramiz?
node guruh.js yangila sinf.txt          # chaqirilganlarni tozalash
```

Namuna natija:

```
15 ta o'quvchi → 4 ta guruh

1-guruh (4 kishi):
  • Saidov Doniyor
  • Karimova Dilnoza
  ...
```

## Test

```bash
node --test
```

## Fayllar

| Fayl | Vazifasi |
|------|----------|
| `logic.js` | Asosiy mantiq: ismlarni o'qish, aralashtirish, guruhlash, takrorlanmas tanlov |
| `guruh.js` | Terminal buyruqlari |
| `test.js`  | Testlar (`node:test`) |
| `sinf.txt` | Namuna ro'yxat |
