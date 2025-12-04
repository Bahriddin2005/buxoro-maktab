from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.views.decorators.cache import cache_control
import os
# from accounts.urls import *
# from tests_app.urls import *

def home_view(request):
    return render(request, 'home.html')

def test_debug_view(request):
    return render(request, 'test_debug.html')

@cache_control(max_age=31536000)  # 1 yil cache
def favicon_view(request):
    from pathlib import Path
    BASE_DIR = Path(__file__).resolve().parent.parent
    favicon_path = BASE_DIR / 'static' / 'images' / 'favicon.svg'
    # Agar static/images/ bo'lsa, uni ishlatamiz
    if not favicon_path.exists():
        # STATICFILES_DIRS'dan qidiramiz
        if settings.STATICFILES_DIRS:
            for static_dir in settings.STATICFILES_DIRS:
                alt_path = Path(static_dir) / 'images' / 'favicon.svg'
                if alt_path.exists():
                    favicon_path = alt_path
                    break
    
    if favicon_path.exists():
        # File handle'ni to'g'ri boshqarish uchun context manager ishlatamiz
        # Favicon kichik fayl bo'lgani uchun, uni xotiraga o'qib olamiz
        with open(favicon_path, 'rb') as f:
            file_content = f.read()
        # Content'ni BytesIO ga o'rab, FileResponse ga beramiz
        from io import BytesIO
        file_stream = BytesIO(file_content)
        file_stream.seek(0)  # Cursor'ni boshiga qaytaramiz
        return FileResponse(file_stream, content_type='image/svg+xml')
    else:
        # Agar favicon topilmasa, 404 qaytaramiz
        return HttpResponse(status=404)

urlpatterns = [
    path("", home_view, name='home'),
    path("favicon.ico", favicon_view, name='favicon'),
    path("admin/", admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('tests/', include('tests_app.urls')),
    path('analytics/', include('analytics.urls')),
    path('debug-tests/', test_debug_view, name='debug_tests'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else settings.STATIC_ROOT)