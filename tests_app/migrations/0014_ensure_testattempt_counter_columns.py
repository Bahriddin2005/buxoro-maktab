# Migration to fix: no such column: tests_app_testattempt.correct_answers
# Adds columns to DB if they don't exist (model already has them from 0012)

from django.db import migrations


def add_columns_if_missing(apps, schema_editor):
    """Add correct_answers, incorrect_answers, unanswered to tests_app_testattempt if missing"""
    db_vendor = schema_editor.connection.vendor
    with schema_editor.connection.cursor() as cursor:
        if db_vendor == 'sqlite':
            cursor.execute("PRAGMA table_info(tests_app_testattempt)")
            columns = [row[1] for row in cursor.fetchall()]
            table = "tests_app_testattempt"
            col_type = "INTEGER NOT NULL DEFAULT 0"
        else:
            cursor.execute("""
                SELECT column_name FROM information_schema.columns
                WHERE table_name = 'tests_app_testattempt'
            """)
            columns = [row[0] for row in cursor.fetchall()]
            table = "tests_app_testattempt"
            col_type = "INTEGER NOT NULL DEFAULT 0"

        for col in ['correct_answers', 'incorrect_answers', 'unanswered']:
            if col not in columns:
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN {col} {col_type}")


def reverse_add_columns(apps, schema_editor):
    """Reverse: SQLite doesn't support easy DROP COLUMN, so we no-op"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("tests_app", "0013_question_default_single_choice"),
    ]

    operations = [
        migrations.RunPython(add_columns_if_missing, reverse_add_columns),
    ]
