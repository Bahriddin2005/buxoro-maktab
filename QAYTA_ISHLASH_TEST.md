# Qayta Ishlash Funksiyasini Test Qilish

## Test Ssenariysi

### 1. O'quvchi Sifatida Test Qilish

1. **Login qiling:**
   - Email: student@student.buxorobilimdonlar.uz
   - Parol: student123

2. **Testni yeching:**
   - Testlar sahifasiga boring
   - Biror testni tanlang
   - "Test yechish" tugmasini bosing
   - Savollarni javoblang
   - "Testni yakunlash" tugmasini bosing

3. **Qayta ishlash so'rovi yuboring:**
   - Natijalar sahifasida "Qayta ishlash so'rovi" tugmasini bosing
   - Sabab kiriting: "Internet tezligi sekin edi, savollarni to'g'ri yuklamadi"
   - OK tugmasini bosing
   - Muvaffaqiyatli xabar ko'rining

4. **Testni yana yechishga urinish:**
   - Testlar sahifasiga qayting
   - "Test yechish" tugmasi disabled bo'lishi kerak
   - Chunki admin hali ruxsat bermagan

### 2. Admin Sifatida Test Qilish

1. **Login qiling:**
   - Email: admin@buxorobilimdonlarmaktabi.uz
   - Parol: admin123

2. **So'rovlarni ko'ring:**
   - Dashboard'da "Qayta Ishlash" tugmasini bosing
   - Yoki to'g'ridan-to'g'ri: http://127.0.0.1:8000/tests/retake-requests/

3. **So'rovni tasdiqlang:**
   - "Kutilmoqda" filterini tanlang
   - O'quvchi so'rovini toping
   - "Ko'rish" yoki "Tasdiqlash" tugmasini bosing
   - Admin javobini yozing (ixtiyoriy)
   - "Tasdiqlash" tugmasini bosing
   - Muvaffaqiyatli xabar ko'rining

### 3. O'quvchi Qayta Test Yechish

1. **O'quvchi sifatida login qiling**

2. **Testlar sahifasiga boring:**
   - "Test yechish" tugmasi yana aktiv bo'lishi kerak
   - Badge ko'rsatiladi: "Qayta ishlash ruxsati berilgan"

3. **Testni qayta yeching:**
   - "Test yechish" tugmasini bosing
   - Yangi attempt yaratiladi
   - Savollarni javoblang
   - "Testni yakunlash" tugmasini bosing

4. **Natijalarni ko'ring:**
   - Yangi natija ko'rsatiladi
   - Qayta ishlash ruxsati ishlatilgan

5. **Yana qayta ishlash so'rovi yuborishga urinish:**
   - "Qayta ishlash so'rovi" tugmasi disabled bo'lishi kerak
   - Yoki so'rov yuborsa, "Allaqachon qayta ishlash so'rovi yuborilgan" xabari chiqadi

---

## API Testlari

### 1. So'rov Yuborish

```bash
curl -X POST http://127.0.0.1:8000/tests/1/request-retake/ \
  -H "Content-Type: application/json" \
  -H "Cookie: csrftoken=YOUR_CSRF_TOKEN; sessionid=YOUR_SESSION_ID" \
  -H "X-CSRFToken: YOUR_CSRF_TOKEN" \
  -d '{"reason": "Internet tezligi sekin edi, savollarni to\'g\'ri yuklamadi"}'
```

**Kutilayotgan Javob:**
```json
{
  "message": "Qayta ishlash so'rovi muvaffaqiyatli yuborildi!",
  "request_id": 1
}
```

### 2. So'rovlarni Olish (Admin)

```bash
curl http://127.0.0.1:8000/tests/retake-requests/ \
  -H "Accept: application/json" \
  -H "Cookie: sessionid=ADMIN_SESSION_ID"
```

**Kutilayotgan Javob:**
```json
{
  "requests": [
    {
      "id": 1,
      "student_name": "Ali Valiyev",
      "student_username": "ali_v",
      "test_title": "Matematika Test 1",
      "test_subject": "Matematika",
      "previous_score": 70,
      "previous_percentage": 70.0,
      "previous_grade": "Yaxshi",
      "reason": "Internet tezligi sekin edi",
      "status": "pending",
      "created_at": "2025-10-24T10:00:00Z"
    }
  ],
  "total": 1,
  "pending": 1,
  "approved": 0,
  "rejected": 0
}
```

### 3. So'rovni Tasdiqlash (Admin)

```bash
curl -X POST http://127.0.0.1:8000/tests/retake-requests/1/handle/ \
  -H "Content-Type: application/json" \
  -H "Cookie: csrftoken=ADMIN_CSRF_TOKEN; sessionid=ADMIN_SESSION_ID" \
  -H "X-CSRFToken: ADMIN_CSRF_TOKEN" \
  -d '{
    "action": "approve",
    "admin_response": "Ruxsat berildi, testni diqqat bilan yeching"
  }'
```

**Kutilayotgan Javob:**
```json
{
  "message": "So'rov tasdiqlandi"
}
```

---

## Database Testlari

### 1. TestRetakeRequest Model

```sql
-- So'rovlarni ko'rish
SELECT * FROM tests_app_testretakerequest;

-- Pending so'rovlar
SELECT * FROM tests_app_testretakerequest WHERE status = 'pending';

-- Approved so'rovlar
SELECT * FROM tests_app_testretakerequest WHERE status = 'approved';

-- Ishlatilgan ruxsatlar
SELECT * FROM tests_app_testretakerequest WHERE is_used = TRUE;
```

### 2. TestAttempt Model

```sql
-- O'quvchining barcha urinishlari
SELECT * FROM tests_app_testattempt WHERE student_id = 1;

-- Test uchun barcha urinishlar
SELECT * FROM tests_app_testattempt WHERE test_id = 1;
```

---

## Edge Cases (Chekkaviy Holatlar)

### 1. Bir vaqtda 2 ta so'rov yuborish

- **Test:** O'quvchi 2 marta "Qayta ishlash so'rovi" tugmasini bosadi
- **Kutilayotgan:** Ikkinchi marta xato xabari: "Allaqachon qayta ishlash so'rovi yuborilgan"

### 2. Ruxsat berilmagan testni yechish

- **Test:** O'quvchi testni yechishga urinadi (ruxsat olmagan)
- **Kutilayotgan:** Xato xabari: "Siz allaqachon bu testni topshirgansiz. Qayta topshirish uchun admin ruxsati kerak."

### 3. Ruxsatni 2 marta ishlatish

- **Test:** O'quvchi ruxsat bilan testni yechadi, keyin yana yechishga urinadi
- **Kutilayotgan:** Ruxsat `is_used=True` bo'ladi, ikkinchi marta yecha olmaydi

### 4. Rad etilgan so'rovdan keyin yana so'rov yuborish

- **Test:** Admin so'rovni rad etadi, o'quvchi yana so'rov yuboradi
- **Kutilayotgan:** Yangi so'rov yaratiladi, status=pending

### 5. Test tugallanmagan holatda so'rov yuborish

- **Test:** O'quvchi testni boshlab, tugallamay, so'rov yuborishga urinadi
- **Kutilayotgan:** Xato xabari: "Siz hali bu testni topshirmadingiz"

---

## UI Testlari

### 1. "Qayta ishlash so'rovi" Tugmasi

- Test tugallanmagan: **Ko'rinmaydi**
- Test tugallangan: **Ko'rinadi**
- So'rov yuborilgan (pending): **Disabled**
- So'rov tasdiqlangan (approved, not used): **Ko'rinmaydi** (test yechish mumkin)
- So'rov rad etilgan (rejected): **Ko'rinadi** (yana yuborish mumkin)

### 2. "Test yechish" Tugmasi

- Hali yechmagan: **Aktiv**
- Yechib bo'lgan: **Disabled**
- Qayta ishlash ruxsati bor: **Aktiv** (badge ko'rsatiladi)
- Davom ettirmoqda: **Aktiv**

### 3. Admin Paneli

- Pending so'rovlar: **Sariq badge**
- Approved so'rovlar: **Yashil badge**
- Rejected so'rovlar: **Qizil badge**

---

## Performance Testlari

### 1. Ko'p So'rovlar

- 100 ta o'quvchi bir vaqtda so'rov yuboradi
- Database query'lar optimallashtirilgan
- N+1 problem yo'q (select_related, prefetch_related)

### 2. Ko'p Ruxsatlar

- 100 ta o'quvchi bir vaqtda testni yechadi (ruxsat bilan)
- Transaction atomic ishlatilgan
- Race condition yo'q

---

## Security Testlari

### 1. Authorization

- O'quvchi boshqa o'quvchining so'rovini ko'ra olmaydi
- O'quvchi admin panelga kira olmaydi
- O'qituvchi qayta ishlash so'rovlarini ko'ra olmaydi

### 2. Validation

- Sabab bo'sh bo'lsa: **Xato**
- Sabab 10 belgidan kam bo'lsa: **Xato**
- Test tugallanmagan: **Xato**
- Ruxsatsiz testni yechish: **Xato**

### 3. CSRF Protection

- CSRF token tekshiriladi
- Har bir POST so'rovda token talab qilinadi

---

## Bug Report Format

Agar xato topsangiz, quyidagi formatda xabar bering:

```
**Title:** [Bug] Qayta ishlash so'rovi yuborilmadi

**Tavsif:**
O'quvchi "Qayta ishlash so'rovi" tugmasini bosdi, lekin so'rov yuborilmadi.

**Takrorlash:**
1. O'quvchi sifatida login qiling
2. Testni yeching
3. "Qayta ishlash so'rovi" tugmasini bosing
4. Sabab kiriting
5. OK tugmasini bosing

**Kutilayotgan natija:**
So'rov yuborilishi va muvaffaqiyatli xabar ko'rinishi kerak.

**Haqiqiy natija:**
Xato xabari: "Server bilan bog'lanishda xatolik"

**Browser Console:**
```
Error: Failed to fetch
    at requestRetake (test_results.html:1010)
```

**Server Logs:**
```
[ERROR] IntegrityError: NOT NULL constraint failed: tests_app_testretakerequest.reason
```

**Muhit:**
- OS: macOS 12.0
- Browser: Chrome 118
- Django: 4.2.7
- Python: 3.13.7
```

