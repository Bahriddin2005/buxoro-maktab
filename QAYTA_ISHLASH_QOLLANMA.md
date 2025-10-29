# Qayta Ishlash Funksiyasi - Foydalanuvchi Qo'llanmasi

## 📋 Umumiy Ma'lumot

Qayta ishlash funksiyasi o'quvchilarga test natijalaridan norozi bo'lganda qayta test yechish uchun so'rov yuborish imkonini beradi. Admin so'rovlarni ko'rib chiqadi va ruxsat beradi yoki rad etadi.

---

## 👨‍🎓 O'quvchi Uchun Qo'llanma

### 1. Test Yakunlangandan Keyin

Test yechib bo'lgandan so'ng, natijalar sahifasida **"Qayta ishlash so'rovi"** tugmasi ko'rinadi.

### 2. Qayta Ishlash So'rovi Yuborish

1. **"Qayta ishlash so'rovi"** tugmasini bosing
2. Qayta ishlash sababini kiriting (kamida 10 ta belgi):
   - Misol: "Internet tezligi sekin edi, savollarni to'g'ri yuklamadi"
   - Misol: "Vaqt yetmadi, barcha savollarga javob bera olmadim"
   - Misol: "Ba'zi savollarni tushunmadim, qayta o'rganib kelmoqchiman"

3. Sabab kiritilgandan keyin **OK** tugmasini bosing
4. Muvaffaqiyatli xabar ko'rinadi: ✅ **"Qayta ishlash so'rovi muvaffaqiyatli yuborildi!"**
5. Admin sizning so'rovingizni ko'rib chiqadi

### 3. So'rov Holati

So'rovning 3 xil holati bo'lishi mumkin:

- 🕐 **Kutilmoqda (pending)**: Admin hali ko'rib chiqmadi
- ✅ **Tasdiqlangan (approved)**: Admin ruxsat berdi, endi qayta test yechishingiz mumkin
- ❌ **Rad etilgan (rejected)**: Admin rad etdi, qayta test yechish mumkin emas

---

## 👨‍💼 Admin Uchun Qo'llanma

### 1. Qayta Ishlash So'rovlariga Kirish

1. Dashboard'ga kiring
2. Yuqori menyuda **"Qayta Ishlash"** tugmasini bosing
3. Yoki to'g'ridan-to'g'ri: `https://buxorobilimdonlarmaktabi.uz/tests/retake-requests/`

### 2. So'rovlarni Ko'rib Chiqish

**Filtrlar:**
- **Barcha so'rovlar**: Barcha so'rovlarni ko'rsatadi
- **Kutilmoqda**: Hali qarab chiqilmagan so'rovlar
- **Tasdiqlangan**: Ruxsat berilgan so'rovlar
- **Rad etilgan**: Rad etilgan so'rovlar

**Qidirish:**
- O'quvchi ismini qidirish maydonida yozib qidiring

### 3. So'rovni Tasdiqlash yoki Rad Etish

1. **Tasdiqlash (Approve)**:
   - O'quvchi ma'lumotlarini tekshiring
   - Oldingi natijani ko'rib chiqing
   - Sabab to'g'ri va asosli bo'lsa, **"Tasdiqlash"** tugmasini bosing
   - Admin javobini yozish mumkin (ixtiyoriy)
   - O'quvchi endi testni qayta yecha oladi

2. **Rad Etish (Reject)**:
   - Sabab yetarli emas yoki noto'g'ri bo'lsa
   - **"Rad etish"** tugmasini bosing
   - Admin javobini yozish mumkin (sabab tushuntirish)
   - O'quvchi qayta test yecha olmaydi

### 4. So'rov Ma'lumotlari

Har bir so'rovda quyidagi ma'lumotlar ko'rsatiladi:

- **O'quvchi**: Ism, familiya, sinf
- **Test**: Test nomi va fan
- **Oldingi Natija**: Ball, foiz, baho
- **Sabab**: O'quvchi yozgan sabab
- **Holat**: Kutilmoqda / Tasdiqlangan / Rad etilgan
- **Sana**: So'rov yuborilgan vaqt

---

## 🔧 Texnik Ma'lumotlar

### API Endpoints

1. **So'rov yuborish** (Student):
   ```
   POST /tests/{test_id}/request-retake/
   Body: { "reason": "Sabab matni" }
   ```

2. **So'rovlarni ko'rish** (Admin):
   ```
   GET /tests/retake-requests/
   Query params: ?status=pending|approved|rejected|all
   ```

3. **So'rovni hal qilish** (Admin):
   ```
   POST /tests/retake-requests/{request_id}/handle/
   Body: { "action": "approve|reject", "admin_response": "Admin javobi" }
   ```

### Database Models

**TestRetakeRequest Model:**
```python
- student: ForeignKey(User)
- test: ForeignKey(Test)
- previous_attempt: ForeignKey(TestAttempt)
- reason: TextField (o'quvchi sababi)
- status: CharField (pending/approved/rejected)
- admin_response: TextField (admin javobi)
- approved_by: ForeignKey(User) (tasdiqlagan admin)
- created_at: DateTimeField
- handled_at: DateTimeField
- is_used: BooleanField (foydalanilganmi)
```

---

## ✅ Xususiyatlar

1. ✅ O'quvchi test yechib bo'lgandan so'ng so'rov yuborishi mumkin
2. ✅ Sabab kiritish majburiy (kamida 10 ta belgi)
3. ✅ Admin barcha so'rovlarni ko'rishi mumkin
4. ✅ Admin so'rovlarni tasdiqlashi yoki rad etishi mumkin
5. ✅ Admin javob yozishi mumkin
6. ✅ Tasdiqlangan so'rov bilan o'quvchi testni qayta yecha oladi
7. ✅ Bir vaqtda faqat bitta pending so'rov bo'lishi mumkin
8. ✅ So'rovlar sana bo'yicha tartiblangan
9. ✅ Real-time yangilanish (Yangilash tugmasi)
10. ✅ Qidirish va filtrlash

---

## 📱 Foydalanish Misoli

### O'quvchi:

1. Test yechdi: 70 ball (60%)
2. "Qayta ishlash so'rovi" tugmasini bosdi
3. Sabab: "Internet uzilib turdi, barcha savollarni ko'ra olmadim"
4. So'rov yuborildi ✅

### Admin:

1. "Qayta Ishlash So'rovlari" sahifasiga kirdi
2. O'quvchi so'rovini ko'rdi
3. Sabab to'g'ri deb topdi
4. "Tasdiqlash" tugmasini bosdi
5. Admin javobi: "Ruxsat berildi, testni diqqat bilan yeching"
6. So'rov tasdiqlandi ✅

### O'quvchi:

1. Testlar sahifasiga kirdi
2. "Test yechish" tugmasi yana aktiv bo'ldi
3. Testni qayta yechdi
4. Yangi natija: 85 ball (85%) ✅

---

## 🚀 Kelajakdagi Yaxshilanishlar

- [ ] Email bildirishnomalar (o'quvchi va admin uchun)
- [ ] SMS bildirishnomalar
- [ ] So'rovlar statistikasi
- [ ] Avtomatik tasdiqlash (ma'lum shartlar bo'yicha)
- [ ] So'rovlar tarixi (o'quvchi profili)
- [ ] Maksimal qayta ishlash soni (masalan: 3 marta)
- [ ] Qayta ishlash uchun to'lov tizimi (ixtiyoriy)

---

## 📞 Yordam

Agar savollaringiz bo'lsa:
- Email: support@buxorobilimdonlarmaktabi.uz
- Telefon: +998 XX XXX XX XX
- Telegram: @buxorabilimdonlar_support

---

**Yaratilgan sana:** 2025-10-24  
**Versiya:** 1.0.0  
**Mualliflar:** Buxoro Bilimdonlar Maktabi IT Jamoasi

