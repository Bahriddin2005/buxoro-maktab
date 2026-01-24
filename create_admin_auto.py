#!/usr/bin/env python
"""
Avtomatik admin foydalanuvchi yaratish (default ma'lumotlar bilan)
"""
import os
import sys
import django

# Django setup
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mytest.settings')
django.setup()

from accounts.models import User

def create_admin_auto():
    """Avtomatik admin yaratish (default ma'lumotlar)"""
    username = "admin"
    email = "admin@buxorobilimdonlar.uz"
    password = "admin123456"  # Production'da o'zgartirish kerak!
    
    # Foydalanuvchi mavjudligini tekshirish
    if User.objects.filter(username=username).exists():
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
        print(f"   Username: {username}")
        print(f"   Password: {password}")
        return True
    
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
        print(f"   Password: {password}")
        print(f"   ⚠️  Eslatma: Production'da parolni o'zgartirishni unutmang!")
        return True
        
    except Exception as e:
        print(f"❌ Xatolik: {str(e)}")
        return False

if __name__ == '__main__':
    print("=" * 50)
    print("Avtomatik Admin Yaratish")
    print("=" * 50)
    success = create_admin_auto()
    if success:
        print("\n✅ Admin foydalanuvchi tayyor!")
        print("Endi /admin/ sahifasiga kirishingiz mumkin.")
    else:
        print("\n❌ Admin yaratilmadi.")
    print("=" * 50)
