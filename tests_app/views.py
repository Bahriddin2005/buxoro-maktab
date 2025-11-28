from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db import transaction
from django.core.paginator import Paginator
from django.db.models import Count, Avg, Max, Min, Q
import json
import random
from .models import Test, Question, Choice, TestAttempt, Answer, TestResult, TestRetakeRequest
from accounts.models import User
from .views_overall import student_overall_results_view, student_export_results_view, test_api_view
from .export_all_students import export_all_students_results

try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill
    OPENPYXL_AVAILABLE = True
except ImportError:
    OPENPYXL_AVAILABLE = False

@login_required
def test_list_view(request):
    """List all available tests for students or created tests for teachers"""
    if request.method == 'GET' and request.headers.get('Accept') == 'application/json':
        # Pagination parametrlari
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 100))  # 100 ta test/sahifa
        
        # Filter parametrlari
        grade_filter = request.GET.get('grade', '')
        subject_filter = request.GET.get('subject', '')
        status_filter = request.GET.get('status', '')
        search_filter = request.GET.get('search', '')
        
        if request.user.role == 'student':
            tests = Test.objects.filter(
                is_active=True,
                grade=request.user.grade
            ).select_related('created_by').prefetch_related('questions').order_by('-created_at')
            
            # Qo'shimcha filterlar (o'quvchi o'z sinfidagi testlarni filtrlash uchun)
            if subject_filter:
                tests = tests.filter(subject=subject_filter)
            if search_filter:
                tests = tests.filter(
                    Q(title__icontains=search_filter) |
                    Q(description__icontains=search_filter)
                )
            
            test_data = []
            for test in tests:
                attempt = TestAttempt.objects.filter(test=test, student=request.user).first()
                
                # Qayta ishlash ruxsati bormi tekshirish
                has_retake_permission = False
                if attempt and attempt.is_completed:
                    has_retake_permission = TestRetakeRequest.objects.filter(
                        student=request.user,
                        test=test,
                        status='approved',
                        is_used=False
                    ).exists()
                
                # O'quvchi testni yecha oladimi?
                can_attempt = test.is_active and (
                    attempt is None or  # Hali yechmagan
                    not attempt.is_completed or  # Davom ettirmoqda
                    has_retake_permission  # Qayta ishlash ruxsati bor
                )
                
                test_data.append({
                    'id': test.id,
                    'title': test.title,
                    'subject': test.subject,
                    'description': test.description,
                    'grade': test.grade,
                    'time_limit': test.time_limit,
                    'max_attempts': test.max_attempts,
                    'total_questions': test.total_questions,
                    'has_attempted': attempt is not None,
                    'attempt_score': round(attempt.percentage, 1) if attempt and attempt.is_completed else None,
                    'can_attempt': can_attempt,
                    'has_retake_permission': has_retake_permission,
                    'created_by': test.created_by.get_full_name() or test.created_by.username,
                    'created_at': test.created_at.isoformat(),
                    'start_time': test.start_time.isoformat() if test.start_time else None,
                    'end_time': test.end_time.isoformat() if test.end_time else None,
                })
            
            # Pagination
            start = (page - 1) * page_size
            end = start + page_size
            total_count = len(test_data)
            paginated_data = test_data[start:end]
            
            return JsonResponse({
                'tests': paginated_data,
                'user_role': 'student',
                'pagination': {
                    'page': page,
                    'page_size': page_size,
                    'total': total_count,
                    'total_pages': (total_count + page_size - 1) // page_size
                }
            })
            
        elif request.user.role == 'teacher':
            # Teacher sees ALL tests (not just their own) - LIMIT to first 100
            tests = Test.objects.all().select_related('created_by').order_by('-created_at')
            
            # Filterlar qo'shish
            if grade_filter:
                tests = tests.filter(grade=int(grade_filter))
            if subject_filter:
                tests = tests.filter(subject=subject_filter)
            if status_filter == 'active':
                tests = tests.filter(is_active=True)
            elif status_filter == 'inactive':
                tests = tests.filter(is_active=False)
            if search_filter:
                tests = tests.filter(
                    Q(title__icontains=search_filter) |
                    Q(description__icontains=search_filter)
                )
            
            # Get total count first
            total_count = tests.count()
            
            # Apply pagination
            start = (page - 1) * page_size
            tests_page = tests[start:start + page_size]
            
            test_data = []
            for test in tests_page:
                attempt_count = TestAttempt.objects.filter(test=test, is_completed=True).count()
                test_data.append({
                    'id': test.id,
                    'title': test.title,
                    'subject': test.subject,
                    'description': test.description,
                    'grade': test.grade,
                    'total_questions': test.total_questions,
                    'is_active': test.is_active,
                    'created_at': test.created_at.isoformat(),
                    'created_by': test.created_by.get_full_name() or test.created_by.username,
                    'attempt_count': attempt_count,
                    'max_attempts': test.max_attempts,
                    'time_limit': test.time_limit,
                })
            
            return JsonResponse({
                'tests': test_data,
                'user_role': 'teacher',
                'pagination': {
                    'page': page,
                    'page_size': page_size,
                    'total': total_count,
                    'total_pages': (total_count + page_size - 1) // page_size
                }
            })
        
        elif request.user.role == 'admin':
            # Admin sees ALL tests - LIMIT to first 100
            tests = Test.objects.all().select_related('created_by').order_by('-created_at')
            
            # Filterlar qo'shish
            if grade_filter:
                tests = tests.filter(grade=int(grade_filter))
            if subject_filter:
                tests = tests.filter(subject=subject_filter)
            if status_filter == 'active':
                tests = tests.filter(is_active=True)
            elif status_filter == 'inactive':
                tests = tests.filter(is_active=False)
            if search_filter:
                tests = tests.filter(
                    Q(title__icontains=search_filter) |
                    Q(description__icontains=search_filter)
                )
            
            # Get total count first
            total_count = tests.count()
            
            # Apply pagination
            start = (page - 1) * page_size
            tests_page = tests[start:start + page_size]
            
            test_data = []
            for test in tests_page:
                attempt_count = TestAttempt.objects.filter(test=test, is_completed=True).count()
                test_data.append({
                    'id': test.id,
                    'title': test.title,
                    'subject': test.subject,
                    'description': test.description,
                    'grade': test.grade,
                    'total_questions': test.total_questions,
                    'is_active': test.is_active,
                    'created_at': test.created_at.isoformat(),
                    'created_by': test.created_by.get_full_name() or test.created_by.username,
                    'attempt_count': attempt_count,
                    'max_attempts': test.max_attempts,
                    'time_limit': test.time_limit,
                })
            
            return JsonResponse({
                'tests': test_data,
                'user_role': 'admin',
                'pagination': {
                    'page': page,
                    'page_size': page_size,
                    'total': total_count,
                    'total_pages': (total_count + page_size - 1) // page_size
                }
            })
    
    return render(request, 'tests_app/test_list.html')

@login_required
@require_http_methods(["POST"])
def create_test(request):
    """Create a new test - Teachers only"""
    if request.user.role != 'teacher':
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    try:
        data = json.loads(request.body)
        
        required_fields = ['title', 'subject', 'grade', 'time_limit']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({'error': f'{field} is required'}, status=400)
        
        with transaction.atomic():
            test = Test.objects.create(
                title=data['title'],
                description=data.get('description', ''),
                subject=data['subject'],
                grade=int(data['grade']),
                time_limit=int(data['time_limit']),
                created_by=request.user,
                start_time=data.get('start_time'),
                end_time=data.get('end_time'),
                max_attempts=data.get('max_attempts', 1),
                show_results=data.get('show_results', True),
                shuffle_questions=data.get('shuffle_questions', False)
            )
            
            questions_data = data.get('questions', [])
            for i, q_data in enumerate(questions_data):
                question = Question.objects.create(
                    test=test,
                    question_text=q_data['question_text'],
                    question_type=q_data['question_type'],
                    points=float(q_data.get('points', 1.0)),
                    order=i + 1,
                    explanation=q_data.get('explanation', '')
                )
                
                if q_data['question_type'] in ['single_choice', 'multiple_choice']:
                    choices_data = q_data.get('choices', [])
                    for choice_data in choices_data:
                        Choice.objects.create(
                            question=question,
                            choice_text=choice_data['text'],
                            is_correct=choice_data.get('is_correct', False)
                        )
        
        return JsonResponse({
            'message': 'Test created successfully',
            'test_id': test.id
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def take_test_view(request, test_id):
    """Start or continue taking a test - Students only"""
    if request.user.role != 'student':
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    test = get_object_or_404(Test, id=test_id, is_active=True)
    
    if test.grade != request.user.grade:
        return JsonResponse({'error': 'This test is not for your grade'}, status=403)
    
    now = timezone.now()
    if test.start_time and now < test.start_time:
        return JsonResponse({'error': 'Test has not started yet'}, status=403)
    
    if test.end_time and now > test.end_time:
        return JsonResponse({'error': 'Test has ended'}, status=403)
    
    if request.method == 'POST':
        existing_attempt = TestAttempt.objects.filter(test=test, student=request.user).first()
        
        # Agar test tugallangan bo'lsa, qayta ishlash ruxsati bormi tekshiramiz
        if existing_attempt and existing_attempt.is_completed:
            # Qayta ishlash ruxsati bormi?
            approved_retake = TestRetakeRequest.objects.filter(
                student=request.user,
                test=test,
                status='approved',
                is_used=False
            ).first()
            
            if not approved_retake:
                return JsonResponse({'error': 'Siz allaqachon bu testni topshirgansiz. Qayta topshirish uchun admin ruxsati kerak.'}, status=400)
            
            # Qayta ishlash ruxsati bor, yangi attempt yaratamiz
            attempt = TestAttempt.objects.create(test=test, student=request.user)
            
            # Ruxsatni ishlatilgan deb belgilaymiz
            approved_retake.is_used = True
            approved_retake.save()
        elif not existing_attempt:
            # Birinchi marta test yechmoqda
            attempt = TestAttempt.objects.create(test=test, student=request.user)
        else:
            # Test tugallanmagan, davom ettirmoqda
            attempt = existing_attempt
        
        # Har bir o'quvchiga savollar random tartibda ko'rsatiladi
        # Query optimallashtirish - select_related va prefetch_related
        questions = list(test.questions.select_related().prefetch_related('choices').order_by('order'))
        
        # Shuffle questions for this student (har bir o'quvchi uchun boshqacha tartib)
        random.shuffle(questions)
        
        questions_data = []
        for question in questions:
            q_data = {
                'id': question.id,
                'question_text': question.question_text,
                'question_type': question.question_type,
                'points': question.points,
                'image': question.image.url if question.image and question.image.url else None
            }
            
            if question.question_type in ['single_choice', 'multiple_choice']:
                q_data['choices'] = [{
                    'id': choice.id,
                    'text': choice.choice_text
                } for choice in question.choices.all()]
            
            questions_data.append(q_data)
        
        return JsonResponse({
            'attempt_id': attempt.id,
            'questions': questions_data,
            'time_limit': test.time_limit,
            'started_at': attempt.started_at.isoformat(),
            'server_time': timezone.now().isoformat()  # Hozirgi server vaqti
        })
    
    # GET so'rovi - sahifa yuklash
    # Avval tugallangan testni tekshiramiz
    existing_attempt = TestAttempt.objects.filter(test=test, student=request.user).first()
    
    if existing_attempt and existing_attempt.is_completed:
        # Test allaqachon tugallangan
        # Qayta ishlash ruxsati bormi tekshiramiz
        approved_retake = TestRetakeRequest.objects.filter(
            student=request.user,
            test=test,
            status='approved',
            is_used=False
        ).first()
        
        if not approved_retake:
            # Ruxsat yo'q - natijalar sahifasiga yo'naltiramiz
            from django.contrib import messages
            messages.warning(request, 'Siz allaqachon bu testni topshirgansiz. Natijalarni ko\'ring yoki qayta topshirish uchun so\'rov yuboring.')
            return redirect('tests:test_results', test_id=test.id)
    
    return render(request, 'tests_app/take_test.html', {'test': test})

@login_required
@require_http_methods(["POST"])
def submit_answer(request, attempt_id):
    """Submit answer for a question"""
    if request.user.role != 'student':
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    try:
        data = json.loads(request.body)
        attempt = get_object_or_404(TestAttempt, id=attempt_id, student=request.user)
        
        if attempt.is_completed:
            return JsonResponse({'error': 'Test already completed'}, status=400)
        
        question_id = data.get('question_id')
        question = get_object_or_404(Question, id=question_id, test=attempt.test)
        
        # Debug logging
        print(f"Submitting answer for question {question_id}, type: {question.question_type}")
        print(f"Data received: {data}")
        
        answer, created = Answer.objects.get_or_create(
            attempt=attempt,
            question=question
        )
        
        # Clear previous answers
        answer.selected_choices.clear()
        answer.text_answer = ''
        
        if question.question_type == 'text_answer':
            answer.text_answer = data.get('text_answer', '')
            print(f"Text answer saved: {answer.text_answer}")
        else:
            choice_ids = data.get('choice_ids', [])
            if choice_ids:
                choices = Choice.objects.filter(id__in=choice_ids, question=question)
                print(f"Choices found: {list(choices.values_list('id', flat=True))}")
                answer.selected_choices.set(choices)
            else:
                print("No choice_ids provided")
        
        answer.save()
        
        # Update current question index for monitoring
        current_index = data.get('current_question_index', 0)
        if current_index is not None:
            attempt.current_question_index = current_index
            attempt.save(update_fields=['current_question_index'])
        
        # Verify answer was saved
        saved_choices = list(answer.selected_choices.values_list('id', flat=True))
        print(f"Answer saved successfully. Selected choices: {saved_choices}")
        
        return JsonResponse({
            'message': 'Answer saved',
            'saved_choices': saved_choices,
            'text_answer': answer.text_answer
        })
        
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {str(e)}")
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        print(f"Error submitting answer: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@require_http_methods(["POST"])
def finish_test(request, attempt_id):
    """Finish the test and calculate score"""
    if request.user.role != 'student':
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    try:
        attempt = get_object_or_404(TestAttempt, id=attempt_id, student=request.user)
        
        if attempt.is_completed:
            return JsonResponse({'error': 'Test already completed'}, status=400)
        
        attempt.finished_at = timezone.now()
        attempt.is_completed = True
        attempt.time_taken = attempt.finished_at - attempt.started_at
        
        # Calculate score using the method and get results
        results = attempt.calculate_score()
        
        # Use calculated values (do not access non-existing TestAttempt DB columns)
        correct_answers = results.get('correct_answers', 0)
        incorrect_answers = results.get('incorrect_answers', 0)
        unanswered = results.get('unanswered', 0)
        score = results.get('score', 0)
        total_points = results.get('total_points', 0)
        percentage = results.get('percentage', 0)

        # Update attempt fields (if model defines them they will be saved; otherwise these are harmless attributes)
        attempt.score = score
        attempt.total_points = total_points
        attempt.percentage = percentage

        test_result = TestResult.objects.create(
            attempt=attempt,
            correct_answers=correct_answers,
            incorrect_answers=incorrect_answers,
            unanswered=unanswered
        )
        test_result.grade = test_result.calculate_grade()
        test_result.save()
        
        attempt.save()
        
        # Create completion message
        total_questions = attempt.test.questions.count()
        answered_count = attempt.answers.count()
        all_answered = answered_count == total_questions
        
        completion_message = "Test yakunlandi!"
        if all_answered:
            completion_message = f"Ajoyib! Barcha {total_questions} ta savolga javob berdingiz!"
        else:
            completion_message = f"Test yakunlandi. {answered_count}/{total_questions} ta savolga javob berildi."
        
        return JsonResponse({
            'message': completion_message,
            'results': {
                'score': results['score'],
                'total_points': results['total_points'],
                'percentage': results['percentage'],
                'grade': test_result.grade,
                'correct_answers': correct_answers,
                'incorrect_answers': incorrect_answers,
                'unanswered': unanswered,
                'time_taken': str(attempt.time_taken),
                'all_answered': all_answered,
                'answered_count': answered_count,
                'total_questions': total_questions,
                'incorrect_questions': results.get('incorrect_questions', [])
            }
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def test_results_view(request, test_id):
    """View test results - Teachers can see all, students see their own"""
    test = get_object_or_404(Test, id=test_id)
    
    if request.headers.get('Accept') == 'application/json':
        if request.user.role == 'student':
            if test.grade != request.user.grade:
                return JsonResponse({'error': 'Access denied'}, status=403)
            
            attempt = TestAttempt.objects.filter(test=test, student=request.user).first()
            if not attempt or not attempt.is_completed:
                return JsonResponse({'error': 'Test not completed'}, status=404)
            
            # Get detailed results
            correct_answers = attempt.result.correct_answers if hasattr(attempt, 'result') else 0
            incorrect_answers = attempt.result.incorrect_answers if hasattr(attempt, 'result') else 0
            unanswered = attempt.result.unanswered if hasattr(attempt, 'result') else 0
            
            # Get incorrect questions details
            incorrect_questions = []
            unanswered_questions = []
            if hasattr(attempt, 'result') and attempt.result:
                # Get all answers for this attempt
                answers = Answer.objects.filter(attempt=attempt).select_related('question')
                answered_question_ids = set(answers.values_list('question_id', flat=True))
                
                # Get all questions for this test
                all_questions = test.questions.all()
                
                for answer in answers:
                    if not answer.is_correct():
                        question = answer.question
                        student_answer = answer.get_student_answer_text()
                        correct_answer = question.get_correct_answer_text()
                        
                        incorrect_questions.append({
                            'question_text': question.question_text,
                            'student_answer': student_answer,
                            'correct_answer': correct_answer,
                            'explanation': question.explanation or ''
                        })
                
                # Find unanswered questions
                for question in all_questions:
                    if question.id not in answered_question_ids:
                        unanswered_questions.append({
                            'question_text': question.question_text,
                            'correct_answer': question.get_correct_answer_text(),
                            'explanation': question.explanation or ''
                        })
            
            result_data = {
                'student': request.user.username,
                'score': attempt.score,
                'total_points': attempt.total_points,
                'percentage': attempt.percentage,
                'grade': attempt.result.grade if hasattr(attempt, 'result') else '',
                'time_taken': str(attempt.time_taken),
                'finished_at': attempt.finished_at.isoformat(),
                'correct_answers': correct_answers,
                'incorrect_answers': incorrect_answers,
                'unanswered': unanswered,
                'all_answered': (unanswered == 0),
                'answered_count': correct_answers + incorrect_answers,
                'total_questions': correct_answers + incorrect_answers + unanswered,
                # O'quvchilarga xato qilgan savollarni ko'rsatmaslik
                # 'incorrect_questions': incorrect_questions,
                # 'unanswered_questions': unanswered_questions
            }
            
            # Test info qo'shish
            test_info = {
                'title': test.title,
                'subject': test.subject,
                'grade': test.grade,
                'total_questions': test.total_questions,
                'time_limit': test.time_limit
            }
            
            return JsonResponse({
                'result': result_data,
                'test_info': test_info,
                'user_role': 'student'
            })
        
        elif (request.user.role == 'teacher' and test.created_by == request.user) or request.user.role == 'admin':
            # Faqat har bir o'quvchining oxirgi (eng so'nggi) natijasini olish
            from django.db.models import Max
            
            # Har bir o'quvchi uchun eng so'nggi attempt ID'sini topish
            latest_attempts = TestAttempt.objects.filter(
                test=test, 
                is_completed=True
            ).values('student').annotate(
                latest_attempt_id=Max('id')
            ).values_list('latest_attempt_id', flat=True)
            
            # Faqat oxirgi attempt'larni olish
            attempts = TestAttempt.objects.filter(
                id__in=latest_attempts
            ).select_related('student', 'result').order_by('student__grade', 'student__class_name', 'student__first_name', 'student__last_name')
            
            results_data = []
            for attempt in attempts:
                # Admin va o'qituvchilar uchun xato qilgan savollarni ham qo'shamiz
                incorrect_questions = []
                unanswered_questions = []
                
                if hasattr(attempt, 'result') and attempt.result:
                    # Get all answers for this attempt
                    answers = Answer.objects.filter(attempt=attempt).select_related('question')
                    answered_question_ids = set(answers.values_list('question_id', flat=True))
                    
                    # Get all questions for this test
                    all_questions = test.questions.all()
                    
                    for answer in answers:
                        if not answer.is_correct():
                            question = answer.question
                            student_answer = answer.get_student_answer_text()
                            correct_answer = question.get_correct_answer_text()
                            
                            incorrect_questions.append({
                                'question_text': question.question_text,
                                'student_answer': student_answer,
                                'correct_answer': correct_answer,
                                'explanation': question.explanation or ''
                            })
                    
                    # Find unanswered questions
                    for question in all_questions:
                        if question.id not in answered_question_ids:
                            unanswered_questions.append({
                                'question_text': question.question_text,
                                'correct_answer': question.get_correct_answer_text(),
                                'explanation': question.explanation or ''
                            })
                
                results_data.append({
                    'student': {
                        'username': attempt.student.username,
                        'first_name': attempt.student.first_name,
                        'last_name': attempt.student.last_name,
                        'student_id': attempt.student.student_id,
                        'class_name': attempt.student.class_name,
                        'grade': attempt.student.grade
                    },
                    'score': attempt.score,
                    'total_points': attempt.total_points,
                    'percentage': attempt.percentage,
                    'grade': attempt.result.grade if hasattr(attempt, 'result') else '',
                    'time_taken': str(attempt.time_taken),
                    'finished_at': attempt.finished_at.isoformat(),
                    'correct_answers': attempt.result.correct_answers if hasattr(attempt, 'result') else 0,
                    'incorrect_answers': attempt.result.incorrect_answers if hasattr(attempt, 'result') else 0,
                    'unanswered': attempt.result.unanswered if hasattr(attempt, 'result') else 0,
                    # Admin va o'qituvchilar uchun xato qilgan savollarni ko'rsatish
                    'incorrect_questions': incorrect_questions,
                    'unanswered_questions': unanswered_questions
                })
            
            # Test info qo'shish
            test_info = {
                'title': test.title,
                'subject': test.subject,
                'grade': test.grade,
                'total_questions': test.total_questions,
                'time_limit': test.time_limit
            }
            
            return JsonResponse({
                'results': results_data,
                'test_info': test_info,
                'user_role': request.user.role
            })
        
        else:
            return JsonResponse({'error': 'Access denied'}, status=403)
    
    return render(request, 'tests_app/test_results.html', {
        'test': test,
        'user_role': request.user.role
    })

@login_required
def export_results(request, test_id):
    """Export test results to Excel - Teachers only"""
    if request.user.role != 'teacher':
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    test = get_object_or_404(Test, id=test_id, created_by=request.user)
    attempts = TestAttempt.objects.filter(test=test, is_completed=True).select_related('student', 'result').order_by('student__grade', 'student__class_name', 'student__first_name', 'student__last_name')
    
    
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Test Results"
    
    # Header qo'shish
    headers = [
        'Student Username', 'First Name', 'Last Name', 'Student ID', 'Grade', 
        'Class', 'Score', 'Total Points', 'Percentage', 'Grade Result',
        'Correct Answers', 'Incorrect Answers', 'Unanswered', 'Time Taken', 'Finished At'
    ]
    
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = Font(bold=True)
        cell.fill = PatternFill(start_color="CCCCCC", end_color="CCCCCC", fill_type="solid")
    
    # Ma'lumotlarni qo'shish
    for row, attempt in enumerate(attempts, 2):
        data = [
            attempt.student.username,
            attempt.student.first_name,
            attempt.student.last_name,
            attempt.student.student_id or '',
            attempt.student.grade or '',
            attempt.student.class_name or '',
            attempt.score,
            attempt.total_points,
            attempt.percentage,
            attempt.result.grade if hasattr(attempt, 'result') else '',
            attempt.result.correct_answers if hasattr(attempt, 'result') else 0,
            attempt.result.incorrect_answers if hasattr(attempt, 'result') else 0,
            attempt.result.unanswered if hasattr(attempt, 'result') else 0,
            str(attempt.time_taken),
            attempt.finished_at.strftime('%Y-%m-%d %H:%M:%S')
        ]
        
        for col, value in enumerate(data, 1):
            ws.cell(row=row, column=col, value=value)
    
    # Excel faylini qaytarish
    from django.http import HttpResponse
    from io import BytesIO
    
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    
    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{test.title}_results.xlsx"'
    
    return response

@login_required
def upload_questions(request, test_id):
    """Upload questions from Excel file - Teachers only"""
    if request.user.role != 'teacher':
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    test = get_object_or_404(Test, id=test_id, created_by=request.user)
    
    if request.method == 'POST':
        try:
            excel_file = request.FILES.get('excel_file')
            if not excel_file:
                return JsonResponse({'error': 'No file uploaded'}, status=400)
            
            # Excel faylini openpyxl bilan o'qish
            from openpyxl import load_workbook
            
            wb = load_workbook(excel_file)
            ws = wb.active
            
            # Header qatorini o'qish
            headers = []
            for cell in ws[1]:
                if cell.value:
                    headers.append(cell.value.lower().replace(' ', '_'))
            
            # Kerakli ustunlarni tekshirish
            required_columns = ['question_text', 'question_type', 'points']
            for col in required_columns:
                if col not in headers:
                    return JsonResponse({'error': f'Missing column: {col}'}, status=400)
            
            questions_created = 0
            
            with transaction.atomic():
                for row_num, row in enumerate(ws.iter_rows(min_row=2, values_only=True), 1):
                    if not row[0]:  # question_text bo'sh bo'lsa
                        continue
                    
                    row_data = dict(zip(headers, row))
                    
                    question = Question.objects.create(
                        test=test,
                        question_text=row_data['question_text'],
                        question_type=row_data['question_type'],
                        points=float(row_data.get('points', 1.0)),
                        order=row_num,
                        explanation=row_data.get('explanation', '')
                    )
                    
                    # Javob variantlarini qo'shish
                    if row_data['question_type'] in ['single_choice', 'multiple_choice']:
                        for i in range(1, 6):  # 5 tagacha variant
                            choice_key = f'choice_{i}'
                            correct_key = f'choice_{i}_correct'
                            
                            if choice_key in row_data and row_data[choice_key]:
                                is_correct = bool(row_data.get(correct_key, False))
                                Choice.objects.create(
                                    question=question,
                                    choice_text=row_data[choice_key],
                                    is_correct=is_correct
                                )
                    
                    questions_created += 1
            
            return JsonResponse({'message': f'{questions_created} questions uploaded successfully'})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return render(request, 'tests_app/upload_questions.html', {'test': test})

@login_required
def create_test_view(request):
    """Create new test - only for teachers"""
    if request.user.role != 'teacher':
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    if request.method == 'GET':
        return render(request, 'tests_app/create_test.html')
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Test yaratish
                test = Test.objects.create(
                    title=request.POST.get('title'),
                    description=request.POST.get('description', ''),
                    subject=request.POST.get('subject'),
                    grade=int(request.POST.get('grade')),
                    time_limit=int(request.POST.get('time_limit', 45)),
                    max_attempts=int(request.POST.get('max_attempts', 1)),
                    show_results=bool(request.POST.get('show_results')),
                    is_active=bool(request.POST.get('is_active')),
                    created_by=request.user
                )
                
                # Savollar qo'shish
                question_texts = request.POST.getlist('question_text[]')
                question_types = request.POST.getlist('question_type[]')
                points_list = request.POST.getlist('points[]')
                explanations = request.POST.getlist('explanation[]')
                
                for i, question_text in enumerate(question_texts):
                    if not question_text.strip():
                        continue
                    
                    question = Question.objects.create(
                        test=test,
                        question_text=question_text,
                        question_type=question_types[i],
                        points=float(points_list[i]) if points_list[i] else 1.0,
                        order=i + 1,
                        explanation=explanations[i] if i < len(explanations) else ''
                    )
                    
                    # Javob variantlarini qo'shish
                    if question_types[i] != 'text_answer':
                        choices_key = f'choices_{i+1}[]'
                        correct_key = f'correct_choice_{i+1}'
                        
                        choices = request.POST.getlist(choices_key)
                        correct_index = request.POST.get(correct_key)
                        
                        for j, choice_text in enumerate(choices):
                            if choice_text.strip():
                                is_correct = str(j) == correct_index
                                Choice.objects.create(
                                    question=question,
                                    choice_text=choice_text,
                                    is_correct=is_correct
                                )
                
                return JsonResponse({
                    'success': True, 
                    'message': 'Test muvaffaqiyatli yaratildi!',
                    'test_id': test.id
                })
                
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
def test_info_view(request, test_id):
    """Get test information for display purposes"""
    test = get_object_or_404(Test, id=test_id)
    
    # Check access permissions
    if request.user.role == 'student' and test.grade != request.user.grade:
        return JsonResponse({'error': 'Access denied'}, status=403)
    elif request.user.role == 'teacher' and test.created_by != request.user:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    return JsonResponse({
        'title': test.title,
        'description': test.description,
        'subject': test.subject,
        'grade': test.grade,
        'time_limit': test.time_limit,
        'max_attempts': test.max_attempts,
        'total_questions': test.total_questions,
        'created_by': test.created_by.get_full_name() or test.created_by.username,
        'created_at': test.created_at.isoformat(),
        'start_time': test.start_time.isoformat() if test.start_time else None,
        'end_time': test.end_time.isoformat() if test.end_time else None,
    })

@login_required
def all_results_view(request):
    """Barcha test natijalarini ko'rsatish - Admin va Teacher uchun"""
    from django.db import connection, OperationalError
    from django.conf import settings
    
    if request.user.role not in ['admin', 'teacher']:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    if request.method == 'GET' and request.headers.get('Accept') == 'application/json':
        try:
            # Database engine aniqlash
            db_engine = settings.DATABASES['default']['ENGINE']
            if 'sqlite' in db_engine.lower():
                param_style = '?'
            else:
                param_style = '%s'
            
            # BARCHA natijalarni olish - RAW SQL ishlatamiz
            # Bu usul correct_answers maydoni yo'q bo'lsa ham xatolik bermaydi
            base_sql = """
                SELECT 
                    ta.id,
                    ta.score,
                    ta.total_points,
                    ta.percentage,
                    ta.finished_at,
                    ta.time_taken,
                    u.id as student_id,
                    u.username as student_username,
                    u.first_name as student_first_name,
                    u.last_name as student_last_name,
                    u.student_id as student_student_id,
                    u.class_name as student_class_name,
                    u.grade as student_grade,
                    t.id as test_id,
                    t.title as test_title,
                    t.subject as test_subject,
                    t.grade as test_grade,
                    teacher.username as teacher_username,
                    teacher.first_name as teacher_first_name,
                    teacher.last_name as teacher_last_name,
                    tr.correct_answers,
                    tr.incorrect_answers,
                    tr.unanswered
                FROM tests_app_testattempt ta
                INNER JOIN accounts_user u ON ta.student_id = u.id
                INNER JOIN tests_app_test t ON ta.test_id = t.id
                INNER JOIN accounts_user teacher ON t.created_by_id = teacher.id
                LEFT JOIN tests_app_testresult tr ON ta.id = tr.attempt_id
                WHERE ta.is_completed = 1
            """ if param_style == '?' else """
                SELECT 
                    ta.id,
                    ta.score,
                    ta.total_points,
                    ta.percentage,
                    ta.finished_at,
                    ta.time_taken,
                    u.id as student_id,
                    u.username as student_username,
                    u.first_name as student_first_name,
                    u.last_name as student_last_name,
                    u.student_id as student_student_id,
                    u.class_name as student_class_name,
                    u.grade as student_grade,
                    t.id as test_id,
                    t.title as test_title,
                    t.subject as test_subject,
                    t.grade as test_grade,
                    teacher.username as teacher_username,
                    teacher.first_name as teacher_first_name,
                    teacher.last_name as teacher_last_name,
                    tr.correct_answers,
                    tr.incorrect_answers,
                    tr.unanswered
                FROM tests_app_testattempt ta
                INNER JOIN accounts_user u ON ta.student_id = u.id
                INNER JOIN tests_app_test t ON ta.test_id = t.id
                INNER JOIN accounts_user teacher ON t.created_by_id = teacher.id
                LEFT JOIN tests_app_testresult tr ON ta.id = tr.attempt_id
                WHERE ta.is_completed = 1
            """
            
            # Teacher uchun filter qo'shish
            where_clauses = []
            params = []
            
            if request.user.role == 'teacher':
                where_clauses.append(f"t.created_by_id = {param_style}")
                params.append(request.user.id)
            
            # Filters
            grade = request.GET.get('grade')
            subject = request.GET.get('subject')
            test_id = request.GET.get('test')
            
            if grade:
                where_clauses.append(f"u.grade = {param_style}")
                params.append(grade)
            if subject:
                where_clauses.append(f"t.subject = {param_style}")
                params.append(subject)
            if test_id:
                where_clauses.append(f"t.id = {param_style}")
                params.append(test_id)
            
            # SQL query tuzish
            if where_clauses:
                sql_query = base_sql + " AND " + " AND ".join(where_clauses)
            else:
                sql_query = base_sql
            
            sql_query += " ORDER BY u.grade, u.last_name, u.first_name, ta.finished_at DESC"
            
            # Ma'lumotlarni olish
            with connection.cursor() as cursor:
                cursor.execute(sql_query, params)
                columns = [col[0] for col in cursor.description]
                
                results_data = []
                for row in cursor.fetchall():
                    row_dict = dict(zip(columns, row))
                    
                    # Calculate grade based on percentage
                    percentage = row_dict['percentage'] or 0
                    if percentage >= 81:
                        grade_text = "A'lo"
                    elif percentage >= 61:
                        grade_text = "Yaxshi"
                    elif percentage >= 31:
                        grade_text = "Qoniqarli"
                    else:
                        grade_text = "Qoniqarsiz"
                    
                    teacher_name = f"{row_dict.get('teacher_first_name', '') or ''} {row_dict.get('teacher_last_name', '') or ''}".strip()
                    if not teacher_name:
                        teacher_name = row_dict.get('teacher_username', '')
                    
                    results_data.append({
                        'test': {
                            'id': row_dict['test_id'],
                            'title': row_dict['test_title'],
                            'subject': row_dict['test_subject'],
                            'grade': row_dict['test_grade'],
                            'created_by': teacher_name
                        },
                        'student': {
                            'id': row_dict['student_id'],
                            'username': row_dict['student_username'],
                            'first_name': row_dict['student_first_name'],
                            'last_name': row_dict['student_last_name'],
                            'student_id': row_dict['student_student_id'],
                            'class_name': row_dict['student_class_name'],
                            'grade': row_dict['student_grade']
                        },
                        'score': row_dict['score'],
                        'total_points': row_dict['total_points'],
                        'percentage': row_dict['percentage'],
                        'grade': grade_text,
                        'time_taken': str(row_dict['time_taken']) if row_dict['time_taken'] else '',
                        'finished_at': row_dict['finished_at'].isoformat() if row_dict['finished_at'] else None,
                        'correct_answers': row_dict.get('correct_answers') or 0,
                        'incorrect_answers': row_dict.get('incorrect_answers') or 0,
                        'unanswered': row_dict.get('unanswered') or 0,
                        'student_name': f"{row_dict['student_first_name'] or ''} {row_dict['student_last_name'] or ''}".strip() or row_dict['student_username'],
                        'username': row_dict['student_username'],
                        'test_title': row_dict['test_title'],
                    })
            
            # Statistics
            stats_sql = "SELECT COUNT(*) FROM tests_app_testattempt WHERE is_completed = 1"
            stats_params = []
            
            if request.user.role == 'teacher':
                stats_sql = """
                    SELECT COUNT(*) 
                    FROM tests_app_testattempt ta
                    INNER JOIN tests_app_test t ON ta.test_id = t.id
                    WHERE ta.is_completed = 1 AND t.created_by_id = ?
                """ if param_style == '?' else """
                    SELECT COUNT(*) 
                    FROM tests_app_testattempt ta
                    INNER JOIN tests_app_test t ON ta.test_id = t.id
                    WHERE ta.is_completed = 1 AND t.created_by_id = %s
                """
                stats_params = [request.user.id]
            
            with connection.cursor() as cursor:
                cursor.execute(stats_sql, stats_params)
                total_results = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM accounts_user WHERE role = 'student' AND is_verified = 1")
                total_students = cursor.fetchone()[0]
            
            # Average percentage hisoblash
            avg_percentage = 0
            excellent_count = 0
            if results_data:
                percentages = [r['percentage'] for r in results_data if r['percentage']]
                if percentages:
                    avg_percentage = sum(percentages) / len(percentages)
                    excellent_count = len([p for p in percentages if p >= 81])
            
            stats = {
                'total_students': total_students,
                'total_results': total_results,
                'avg_percentage': round(avg_percentage, 2),
                'excellent_count': excellent_count,
            }
            
            return JsonResponse({
                'results': results_data,
                'stats': stats
            })
        
        except OperationalError as e:
            error_message = str(e)
            if 'correct_answers' in error_message or 'no such column' in error_message.lower():
                return JsonResponse({
                    'results': [],
                    'stats': {'total_students': 0, 'total_results': 0, 'avg_percentage': 0, 'excellent_count': 0},
                    'error': 'Database schema mismatch'
                })
            else:
                raise
    
    return render(request, 'tests_app/all_students_results.html', {
        'user_role': request.user.role
    })

@login_required
@require_http_methods(["POST"])
def request_retake_view(request, test_id):
    """O'quvchi qayta ishlash so'rovi yuborish"""
    if request.user.role != 'student':
        return JsonResponse({'error': 'Faqat o\'quvchilar qayta ishlash so\'rovi yuborishi mumkin'}, status=403)
    
    test = get_object_or_404(Test, id=test_id)
    
    try:
        # O'quvchining oxirgi attempt'ini topamiz
        attempt = TestAttempt.objects.filter(test=test, student=request.user, is_completed=True).last()
        if not attempt:
            return JsonResponse({'error': 'Siz hali bu testni topshirmadingiz'}, status=400)
        
        # Qayta ishlash so'rashi mumkinmi?
        if not attempt.can_request_retake():
            return JsonResponse({'error': 'Allaqachon qayta ishlash so\'rovi yuborilgan yoki kutilmoqda'}, status=400)
        
        # JSON ma'lumotni olish
        try:
            if request.body:
                data = json.loads(request.body)
                reason = data.get('reason', '').strip()
            else:
                reason = ''
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Noto\'g\'ri JSON ma\'lumot. Iltimos, to\'g\'ri format kiriting.'}, status=400)
        
        # Agar sabab bo'sh bo'lsa, default sabab
        if not reason or len(reason) < 10:
            return JsonResponse({'error': 'Qayta ishlash sababi kamida 10 ta belgidan iborat bo\'lishi kerak'}, status=400)
        
        # Qayta ishlash so'rovini yaratamiz
        retake_request = TestRetakeRequest.objects.create(
            student=request.user,
            test=test,
            previous_attempt=attempt,
            reason=reason
        )
        
        return JsonResponse({
            'message': 'Qayta ishlash so\'rovi muvaffaqiyatli yuborildi!',
            'request_id': retake_request.id
        })
        
    except Exception as e:
        print(f"Request retake error: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': f'Xatolik yuz berdi: {str(e)}'}, status=500)

@login_required  
def retake_requests_view(request):
    """Admin qayta ishlash so'rovlarini ko'rish va boshqarish"""
    if request.user.role != 'admin':
        return JsonResponse({'error': 'Faqat adminlar kirishi mumkin'}, status=403)
    
    if request.method == 'GET' and request.headers.get('Accept') == 'application/json':
        # JSON API so'rovi
        status_filter = request.GET.get('status', 'all')
        
        requests_qs = TestRetakeRequest.objects.select_related(
            'student', 'test', 'previous_attempt', 'approved_by'
        ).order_by('-created_at')
        
        if status_filter != 'all':
            requests_qs = requests_qs.filter(status=status_filter)
        
        requests_data = []
        for req in requests_qs:
            requests_data.append({
                'id': req.id,
                'student_name': req.student.get_full_name(),
                'student_username': req.student.username,
                'student_grade': req.student.grade,
                'student_class': req.student.class_name,
                'test_title': req.test.title,
                'test_subject': req.test.subject,
                'previous_score': req.previous_attempt.score,
                'previous_percentage': req.previous_attempt.percentage,
                'reason': req.reason,
                'status': req.status,
                'status_display': req.get_status_display(),
                'admin_response': req.admin_response,
                'approved_by': req.approved_by.get_full_name() if req.approved_by else None,
                'created_at': req.created_at.isoformat(),
                'updated_at': req.updated_at.isoformat()
            })
        
        return JsonResponse({
            'requests': requests_data,
            'total_count': len(requests_data)
        })
    
    # HTML template
    return render(request, 'tests_app/retake_requests.html')

@login_required
@require_http_methods(["POST"])
def handle_retake_request_view(request, request_id):
    """Admin qayta ishlash so'rovini tasdiqlash yoki rad etish"""
    if request.user.role != 'admin':
        return JsonResponse({'error': 'Faqat adminlar kirishi mumkin'}, status=403)
    
    retake_request = get_object_or_404(TestRetakeRequest, id=request_id)
    
    if retake_request.status != 'pending':
        return JsonResponse({'error': 'Bu so\'rov allaqachon ko\'rib chiqilgan'}, status=400)
    
    try:
        data = json.loads(request.body)
        action = data.get('action')  # 'approve' yoki 'reject'
        admin_response = data.get('admin_response', '').strip()
        
        if action not in ['approve', 'reject']:
            return JsonResponse({'error': 'Noto\'g\'ri harakat'}, status=400)
        
        retake_request.status = 'approved' if action == 'approve' else 'rejected'
        retake_request.admin_response = admin_response
        retake_request.approved_by = request.user
        retake_request.save()
        
        return JsonResponse({
            'message': f'So\'rov {"tasdiqlandi" if action == "approve" else "rad etildi"}!',
            'status': retake_request.status
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Noto\'g\'ri JSON ma\'lumot'}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Xatolik yuz berdi'}, status=500)


@login_required
def open_test_for_student(request, test_id, student_id):
    """Admin tomonidan o'quvchi uchun testni qayta ochish"""
    if request.user.role != 'admin':
        return JsonResponse({'error': 'Ruxsat berilmagan'}, status=403)
    
    if request.method != 'POST':
        return JsonResponse({'error': 'POST so\'rov talab qilinadi'}, status=405)
    
    try:
        test = Test.objects.get(id=test_id)
        student = User.objects.get(id=student_id, role='student')
        
        # O'quvchining bu testdagi avvalgi urinishlarini tekshirish
        previous_attempts = TestAttempt.objects.filter(
            student=student,
            test=test
        ).count()
        
        # Yangi urinish yaratish (qayta ishlash imkoniyati)
        new_attempt = TestAttempt.objects.create(
            student=student,
            test=test,
            attempt_number=previous_attempts + 1,
            is_retake=True
        )
        
        # Agar qayta ishlash so'rovi mavjud bo'lsa, uni tasdiqlangan deb belgilash
        retake_request = TestRetakeRequest.objects.filter(
            student=student,
            test=test,
            status='approved'
        ).first()
        
        if retake_request:
            retake_request.is_used = True
            retake_request.save()
        
        return JsonResponse({
            'message': f'{student.get_full_name()} uchun "{test.title}" testi qayta ochildi!',
            'attempt_id': new_attempt.id,
            'attempt_number': new_attempt.attempt_number
        })
        
    except Test.DoesNotExist:
        return JsonResponse({'error': 'Test topilmadi'}, status=404)
    except User.DoesNotExist:
        return JsonResponse({'error': 'O\'quvchi topilmadi'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def student_test_management(request):
    """Admin uchun o'quvchilarning test holatlarini boshqarish"""
    if request.user.role != 'admin':
        return redirect('accounts:dashboard')
    
    # Barcha faol testlar
    tests = Test.objects.filter(is_active=True)
    
    # Barcha tasdiqlangan o'quvchilar
    students = User.objects.filter(role='student', is_verified=True)
    
    # Har bir o'quvchi va test uchun urinishlar ma'lumotlari
    student_test_data = []
    
    for student in students:
        student_tests = []
        for test in tests:
            attempts = TestAttempt.objects.filter(student=student, test=test)
            latest_attempt = attempts.order_by('-started_at').first()
            
            # Qayta ishlash so'rovlari
            retake_requests = TestRetakeRequest.objects.filter(
                student=student,
                test=test
            ).order_by('-created_at')
            
            test_info = {
                'test': test,
                'attempts_count': attempts.count(),
                'latest_attempt': latest_attempt,
                'can_retake': latest_attempt is not None,
                'retake_requests': retake_requests
            }
            student_tests.append(test_info)
        
        student_test_data.append({
            'student': student,
            'tests': student_tests
        })
    
    context = {
        'student_test_data': student_test_data,
        'all_tests': tests
    }
    
    return render(request, 'tests_app/student_test_management.html', context)

@login_required
@require_http_methods(["POST", "DELETE"])
def delete_test_view(request, test_id):
    """Delete a test - Teachers (only their own tests) and Admins (any test)"""
    if request.user.role not in ['teacher', 'admin']:
        return JsonResponse({'error': 'Ruxsat berilmagan'}, status=403)
    
    # Teachers can only delete their own tests, admins can delete any test
    if request.user.role == 'teacher':
        test = get_object_or_404(Test, id=test_id, created_by=request.user)
    else:  # admin
        test = get_object_or_404(Test, id=test_id)
    
    try:
        test_title = test.title
        test.delete()
        return JsonResponse({
            'success': True,
            'message': f'"{test_title}" testi muvaffaqiyatli o\'chirildi!'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Testni o\'chirishda xatolik: {str(e)}'
        }, status=500)

@login_required
def edit_test_view(request, test_id):
    """Edit an existing test and its questions (teachers and admins)"""
    # Teachers can only edit their own tests, admins can edit any test
    if request.user.role == 'teacher':
        test = get_object_or_404(Test, id=test_id, created_by=request.user)
    elif request.user.role == 'admin':
        test = get_object_or_404(Test, id=test_id)
    else:
        return JsonResponse({'error': 'Access denied'}, status=403)

    if request.method == 'POST':
        try:
            # Check if it's FormData (for image upload) or JSON
            print(f"Request content type: {request.content_type}")
            print(f"Request method: {request.method}")
            print(f"Request POST data: {request.POST}")
            print(f"Request FILES: {request.FILES}")
            
            if request.content_type and 'multipart/form-data' in request.content_type:
                # Handle FormData for image upload or removal
                
                # Check if this is an image update/removal for existing question
                if request.POST.get('update_image_only') or request.POST.get('remove_image'):
                    question_id = request.POST.get('question_id')
                    if not question_id:
                        return JsonResponse({'success': False, 'error': 'Question ID kerak!'})
                    
                    try:
                        question = Question.objects.get(id=question_id, test=test)
                        
                        if request.POST.get('remove_image'):
                            # Remove image
                            if question.image:
                                question.image.delete(save=False)
                                question.image = None
                                question.save()
                                return JsonResponse({'success': True, 'message': 'Rasm o\'chirildi!'})
                            else:
                                return JsonResponse({'success': False, 'error': 'Rasm mavjud emas!'})
                        
                        elif request.POST.get('update_image_only'):
                            # Update image only
                            question_image = request.FILES.get('question_image')
                            if question_image:
                                # Remove old image if exists
                                if question.image:
                                    question.image.delete(save=False)
                                question.image = question_image
                                question.save()
                                return JsonResponse({
                                    'success': True, 
                                    'message': 'Rasm yuklandi!',
                                    'image_url': question.image.url
                                })
                            else:
                                return JsonResponse({'success': False, 'error': 'Rasm fayli topilmadi!'})
                    
                    except Question.DoesNotExist:
                        return JsonResponse({'success': False, 'error': 'Savol topilmadi!'})
                    except Exception as e:
                        return JsonResponse({'success': False, 'error': str(e)})
                
                # Handle new question creation with image
                question_text = request.POST.get('question_text')
                question_type = request.POST.get('question_type')
                points = request.POST.get('points', 1)
                explanation = request.POST.get('explanation', '')
                question_image = request.FILES.get('question_image')
                
                print(f"Question text: {question_text}")
                print(f"Question type: {question_type}")
                print(f"Points: {points}")
                print(f"Explanation: {explanation}")
                print(f"Question image: {question_image}")
                
                # Validation
                if not question_text:
                    return JsonResponse({
                        'success': False,
                        'error': 'Savol matni kiritilishi shart!'
                    })
                
                if not question_type:
                    return JsonResponse({
                        'success': False,
                        'error': 'Savol turi tanlanishi shart!'
                    })
                
                # Create new question with image
                try:
                    question = Question.objects.create(
                        test=test,
                        question_text=question_text,
                        question_type=question_type,
                        points=float(points),
                        order=test.questions.count() + 1,
                        explanation=explanation,
                        image=question_image
                    )
                    print(f"Question created successfully with ID: {question.id}")
                except Exception as e:
                    print(f"Error creating question: {e}")
                    return JsonResponse({
                        'success': False,
                        'error': f'Question yaratishda xatolik: {str(e)}'
                    })
                
                # Handle choices
                try:
                    if question_type in ['single_choice', 'multiple_choice']:
                        choice_index = 0
                        while f'choices[{choice_index}][text]' in request.POST:
                            choice_text = request.POST.get(f'choices[{choice_index}][text]')
                            is_correct = request.POST.get(f'choices[{choice_index}][is_correct]') == 'true'
                            if choice_text:
                                Choice.objects.create(
                                    question=question,
                                    choice_text=choice_text,
                                    is_correct=is_correct
                                )
                                print(f"Choice {choice_index} created: {choice_text}")
                            choice_index += 1
                except Exception as e:
                    print(f"Error creating choices: {e}")
                    # Don't return error here, question is already created
                
                return JsonResponse({
                    'success': True,
                    'message': 'Savol muvaffaqiyatli qo\'shildi!',
                    'question_id': question.id
                })
            else:
                # Handle JSON data (existing functionality)
                data = json.loads(request.body)
                print(f"Received data for test {test_id}: {data}")
            
                # Update test fields
                test.title = data.get('title', test.title)
                test.description = data.get('description', test.description)
                test.subject = data.get('subject', test.subject)
                test.grade = int(data.get('grade', test.grade))
                test.time_limit = int(data.get('time_limit', test.time_limit))
                test.max_attempts = int(data.get('max_attempts', test.max_attempts))
                test.show_results = data.get('show_results', test.show_results)
                test.is_active = data.get('is_active', test.is_active)
                test.shuffle_questions = data.get('shuffle_questions', test.shuffle_questions)
                test.save()
                print(f"Test {test_id} updated successfully")

                # Update questions
                questions_data = data.get('questions', [])
                print(f"Processing {len(questions_data)} questions")
            
                # Get existing question IDs
                existing_question_ids = set(test.questions.values_list('id', flat=True))
                new_question_ids = set()
            
                for i, q_data in enumerate(questions_data):
                    question_id = q_data.get('id')
                    print(f"Processing question {i+1}: ID={question_id}, Text='{q_data.get('question_text', '')[:50]}...'")
                
                    if question_id and question_id in existing_question_ids:
                        # Update existing question
                        try:
                            question = Question.objects.get(id=question_id, test=test)
                            question.question_text = q_data['question_text']
                            question.question_type = q_data['question_type']
                            question.points = float(q_data.get('points', 1.0))
                            question.order = i + 1
                            question.explanation = q_data.get('explanation', '')
                            question.save()
                            new_question_ids.add(question_id)
                            print(f"Updated existing question {question_id}")
                        
                            # Update choices
                            if q_data['question_type'] in ['single_choice', 'multiple_choice']:
                                choices_data = q_data.get('choices', [])
                                # Clear existing choices
                                question.choices.all().delete()
                                # Add new choices
                                for c_data in choices_data:
                                    if c_data.get('text'):  # Only add if text is not empty
                                        Choice.objects.create(
                                            question=question,
                                            choice_text=c_data['text'],
                                            is_correct=c_data.get('is_correct', False)
                                        )
                            else:
                                # For text answers, remove all choices
                                question.choices.all().delete()
                            
                        except Question.DoesNotExist:
                            # If question doesn't exist, create new one
                            question = Question.objects.create(
                                test=test,
                                question_text=q_data['question_text'],
                                question_type=q_data['question_type'],
                                points=float(q_data.get('points', 1.0)),
                                order=i + 1,
                                explanation=q_data.get('explanation', '')
                            )
                            new_question_ids.add(question.id)
                        
                            if q_data['question_type'] in ['single_choice', 'multiple_choice']:
                                for c_data in q_data.get('choices', []):
                                    if c_data.get('text'):
                                        Choice.objects.create(
                                            question=question,
                                            choice_text=c_data['text'],
                                            is_correct=c_data.get('is_correct', False)
                                        )
                    else:
                        # Create new question
                        print(f"Creating new question: {q_data['question_text'][:50]}...")
                        question = Question.objects.create(
                            test=test,
                            question_text=q_data['question_text'],
                            question_type=q_data['question_type'],
                            points=float(q_data.get('points', 1.0)),
                            order=i + 1,
                            explanation=q_data.get('explanation', '')
                        )
                        new_question_ids.add(question.id)
                        print(f"Created new question with ID {question.id}")
                    
                        if q_data['question_type'] in ['single_choice', 'multiple_choice']:
                            for c_data in q_data.get('choices', []):
                                if c_data.get('text'):
                                    Choice.objects.create(
                                        question=question,
                                        choice_text=c_data['text'],
                                        is_correct=c_data.get('is_correct', False)
                                    )
            
                # Remove questions that are no longer in the list
                questions_to_delete = existing_question_ids - new_question_ids
                if questions_to_delete:
                    test.questions.filter(id__in=questions_to_delete).delete()
                
                # Saqlangan savollarni JSON ko'rinishda qaytarish:
                questions = test.questions.all().order_by('order')
                questions_data = []
                for q in questions:
                    q_data = {
                        "id": q.id,
                        "question_text": q.question_text,
                        "question_type": q.question_type,
                        "points": q.points,
                        "explanation": q.explanation,
                        "image": q.image.url if q.image else None,
                        "choices": [
                            {"text": c.choice_text, "is_correct": c.is_correct}
                            for c in q.choices.all()
                        ]
                    }
                    questions_data.append(q_data)
                return JsonResponse({"success": True, "questions": questions_data})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    # GET: Render edit page with test and questions
    if request.headers.get('Accept') == 'application/json':
        # Return JSON data for AJAX requests
        questions = test.questions.all().order_by('order')
        questions_data = []
        for q in questions:
            q_data = {
                'id': q.id,
                'question_text': q.question_text,
                'question_type': q.question_type,
                'points': q.points,
                'explanation': q.explanation,
                'image': q.image.url if q.image else None,  # Add image URL
                'choices': []
            }
            if q.question_type in ['single_choice', 'multiple_choice']:
                q_data['choices'] = [
                    {'id': c.id, 'text': c.choice_text, 'is_correct': c.is_correct}
                    for c in q.choices.all()
                ]
            questions_data.append(q_data)
        
        print(f"Returning {len(questions_data)} questions for test {test.id}")
        for i, q in enumerate(questions_data):
            print(f"  Question {i+1}: {q['question_text'][:50]}... ({q['question_type']})")
        
        return JsonResponse({
            'test': {
                'id': test.id,
                'title': test.title,
                'subject': test.subject,
                'grade': test.grade,
                'time_limit': test.time_limit,
                'max_attempts': test.max_attempts,
                'description': test.description,
                'show_results': test.show_results,
                'is_active': test.is_active
            },
            'questions': questions_data
        })
    
    # Regular HTML request
    questions = test.questions.all().order_by('order')
    questions_data = []
    for q in questions:
        q_data = {
            'id': q.id,
            'question_text': q.question_text,
            'question_type': q.question_type,
            'points': q.points,
            'explanation': q.explanation,
            'image': q.image.url if q.image else None,  # Add image URL
            'choices': []
        }
        if q.question_type in ['single_choice', 'multiple_choice']:
            q_data['choices'] = [
                {'id': c.id, 'text': c.choice_text, 'is_correct': c.is_correct}
                for c in q.choices.all()
            ]
        questions_data.append(q_data)
    context = {
        'test': test,
        'questions': questions_data
    }
    return render(request, 'tests_app/edit_test.html', context)

@login_required
def start_test_view(request, test_id):
    """Admin tomonidan o'quvchi uchun testi boshlash"""
    test = get_object_or_404(Test, pk=test_id)
    questions = list(test.questions.all())
    random.shuffle(questions)  # Har bir o‘quvchi uchun random tartib
    
    context = {
        'test': test,
        'questions': questions,
    }
    return render(request, 'tests_app/start_test.html', context)

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from .models import Test

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def admin_teacher_tests(request):
    """
    Admin uchun: barcha testlarni ko'rsatish
    URL: /tests/admin/teacher-tests/
    """
    tests = (
        Test.objects
        .all()  # Barcha testlar
        .select_related('created_by')
        .prefetch_related('attempts')
        .order_by('-created_at')
    )

    return render(request, 'admin/tests_teacher_list.html', {
        'teacher_tests': tests
    })

@login_required
def grade_based_results_view(request):
    """Sinf bo'yicha test natijalarini ko'rsatish"""
    if request.user.role not in ['teacher', 'admin']:
        return redirect('accounts:dashboard')
    
    # Barcha sinflarni olish (1-11)
    grades = list(range(1, 12))
    
    # Har bir sinf uchun statistikalar
    grade_stats = []
    for grade in grades:
        # Bu sinf uchun testlar
        tests = Test.objects.filter(grade=grade, is_active=True)
        
        # Bu sinf o'quvchilari
        students = User.objects.filter(role='student', grade=grade, is_verified=True)
        
        # Bu sinf uchun test urinishlari - faqat har bir o'quvchining oxirgi natijasi
        from django.db.models import Max
        
        # Har bir o'quvchi uchun eng so'nggi attempt ID'sini topish
        latest_attempts = TestAttempt.objects.filter(
            test__grade=grade,
            student__grade=grade,
            is_completed=True
        ).values('student').annotate(
            latest_attempt_id=Max('id')
        ).values_list('latest_attempt_id', flat=True)
        
        # Faqat oxirgi attempt'larni olish
        # Override model default ordering (which referenced a removed column) by ordering by id
        attempts = list(TestAttempt.objects.filter(
            id__in=latest_attempts
        ).select_related('student', 'test').prefetch_related('result').order_by('id'))
        
        # Collect percentages safely (prefer TestResult, fallback to stored attempt field if exists, else calculate)
        percentages = []
        attempt_data_map = {}
        for attempt in attempts:
            pct = None
            # try related TestResult first
            if hasattr(attempt, 'result') and getattr(attempt, 'result') is not None:
                pct = getattr(attempt.result, 'percentage', None)
                score = getattr(attempt.result, 'score', None)
                total_points = getattr(attempt.result, 'total_points', None)
            else:
                # fallback to attempt fields if present
                pct = getattr(attempt, 'percentage', None)
                score = getattr(attempt, 'score', None)
                total_points = getattr(attempt, 'total_points', None)
                # last fallback: call calculate_score() if available (may be expensive)
                if pct is None:
                    try:
                        calc = attempt.calculate_score()
                        pct = calc.get('percentage', 0)
                        score = calc.get('score', score)
                        total_points = calc.get('total_points', total_points)
                    except Exception:
                        pct = 0
            pct = 0 if pct is None else pct
            percentages.append(pct)
            attempt_data_map[attempt.id] = {
                'attempt': attempt,
                'percentage': pct,
                'score': score,
                'total_points': total_points
            }
        
        total_students = students.count()
        total_tests = tests.count()
        total_attempts = len(attempts)
        
        if total_attempts > 0:
            avg_percentage = sum(percentages) / total_attempts
            highest_score = max(percentages)
            lowest_score = min(percentages)
        else:
            avg_percentage = 0
            highest_score = 0
            lowest_score = 0
        
        # BARCHA natijalar (faqat top 5 emas!)
        sorted_attempts = sorted(attempt_data_map.values(), key=lambda x: x['percentage'], reverse=True)
        
        grade_stats.append({
            'grade': grade,
            'total_students': total_students,
            'total_tests': total_tests,
            'total_attempts': total_attempts,
            'avg_percentage': round(avg_percentage, 1),
            'highest_score': round(highest_score, 1),
            'lowest_score': round(lowest_score, 1),
            'all_results': [
                {
                    'student_name': f"{item['attempt'].student.first_name} {item['attempt'].student.last_name}",
                    'student_username': item['attempt'].student.username,
                    'test_title': item['attempt'].test.title,
                    'percentage': round(item['percentage'], 1),
                    'score': item.get('score') or item['attempt'].score if hasattr(item['attempt'], 'score') else None,
                    'total_points': item.get('total_points') or item['attempt'].total_points if hasattr(item['attempt'], 'total_points') else None,
                    'finished_at': item['attempt'].finished_at
                }
                for item in sorted_attempts
            ]
        })
    
    # Umumiy statistika
    total_students = User.objects.filter(role='student', is_verified=True).count()
    total_teachers = User.objects.filter(role='teacher', is_verified=True).count()
    total_tests = Test.objects.filter(is_active=True).count()
    total_attempts = TestAttempt.objects.filter(is_completed=True).count()
    
    context = {
        'grade_stats': grade_stats,
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_tests': total_tests,
        'total_attempts': total_attempts,
    }
    
    return render(request, 'tests_app/grade_based_results.html', context)

@login_required
def export_grade_results_view(request):
    """Sinf bo'yicha natijalarni Excel faylga export qilish"""
    if request.user.role not in ['teacher', 'admin']:
        return redirect('accounts:dashboard')
    
    if not OPENPYXL_AVAILABLE:
        return JsonResponse({'error': 'Excel export funksiyasi mavjud emas. Iltimos openpyxl kutubxonasini o\'rnating.'}, status=500)
    
    try:
        # Excel workbook yaratish
        wb = Workbook()
        
        # Barcha sinflarni olish (1-11)
        grades = list(range(1, 12))
        
        for grade in grades:
            # Har bir sinf uchun alohida sheet yaratish
            ws = wb.create_sheet(title=f"{grade}-sinf")
        
        # Header qo'shish
        ws['A1'] = f"{grade}-sinf Test Natijalari"
        ws['A1'].font = Font(bold=True, size=16)
        ws['A1'].fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
        
        # Umumiy ma'lumotlar
        ws['A3'] = "Umumiy Ma'lumotlar:"
        ws['A3'].font = Font(bold=True)
        
        # Bu sinf uchun testlar
        tests = Test.objects.filter(grade=grade, is_active=True)
        
        # Bu sinf o'quvchilari
        students = User.objects.filter(role='student', grade=grade, is_verified=True)
        
        # Bu sinf uchun test urinishlari - faqat har bir o'quvchining oxirgi natijasi
        from django.db.models import Max
        
        # Har bir o'quvchi uchun eng so'nggi attempt ID'sini topish
        latest_attempts = TestAttempt.objects.filter(
            test__grade=grade,
            student__grade=grade,
            is_completed=True
        ).values('student').annotate(
            latest_attempt_id=Max('id')
        ).values_list('latest_attempt_id', flat=True)
        
        # Faqat oxirgi attempt'larni olish
        attempts = TestAttempt.objects.filter(
            id__in=latest_attempts
        ).select_related('student', 'test', 'result')
        
        # Statistika hisoblash
        total_students = students.count()
        total_tests = tests.count()
        total_attempts = attempts.count()
        
        if total_attempts > 0:
            avg_percentage = attempts.aggregate(avg=Avg('percentage'))['avg'] or 0
            highest_score = attempts.aggregate(max=Max('percentage'))['max'] or 0
            lowest_score = attempts.aggregate(min=Min('percentage'))['min'] or 0
        else:
            avg_percentage = 0
            highest_score = 0
            lowest_score = 0
        
        # Ma'lumotlarni yozish
        ws['A4'] = f"Jami O'quvchilar: {total_students}"
        ws['A5'] = f"Jami Testlar: {total_tests}"
        ws['A6'] = f"Jami Urinishlar: {total_attempts}"
        ws['A7'] = f"O'rtacha Ball: {avg_percentage:.1f}%"
        ws['A8'] = f"Eng Yuqori Ball: {highest_score:.1f}%"
        ws['A9'] = f"Eng Past Ball: {lowest_score:.1f}%"
        
        # Bo'sh qator
        ws['A11'] = "Barcha Natijalar:"
        ws['A11'].font = Font(bold=True)
        
        # Header qator
        headers = ['O\'quvchi', 'Test', 'Ball', 'Foiz', 'Vaqt', 'Sana']
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=12, column=col, value=header)
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color="D9E2F3", end_color="D9E2F3", fill_type="solid")
        
        # Natijalarni yozish
        row = 13
        for attempt in attempts.order_by('-percentage'):
            student_name = f"{attempt.student.first_name} {attempt.student.last_name}"
            if not student_name.strip():
                student_name = attempt.student.username
            
            ws.cell(row=row, column=1, value=student_name)
            ws.cell(row=row, column=2, value=attempt.test.title)
            ws.cell(row=row, column=3, value=attempt.score)
            ws.cell(row=row, column=4, value=f"{attempt.percentage:.1f}%")
            ws.cell(row=row, column=5, value=str(attempt.time_taken))
            ws.cell(row=row, column=6, value=attempt.finished_at.strftime('%Y-%m-%d %H:%M:%S'))
            
            # Ball bo'yicha rang berish
            if attempt.percentage >= 81:
                fill_color = "C6EFCE"  # Yashil
            elif attempt.percentage >= 61:
                fill_color = "FFEB9C"  # Sariq
            elif attempt.percentage >= 31:
                fill_color = "FFC7CE"  # Qizil
            else:
                fill_color = "FFC7CE"  # Qizil
            
            for col in range(1, 7):
                ws.cell(row=row, column=col).fill = PatternFill(start_color=fill_color, end_color=fill_color, fill_type="solid")
            
            row += 1
        
        # Ustun kengliklarini sozlash
        ws.column_dimensions['A'].width = 25
        ws.column_dimensions['B'].width = 30
        ws.column_dimensions['C'].width = 10
        ws.column_dimensions['D'].width = 10
        ws.column_dimensions['E'].width = 15
        ws.column_dimensions['F'].width = 20
    
        # Default sheet'ni o'chirish
        if 'Sheet' in wb.sheetnames:
            wb.remove(wb['Sheet'])
        
        # Response yaratish
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="sinf_natijalari.xlsx"'
        
        # Excel faylni saqlash
        wb.save(response)
        
        return response
        
    except Exception as e:
        print(f"Export error: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': f'Export xatolik yuz berdi: {str(e)}'}, status=500)

@login_required
def export_single_grade_results_view(request, grade):
    """Bitta sinf uchun Excel fayl yaratish"""
   

   
    if request.user.role not in ['teacher', 'admin']:
        return redirect('accounts:dashboard')
    
    if not OPENPYXL_AVAILABLE:
        return JsonResponse({'error': 'Excel export funksiyasi mavjud emas. Iltimos openpyxl kutubxonasini o\'rnating.'}, status=500)
    
    try:
        # Excel workbook yaratish
        wb = Workbook()
        ws = wb.active
        ws.title = f"{grade}-sinf"
        
        # Header qo'shish
        ws['A1'] = f"{grade}-sinf Test Natijalari"
        ws['A1'].font = Font(bold=True, size=16)
        ws['A1'].fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    
        # Umumiy ma'lumotlar
        ws['A3'] = "Umumiy Ma'lumotlar:"
        ws['A3'].font = Font(bold=True)
    
        # Bu sinf uchun testlar
        tests = Test.objects.filter(grade=grade, is_active=True)
    
        # Bu sinf o'quvchilari
        students = User.objects.filter(role='student', grade=grade, is_verified=True)
    
        # Bu sinf uchun test urinishlari - faqat har bir o'quvchining oxirgi natijasi
        from django.db.models import Max
    
        # Har bir o'quvchi uchun eng so'nggi attempt ID'sini topish
        latest_attempts = TestAttempt.objects.filter(
        test__grade=grade,
        student__grade=grade,
        is_completed=True
        ).values('student').annotate(
        latest_attempt_id=Max('id')
        ).values_list('latest_attempt_id', flat=True)
    
        # Faqat oxirgi attempt'larni olish
        attempts = TestAttempt.objects.filter(
        id__in=latest_attempts
        ).select_related('student', 'test', 'result')
    
        # Statistika hisoblash
        total_students = students.count()
        total_tests = tests.count()
        total_attempts = attempts.count()
    
        if total_attempts > 0:
            avg_percentage = attempts.aggregate(avg=Avg('percentage'))['avg'] or 0
            highest_score = attempts.aggregate(max=Max('percentage'))['max'] or 0
            lowest_score = attempts.aggregate(min=Min('percentage'))['min'] or 0
        else:
            avg_percentage = 0
            highest_score = 0
            lowest_score = 0
    
        # Ma'lumotlarni yozish
        ws['A4'] = f"Jami O'quvchilar: {total_students}"
        ws['A5'] = f"Jami Testlar: {total_tests}"
        ws['A6'] = f"Jami Urinishlar: {total_attempts}"
        ws['A7'] = f"O'rtacha Ball: {avg_percentage:.1f}%"
        ws['A8'] = f"Eng Yuqori Ball: {highest_score:.1f}%"
        ws['A9'] = f"Eng Past Ball: {lowest_score:.1f}%"
    
        # Bo'sh qator
        ws['A11'] = "Barcha Natijalar:"
        ws['A11'].font = Font(bold=True)
    
        # Header qator
        headers = ['O\'quvchi', 'Test', 'Ball', 'Foiz', 'Vaqt', 'Sana']
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=12, column=col, value=header)
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color="D9E2F3", end_color="D9E2F3", fill_type="solid")
    
        # Natijalarni yozish
        row = 13
        for attempt in attempts.order_by('-percentage'):
            student_name = f"{attempt.student.first_name} {attempt.student.last_name}"
            if not student_name.strip():
                student_name = attempt.student.username
            
            ws.cell(row=row, column=1, value=student_name)
            ws.cell(row=row, column=2, value=attempt.test.title)
            ws.cell(row=row, column=3, value=attempt.score)
            ws.cell(row=row, column=4, value=f"{attempt.percentage:.1f}%")
            ws.cell(row=row, column=5, value=str(attempt.time_taken))
            ws.cell(row=row, column=6, value=attempt.finished_at.strftime('%Y-%m-%d %H:%M:%S'))
            
            # Ball bo'yicha rang berish
            if attempt.percentage >= 81:
                fill_color = "C6EFCE"  # Yashil
            elif attempt.percentage >= 61:
                fill_color = "FFEB9C"  # Sariq
            elif attempt.percentage >= 31:
                fill_color = "FFC7CE"  # Qizil
            else:
                fill_color = "FFC7CE"  # Qizil
            
            for col in range(1, 7):
                ws.cell(row=row, column=col).fill = PatternFill(start_color=fill_color, end_color=fill_color, fill_type="solid")
            
            row += 1
    
        # Ustun kengliklarini sozlash
        ws.column_dimensions['A'].width = 25
        ws.column_dimensions['B'].width = 30
        ws.column_dimensions['C'].width = 10
        ws.column_dimensions['D'].width = 10
        ws.column_dimensions['E'].width = 15
        ws.column_dimensions['F'].width = 20
        
        # Response yaratish
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{grade}-sinf_natijalari.xlsx"'
        
        # Excel faylni saqlash
        wb.save(response)
        
        return response
        
    except Exception as e:
        print(f"Export error: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': f'Export xatolik yuz berdi: {str(e)}'}, status=500)

@login_required
def export_all_results_view(request):
    """Barcha sinflar va fanlar bo'yicha natijalarni Excel formatida export qilish"""
    if request.user.role not in ['admin', 'teacher']:
        return JsonResponse({'error': 'Faqat admin va o\'qituvchilar kirishi mumkin'}, status=403)
    
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
        from openpyxl.utils import get_column_letter
        from django.db.models import Avg, Count, Max, Min
        
        # Yangi workbook yaratish
        wb = Workbook()
        
        # Barcha sinflar uchun umumiy statistikalar
        ws_summary = wb.active
        ws_summary.title = "Umumiy Statistika"
        
        # Header qo'shish
        headers = ['Sinf', 'Fan', 'Testlar Soni', 'Jami Urinishlar', 'O\'rtacha Foiz', 'Eng Yaxshi Natija', 'Eng Past Natija']
        for col, header in enumerate(headers, 1):
            cell = ws_summary.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
            cell.alignment = Alignment(horizontal="center")
        
        row = 2
        
        # Har bir sinf uchun
        for grade in range(1, 12):  # 1-11 sinflar
            # Har bir fan uchun
            subjects = ['Matematika', 'Fizika', 'Kimyo', 'Biologiya', 'Ona tili', 'Ingliz tili', 'Tarix', 'Geografiya']
            
            for subject in subjects:
                # Bu sinf va fan uchun testlar
                tests = Test.objects.filter(grade=grade, subject=subject)
                
                if tests.exists():
                    # Bu sinf va fan uchun barcha urinishlar
                    attempts = TestAttempt.objects.filter(
                        test__in=tests,
                        completed_at__isnull=False
                    ).select_related('student', 'test')
                    
                    if attempts.exists():
                        # Statistikalarni hisoblash
                        total_tests = tests.count()
                        total_attempts = attempts.count()
                        avg_percentage = attempts.aggregate(avg=Avg('percentage'))['avg'] or 0
                        max_percentage = attempts.aggregate(max=Max('percentage'))['max'] or 0
                        min_percentage = attempts.aggregate(min=Min('percentage'))['min'] or 0
                        
                        # Ma'lumotlarni qo'shish
                        ws_summary.cell(row=row, column=1, value=f"{grade}-sinf")
                        ws_summary.cell(row=row, column=2, value=subject)
                        ws_summary.cell(row=row, column=3, value=total_tests)
                        ws_summary.cell(row=row, column=4, value=total_attempts)
                        ws_summary.cell(row=row, column=5, value=f"{avg_percentage:.1f}%")
                        ws_summary.cell(row=row, column=6, value=f"{max_percentage:.1f}%")
                        ws_summary.cell(row=row, column=7, value=f"{min_percentage:.1f}%")
                        
                        row += 1
        
        # Ustun kengliklarini sozlash
        for col in range(1, 8):
            ws_summary.column_dimensions[get_column_letter(col)].width = 15
        
        # Har bir sinf uchun alohida worksheet yaratish
        for grade in range(1, 12):
            ws = wb.create_sheet(title=f"{grade}-sinf")
            
            # Header qo'shish
            headers = ['O\'quvchi', 'Fan', 'Test', 'Foiz', 'Ball', 'Urinishlar Soni', 'Oxirgi Urinish']
            for col, header in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col, value=header)
                cell.font = Font(bold=True, color="FFFFFF")
                cell.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
                cell.alignment = Alignment(horizontal="center")
            
            row = 2
            
            # Bu sinf uchun barcha testlar
            tests = Test.objects.filter(grade=grade)
            
            for test in tests:
                # Bu test uchun barcha urinishlar
                attempts = TestAttempt.objects.filter(
                    test=test,
                    completed_at__isnull=False
                ).select_related('student').order_by('-completed_at')
                
                for attempt in attempts:
                    student_name = f"{attempt.student.first_name} {attempt.student.last_name}"
                    if not student_name.strip():
                        student_name = attempt.student.username
                    
                    # Eng oxirgi urinishni topish
                    latest_attempt = TestAttempt.objects.filter(
                        student=attempt.student,
                        test=test,
                        completed_at__isnull=False
                    ).order_by('-completed_at').first()
                    
                    ws.cell(row=row, column=1, value=student_name)
                    ws.cell(row=row, column=2, value=test.subject)
                    ws.cell(row=row, column=3, value=test.title)
                    ws.cell(row=row, column=4, value=attempt.percentage)
                    ws.cell(row=row, column=5, value=attempt.score)
                    ws.cell(row=row, column=6, value=attempt.attempt_number)
                    ws.cell(row=row, column=7, value=attempt.completed_at.strftime('%d.%m.%Y %H:%M') if attempt.completed_at else '')
                    
                    # Rang berish
                    if attempt.percentage >= 81:
                        fill_color = "C6EFCE"  # Yashil
                    elif attempt.percentage >= 61:
                        fill_color = "FFEB9C"  # Sariq
                    elif attempt.percentage >= 31:
                        fill_color = "BDD7EE"  # Ko'k
                    else:
                        fill_color = "FFC7CE"  # Qizil
                    
                    for col in range(1, 8):
                        ws.cell(row=row, column=col).fill = PatternFill(start_color=fill_color, end_color=fill_color, fill_type="solid")
                    
                    row += 1
            
            # Ustun kengliklarini sozlash
            ws.column_dimensions['A'].width = 25
            ws.column_dimensions['B'].width = 10
            ws.column_dimensions['C'].width = 30
            ws.column_dimensions['D'].width = 10
            ws.column_dimensions['E'].width = 10
            ws.column_dimensions['F'].width = 10
            ws.column_dimensions['G'].width = 12
            ws.column_dimensions['H'].width = 18
        
        # Agar hech qanday fan topilmasa
        if len(wb.sheetnames) == 0:
            ws = wb.create_sheet(title="Ma'lumot yo'q")
            ws['A1'] = "Hozircha natijalar mavjud emas"
            ws['A1'].font = Font(bold=True, size=14)
        
        # Response yaratish
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="barcha_sinflar_natijalari.xlsx"'
        
        # Excel faylni saqlash
        wb.save(response)
        
        return response
        
    except Exception as e:
        print(f"Export all results error: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': f'Export xatolik yuz berdi: {str(e)}'}, status=500)


@login_required
@user_passes_test(lambda u: u.role in ['teacher', 'admin'])
def export_subject_results_view(request):
    """Fanlar bo'yicha natijalarni Excel faylga export qilish - har bir fan alohida sheet"""
    if not OPENPYXL_AVAILABLE:
        return JsonResponse({'error': 'Excel export funksiyasi mavjud emas.'}, status=500)
    
    try:
        from openpyxl.utils import get_column_letter
        from openpyxl.styles import Alignment
        
        # Excel workbook yaratish
        wb = Workbook()
        wb.remove(wb.active)  # Default sheet'ni o'chirish
        
        # Barcha fanlarni olish
        subjects = Test.objects.values_list('subject', flat=True).distinct().order_by('subject')
        
        print(f"Found subjects: {list(subjects)}")
        
        for subject in subjects:
            if not subject:
                continue
                
            print(f"\nProcessing subject: {subject}")
            
            # Sheet yaratish
            ws = wb.create_sheet(title=subject[:31])  # Excel sheet name limit: 31 characters
            
            # Header qo'shish
            ws['A1'] = f"{subject} - Barcha Natijalar"
            ws['A1'].font = Font(bold=True, size=16, color="FFFFFF")
            ws['A1'].fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
            ws.merge_cells('A1:H1')
            ws['A1'].alignment = Alignment(horizontal="center")
            
            # Umumiy statistika
            tests = Test.objects.filter(subject=subject, is_active=True)
            total_tests = tests.count()
            
            attempts = TestAttempt.objects.filter(
                test__subject=subject,
                is_completed=True
            ).select_related('student', 'test')
            
            total_attempts = attempts.count()
            
            if total_attempts > 0:
                avg_percentage = attempts.aggregate(avg=Avg('percentage'))['avg'] or 0
                max_percentage = attempts.aggregate(max=Max('percentage'))['max'] or 0
                min_percentage = attempts.aggregate(min=Min('percentage'))['min'] or 0
            else:
                avg_percentage = max_percentage = min_percentage = 0
            
            # Statistika qo'shish
            ws['A3'] = "Umumiy Ma'lumotlar:"
            ws['A3'].font = Font(bold=True, size=12)
    
            ws['A4'] = f"Jami Testlar: {total_tests}"
            ws['A5'] = f"Jami Urinishlar: {total_attempts}"
            ws['A6'] = f"O'rtacha Foiz: {avg_percentage:.1f}%"
            ws['A7'] = f"Eng Yuqori Foiz: {max_percentage:.1f}%"
            ws['A8'] = f"Eng Past Foiz: {min_percentage:.1f}%"
            
            # Natijalar jadvali header
            ws['A10'] = "Barcha Natijalar:"
            ws['A10'].font = Font(bold=True, size=12)
            
            headers = ['O\'quvchi', 'Sinf', 'Test Nomi', 'Ball', 'Maksimal', 'Foiz', 'Vaqt', 'Sana']
            for col, header in enumerate(headers, 1):
                cell = ws.cell(row=11, column=col, value=header)
                cell.font = Font(bold=True, color="FFFFFF")
                cell.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
                cell.alignment = Alignment(horizontal="center")
            
            # Natijalarni yozish
            row = 12
            for attempt in attempts.order_by('-percentage', '-finished_at'):
                student_name = f"{attempt.student.first_name} {attempt.student.last_name}".strip()
                if not student_name:
                    student_name = attempt.student.username
                
                ws.cell(row=row, column=1, value=student_name)
                ws.cell(row=row, column=2, value=attempt.student.grade or '')
                ws.cell(row=row, column=3, value=attempt.test.title)
                ws.cell(row=row, column=4, value=attempt.score)
                ws.cell(row=row, column=5, value=attempt.total_points)
                ws.cell(row=row, column=6, value=f"{attempt.percentage:.1f}%")
                ws.cell(row=row, column=7, value=str(attempt.time_taken) if attempt.time_taken else '-')
                ws.cell(row=row, column=8, value=attempt.finished_at.strftime('%d.%m.%Y %H:%M') if attempt.finished_at else '-')
                
                # Rangli formatlar
                if attempt.percentage >= 81:
                    fill_color = "C6EFCE"  # Yashil
                elif attempt.percentage >= 61:
                    fill_color = "FFEB9C"  # Sariq
                elif attempt.percentage >= 31:
                    fill_color = "BDD7EE"  # Ko'k
                else:
                    fill_color = "FFC7CE"  # Qizil
                
                for col in range(1, 9):
                    ws.cell(row=row, column=col).fill = PatternFill(start_color=fill_color, end_color=fill_color, fill_type="solid")
                
                row += 1
            
            # Ustun kengliklarini sozlash
            ws.column_dimensions['A'].width = 25
            ws.column_dimensions['B'].width = 10
            ws.column_dimensions['C'].width = 35
            ws.column_dimensions['D'].width = 10
            ws.column_dimensions['E'].width = 10
            ws.column_dimensions['F'].width = 10
            ws.column_dimensions['G'].width = 12
            ws.column_dimensions['H'].width = 18
        
        # Agar hech qanday fan topilmasa
        if len(wb.sheetnames) == 0:
            ws = wb.create_sheet(title="Ma'lumot yo'q")
            ws['A1'] = "Hozircha natijalar mavjud emas"
            ws['A1'].font = Font(bold=True, size=14)
        
        # Response yaratish
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="fanlar_boyicha_natijalar.xlsx"'
        
        # Excel faylni saqlash
        wb.save(response)
        
        print(f"Excel file created successfully with {len(wb.sheetnames)} sheets")
        return response
        
    except Exception as e:
        print(f"Export subject results error: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': f'Export xatolik yuz berdi: {str(e)}'}, status=500)

@login_required
@user_passes_test(lambda u: u.role == 'admin')
@require_http_methods(["POST"])
def delete_all_tests_view(request):
    """Barcha testlarni o'chirish (faqat admin) - O'quvchilar saqlanadi"""
    try:
        # Hisob-kitob
        total_tests = Test.objects.count()
        total_questions = Question.objects.count()
        total_choices = Choice.objects.count()
        total_attempts = TestAttempt.objects.count()
        total_answers = Answer.objects.count()
        total_results = TestResult.objects.count()
        total_retake_requests = TestRetakeRequest.objects.count()
        total_users = User.objects.count()
        
        # Barcha testlarni o'chirish (CASCADE bo'lgani uchun bog'liq obyektlar avtomatik o'chadi)
        deleted_count = Test.objects.all().delete()[0]
        
        # Tekshirish
        remaining_users = User.objects.count()
        
        return JsonResponse({
            'success': True,
            'message': f'Barcha testlar muvaffaqiyatli o\'chirildi!',
            'deleted': {
                'tests': total_tests,
                'questions': total_questions,
                'choices': total_choices,
                'attempts': total_attempts,
                'answers': total_answers,
                'results': total_results,
                'retake_requests': total_retake_requests,
                'total_deleted': deleted_count
            },
            'preserved': {
                'users': total_users,
                'users_after': remaining_users
            }
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'error': f'Testlarni o\'chirishda xatolik: {str(e)}'
        }, status=500)
