from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils import timezone
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.utils.html import format_html

# Faqat mavjud modellarni import qilamiz
try:
    from .models import User, VerificationRequest
except ImportError:
    User = None
    VerificationRequest = None

# Agar User modeli mavjud bo'lsa va custom fieldlarga ega bo'lsa
if User and hasattr(User, 'role'):
    
    class CustomUserChangeForm(UserChangeForm):
        class Meta(UserChangeForm.Meta):
            model = User
            fields = '__all__'
        
        def save(self, commit=True):
            """Save user and store password for export"""
            user = super().save(commit=False)
            # Parol o'zgartirilganda temporary_password ni saqlash
            if 'password1' in self.cleaned_data and self.cleaned_data['password1']:
                user.temporary_password = self.cleaned_data['password1']
            if commit:
                user.save()
            return user
    
    class CustomUserAdmin(UserAdmin):
        model = User
        form = CustomUserChangeForm
        
        list_display = ['username', 'full_name', 'email', 'role_badge', 'grade_badge', 'is_verified_icon', 'student_id', 'is_active_icon']
        list_filter = ['role', 'is_verified', 'school_email_verified', 'is_active', 'grade']
        search_fields = ['username', 'email', 'student_id', 'first_name', 'last_name']
        list_per_page = 30
        
        def full_name(self, obj):
            return f"{obj.first_name} {obj.last_name}" if obj.first_name else obj.username
        full_name.short_description = 'Ism Familiya'
        
        def role_badge(self, obj):
            colors = {
                'admin': '#dc3545',
                'teacher': '#007bff',
                'student': '#28a745'
            }
            icons = {
                'admin': '👑',
                'teacher': '👨‍🏫',
                'student': '👨‍🎓'
            }
            return format_html(
                '<span style="background-color: {}; color: white; padding: 4px 12px; border-radius: 6px; font-weight: bold;">{} {}</span>',
                colors.get(obj.role, '#6c757d'),
                icons.get(obj.role, ''),
                obj.get_role_display() if hasattr(obj.get_role_display, '__call__') else obj.role
            )
        role_badge.short_description = 'Rol'
        
        def grade_badge(self, obj):
            if obj.grade:
                return format_html(
                    '<span style="background-color: #6f42c1; color: white; padding: 4px 10px; border-radius: 6px; font-weight: bold;">{}-sinf</span>',
                    obj.grade
                )
            return '-'
        grade_badge.short_description = 'Sinf'
        
        def is_verified_icon(self, obj):
            if obj.is_verified:
                return format_html('<span style="color: green; font-size: 18px;" title="Tasdiqlangan">✓</span>')
            return format_html('<span style="color: red; font-size: 18px;" title="Tasdiqlanmagan">✗</span>')
        is_verified_icon.short_description = 'Tasdiqlangan'
        
        def is_active_icon(self, obj):
            if obj.is_active:
                return format_html('<span style="color: green; font-size: 18px;" title="Aktiv">✓</span>')
            return format_html('<span style="color: red; font-size: 18px;" title="Faol emas">✗</span>')
        is_active_icon.short_description = 'Aktiv'
        
        # To'liq qayta aniqlangan fieldsets
        fieldsets = (
            (None, {'fields': ('username', 'password')}),
            ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
            ('Permissions', {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            }),
            ('Important dates', {'fields': ('last_login',)}),  # Faqat last_login
            ('School Info', {
                'fields': ('role', 'student_id', 'is_verified', 'school_email_verified', 
                          'phone_number', 'class_name', 'grade', 'subject')
            }),
        )
        
        add_fieldsets = (
            (None, {
                'classes': ('wide',),
                'fields': ('username', 'password1', 'password2'),
            }),
            ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
            ('School Info', {
                'fields': ('role', 'student_id', 'phone_number', 'class_name', 'grade', 'subject')
            }),
        )
        
        def save_model(self, request, obj, form, change):
            """Save user and store password for export"""
            # Django UserAdmin parol o'zgartirish uchun alohida logikaga ega
            # Parol o'zgartirilganda request.POST dan olish
            if 'password1' in request.POST and request.POST['password1']:
                password = request.POST['password1']
                if password:
                    obj.temporary_password = password
            
            # Form orqali parol o'zgartirilganda
            if hasattr(form, 'cleaned_data') and 'password1' in form.cleaned_data:
                password = form.cleaned_data['password1']
                if password:
                    obj.temporary_password = password
            
            super().save_model(request, obj, form, change)
        
        filter_horizontal = ('groups', 'user_permissions',)
        
        # Export actions - Barcha foydalanuvchilar uchun ishlaydi (queryset e'tiborsiz)
        def export_teachers_credentials(self, request, queryset):
            """Export ALL teachers credentials to Excel (ignores queryset selection)"""
            from accounts.admin_views import export_teachers_credentials_view
            return export_teachers_credentials_view(request)
        
        def export_students_credentials(self, request, queryset):
            """Export ALL students credentials to Excel (ignores queryset selection)"""
            from accounts.admin_views import export_students_credentials_view
            return export_students_credentials_view(request)
        
        def export_teachers_with_reset(self, request, queryset):
            """Export ALL teachers credentials with password reset for missing (ignores queryset selection)"""
            from django.http import QueryDict
            from accounts.admin_views import export_teachers_credentials_view
            # GET parametriga reset_missing=1 qo'shish
            request.GET = QueryDict('reset_missing=1')
            return export_teachers_credentials_view(request)
        
        def export_students_with_reset(self, request, queryset):
            """Export ALL students credentials with password reset for missing (ignores queryset selection)"""
            from django.http import QueryDict
            from accounts.admin_views import export_students_credentials_view
            # GET parametriga reset_missing=1 qo'shish
            request.GET = QueryDict('reset_missing=1')
            return export_students_credentials_view(request)
        
        def reset_selected_passwords(self, request, queryset):
            """Tanlangan foydalanuvchilar uchun yangi parol generatsiya qilish"""
            import secrets
            import string
            
            def generate_password(length=12):
                alphabet = string.ascii_letters + string.digits
                password = [
                    secrets.choice(string.ascii_uppercase),
                    secrets.choice(string.ascii_lowercase),
                    secrets.choice(string.digits),
                ]
                password += [secrets.choice(alphabet) for _ in range(length - 3)]
                secrets.SystemRandom().shuffle(password)
                return ''.join(password)
            
            count = 0
            for user in queryset:
                new_password = generate_password()
                user.set_password(new_password)
                user.save()
                count += 1
            
            self.message_user(request, f'{count} ta foydalanuvchi uchun yangi parol berildi.')
        
        export_teachers_credentials.short_description = "📥 O'qituvchilar - mavjud parollar bilan"
        export_students_credentials.short_description = "📥 O'quvchilar - mavjud parollar bilan"
        export_teachers_with_reset.short_description = "🔑 O'qituvchilar - YANGI parol berib yuklab olish"
        export_students_with_reset.short_description = "🔑 O'quvchilar - YANGI parol berib yuklab olish"
        reset_selected_passwords.short_description = "🔐 Tanlanganlarga yangi parol berish"
        
        actions = [
            export_teachers_credentials, 
            export_students_credentials,
            export_teachers_with_reset,
            export_students_with_reset,
            reset_selected_passwords
        ]
    
    admin.site.register(User, CustomUserAdmin)

# VerificationRequest admin
if VerificationRequest:
    @admin.register(VerificationRequest)
    class VerificationRequestAdmin(admin.ModelAdmin):
        list_display = ['user_info', 'requested_at', 'status_badge', 'processed_by', 'processed_at']
        list_filter = ['is_approved', 'requested_at']
        search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
        readonly_fields = ['requested_at']
        list_per_page = 20
        date_hierarchy = 'requested_at'
        
        def user_info(self, obj):
            user = obj.user
            name = f"{user.first_name} {user.last_name}" if user.first_name else user.username
            role_colors = {
                'admin': '#dc3545',
                'teacher': '#007bff',
                'student': '#28a745'
            }
            return format_html(
                '{} <span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold;">{}</span>',
                name,
                role_colors.get(user.role, '#6c757d'),
                user.get_role_display() if hasattr(user.get_role_display, '__call__') else user.role
            )
        user_info.short_description = 'Foydalanuvchi'
        
        def status_badge(self, obj):
            if obj.is_approved is None:
                return format_html('<span style="background-color: #ffc107; color: white; padding: 4px 12px; border-radius: 6px; font-weight: bold;">⏳ Kutilmoqda</span>')
            elif obj.is_approved:
                return format_html('<span style="background-color: #28a745; color: white; padding: 4px 12px; border-radius: 6px; font-weight: bold;">✓ Tasdiqlangan</span>')
            else:
                return format_html('<span style="background-color: #dc3545; color: white; padding: 4px 12px; border-radius: 6px; font-weight: bold;">✗ Rad etilgan</span>')
        status_badge.short_description = 'Holat'
        
        def approve_request(self, request, queryset):
            for verification_request in queryset:
                verification_request.user.is_verified = True
                verification_request.user.save()
                verification_request.is_approved = True
                verification_request.processed_by = request.user
                verification_request.processed_at = timezone.now()
                verification_request.save()
            self.message_user(request, f'{queryset.count()} requests approved.')
        
        def reject_request(self, request, queryset):
            for verification_request in queryset:
                verification_request.is_approved = False
                verification_request.processed_by = request.user
                verification_request.processed_at = timezone.now()
                verification_request.save()
            self.message_user(request, f'{queryset.count()} requests rejected.')
        
        approve_request.short_description = "Approve selected requests"
        reject_request.short_description = "Reject selected requests"
        actions = [approve_request, reject_request]