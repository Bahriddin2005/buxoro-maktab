#!/usr/bin/env python
"""
Admin foydalanuvchi yaratish uchun script
"""
import os
import sys
import django

# Django setup
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mytest.settings')
django.setup()

from accounts.models import User

def create_admin():
    """Admin foydalanuvchi yaratish"""
    print("=" * 50)
    print("Admin Foydalanuvchi Yaratish")
    print("=" * 50)
    
    # Admin ma'lumotlari
    username = input("Username kiriting (default: admin): ").strip() or "admin"
    email = input("Email kiriting (default: admin@buxorobilimdonlar.uz): ").strip() or "admin@buxorobilimdonlar.uz"
    password = input("Parol kiriting: ").strip()
    
    if not password:
        print("❌ Parol kiritilmadi!")
        return False
    
    # Foydalanuvchi mavjudligini tekshirish
    if User.objects.filter(username=username).exists():
        print(f"❌ '{username}' username allaqachon mavjud!")
        update = input("O'zgartirishni xohlaysizmi? (y/n): ").strip().lower()
        if update == 'y':
            user = User.objects.get(username=username)
            user.set_password(password)
            user.temporary_password = password
            user.role = 'admin'
            user.is_verified = True
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.save()
            print(f"✅ '{username}' foydalanuvchisi admin sifatida yangilandi!")
            return True
        else:
            return False
    
    if User.objects.filter(email=email).exists():
        print(f"❌ '{email}' email allaqachon mavjud!")
        return False
    
    # Yangi admin yaratish
    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name="Admin",
            last_name="User",
            role='admin',
            is_verified=True,
            is_staff=True,
            is_superuser=True,
            is_active=True
        )
        
        # Parolni saqlash (export uchun)
        user.temporary_password = password
        user.save()
        
        print(f"✅ Admin foydalanuvchi muvaffaqiyatli yaratildi!")
        print(f"   Username: {username}")
        print(f"   Email: {email}")
        print(f"   Role: admin")
        print(f"   Superuser: Yes")
        print(f"   Staff: Yes")
        print(f"   Verified: Yes")
        return True
        
    except Exception as e:
        print(f"❌ Xatolik: {str(e)}")
        return False

if __name__ == '__main__':
    success = create_admin()
    if success:
        print("\n✅ Admin foydalanuvchi tayyor!")
        print("Endi /admin/ sahifasiga kirishingiz mumkin.")
    else:
        print("\n❌ Admin yaratilmadi.")
    print("=" * 50)
