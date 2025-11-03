from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count, Sum, Avg, Q
from datetime import datetime, timedelta
from accounts.models import User
from tests_app.models import Test, TestAttempt, TestResult
from .models import DailyStats, UserActivity, PageView


@login_required
def analytics_dashboard_view(request):
    """Analytics Dashboard - faqat admin va teacher uchun"""
    if request.user.role not in ['admin', 'teacher']:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    context = {
        'verification_requests_count': 0
    }
    
    # Admin uchun verification requests count
    if request.user.role == 'admin':
        from accounts.models import VerificationRequest
        context['verification_requests_count'] = VerificationRequest.objects.filter(is_approved=None).count()
    
    return render(request, 'analytics/dashboard.html', context)


@login_required
def analytics_api_view(request):
    """Analytics ma'lumotlarini JSON formatda qaytarish"""
    if request.user.role not in ['admin', 'teacher']:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    try:
        # Bugungi va oxirgi 7 kunlik ma'lumotlar
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # 1. BUGUNGI STATISTIKA
        today_stats = get_today_stats(today)
        
        # 2. HAFTALIK STATISTIKA
        weekly_stats = get_weekly_stats(week_ago, today)
        
        # 3. OYLIK STATISTIKA
        monthly_stats = get_monthly_stats(month_ago, today)
        
        # 4. FOYDALANUVCHILAR BO'YICHA
        users_stats = get_users_stats()
        
        # 5. TESTLAR BO'YICHA
        tests_stats = get_tests_stats()
        
        # 6. AKTIVLIK GRAFIGI (oxirgi 7 kun)
        activity_chart = get_activity_chart_data(week_ago, today)
        
        # 7. TOP TESTLAR
        top_tests = get_top_tests()
        
        # 8. TOP O'QUVCHILAR
        top_students = get_top_students()
        
        # 9. REAL-TIME STATS
        realtime_stats = get_realtime_stats()
        
        return JsonResponse({
            'today': today_stats,
            'weekly': weekly_stats,
            'monthly': monthly_stats,
            'users': users_stats,
            'tests': tests_stats,
            'activity_chart': activity_chart,
            'top_tests': top_tests,
            'top_students': top_students,
            'realtime': realtime_stats,
        })
        
    except Exception as e:
        print(f"Analytics API error: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)


def get_today_stats(today):
    """Bugungi statistika"""
    # Bugungi loginlar
    today_logins = UserActivity.objects.filter(
        activity_type='login',
        timestamp__date=today
    ).count()
    
    # Bugungi ro'yxatdan o'tganlar
    today_signups = User.objects.filter(
        date_joined__date=today
    ).count()
    
    # Bugungi testlar
    today_tests = Test.objects.filter(
        created_at__date=today
    ).count()
    
    # Bugungi test urinishlari
    today_attempts = TestAttempt.objects.filter(
        started_at__date=today
    ).count()
    
    # Bugungi tugallangan testlar
    today_completed = TestAttempt.objects.filter(
        finished_at__date=today,
        is_completed=True
    ).count()
    
    return {
        'logins': today_logins,
        'signups': today_signups,
        'new_tests': today_tests,
        'attempts': today_attempts,
        'completed': today_completed,
    }


def get_weekly_stats(week_ago, today):
    """Haftalik statistika"""
    weekly_logins = UserActivity.objects.filter(
        activity_type='login',
        timestamp__date__gte=week_ago,
        timestamp__date__lte=today
    ).count()
    
    weekly_signups = User.objects.filter(
        date_joined__date__gte=week_ago,
        date_joined__date__lte=today
    ).count()
    
    weekly_tests = Test.objects.filter(
        created_at__date__gte=week_ago,
        created_at__date__lte=today
    ).count()
    
    weekly_attempts = TestAttempt.objects.filter(
        started_at__date__gte=week_ago,
        started_at__date__lte=today
    ).count()
    
    # O'sish foizi (haftaga nisbatan)
    prev_week = week_ago - timedelta(days=7)
    prev_weekly_logins = UserActivity.objects.filter(
        activity_type='login',
        timestamp__date__gte=prev_week,
        timestamp__date__lt=week_ago
    ).count()
    
    login_growth = calculate_growth(weekly_logins, prev_weekly_logins)
    
    return {
        'logins': weekly_logins,
        'signups': weekly_signups,
        'tests': weekly_tests,
        'attempts': weekly_attempts,
        'login_growth': login_growth,
    }


def get_monthly_stats(month_ago, today):
    """Oylik statistika"""
    monthly_logins = UserActivity.objects.filter(
        activity_type='login',
        timestamp__date__gte=month_ago,
        timestamp__date__lte=today
    ).count()
    
    monthly_signups = User.objects.filter(
        date_joined__date__gte=month_ago,
        date_joined__date__lte=today
    ).count()
    
    monthly_tests = Test.objects.filter(
        created_at__date__gte=month_ago,
        created_at__date__lte=today
    ).count()
    
    monthly_attempts = TestAttempt.objects.filter(
        started_at__date__gte=month_ago,
        started_at__date__lte=today
    ).count()
    
    return {
        'logins': monthly_logins,
        'signups': monthly_signups,
        'tests': monthly_tests,
        'attempts': monthly_attempts,
    }


def get_users_stats():
    """Foydalanuvchilar statistikasi"""
    total_users = User.objects.count()
    verified_users = User.objects.filter(is_verified=True).count()
    students = User.objects.filter(role='student').count()
    teachers = User.objects.filter(role='teacher').count()
    admins = User.objects.filter(role='admin').count()
    
    # Aktiv foydalanuvchilar (oxirgi 24 soatda)
    day_ago = timezone.now() - timedelta(hours=24)
    active_24h = UserActivity.objects.filter(
        activity_type='login',
        timestamp__gte=day_ago
    ).values('user').distinct().count()
    
    return {
        'total': total_users,
        'verified': verified_users,
        'students': students,
        'teachers': teachers,
        'admins': admins,
        'active_24h': active_24h,
        'verification_rate': round((verified_users / total_users * 100) if total_users > 0 else 0, 1),
    }


def get_tests_stats():
    """Testlar statistikasi"""
    total_tests = Test.objects.count()
    active_tests = Test.objects.filter(is_active=True).count()
    total_attempts = TestAttempt.objects.count()
    completed_attempts = TestAttempt.objects.filter(is_completed=True).count()
    
    # O'rtacha ball
    avg_score = TestAttempt.objects.filter(
        is_completed=True,
        percentage__isnull=False
    ).aggregate(avg=Avg('percentage'))['avg'] or 0
    
    # Fanlar bo'yicha
    subjects_count = Test.objects.values('subject').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    # Sinflar bo'yicha
    grades_count = Test.objects.values('grade').annotate(
        count=Count('id')
    ).order_by('-count')
    
    return {
        'total': total_tests,
        'active': active_tests,
        'total_attempts': total_attempts,
        'completed_attempts': completed_attempts,
        'completion_rate': round((completed_attempts / total_attempts * 100) if total_attempts > 0 else 0, 1),
        'avg_score': round(avg_score, 1),
        'subjects': list(subjects_count),
        'grades': list(grades_count),
    }


def get_activity_chart_data(week_ago, today):
    """Oxirgi 7 kunlik aktivlik grafigi uchun ma'lumotlar"""
    data = []
    current_date = week_ago
    
    while current_date <= today:
        logins = UserActivity.objects.filter(
            activity_type='login',
            timestamp__date=current_date
        ).count()
        
        signups = User.objects.filter(
            date_joined__date=current_date
        ).count()
        
        tests_completed = TestAttempt.objects.filter(
            finished_at__date=current_date,
            is_completed=True
        ).count()
        
        data.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'day': current_date.strftime('%a'),
            'logins': logins,
            'signups': signups,
            'completed': tests_completed,
        })
        
        current_date += timedelta(days=1)
    
    return data


def get_top_tests():
    """Eng ko'p ishlangan testlar"""
    top_tests = Test.objects.annotate(
        attempts_count=Count('attempts'),
        avg_score=Avg('attempts__percentage', filter=Q(attempts__is_completed=True))
    ).order_by('-attempts_count')[:5]
    
    return [{
        'id': test.id,
        'title': test.title,
        'subject': test.subject,
        'grade': test.grade,
        'attempts': test.attempts_count,
        'avg_score': round(test.avg_score, 1) if test.avg_score else 0,
    } for test in top_tests]


def get_top_students():
    """Eng yaxshi o'quvchilar"""
    students = User.objects.filter(
        role='student',
        is_verified=True
    ).annotate(
        tests_count=Count('test_attempts', filter=Q(test_attempts__is_completed=True)),
        avg_score=Avg('test_attempts__percentage', filter=Q(test_attempts__is_completed=True))
    ).filter(tests_count__gt=0).order_by('-avg_score')[:10]
    
    return [{
        'id': student.id,
        'name': f"{student.first_name} {student.last_name}",
        'username': student.username,
        'grade': student.grade,
        'class_name': student.class_name,
        'tests_count': student.tests_count,
        'avg_score': round(student.avg_score, 1) if student.avg_score else 0,
    } for student in students]


def get_realtime_stats():
    """Real-time statistika (oxirgi 5 daqiqa)"""
    five_min_ago = timezone.now() - timedelta(minutes=5)
    
    recent_logins = UserActivity.objects.filter(
        activity_type='login',
        timestamp__gte=five_min_ago
    ).count()
    
    recent_activities = UserActivity.objects.filter(
        timestamp__gte=five_min_ago
    ).select_related('user').order_by('-timestamp')[:10]
    
    activities = []
    for activity in recent_activities:
        activities.append({
            'user': activity.user.username if activity.user else 'Anonymous',
            'type': activity.activity_type,
            'timestamp': activity.timestamp.isoformat(),
            'time_ago': get_time_ago(activity.timestamp),
        })
    
    return {
        'recent_logins': recent_logins,
        'activities': activities,
    }


def calculate_growth(current, previous):
    """O'sish foizini hisoblash"""
    if previous == 0:
        return 100 if current > 0 else 0
    return round(((current - previous) / previous) * 100, 1)


def get_time_ago(timestamp):
    """Necha vaqt oldin"""
    now = timezone.now()
    diff = now - timestamp
    
    if diff.seconds < 60:
        return f"{diff.seconds} soniya oldin"
    elif diff.seconds < 3600:
        return f"{diff.seconds // 60} daqiqa oldin"
    elif diff.seconds < 86400:
        return f"{diff.seconds // 3600} soat oldin"
    else:
        return f"{diff.days} kun oldin"

