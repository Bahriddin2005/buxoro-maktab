"""
Umumiy test natijalari uchun views
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Max
from .models import TestAttempt


@login_required
def student_overall_results_view(request):
    """O'quvchining barcha testlar bo'yicha umumiy natijalari"""
    if request.user.role != 'student':
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    if request.headers.get('Accept') == 'application/json':
        # O'quvchining barcha tugallangan testlari
        # Har bir test uchun eng so'nggi attempt'ni olish
        latest_attempts = TestAttempt.objects.filter(
            student=request.user,
            completed_at__isnull=False
        ).values('test').annotate(
            latest_attempt_id=Max('id')
        ).values_list('latest_attempt_id', flat=True)
        
        attempts = TestAttempt.objects.filter(
            id__in=latest_attempts
        ).select_related('test').order_by('-completed_at')
        
        # Umumiy statistika
        total_tests = attempts.count()
        if total_tests == 0:
            return JsonResponse({
                'total_tests': 0,
                'average_score': 0,
                'average_percentage': 0,
                'total_points_earned': 0,
                'total_points_possible': 0,
                'overall_grade': 'N/A',
                'tests': [],
                'grade_distribution': {
                    'excellent': 0,
                    'good': 0,
                    'average': 0,
                    'poor': 0
                }
            })
        
        # Hisoblashlar
        total_score = sum(attempt.score for attempt in attempts)
        total_points = sum(attempt.total_points for attempt in attempts)
        average_percentage = (total_score / total_points * 100) if total_points > 0 else 0
        
        # Baholar bo'yicha taqsimlash
        grade_distribution = {
            'excellent': attempts.filter(percentage__gte=81).count(),
            'good': attempts.filter(percentage__gte=61, percentage__lt=81).count(),
            'average': attempts.filter(percentage__gte=31, percentage__lt=61).count(),
            'poor': attempts.filter(percentage__lt=31).count()
        }
        
        # Umumiy baho
        if average_percentage >= 81:
            overall_grade = "A'lo"
        elif average_percentage >= 61:
            overall_grade = "Yaxshi"
        elif average_percentage >= 31:
            overall_grade = "Qoniqarli"
        else:
            overall_grade = "Qoniqarsiz"
        
        # Har bir testning ma'lumotlari
        tests_data = []
        for attempt in attempts:
            # Baho'ni hisoblash
            percentage = attempt.percentage or 0
            if percentage >= 81:
                result_grade = "A'lo"
            elif percentage >= 61:
                result_grade = "Yaxshi"
            elif percentage >= 31:
                result_grade = "Qoniqarli"
            else:
                result_grade = "Qoniqarsiz"
            
            tests_data.append({
                'test_id': attempt.test.id,
                'test_title': attempt.test.title,
                'subject': attempt.test.subject,
                'grade': attempt.test.grade,
                'score': attempt.score,
                'total_points': attempt.total_points,
                'percentage': round(percentage, 1),
                'result_grade': result_grade,
                'correct_answers': attempt.correct_answers or 0,
                'incorrect_answers': attempt.incorrect_answers or 0,
                'unanswered': attempt.unanswered or 0,
                'time_taken': str(attempt.time_taken) if attempt.time_taken else '0:00:00',
                'finished_at': attempt.completed_at.isoformat() if attempt.completed_at else ''
            })
        
        return JsonResponse({
            'total_tests': total_tests,
            'average_score': round(total_score / total_tests, 1) if total_tests > 0 else 0,
            'average_percentage': round(average_percentage, 1),
            'total_points_earned': total_score,
            'total_points_possible': total_points,
            'overall_grade': overall_grade,
            'tests': tests_data,
            'grade_distribution': grade_distribution,
            'highest_score': round(max(attempt.percentage for attempt in attempts), 1) if attempts else 0,
            'lowest_score': round(min(attempt.percentage for attempt in attempts), 1) if attempts else 0
        })
    
    return render(request, 'tests_app/overall_results.html')

