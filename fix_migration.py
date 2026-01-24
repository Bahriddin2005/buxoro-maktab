#!/usr/bin/env python
"""
Production serverda migration qo'llash uchun script
Bu script temporary_password ustunini qo'shadi
"""
import os
import sys
import django

# Django setup
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mytest.settings')
django.setup()

from django.db import connection
from django.core.management import execute_from_command_line

def fix_temporary_password_column():
    """temporary_password ustunini qo'shish"""
    try:
        with connection.cursor() as cursor:
            # SQLite uchun
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='accounts_user';
            """)
            table_exists = cursor.fetchone()
            
            if table_exists:
                # Ustun mavjudligini tekshirish
                cursor.execute("PRAGMA table_info(accounts_user);")
                columns = [row[1] for row in cursor.fetchall()]
                
                if 'temporary_password' not in columns:
                    print("temporary_password ustuni yo'q. Qo'shilmoqda...")
                    cursor.execute("""
                        ALTER TABLE accounts_user 
                        ADD COLUMN temporary_password varchar(128) NULL;
                    """)
                    print("✅ temporary_password ustuni muvaffaqiyatli qo'shildi!")
                else:
                    print("✅ temporary_password ustuni allaqachon mavjud.")
            else:
                print("❌ accounts_user jadvali topilmadi!")
                return False
        
        # Migration'ni qo'llash
        print("\nMigration'ni qo'llash...")
        execute_from_command_line(['manage.py', 'migrate', 'accounts', '--fake'])
        print("✅ Migration muvaffaqiyatli qo'llandi!")
        return True
        
    except Exception as e:
        print(f"❌ Xatolik: {str(e)}")
        return False

if __name__ == '__main__':
    print("=" * 50)
    print("Migration Fix Script")
    print("=" * 50)
    success = fix_temporary_password_column()
    if success:
        print("\n✅ Barcha o'zgarishlar muvaffaqiyatli amalga oshirildi!")
    else:
        print("\n❌ Xatolik yuz berdi. Iltimos, qo'lda tekshiring.")
    print("=" * 50)
