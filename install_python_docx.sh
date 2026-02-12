#!/bin/bash
# python-docx (Word fayllarni o'qish) o'rnatish uchun script
# Word/TXT import xususiyati uchun kerak

echo "=========================================="
echo "python-docx O'rnatish"
echo "=========================================="

# Projekt papkasiga o'tish
cd "$(dirname "$0")"

# Virtual environment mavjud bo'lsa, aktivlashtirish
if [ -d "venv" ]; then
    echo "Virtual environment aktivlashtirilmoqda..."
    source venv/bin/activate
elif [ -d "../venv" ]; then
    source ../venv/bin/activate
fi

# python-docx o'rnatish
echo "python-docx o'rnatilmoqda..."
pip install python-docx>=1.1.0

# Yoki requirements.txt dan barcha paketlarni o'rnatish (tavsiya etiladi)
# pip install -r requirements.txt

echo "=========================================="
echo "✅ python-docx muvaffaqiyatli o'rnatildi!"
echo "=========================================="
echo ""
echo "Qayta ishga tushirish: sudo systemctl restart buxoro-test"
