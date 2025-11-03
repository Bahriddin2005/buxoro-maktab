from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
# from accounts.urls import *
# from tests_app.urls import *

def home_view(request):
    return render(request, 'home.html')

def test_debug_view(request):
    return render(request, 'test_debug.html')

urlpatterns = [
    path("", home_view, name='home'),
    path("admin/", admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('tests/', include('tests_app.urls')),
    path('analytics/', include('analytics.urls')),
    path('debug-tests/', test_debug_view, name='debug_tests'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else settings.STATIC_ROOT)
