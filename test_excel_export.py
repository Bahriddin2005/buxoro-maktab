#!/usr/bin/env python
"""
Excel Export funksiyasini test qilish
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mytest.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth import get_user_model
from tests_app.export_all_students import export_all_students_results

User = get_user_model()

print("\n" + "="*70)
print("🧪 EXCEL EXPORT FUNKSIYASINI TEST QILISH")
print("="*70 + "\n")

# Admin user yaratish yoki topish
try:
    admin = User.objects.filter(role='admin').first()
    if not admin:
        print("❌ Admin topilmadi!")
        sys.exit(1)
    print(f"✅ Admin topildi: {admin.username}\n")
except Exception as e:
    print(f"❌ Xato: {e}")
    sys.exit(1)

# Request yaratish
factory = RequestFactory()
request = factory.get('/tests/export-all-students/')
request.user = admin

print("🔄 Export funksiyasini chaqiryapmiz...\n")

try:
    response = export_all_students_results(request)
    
    print(f"✅ Status Code: {response.status_code}")
    
    if response.status_code == 200:
        # Check content type
        content_type = response.get('Content-Type', '')
        print(f"✅ Content-Type: {content_type}")
        
        # Check content disposition
        content_disposition = response.get('Content-Disposition', '')
        print(f"✅ Content-Disposition: {content_disposition}")
        
        # Check file size
        file_size = len(response.content)
        print(f"✅ File Size: {file_size} bytes ({file_size/1024:.2f} KB)")
        
        if file_size > 0:
            print("\n" + "="*70)
            print("🎉 MUVAFFAQIYATLI!")
            print("="*70)
            print("\n✅ Excel fayl yaratildi!")
            print(f"✅ Fayl hajmi: {file_size/1024:.2f} KB")
            print(f"✅ Fayl nomi: barcha_oquvchilar_natijalari.xlsx")
            
            # Save to file for testing
            output_file = 'test_export.xlsx'
            with open(output_file, 'wb') as f:
                f.write(response.content)
            print(f"\n✅ Test fayli saqlandi: {output_file}")
            print(f"   Ushbu faylni Excel'da ochib ko'ring!\n")
        else:
            print("\n❌ Fayl bo'sh!")
    else:
        print(f"\n❌ Xato: Status code {response.status_code}")
        if hasattr(response, 'content'):
            print(f"Response: {response.content[:200]}")
            
except Exception as e:
    print(f"\n❌ XATO: {e}")
    import traceback
    traceback.print_exc()
    
print("="*70 + "\n")

