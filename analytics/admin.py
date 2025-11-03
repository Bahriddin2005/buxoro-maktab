from django.contrib import admin
from .models import DailyStats, UserActivity, PageView


@admin.register(DailyStats)
class DailyStatsAdmin(admin.ModelAdmin):
    list_display = ['date', 'new_users', 'total_logins', 'new_tests', 'completed_tests', 'student_count', 'teacher_count']
    list_filter = ['date']
    search_fields = ['date']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'timestamp', 'ip_address']
    list_filter = ['activity_type', 'timestamp']
    search_fields = ['user__username', 'user__email', 'ip_address']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ['path', 'user', 'timestamp', 'response_time', 'ip_address']
    list_filter = ['path', 'timestamp']
    search_fields = ['path', 'user__username', 'ip_address']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'

