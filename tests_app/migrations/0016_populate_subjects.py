# Generated manually - boshlang'ich fanlarni qo'shish

from django.db import migrations


def create_initial_subjects(apps, schema_editor):
    Subject = apps.get_model('tests_app', 'Subject')
    initial = [
        {'name': 'Fizika', 'slug': 'fizika', 'icon': 'fa-atom', 'order': 1},
        {'name': 'Ingliz tili', 'slug': 'ingliz-tili', 'icon': 'fa-language', 'order': 2},
        {'name': 'Matematika', 'slug': 'matematika', 'icon': 'fa-calculator', 'order': 3},
        {'name': 'Informatika', 'slug': 'informatika', 'icon': 'fa-laptop-code', 'order': 4},
    ]
    for s in initial:
        Subject.objects.get_or_create(slug=s['slug'], defaults=s)


def reverse_func(apps, schema_editor):
    Subject = apps.get_model('tests_app', 'Subject')
    Subject.objects.filter(slug__in=['fizika', 'ingliz-tili', 'matematika', 'informatika']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tests_app', '0015_add_subject_model'),
    ]

    operations = [
        migrations.RunPython(create_initial_subjects, reverse_func),
    ]
