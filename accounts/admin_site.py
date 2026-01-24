"""
Custom Admin Site with export functionality
"""
from django.contrib import admin
from django.urls import path
from django.utils.html import format_html
from django.urls import reverse


class CustomAdminSite(admin.AdminSite):
    site_header = "🎓 Buxoro Bilimdonlar Maktabi Admin"
    site_title = "Buxoro Bilimdonlar Maktabi Admin"
    index_title = "Admin Panel"
    
    def get_urls(self):
        urls = super().get_urls()
        from accounts.admin_views import export_teachers_credentials_view, export_students_credentials_view
        
        custom_urls = [
            path('export-teachers-credentials/', self.admin_view(export_teachers_credentials_view), name='export_teachers_credentials'),
            path('export-students-credentials/', self.admin_view(export_students_credentials_view), name='export_students_credentials'),
        ]
        return custom_urls + urls
    
    def index(self, request, extra_context=None):
        """
        Display the main admin index page with export links
        """
        extra_context = extra_context or {}
        
        # Add export links to context
        extra_context['export_links'] = [
            {
                'name': "📥 O'qituvchilar Login, Email va Parollarini Yuklab Olish",
                'url': reverse('admin:export_teachers_credentials'),
                'icon': 'fas fa-download',
                'description': 'O\'qituvchilar login, email va parollarini Excel formatida yuklab olish (parolsizlarga avtomatik yangi parol beriladi)'
            },
            {
                'name': "📥 O'quvchilar Login, Email va Parollarini Yuklab Olish",
                'url': reverse('admin:export_students_credentials'),
                'icon': 'fas fa-download',
                'description': 'O\'quvchilar login, email va parollarini Excel formatida yuklab olish (parolsizlarga avtomatik yangi parol beriladi)'
            }
        ]
        
        return super().index(request, extra_context)
