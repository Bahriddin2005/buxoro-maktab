#!/bin/bash
# Pillow o'rnatish uchun script

echo "=========================================="
echo "Pillow O'rnatish"
echo "=========================================="

# Virtual environment aktivlashtirish
source venv/bin/activate

# Pillow o'rnatish
echo "Pillow o'rnatilmoqda..."
pip install Pillow==10.4.0

# Yoki requirements.txt dan barcha paketlarni o'rnatish
# pip install -r requirements.txt

echo "=========================================="
echo "✅ Pillow muvaffaqiyatli o'rnatildi!"
echo "=========================================="
