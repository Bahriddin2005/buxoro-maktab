from django.contrib import admin
from django.utils.html import format_html
from django.utils.text import slugify
from .models import Test, Question, Choice, TestAttempt, Answer, TestResult, TestRetakeRequest, Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']

    def save_model(self, request, obj, form, change):
        if not obj.slug and obj.name:
            obj.slug = slugify(obj.name)
        super().save_model(request, obj, form, change)

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4
    fields = ['choice_text', 'is_correct']
    classes = ['collapse']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text_short', 'test', 'question_type_badge', 'points', 'order', 'has_image']
    list_filter = ['question_type', 'test__subject', 'test__grade']
    search_fields = ['question_text', 'test__title']
    inlines = [ChoiceInline]
    list_editable = ['points', 'order']
    list_per_page = 20
    
    def question_text_short(self, obj):
        return obj.question_text[:50] + '...' if len(obj.question_text) > 50 else obj.question_text
    question_text_short.short_description = 'Savol'
    
    def question_type_badge(self, obj):
        colors = {
            'single': '#28a745',
            'multiple': '#007bff',
            'text': '#ffc107'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold;">{}</span>',
            colors.get(obj.question_type, '#6c757d'),
            obj.get_question_type_display()
        )
    question_type_badge.short_description = 'Turi'
    
    def has_image(self, obj):
        if obj.image:
            return format_html('<span style="color: green;">✓</span>')
        return format_html('<span style="color: red;">✗</span>')
    has_image.short_description = 'Rasm'

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    show_change_link = True

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject_badge', 'grade_badge', 'created_by', 'is_active_icon', 'time_limit', 'total_questions', 'total_points']
    list_filter = ['subject', 'grade', 'is_active', 'created_by']
    search_fields = ['title', 'description']
    inlines = [QuestionInline]
    readonly_fields = ['total_questions', 'total_points']
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    def subject_badge(self, obj):
        colors = {
            'matematika': '#007bff',
            'fizika': '#dc3545',
            'kimyo': '#28a745',
            'biologiya': '#20c997',
            'ona_tili': '#ffc107',
            'adabiyot': '#17a2b8'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; border-radius: 6px; font-weight: bold;">{}</span>',
            colors.get(obj.subject.lower() if obj.subject else '', '#6c757d'),
            obj.subject
        )
    subject_badge.short_description = 'Fan'
    
    def grade_badge(self, obj):
        return format_html(
            '<span style="background-color: #6f42c1; color: white; padding: 4px 10px; border-radius: 6px; font-weight: bold;">{}-sinf</span>',
            obj.grade
        )
    grade_badge.short_description = 'Sinf'
    
    def is_active_icon(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green; font-size: 18px;">✓</span>')
        return format_html('<span style="color: red; font-size: 18px;">✗</span>')
    is_active_icon.short_description = 'Aktiv'

@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'test', 'started_at', 'finished_at', 'score_badge', 'percentage_badge', 'status_icon']
    list_filter = ['is_completed', 'test__subject', 'started_at']
    search_fields = ['student__username', 'student__first_name', 'student__last_name', 'test__title']
    readonly_fields = ['started_at', 'score', 'percentage', 'time_taken']
    list_per_page = 30
    date_hierarchy = 'started_at'
    
    def student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}" if obj.student.first_name else obj.student.username
    student_name.short_description = 'O\'quvchi'
    
    def score_badge(self, obj):
        return format_html(
            '<span style="background-color: #17a2b8; color: white; padding: 4px 10px; border-radius: 6px; font-weight: bold;">{} / {}</span>',
            obj.score, obj.total_points
        )
    score_badge.short_description = 'Ball'
    
    def percentage_badge(self, obj):
        if obj.percentage is None:
            return format_html('<span style="color: #6c757d;">-</span>')
        color = '#28a745' if obj.percentage >= 70 else '#ffc107' if obj.percentage >= 50 else '#dc3545'
        percentage_text = f"{obj.percentage:.1f}%"
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 10px; border-radius: 6px; font-weight: bold;">{}</span>',
            color, percentage_text
        )
    percentage_badge.short_description = 'Foiz'
    
    def status_icon(self, obj):
        if obj.is_completed:
            return format_html('<span style="color: green; font-size: 18px;">✓ Tugallangan</span>')
        return format_html('<span style="color: orange; font-size: 18px;">⏳ Jarayonda</span>')
    status_icon.short_description = 'Holat'

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['attempt_info', 'question_short', 'is_correct_icon', 'answered_at']
    list_filter = ['question__question_type', 'answered_at']
    search_fields = ['attempt__student__username', 'question__question_text']
    list_per_page = 50
    
    def attempt_info(self, obj):
        student = obj.attempt.student
        name = f"{student.first_name} {student.last_name}" if student.first_name else student.username
        return f"{name} - {obj.attempt.test.title}"
    attempt_info.short_description = 'O\'quvchi - Test'
    
    def question_short(self, obj):
        return obj.question.question_text[:40] + '...' if len(obj.question.question_text) > 40 else obj.question.question_text
    question_short.short_description = 'Savol'
    
    def is_correct_icon(self, obj):
        if obj.is_correct():
            return format_html('<span style="color: green; font-size: 18px;">✓ To\'g\'ri</span>')
        return format_html('<span style="color: red; font-size: 18px;">✗ Noto\'g\'ri</span>')
    is_correct_icon.short_description = 'Natija'

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ['student_test_info', 'correct_answers', 'incorrect_answers', 'grade_badge', 'created_at']
    list_filter = ['grade', 'created_at']
    search_fields = ['attempt__student__username', 'attempt__student__first_name', 'attempt__student__last_name', 'attempt__test__title']
    list_per_page = 30
    date_hierarchy = 'created_at'
    
    def student_test_info(self, obj):
        student = obj.attempt.student
        name = f"{student.first_name} {student.last_name}" if student.first_name else student.username
        return f"{name} - {obj.attempt.test.title}"
    student_test_info.short_description = 'O\'quvchi - Test'
    
    def grade_badge(self, obj):
        colors = {
            '5': '#28a745',
            '4': '#20c997',
            '3': '#ffc107',
            '2': '#dc3545'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 6px 14px; border-radius: 6px; font-weight: bold; font-size: 16px;">{}</span>',
            colors.get(obj.grade, '#6c757d'),
            obj.grade
        )
    grade_badge.short_description = 'Baho'

@admin.register(TestRetakeRequest)
class TestRetakeRequestAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'test', 'status_badge', 'reason_short', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['student__username', 'student__first_name', 'student__last_name', 'test__title']
    list_per_page = 20
    date_hierarchy = 'created_at'
    
    def student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}" if obj.student.first_name else obj.student.username
    student_name.short_description = 'O\'quvchi'
    
    def status_badge(self, obj):
        colors = {
            'pending': '#ffc107',
            'approved': '#28a745',
            'rejected': '#dc3545'
        }
        labels = {
            'pending': '⏳ Kutilmoqda',
            'approved': '✓ Tasdiqlangan',
            'rejected': '✗ Rad etilgan'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; border-radius: 6px; font-weight: bold;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            labels.get(obj.status, obj.status)
        )
    status_badge.short_description = 'Holat'
    
    def reason_short(self, obj):
        return obj.reason[:50] + '...' if len(obj.reason) > 50 else obj.reason
    reason_short.short_description = 'Sabab'
