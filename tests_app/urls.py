from django.urls import path
from . import views
from . import monitoring_views

app_name = 'tests'

urlpatterns = [
    path('', views.test_list_view, name='tests'),
    path('create/', views.create_test_view, name='create_test'),
    path('<int:test_id>/edit/', views.edit_test_view, name='edit_test'),
    path('<int:test_id>/delete/', views.delete_test_view, name='delete_test'),
    path('<int:test_id>/take/', views.take_test_view, name='take_test'),
    path('attempt/<int:attempt_id>/submit-answer/', views.submit_answer, name='submit_answer'),
    path('attempt/<int:attempt_id>/finish/', views.finish_test, name='finish_test'),
    path('<int:test_id>/results/', views.test_results_view, name='test_results'),
    path('<int:test_id>/info/', views.test_info_view, name='test_info'),
    path('<int:test_id>/export/', views.export_results, name='export_results'),
    path('<int:test_id>/upload-questions/', views.upload_questions, name='upload_questions'),
    path('all-results/', views.all_results_view, name='all_results'),
    path('<int:test_id>/request-retake/', views.request_retake_view, name='request_retake'),
    path('retake-requests/', views.retake_requests_view, name='retake_requests'),
    path('retake-requests/<int:request_id>/handle/', views.handle_retake_request_view, name='handle_retake_request'),
    path('student-management/', views.student_test_management, name='student_test_management'),
    path('<int:test_id>/open-for-student/<int:student_id>/', views.open_test_for_student, name='open_test_for_student'),
    path('admin/teacher-tests/', views.admin_teacher_tests, name='admin_teacher_tests'),
    path('overall-results/', views.student_overall_results_view, name='overall_results'),
    path('export-all-results/', views.export_all_results_view, name='export_all_results'),
    path('student-export-results/', views.student_export_results_view, name='student_export_results'),
    path('test-api/', views.test_api_view, name='test_api'),
    path('export-all-students/', views.export_all_students_results, name='export_all_students'),
    # Real-time monitoring
    path('<int:test_id>/active-sessions/', monitoring_views.active_test_sessions_view, name='active_sessions'),
    path('attempt/<int:attempt_id>/terminate/', monitoring_views.terminate_test_attempt_view, name='terminate_attempt'),
    path('attempt/<int:attempt_id>/detail/', monitoring_views.student_test_detail_view, name='student_test_detail'),
    path('attempt/<int:attempt_id>/control-time/', monitoring_views.control_time_view, name='control_time'),
    path('students-monitoring/', monitoring_views.students_monitoring_view, name='students_monitoring'),
    path('export-cross-grade-results/', monitoring_views.export_cross_grade_results, name='export_cross_grade_results'),
    path('export-subject-results/', views.export_subject_results_view, name='export_subject_results'),
    path('delete-all-tests/', views.delete_all_tests_view, name='delete_all_tests'),
]