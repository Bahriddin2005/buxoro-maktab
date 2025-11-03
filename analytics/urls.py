from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('dashboard/', views.analytics_dashboard_view, name='dashboard'),
    path('api/', views.analytics_api_view, name='api'),
]

