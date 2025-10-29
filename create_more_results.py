#!/usr/bin/env python
"""
Ko'proq test natijalarini yaratish
"""
import os
import sys
import django
from datetime import timedelta
from django.utils import timezone

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mytest.settings')
django.setup()

from tests_app.models import Test, TestAttempt, Answer, TestResult
from accounts.models import User

print("\n" + "="*70)
print("🔍 TEST NATIJALARI TEKSHIRUVI")
print("="*70 + "\n")

# Student1 ni topish
try:
    student = User.objects.get(username='student1')
    print(f"✅ O'quvchi: {student.username} ({student.first_name} {student.last_name})")
except User.DoesNotExist:
    print("❌ student1 topilmadi!")
    sys.exit(1)

# Mavjud natijalarni tekshirish
existing_attempts = TestAttempt.objects.filter(
    student=student,
    is_completed=True
)

print(f"\n📊 MAVJUD NATIJALAR: {existing_attempts.count()} ta\n")

if existing_attempts.count() > 0:
    print("┌" + "─"*68 + "┐")
    print("│ {:<40} │ {:>8} │ {:>13} │".format("Test nomi", "Ball", "Foiz"))
    print("├" + "─"*68 + "┤")
    
    for attempt in existing_attempts:
        test_name = attempt.test.title[:40]
        score = f"{attempt.score:.0f}/{attempt.total_points:.0f}"
        percentage = f"{attempt.percentage:.1f}%"
        print("│ {:<40} │ {:>8} │ {:>13} │".format(test_name, score, percentage))
    
    print("└" + "─"*68 + "┘\n")

# Testlarni tekshirish
tests = Test.objects.all()
print(f"📚 MAVJUD TESTLAR: {tests.count()} ta\n")

if tests.count() == 0:
    print("❌ Testlar topilmadi!")
    print("   Sample data yarating: python create_sample_data.py")
    sys.exit(1)

# Agar natijalar kam bo'lsa, ko'proq yaratish
if existing_attempts.count() < tests.count():
    print("🔄 Ko'proq natijalar yaratilmoqda...\n")
    
    for test in tests:
        # Bu test uchun natija bormi?
        existing = TestAttempt.objects.filter(
            student=student,
            test=test,
            is_completed=True
        ).exists()
        
        if existing:
            print(f"   ⏭️  {test.title}: Allaqachon mavjud")
            continue
        
        print(f"   ➕ {test.title}: Yaratilmoqda...")
        
        # Test attempt yaratish
        import random
        days_ago = random.randint(1, 30)
        hours_ago = random.randint(1, 5)
        
        attempt = TestAttempt.objects.create(
            test=test,
            student=student,
            started_at=timezone.now() - timedelta(days=days_ago, hours=hours_ago),
            finished_at=timezone.now() - timedelta(days=days_ago, hours=hours_ago-1),
            is_completed=True,
            attempt_number=1,
            is_retake=False
        )
        
        # Savollar bo'yicha javoblar
        questions = test.questions.all()
        for question in questions:
            if question.question_type in ['single_choice', 'multiple_choice']:
                correct_choices = question.choices.filter(is_correct=True)
                if correct_choices.exists():
                    answer = Answer.objects.create(
                        attempt=attempt,
                        question=question
                    )
                    # 70-90% ehtimol bilan to'g'ri javob
                    if random.random() < random.uniform(0.7, 0.9):
                        answer.selected_choices.set(correct_choices)
                    else:
                        wrong_choices = question.choices.filter(is_correct=False)
                        if wrong_choices.exists():
                            answer.selected_choices.set([wrong_choices.first()])
            elif question.question_type == 'text_answer':
                Answer.objects.create(
                    attempt=attempt,
                    question=question,
                    text_answer="Javob yozildi"
                )
        
        # Natijalarni hisoblash
        result = attempt.calculate_score()
        
        # TestResult yaratish
        def get_grade(percentage):
            if percentage >= 81:
                return "A'lo"
            elif percentage >= 61:
                return "Yaxshi"
            elif percentage >= 31:
                return "Qoniqarli"
            else:
                return "Qoniqarsiz"
        
        TestResult.objects.create(
            attempt=attempt,
            correct_answers=attempt.correct_answers,
            incorrect_answers=attempt.incorrect_answers,
            unanswered=attempt.unanswered,
            grade=get_grade(result['percentage']),
            feedback="Yaxshi ish!"
        )
        
        print(f"      ✅ {result['score']:.0f}/{result['total_points']:.0f} ({result['percentage']:.1f}%) - {get_grade(result['percentage'])}")

# Yakuniy natijalarni ko'rsatish
print("\n" + "="*70)
print("📊 YAKUNIY NATIJALAR")
print("="*70 + "\n")

final_attempts = TestAttempt.objects.filter(
    student=student,
    is_completed=True
).order_by('-finished_at')

if final_attempts.count() > 0:
    total_score = sum(a.score or 0 for a in final_attempts)
    total_possible = sum(a.total_points or 0 for a in final_attempts)
    avg_percentage = (total_score / total_possible * 100) if total_possible > 0 else 0
    
    print(f"✅ Jami testlar: {final_attempts.count()} ta")
    print(f"✅ O'rtacha natija: {avg_percentage:.1f}%")
    print(f"✅ Jami ball: {total_score:.0f}/{total_possible:.0f}")
    
    # Baholar taqsimoti
    excellent = final_attempts.filter(percentage__gte=81).count()
    good = final_attempts.filter(percentage__gte=61, percentage__lt=81).count()
    average = final_attempts.filter(percentage__gte=31, percentage__lt=61).count()
    poor = final_attempts.filter(percentage__lt=31).count()
    
    print(f"\n📈 Baholar taqsimoti:")
    print(f"   ⭐⭐⭐⭐⭐ A'lo: {excellent} ta")
    print(f"   ⭐⭐⭐⭐ Yaxshi: {good} ta")
    print(f"   ⭐⭐⭐ Qoniqarli: {average} ta")
    print(f"   ⭐⭐ Qoniqarsiz: {poor} ta")

print("\n" + "="*70)
print("🌐 NATIJALARNI KO'RISH:")
print("="*70)
print("\n   http://127.0.0.1:8000/tests/overall-results/\n")
print("   Username: student1")
print("   Password: student123")
print("\n" + "="*70 + "\n")

