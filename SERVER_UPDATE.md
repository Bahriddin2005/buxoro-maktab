# Server Yangilash Ko'rsatmasi

## python-docx xatosi (Word import ishlamasa)

**Xatolik:** `python-docx kutubxonasi o'rnatilmagan`

**Yechim — serverni SSH orqali ulang va quyidagilarni bajaring:**

```bash
# 1. Projekt papkasiga o'ting
cd /home/baxadev/my_test   # yoki loyihangiz joylashuvi

# 2. Virtual environment aktivlashtiring
source venv/bin/activate

# 3. python-docx o'rnating
pip install python-docx

# Yoki barcha requirements ni qayta o'rnating:
pip install -r requirements.txt

# 4. Gunicorn qayta ishga tushiring
sudo systemctl restart buxoro-test
```

Yoki script ishlatish:
```bash
chmod +x install_python_docx.sh
./install_python_docx.sh
sudo systemctl restart buxoro-test
```

---

## Muammo (oldingi)
`/tests/grade-results/` sahifasi local'da ko'rinmoqda, serverda ko'rinmayapti.

## Yechim

### 1. Local Serverni Yangilash

```bash
# Local serverni to'xtating (Ctrl+C)

# Keyin qayta ishga tushiring:
python manage.py runserver

# Yoki agar development server boshqa usulda ishlayotgan bo'lsa:
# Supervisord yoki systemd orqali qayta ishga tushiring
```

### 2. Browser Cache'ni Tozalash

Local'da sahifani ko'rish uchun:
- **Chrome/Edge**: `Ctrl+Shift+R` (Windows) yoki `Cmd+Shift+R` (Mac)
- **Firefox**: `Ctrl+F5` (Windows) yoki `Cmd+Shift+R` (Mac)
- Yoki Browser Developer Tools (F12) -> Network tab -> "Disable cache" ni yoqib, sahifani qayta yuklang

### 3. Tekshirish

`/tests/grade-results/` sahifasi endi 404 xatolik ko'rsatishi kerak, chunki:
- ✅ URL konfiguratsiyasidan o'chirildi
- ✅ View funksiyasi o'chirildi
- ✅ Template fayli o'chirildi
- ✅ Barcha linklar o'chirildi yoki `/tests/all-results/` ga yo'naltirildi

### 4. Yangi Sahifa

Endi barcha natijalar `/tests/all-results/` sahifasida ko'rsatiladi.

