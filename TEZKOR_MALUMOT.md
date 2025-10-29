# ⚡ TEZKOR MA'LUMOT - Buxoro Bilimdonlar Maktabi

**Proyekt:** Test Platformasi  
**Versiya:** 1.0.0  
**Django:** 5.2.5  
**Status:** ✅ Production Ready

---

## 🚀 TEZKOR ISHGA TUSHIRISH

```bash
# 1. Virtual environment aktivatsiya
source venv/bin/activate

# 2. Dependencies o'rnatish (agar kerak bo'lsa)
pip install -r requirements.txt

# 3. Migratsiyalar (agar kerak bo'lsa)
python manage.py migrate

# 4. Serverni ishga tushirish
python manage.py runserver 0.0.0.0:8000

# 5. Brauzerda ochish
# http://127.0.0.1:8000
```

---

## 👥 DEMO ACCOUNTS

### Admin:
- **Email:** admin@buxorobilimdonlarmaktabi.uz
- **Password:** admin123
- **Imkoniyatlar:** Barcha funksiyalar

### O'qituvchi:
- **Email:** teacher1@buxorobilimdonlar.uz
- **Password:** teacher123
- **Imkoniyatlar:** Test yaratish, natijalarni ko'rish

### O'quvchi:
- **Email:** student1@student.buxorobilimdonlar.uz
- **Password:** student123
- **Imkoniyatlar:** Test yechish, natijalarni ko'rish

---

## 📱 SAHIFALAR

### Asosiy:
- `/` - Bosh sahifa
- `/admin/` - Django admin panel
- `/accounts/login/` - Kirish
- `/accounts/signup/` - Ro'yxatdan o'tish
- `/accounts/dashboard/` - Dashboard

### Testlar:
- `/tests/` - Testlar ro'yxati
- `/tests/create/` - Test yaratish
- `/tests/<id>/take/` - Test yechish
- `/tests/<id>/results/` - Natijalar
- `/tests/all-results/` - Barcha natijalar

### Admin:
- `/accounts/verification-requests/` - Tasdiqlash so'rovlari
- `/tests/retake-requests/` - Qayta ishlash so'rovlari
- `/tests/grade-results/` - Sinf bo'yicha natijalar

---

## 🔧 DJANGO COMMANDS

```bash
# Superuser yaratish
python manage.py createsuperuser

# Migratsiyalar
python manage.py makemigrations
python manage.py migrate

# Static files yig'ish
python manage.py collectstatic

# Sample data yaratish
python create_sample_data.py

# Server
python manage.py runserver 0.0.0.0:8000

# Shell
python manage.py shell
```

---

## 🎯 ASOSIY FUNKSIYALAR

### ✅ Authentication
- Ro'yxatdan o'tish
- Kirish/Chiqish
- Email domain validatsiyasi
- Admin tasdiqlash

### ✅ Test Management
- Test CRUD (yaratish, o'qish, yangilash, o'chirish)
- 3 xil savol turi
- Rasmli savollar
- Excel import/export
- Vaqt chegarasi

### ✅ Test Taking
- Real-time timer
- Javoblarni saqlash
- Progress tracking
- Avtomatik baholash

### ✅ Results & Analytics
- Shaxsiy natijalar
- Sinf bo'yicha statistika
- Umumiy ko'rsatkichlar
- Excel export

### ✅ Retake System
- So'rov yuborish
- Admin tasdiqlash
- Qayta test yechish

---

## 📊 MODELLAR (Quick Reference)

```python
# User Model
User(username, email, role, is_verified, grade, class_name)

# Test Model
Test(title, subject, grade, time_limit, max_attempts)

# Question Model
Question(test, question_text, question_type, points, image)

# TestAttempt Model
TestAttempt(student, test, score, percentage, is_completed)

# TestRetakeRequest Model
TestRetakeRequest(student, test, reason, status, admin_response)
```

---

## 🔐 ROLES & PERMISSIONS

### Student (O'quvchi):
- ✅ Test yechish
- ✅ Natijalarni ko'rish
- ✅ Qayta ishlash so'rovi
- ❌ Test yaratish
- ❌ Boshqalarning natijalarini ko'rish

### Teacher (O'qituvchi):
- ✅ Test yaratish/tahrirlash
- ✅ Savol qo'shish
- ✅ Natijalarni ko'rish
- ✅ Excel import/export
- ❌ Foydalanuvchilarni tasdiqlash

### Admin (Administrator):
- ✅ Barcha funksiyalar
- ✅ Foydalanuvchilarni tasdiqlash
- ✅ Qayta ishlash so'rovlari
- ✅ Barcha testlar va natijalar
- ✅ Tizim sozlamalari

---

## 📁 MUHIM FAYLLAR

### Settings:
- `mytest/settings.py` - Asosiy sozlamalar
- `mytest/urls.py` - URL routing
- `requirements.txt` - Dependencies

### Models:
- `accounts/models.py` - User, VerificationRequest
- `tests_app/models.py` - Test, Question, Answer, etc.

### Views:
- `accounts/views.py` - Auth va dashboard
- `tests_app/views.py` - Test CRUD va yechish
- `tests_app/views_overall.py` - Umumiy natijalar

### Templates:
- `templates/base.html` - Asosiy shablon
- `templates/accounts/` - Auth sahifalari
- `templates/tests_app/` - Test sahifalari

---

## 🐛 DEBUG & LOGGING

### Debug Mode:
```python
# settings.py
DEBUG = True  # Development
DEBUG = False  # Production
```

### Logs:
```bash
# Log fayli
logs/django.log

# Log ko'rish
tail -f logs/django.log

# Log tozalash
> logs/django.log
```

### Django Shell:
```bash
python manage.py shell

# Test qilish
>>> from accounts.models import User
>>> User.objects.all()
>>> from tests_app.models import Test
>>> Test.objects.filter(is_active=True)
```

---

## 🌐 API ENDPOINTS

### Authentication:
```
POST /accounts/signup/
POST /accounts/login/
POST /accounts/logout/
GET  /accounts/dashboard/
GET  /accounts/profile/
```

### Tests:
```
GET    /tests/
POST   /tests/create/
GET    /tests/<id>/
PUT    /tests/<id>/edit/
DELETE /tests/<id>/delete/
POST   /tests/<id>/take/
POST   /tests/<id>/request-retake/
```

### Results:
```
GET /tests/<id>/results/
GET /tests/all-results/
GET /tests/grade-results/
GET /tests/overall-results/
GET /tests/<id>/export/
```

### Admin:
```
GET  /accounts/verification-requests/
POST /accounts/approve-verification/<id>/
POST /accounts/reject-verification/<id>/
GET  /tests/retake-requests/
POST /tests/retake-requests/<id>/handle/
```

---

## 🔥 TEZKOR YECHIMLAR

### Problem: Port band
```bash
# Boshqa portda ishga tushirish
python manage.py runserver 8080
```

### Problem: Static files yuklanmayapti
```bash
# Static files yig'ish
python manage.py collectstatic --noinput
```

### Problem: Database xatosi
```bash
# Migratsiyalarni qayta ishlatish
python manage.py migrate --run-syncdb
```

### Problem: Admin panel kirish imkoni yo'q
```bash
# Yangi superuser yaratish
python manage.py createsuperuser
```

### Problem: Secret key xatosi
```bash
# settings.py da SECRET_KEY ni o'zgartiring
# yoki environment variable sifatida qo'ying
export SECRET_KEY='your-secret-key'
```

---

## 📦 DEPENDENCIES YANGILASH

```bash
# Barcha packages ni ko'rish
pip list

# Outdated packages
pip list --outdated

# Yangilash
pip install --upgrade django
pip install --upgrade djangorestframework

# requirements.txt yangilash
pip freeze > requirements.txt
```

---

## 🚀 PRODUCTION DEPLOYMENT

### 1. Environment Variables:
```bash
export DEBUG=False
export SECRET_KEY='your-secret-key-here'
export ALLOWED_HOSTS='buxorobilimdonlarmaktabi.uz,www.buxorobilimdonlarmaktabi.uz'
```

### 2. Static Files:
```bash
python manage.py collectstatic --noinput
```

### 3. Gunicorn:
```bash
gunicorn mytest.wsgi:application --bind 0.0.0.0:8000
```

### 4. Nginx:
```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```

### 5. Systemd Service:
```bash
sudo cp buxoro-test.service /etc/systemd/system/
sudo systemctl start buxoro-test
sudo systemctl enable buxoro-test
```

---

## 📞 MUAMMOLAR VA YORDAMLAR

### Xatolar:
- **404 Error:** URL to'g'ri tekshiring
- **500 Error:** settings.py va logs ni tekshiring
- **403 Error:** CSRF token yoki permissions
- **Database locked:** SQLite faylni tekshiring

### Logs:
```bash
# Django logs
tail -f logs/django.log

# Gunicorn logs
journalctl -u buxoro-test -f

# Nginx logs
sudo tail -f /var/log/nginx/error.log
```

### Test Qilish:
```bash
# URL testlari
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/accounts/login/

# API testlari
curl -X POST http://127.0.0.1:8000/accounts/signup/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@buxorobilimdonlar.uz","password":"test123"}'
```

---

## 📚 QOSHIMCHA DOKUMENTATSIYA

- `README.md` - Asosiy qo'llanma
- `PROYEKT_TAHLILI.md` - To'liq proyekt tahlili
- `TOZALASH_HISOBOTI.md` - Tozalash hisoboti
- `QAYTA_ISHLASH_QOLLANMA.md` - Qayta ishlash funksiyasi
- `QAYTA_ISHLASH_TEST.md` - Test qilish yo'riqnomasi

---

## 🎯 TEZKOR CHECKLIST

### Development:
- [ ] Virtual environment aktivlashtirildi
- [ ] Dependencies o'rnatildi
- [ ] Database migratsiyalari bajarildi
- [ ] Superuser yaratildi
- [ ] Server ishga tushirildi
- [ ] Brauzerda ochildi

### Production:
- [ ] DEBUG=False
- [ ] SECRET_KEY o'rnatildi
- [ ] ALLOWED_HOSTS sozlandi
- [ ] Static files yig'ildi
- [ ] Database backup qilindi
- [ ] Gunicorn sozlandi
- [ ] Nginx sozlandi
- [ ] SSL sertifikat o'rnatildi
- [ ] Systemd service yaratildi

---

## 🏆 YORDAM

**Savol yoki muammo bo'lsa:**
- Email: info@buxorobilimdonlar.uz
- Website: https://buxorobilimdonlarmaktabi.uz
- Server: 176.96.241.174

**Django Documentation:**
- https://docs.djangoproject.com/

**Proyekt Repository:**
- Git: (sizning repository manzilingiz)

---

**Oxirgi yangilanish:** 29 Oktabr, 2025  
**Versiya:** 1.0.0

© 2025 Buxoro Bilimdonlar Maktabi

