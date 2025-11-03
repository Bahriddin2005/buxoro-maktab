from django.core.management.base import BaseCommand
from tests_app.models import Test, Question, Choice, TestAttempt, Answer, TestResult, TestRetakeRequest

class Command(BaseCommand):
    help = 'Barcha testlarni o\'chirish (CASCADE delete)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='O\'chirishni tasdiqlash',
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(self.style.WARNING('DIQQAT! Bu buyruq BARCHA testlarni o\'chiradi!'))
            self.stdout.write(self.style.WARNING('O\'chirish uchun --confirm flag qo\'shing:'))
            self.stdout.write(self.style.WARNING('python manage.py delete_all_tests --confirm'))
            return

        # Statistika olish
        tests_count = Test.objects.count()
        questions_count = Question.objects.count()
        choices_count = Choice.objects.count()
        attempts_count = TestAttempt.objects.count()
        answers_count = Answer.objects.count()
        results_count = TestResult.objects.count()
        retake_requests_count = TestRetakeRequest.objects.count()

        self.stdout.write('=' * 70)
        self.stdout.write(self.style.WARNING('O\'CHIRILAYOTGAN MA\'LUMOTLAR:'))
        self.stdout.write('=' * 70)
        self.stdout.write(f'Testlar: {tests_count} ta')
        self.stdout.write(f'Savollar: {questions_count} ta')
        self.stdout.write(f'Variantlar: {choices_count} ta')
        self.stdout.write(f'Test Attempts: {attempts_count} ta')
        self.stdout.write(f'Javoblar: {answers_count} ta')
        self.stdout.write(f'Natijalar: {results_count} ta')
        self.stdout.write(f'Retake Requests: {retake_requests_count} ta')
        self.stdout.write('=' * 70)

        # Tasdiqlash
        confirm = input('Rostdan ham o\'chirmoqchimisiz? (yes/no): ')
        if confirm.lower() != 'yes':
            self.stdout.write(self.style.WARNING('O\'chirish bekor qilindi.'))
            return

        # O'chirish (CASCADE)
        self.stdout.write(self.style.WARNING('O\'chirish boshlandi...'))
        
        # Test.objects.all().delete() CASCADE orqali barcha bog'liq ma'lumotlarni o'chiradi
        deleted_count, deleted_details = Test.objects.all().delete()

        self.stdout.write('=' * 70)
        self.stdout.write(self.style.SUCCESS('O\'CHIRILDI!'))
        self.stdout.write('=' * 70)
        self.stdout.write(f'Jami o\'chirilgan: {deleted_count} ta yozuv')
        self.stdout.write('\nTafsilotlar:')
        for model, count in deleted_details.items():
            self.stdout.write(f'  {model}: {count} ta')
        self.stdout.write('=' * 70)
        self.stdout.write(self.style.SUCCESS('✅ Barcha testlar o\'chirildi!'))

