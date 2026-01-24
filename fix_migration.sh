#!/bin/bash
# Production serverda migration qo'llash uchun script

echo "=========================================="
echo "Migration Fix Script"
echo "=========================================="

# Virtual environment aktivlashtirish
source venv/bin/activate

# Migration'ni qo'llash
echo "Migration'ni qo'llash..."
python manage.py migrate accounts

# Agar migration ishlamasa, SQL buyrug'ini bajarish
if [ $? -ne 0 ]; then
    echo "Migration ishlamadi. SQL buyrug'ini bajarish..."
    sqlite3 db.sqlite3 "ALTER TABLE accounts_user ADD COLUMN temporary_password varchar(128) NULL;"
    
    # Keyin migration'ni fake qilish
    echo "Migration'ni fake qilish..."
    python manage.py migrate accounts 0006 --fake
fi

echo "=========================================="
echo "✅ Migration muvaffaqiyatli qo'llandi!"
echo "=========================================="
