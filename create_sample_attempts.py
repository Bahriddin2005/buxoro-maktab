#!/usr/bin/env python
"""
Sample Test Attempts yaratish
O'quvchilar uchun test natijalari yaratadi
"""

import os
import sys
import django
from datetime import timedelta
import random

# Django setup
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mytest.settings')
django.setup()

from django.utils import timezone
from accounts.models import User
from tests_app.models import Test, Question, Choice, TestAttempt, Answer, TestResult

def create_sample_attempts():
    """Sample test attempts yaratish"""
    
    print("=" * 60)
    print("SAMPLE TEST ATTEMPTS YARATISH")
    print("=" * 60)
    
    # O'quvchilarni olish
    students = User.objects.filter(role='student', is_verified=True)
    print(f"\n✅ Topildi: {students.count()} ta tasdiqlangan o'quvchi")
    
    if students.count() == 0:
        print("❌ Tasdiqlangan o'quvchilar yo'q!")
        return
    
    # Barcha testlarni olish
    tests = Test.objects.filter(is_active=True)
    print(f"✅ Topildi: {tests.count()} ta faol test")
    
    if tests.count() == 0:
        print("❌ Faol testlar yo'q!")
        return
    
    attempts_created = 0
    
    # Har bir o'quvchi uchun
    for student in students:
        print(f"\n👤 O'quvchi: {student.username} ({student.grade}-sinf)")
        
        # O'quvchining sinfiga mos testlarni olish
        student_tests = tests.filter(grade=student.grade)
        print(f"   Mos testlar: {student_tests.count()} ta")
        
        # Har bir test uchun 50% ehtimol bilan attempt yaratish
        for test in student_tests:
            if random.random() < 0.5:  # 50% chance
                # Allaqachon attempt bormi?
                existing = TestAttempt.objects.filter(student=student, test=test).first()
                if existing:
                    print(f"   ⏭️  {test.title} - allaqachon bor")
                    continue
                
                # Random natija yaratish
                total_questions = test.questions.count()
                if total_questions == 0:
                    print(f"   ⚠️  {test.title} - savollar yo'q!")
                    continue
                
                # Random to'g'ri javoblar (40-100% oralig'ida)
                correct_percentage = random.randint(40, 100)
                correct_answers = int(total_questions * correct_percentage / 100)
                incorrect_answers = total_questions - correct_answers
                
                # Ball hisoblas h
                total_points = sum(q.points for q in test.questions.all())
                score = round(total_points * correct_percentage / 100, 2)
                percentage = correct_percentage
                
                # Vaqt (random 10-40 daqiqa)
                time_taken_minutes = random.randint(10, min(40, test.time_limit))
                
                # TestAttempt yaratish
                finished_time = timezone.now() - timedelta(days=random.randint(0, 7))
                
                attempt = TestAttempt.objects.create(
                    student=student,
                    test=test,
                    is_completed=True,
                    finished_at=finished_time,
                    score=score,
                    total_points=total_points,
                    percentage=percentage,
                    time_taken=timedelta(minutes=time_taken_minutes)
                )
                
                # TestResult yaratish
                TestResult.objects.create(
                    attempt=attempt,
                    correct_answers=correct_answers,
                    incorrect_answers=incorrect_answers,
                    unanswered=0,
                    grade=get_grade_text(percentage)
                )
                
                # Sample Answer'lar yaratish
                questions = list(test.questions.all())
                for i, question in enumerate(questions):
                    should_be_correct = i < correct_answers
                    
                    if question.question_type in ['single_choice', 'multiple_choice']:
                        correct_choice = question.choices.filter(is_correct=True).first()
                        if should_be_correct and correct_choice:
                            selected_choice = correct_choice
                        else:
                            wrong_choices = question.choices.filter(is_correct=False)
                            selected_choice = wrong_choices.first() if wrong_choices.exists() else correct_choice
                        
                        if selected_choice:
                            answer = Answer.objects.create(
                                attempt=attempt,
                                question=question
                            )
                            answer.selected_choices.add(selected_choice)
                    else:
                        # Text answer
                        Answer.objects.create(
                            attempt=attempt,
                            question=question,
                            text_answer="Sample javob - bu test ma'lumoti"
                        )
                
                print(f"   ✅ {test.title}: {percentage}% ({correct_answers}/{total_questions})")
                attempts_created += 1
    
    print(f"\n{'=' * 60}")
    print(f"✅ YAKUNLANDI!")
    print(f"   Yaratildi: {attempts_created} ta test attempt")
    print(f"   O'quvchilar: {students.count()} ta")
    print(f"{'=' * 60}")

def get_grade_text(percentage):
    """Foiz asosida baho berish"""
    if percentage >= 81:
        return "A'lo"
    elif percentage >= 61:
        return "Yaxshi"
    elif percentage >= 31:
        return "Qoniqarli"
    else:
        return "Qoniqarsiz"

if __name__ == '__main__':
    try:
        create_sample_attempts()
        print("\n✅ SUCCESS! Excel export endi ma'lumotli bo'ladi!")
    except Exception as e:
        print(f"\n❌ XATOLIK: {e}")
        import traceback
        traceback.print_exc()

