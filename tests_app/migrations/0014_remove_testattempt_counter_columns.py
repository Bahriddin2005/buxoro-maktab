# Fix: no such column: tests_app_testattempt.correct_answers
# Bu ustunlar faqat TestResult da saqlanadi. TestAttempt modelidan olib tashlanadi.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tests_app", "0013_question_default_single_choice"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RemoveField(model_name="testattempt", name="correct_answers"),
                migrations.RemoveField(model_name="testattempt", name="incorrect_answers"),
                migrations.RemoveField(model_name="testattempt", name="unanswered"),
            ],
            database_operations=[],  # DB ga o'zgartirish yo'q
        ),
    ]
