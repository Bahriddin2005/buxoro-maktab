from django.db import models
from django.conf import settings
from django.utils import timezone


class DailyStats(models.Model):
    """Kunlik statistika - har kun uchun umumiy ma'lumotlar"""
    date = models.DateField(unique=True, db_index=True)
    
    # Foydalanuvchilar statistikasi
    new_users = models.IntegerField(default=0, help_text="Yangi ro'yxatdan o'tganlar")
    verified_users = models.IntegerField(default=0, help_text="Tasdiqlangan foydalanuvchilar")
    total_users = models.IntegerField(default=0, help_text="Jami foydalanuvchilar")
    
    # Login statistikasi
    total_logins = models.IntegerField(default=0, help_text="Jami kirganlar")
    unique_logins = models.IntegerField(default=0, help_text="Noyob foydalanuvchilar")
    
    # Test statistikasi
    new_tests = models.IntegerField(default=0, help_text="Yangi testlar")
    completed_tests = models.IntegerField(default=0, help_text="Tugallangan testlar")
    total_attempts = models.IntegerField(default=0, help_text="Jami urinishlar")
    
    # Role bo'yicha
    student_count = models.IntegerField(default=0, help_text="O'quvchilar soni")
    teacher_count = models.IntegerField(default=0, help_text="O'qituvchilar soni")
    admin_count = models.IntegerField(default=0, help_text="Adminlar soni")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name = 'Kunlik Statistika'
        verbose_name_plural = 'Kunlik Statistikalar'
    
    def __str__(self):
        return f"Stats for {self.date}"


class UserActivity(models.Model):
    """Foydalanuvchi faolligi - har bir login/logout"""
    ACTIVITY_TYPES = (
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('signup', 'Signup'),
        ('test_start', 'Test Started'),
        ('test_finish', 'Test Finished'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activities', null=True, blank=True)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    # Qo'shimcha ma'lumotlar
    session_duration = models.DurationField(null=True, blank=True, help_text="Session davomiyligi (faqat logout uchun)")
    test_id = models.IntegerField(null=True, blank=True, help_text="Test ID (agar test bilan bog'liq bo'lsa)")
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Foydalanuvchi Faolligi'
        verbose_name_plural = 'Foydalanuvchi Faolliklari'
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['activity_type', '-timestamp']),
        ]
    
    def __str__(self):
        username = self.user.username if self.user else 'Anonymous'
        return f"{username} - {self.activity_type} at {self.timestamp}"


class PageView(models.Model):
    """Sahifa ko'rishlar - har bir sahifa ochilganda"""
    path = models.CharField(max_length=255, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    response_time = models.FloatField(null=True, blank=True, help_text="Milliseconds")
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Sahifa Ko\'rish'
        verbose_name_plural = 'Sahifa Ko\'rishlar'
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['path', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.path} - {self.timestamp}"

