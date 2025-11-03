#!/usr/bin/env python
"""
Barcha fanlardan testlar va savollar yaratish
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mytest.settings')
django.setup()

from accounts.models import User
from tests_app.models import Test, Question, Choice
from django.utils import timezone

def create_tests():
    """10 ta fandan har biridan 30 savollik testlar yaratish"""
    
    # Admin yoki teacher topish
    try:
        admin = User.objects.filter(role='admin').first()
        if not admin:
            print("Admin topilmadi! Avval admin yarating.")
            return
    except Exception as e:
        print(f"Xato: {e}")
        return
    
    # Fanlar ro'yxati
    subjects = [
        "Informatika",
        "Matematika",
        "Ona tili",
        "Adabiyot",
        "Fizika",
        "Tabiiy fan",
        "Geografiya",
        "Ingliz tili",
        "Rus tili",
        "Tarix"
    ]
    
    # Har bir fan uchun
    for subject in subjects:
        print(f"\n{'='*50}")
        print(f"📚 {subject} testlarini yaratish...")
        print(f"{'='*50}")
        
        # Har bir sinf uchun (5-11 sinf)
        for grade in range(5, 12):
            test_title = f"{subject} - {grade}-sinf Test"
            
            # Test mavjudligini tekshirish
            if Test.objects.filter(title=test_title, subject=subject, grade=grade).exists():
                print(f"  ⏭️  {test_title} allaqachon mavjud")
                continue
            
            # Test yaratish
            test = Test.objects.create(
                title=test_title,
                description=f"{subject} fanidan {grade}-sinf uchun 30 savollik test. Barcha mavzularni qamrab oladi.",
                subject=subject,
                grade=grade,
                created_by=admin,
                time_limit=45,  # 45 daqiqa
                is_active=True,
                max_attempts=3,
                show_results=True,
                shuffle_questions=True
            )
            
            print(f"  ✅ Test yaratildi: {test_title}")
            
            # 30 ta savol yaratish
            questions_data = get_questions_for_subject(subject, grade)
            
            for i, q_data in enumerate(questions_data[:30], 1):
                question = Question.objects.create(
                    test=test,
                    question_text=q_data['text'],
                    question_type='single_choice',
                    points=1.0,
                    order=i,
                    explanation=q_data.get('explanation', '')
                )
                
                # Javob variantlarini yaratish
                for choice_text, is_correct in q_data['choices']:
                    Choice.objects.create(
                        question=question,
                        choice_text=choice_text,
                        is_correct=is_correct
                    )
            
            print(f"  ✅ 30 ta savol qo'shildi")
    
    print(f"\n{'='*50}")
    print("✅ BARCHA TESTLAR YARATILDI!")
    print(f"{'='*50}")
    print(f"📊 Jami: {len(subjects)} fan x 7 sinf = {len(subjects) * 7} ta test")
    print(f"📝 Har birida: 30 ta savol")
    print(f"📈 Jami savollar: {len(subjects) * 7 * 30} ta")


def get_questions_for_subject(subject, grade):
    """Har bir fan uchun savollar"""
    
    questions = {
        "Informatika": [
            {
                "text": "Kompyuterning asosiy xotirasi qanday nomlanadi?",
                "choices": [
                    ("RAM", True),
                    ("ROM", False),
                    ("CPU", False),
                    ("Hard Disk", False)
                ],
                "explanation": "RAM (Random Access Memory) - kompyuterning asosiy xotirasi."
            },
            {
                "text": "Qaysi qurilma ma'lumotlarni doimiy saqlaydi?",
                "choices": [
                    ("Hard Disk", True),
                    ("RAM", False),
                    ("Cache", False),
                    ("Register", False)
                ]
            },
            {
                "text": "Python dasturlash tilida o'zgaruvchi e'lon qilish uchun nima ishlatiladi?",
                "choices": [
                    ("Faqat nom yozish kifoya", True),
                    ("var kalit so'zi", False),
                    ("let kalit so'zi", False),
                    ("dim kalit so'zi", False)
                ]
            },
            {
                "text": "Internet tarmog'ida ma'lumot uzatish protokoli?",
                "choices": [
                    ("TCP/IP", True),
                    ("HTTP", False),
                    ("FTP", False),
                    ("SMTP", False)
                ]
            },
            {
                "text": "1 Byte necha bitga teng?",
                "choices": [
                    ("8 bit", True),
                    ("4 bit", False),
                    ("16 bit", False),
                    ("32 bit", False)
                ]
            },
            {
                "text": "HTML nima?",
                "choices": [
                    ("HyperText Markup Language", True),
                    ("HyperText Machine Language", False),
                    ("HighText Markup Language", False),
                    ("Home Tool Markup Language", False)
                ]
            },
            {
                "text": "CPU ning vazifasi nima?",
                "choices": [
                    ("Hisoblashlarni bajarish", True),
                    ("Ma'lumot saqlash", False),
                    ("Ekranga chiqarish", False),
                    ("Tovush chiqarish", False)
                ]
            },
            {
                "text": "Qaysi dastur Microsoft Office'ga kirmaydi?",
                "choices": [
                    ("Adobe Photoshop", True),
                    ("Microsoft Word", False),
                    ("Microsoft Excel", False),
                    ("Microsoft PowerPoint", False)
                ]
            },
            {
                "text": "IP address nima uchun ishlatiladi?",
                "choices": [
                    ("Tarmoqda qurilmani identifikatsiya qilish", True),
                    ("Ma'lumot shifrlash", False),
                    ("Parol saqlash", False),
                    ("Fayl yuklash", False)
                ]
            },
            {
                "text": "SQL nima?",
                "choices": [
                    ("Ma'lumotlar bazasi boshqaruv tili", True),
                    ("Dasturlash tili", False),
                    ("Operatsion tizim", False),
                    ("Grafik dastur", False)
                ]
            },
            # Yana 20 ta savol...
            {
                "text": "Windows operatsion tizimini ishlab chiqargan kompaniya?",
                "choices": [("Microsoft", True), ("Apple", False), ("Google", False), ("IBM", False)]
            },
            {
                "text": "WWW ning to'liq shakli?",
                "choices": [("World Wide Web", True), ("World Web Wide", False), ("Wide World Web", False), ("Web World Wide", False)]
            },
            {
                "text": "Antivirusning vazifasi nima?",
                "choices": [("Viruslardan himoya qilish", True), ("Internet tezlashtrish", False), ("Fayl siqish", False), ("Rasm tahrirlash", False)]
            },
            {
                "text": "E-mail nima?",
                "choices": [("Elektron pochta", True), ("Elektron kitob", False), ("Elektron jurnal", False), ("Elektron daftar", False)]
            },
            {
                "text": "URL nima?",
                "choices": [("Veb-manzil", True), ("Dastur", False), ("Fayl", False), ("Papka", False)]
            },
            {
                "text": "Keyboard qanday qurilma?",
                "choices": [("Kiritish qurilmasi", True), ("Chiqarish qurilmasi", False), ("Saqlash qurilmasi", False), ("Ishlov berish qurilmasi", False)]
            },
            {
                "text": "Monitor qanday qurilma?",
                "choices": [("Chiqarish qurilmasi", True), ("Kiritish qurilmasi", False), ("Saqlash qurilmasi", False), ("Ishlov berish qurilmasi", False)]
            },
            {
                "text": "USB nima?",
                "choices": [("Universal Serial Bus", True), ("United System Bus", False), ("Universal System Base", False), ("United Serial Base", False)]
            },
            {
                "text": "Browser nima uchun ishlatiladi?",
                "choices": [("Internet saytlarni ko'rish", True), ("Rasm tahrirlash", False), ("Musiqa tinglash", False), ("O'yin o'ynash", False)]
            },
            {
                "text": "PDF fayli qanday dasturda ochiladi?",
                "choices": [("Adobe Reader", True), ("Microsoft Word", False), ("Notepad", False), ("Paint", False)]
            },
            {
                "text": "Cloud storage nima?",
                "choices": [("Bulutli saqlash xizmati", True), ("Antivirus", False), ("O'yin", False), ("Brauzyer", False)]
            },
            {
                "text": "Copyright nima?",
                "choices": [("Mualliflik huquqi", True), ("Virus", False), ("Dastur", False), ("Fayl", False)]
            },
            {
                "text": "Firewall vazifasi?",
                "choices": [("Tarmoq xavfsizligini ta'minlash", True), ("Fayl o'chirish", False), ("Internet tezlashtirish", False), ("Rasm tahrirlash", False)]
            },
            {
                "text": "Backup nima?",
                "choices": [("Zaxira nusxa", True), ("Virusli fayl", False), ("O'yin", False), ("Dastur", False)]
            },
            {
                "text": "Wi-Fi nima?",
                "choices": [("Simsiz internet", True), ("Kabel internet", False), ("Telefon", False), ("Kompyuter", False)]
            },
            {
                "text": "Qaysi fayl formati rasm uchun?",
                "choices": [("JPG", True), ("MP3", False), ("AVI", False), ("TXT", False)]
            },
            {
                "text": "Qaysi fayl formati video uchun?",
                "choices": [("MP4", True), ("JPG", False), ("DOC", False), ("PDF", False)]
            },
            {
                "text": "Ctrl+C klavish kombinatsiyasi nima qiladi?",
                "choices": [("Nusxalash (Copy)", True), ("Qirqish (Cut)", False), ("Yopish (Close)", False), ("Saqlash (Save)", False)]
            },
            {
                "text": "Ctrl+V klavish kombinatsiyasi nima qiladi?",
                "choices": [("Qo'yish (Paste)", True), ("Nusxalash", False), ("Yopish", False), ("Ochish", False)]
            },
            {
                "text": "Kompyuter viruslari orqali tarqaladi?",
                "choices": [("Internet, USB, Email", True), ("Faqat Internet", False), ("Faqat USB", False), ("Tarqalmaydi", False)]
            },
        ],
        
        "Matematika": [
            {
                "text": "2 + 2 = ?",
                "choices": [("4", True), ("3", False), ("5", False), ("6", False)]
            },
            {
                "text": "10 - 3 = ?",
                "choices": [("7", True), ("6", False), ("8", False), ("5", False)]
            },
            {
                "text": "5 × 6 = ?",
                "choices": [("30", True), ("25", False), ("35", False), ("40", False)]
            },
            {
                "text": "20 ÷ 4 = ?",
                "choices": [("5", True), ("4", False), ("6", False), ("10", False)]
            },
            {
                "text": "3² = ?",
                "choices": [("9", True), ("6", False), ("12", False), ("27", False)]
            },
            {
                "text": "√16 = ?",
                "choices": [("4", True), ("2", False), ("8", False), ("16", False)]
            },
            {
                "text": "15% dan 100 = ?",
                "choices": [("15", True), ("10", False), ("20", False), ("25", False)]
            },
            {
                "text": "Agar x + 5 = 10 bo'lsa, x = ?",
                "choices": [("5", True), ("10", False), ("15", False), ("2", False)]
            },
            {
                "text": "To'g'ri burchak necha gradus?",
                "choices": [("90°", True), ("180°", False), ("45°", False), ("60°", False)]
            },
            {
                "text": "Uchburchakning ichki burchaklari yig'indisi?",
                "choices": [("180°", True), ("90°", False), ("360°", False), ("270°", False)]
            },
            {
                "text": "1/2 + 1/4 = ?",
                "choices": [("3/4", True), ("1/6", False), ("2/6", False), ("1/3", False)]
            },
            {
                "text": "0.5 + 0.3 = ?",
                "choices": [("0.8", True), ("0.6", False), ("0.7", False), ("0.9", False)]
            },
            {
                "text": "12 ning 1/3 qismi = ?",
                "choices": [("4", True), ("3", False), ("6", False), ("2", False)]
            },
            {
                "text": "Kvadratning barcha tomonlari?",
                "choices": [("Teng", True), ("Turli", False), ("Parallel", False), ("Perpendikular", False)]
            },
            {
                "text": "Pi (π) taxminan qanchaga teng?",
                "choices": [("3.14", True), ("2.14", False), ("4.14", False), ("3.41", False)]
            },
            {
                "text": "100 ning 50% i = ?",
                "choices": [("50", True), ("25", False), ("75", False), ("100", False)]
            },
            {
                "text": "Agar 2x = 10 bo'lsa, x = ?",
                "choices": [("5", True), ("10", False), ("20", False), ("2", False)]
            },
            {
                "text": "Doiraning radiusi 5 cm bo'lsa, diametri?",
                "choices": [("10 cm", True), ("5 cm", False), ("15 cm", False), ("20 cm", False)]
            },
            {
                "text": "1 metr necha santimetrga teng?",
                "choices": [("100 sm", True), ("10 sm", False), ("1000 sm", False), ("50 sm", False)]
            },
            {
                "text": "24 ning bo'luvchilari nechta?",
                "choices": [("8 ta", True), ("6 ta", False), ("4 ta", False), ("10 ta", False)]
            },
            {
                "text": "Tub son qaysi?",
                "choices": [("7", True), ("4", False), ("6", False), ("8", False)]
            },
            {
                "text": "(-5) + 8 = ?",
                "choices": [("3", True), ("-3", False), ("13", False), ("-13", False)]
            },
            {
                "text": "3 × (-4) = ?",
                "choices": [("-12", True), ("12", False), ("-7", False), ("7", False)]
            },
            {
                "text": "Parallelogram deb nimaga aytiladi?",
                "choices": [("Qarama-qarshi tomonlari parallel to'rtburchak", True), ("Barcha tomonlari teng shakl", False), ("Uchburchak", False), ("Doira", False)]
            },
            {
                "text": "1 km necha metrga teng?",
                "choices": [("1000 m", True), ("100 m", False), ("10 m", False), ("10000 m", False)]
            },
            {
                "text": "0.25 ni kasr ko'rinishida yozing:",
                "choices": [("1/4", True), ("1/2", False), ("1/3", False), ("1/5", False)]
            },
            {
                "text": "Agar a = 3, b = 4 bo'lsa, a² + b² = ?",
                "choices": [("25", True), ("7", False), ("12", False), ("49", False)]
            },
            {
                "text": "Aylananing uzunligi formulasi?",
                "choices": [("C = 2πr", True), ("C = πr²", False), ("C = πr", False), ("C = 2r", False)]
            },
            {
                "text": "Agar x/5 = 3 bo'lsa, x = ?",
                "choices": [("15", True), ("8", False), ("5/3", False), ("5", False)]
            },
            {
                "text": "10! (faktorial) ning oxirida nechta 0 bor?",
                "choices": [("2 ta", True), ("1 ta", False), ("3 ta", False), ("0 ta", False)]
            },
        ],
        
        "Ona tili": [
            {
                "text": "O'zbek tilida nechta unli tovush bor?",
                "choices": [("6 ta", True), ("5 ta", False), ("7 ta", False), ("8 ta", False)]
            },
            {
                "text": "Fe'l so'z turkumi nimani bildiradi?",
                "choices": [("Harakat", True), ("Narsa", False), ("Belgi", False), ("Son", False)]
            },
            {
                "text": "Ot so'z turkumi nimani bildiradi?",
                "choices": [("Narsa-buyum", True), ("Harakat", False), ("Belgi", False), ("Miqdor", False)]
            },
            {
                "text": "Sifat so'z turkumi nimani bildiradi?",
                "choices": [("Belgi-xususiyat", True), ("Narsa", False), ("Harakat", False), ("Son", False)]
            },
            {
                "text": "O'zbek alifbosida nechta harf bor?",
                "choices": [("29 ta", True), ("28 ta", False), ("30 ta", False), ("26 ta", False)]
            },
            {
                "text": "Gap nima?",
                "choices": [("Tugal fikr bildiruvchi so'zlar birikmas", True), ("Bitta so'z", False), ("Ikki so'z", False), ("Harf", False)]
            },
            {
                "text": "Kesim gapning qaysi bo'lagi?",
                "choices": [("Bosh bo'lak", True), ("Ikkinchi darajali", False), ("Aniqlovchi", False), ("To'ldiruvchi", False)]
            },
            {
                "text": "Ega gapning qaysi bo'lagi?",
                "choices": [("Bosh bo'lak", True), ("Ikkinchi darajali", False), ("Hol", False), ("Aniqlovchi", False)]
            },
            {
                "text": "Nuqta belgisi qachon qo'yiladi?",
                "choices": [("Gap oxirida", True), ("Gap boshida", False), ("Gap o'rtasida", False), ("Qo'yilmaydi", False)]
            },
            {
                "text": "Undosh tovushlar nechta?",
                "choices": [("23 ta", True), ("6 ta", False), ("20 ta", False), ("29 ta", False)]
            },
            {
                "text": "Ko'plik qo'shimchasi qaysi?",
                "choices": [("-lar", True), ("-da", False), ("-ni", False), ("-dan", False)]
            },
            {
                "text": "Ergash gap qanday gap?",
                "choices": [("Bosh gapga bog'liq gap", True), ("Mustaqil gap", False), ("So'roq gap", False), ("Buyruq gap", False)]
            },
            {
                "text": "Ravish so'z turkumi nimani bildiradi?",
                "choices": [("Harakat belgisi", True), ("Narsa", False), ("Harakat", False), ("Son", False)]
            },
            {
                "text": "Olmosh nima qiladi?",
                "choices": [("Ot o'rnida qo'llanadi", True), ("Fe'l o'rnida", False), ("Sifat o'rnida", False), ("Hech narsa", False)]
            },
            {
                "text": "Son so'z turkumi nimani bildiradi?",
                "choices": [("Miqdor, tartib", True), ("Harakat", False), ("Narsa", False), ("Belgi", False)]
            },
            {
                "text": "Aniqlovchi gapning qaysi bo'lagi?",
                "choices": [("Ikkinchi darajali", True), ("Bosh bo'lak", False), ("Mustaqil", False), ("Bog'lovchi", False)]
            },
            {
                "text": "To'ldiruvchi qaysi savolga javob beradi?",
                "choices": [("Kimni? Nima?", True), ("Qaerda?", False), ("Qachon?", False), ("Qanday?", False)]
            },
            {
                "text": "Hol qaysi savolga javob beradi?",
                "choices": [("Qanday? Qaerda? Qachon?", True), ("Kim? Nima?", False), ("Necha?", False), ("Qaysi?", False)]
            },
            {
                "text": "Sodda gap nima?",
                "choices": [("Bir kesimli gap", True), ("Ikki kesimli gap", False), ("Ko'p kesimli gap", False), ("Kesimsiz gap", False)]
            },
            {
                "text": "Qo'shma gap nima?",
                "choices": [("Ikki yoki undan ortiq sodda gapdan iborat", True), ("Bir sodda gap", False), ("Ergash gap", False), ("So'roq gap", False)]
            },
            {
                "text": "Undov so'z nimani bildiradi?",
                "choices": [("His-tuyg'u", True), ("Narsa", False), ("Harakat", False), ("Son", False)]
            },
            {
                "text": "Yuklama so'z turkumining vazifasi?",
                "choices": [("Urg'u berish, kuchaytirish", True), ("Bog'lash", False), ("So'rash", False), ("Buyurish", False)]
            },
            {
                "text": "Bog'lovchi so'z nimani bog'laydi?",
                "choices": [("So'zlar va gaplarni", True), ("Faqat so'zlarni", False), ("Faqat gaplarni", False), ("Hech narsani", False)]
            },
            {
                "text": "Shakldosh so'zlar nima?",
                "choices": [("Yozilishi bir xil, ma'nosi har xil", True), ("Ma'nosi bir xil", False), ("Antonim", False), ("Sinonim", False)]
            },
            {
                "text": "Sinonim so'zlar nima?",
                "choices": [("Ma'nosi yaqin so'zlar", True), ("Ma'nosi qarama-qarshi", False), ("Yozilishi bir xil", False), ("Tovushi bir xil", False)]
            },
            {
                "text": "Antonim so'zlar nima?",
                "choices": [("Ma'nosi qarama-qarshi so'zlar", True), ("Ma'nosi yaqin", False), ("Yozilishi bir xil", False), ("Tovushi bir xil", False)]
            },
            {
                "text": "Imlo nima?",
                "choices": [("To'g'ri yozish qoidalari", True), ("To'g'ri o'qish", False), ("To'g'ri gapirish", False), ("To'g'ri eshitish", False)]
            },
            {
                "text": "Nuqtali vergul qachon qo'yiladi?",
                "choices": [("Qo'shma gap bo'laklari orasida", True), ("Sodda gap oxirida", False), ("Gap boshida", False), ("Qo'yilmaydi", False)]
            },
            {
                "text": "Tire belgisi qachon ishlatiladi?",
                "choices": [("Ega va kesim orasida", True), ("Gap oxirida", False), ("Gap boshida", False), ("Hech qachon", False)]
            },
            {
                "text": "Qo'shtirnoq ichida nima yoziladi?",
                "choices": [("To'g'ridan-to'g'ri nutq", True), ("Hech narsa", False), ("Faqat so'zlar", False), ("Faqat gaplar", False)]
            },
        ],
        
        "Adabiyot": [
            {
                "text": "Alisher Navoiy asarlari qaysi tilda?",
                "choices": [("O'zbek (Chagatoy) tili", True), ("Fors tili", False), ("Arab tili", False), ("Rus tili", False)]
            },
            {
                "text": "'Xamsa' asari kimga tegishli?",
                "choices": [("Alisher Navoiy", True), ("Abdulla Oripov", False), ("Erkin Vohidov", False), ("Hamid Olimjon", False)]
            },
            {
                "text": "'Boburnoma' asarini kim yozgan?",
                "choices": [("Zahiriddin Muhammad Bobur", True), ("Alisher Navoiy", False), ("Abdulla Qodiriy", False), ("Cho'lpon", False)]
            },
            {
                "text": "Abdulla Qodiriyning mashhur romani?",
                "choices": [("O'tkan kunlar", True), ("Mehrobdan chayon", False), ("Kecha va kunduz", False), ("Sinchalak", False)]
            },
            {
                "text": "Cho'lponning haqiqiy ismi?",
                "choices": [("Abdulhamid Sulaymon o'g'li", True), ("Abdulla Qodiriy", False), ("Hamid Olimjon", False), ("G'afur G'ulom", False)]
            },
            {
                "text": "'Mehrobdan chayon' romanini kim yozgan?",
                "choices": [("Abdulla Qodiriy", True), ("Cho'lpon", False), ("Oybek", False), ("Hamid Olimjon", False)]
            },
            {
                "text": "Oybek ning 'Navoiy' romani nima haqida?",
                "choices": [("Alisher Navoiy hayoti", True), ("Urush haqida", False), ("Sevgi haqida", False), ("Tabiat haqida", False)]
            },
            {
                "text": "G'afur G'ulomning mashhur she'ri?",
                "choices": [("Sen yetim emassan", True), ("O'zbegim", False), ("Vatan", False), ("Ona", False)]
            },
            {
                "text": "Erkin Vohidovning 'O'zbegim' she'ri nima haqida?",
                "choices": [("Vatan sevgisi", True), ("Ona haqida", False), ("Do'stlik", False), ("Tabiat", False)]
            },
            {
                "text": "Abdulla Oripovning 'Qizil olma' she'ri qaysi janrda?",
                "choices": [("Lirik she'r", True), ("Doston", False), ("Roman", False), ("Qissa", False)]
            },
            {
                "text": "Badiiy asar nima?",
                "choices": [("Tasviriy, fantaziyali asar", True), ("Ilmiy asar", False), ("Tarixiy hujjat", False), ("Ma'lumotnoma", False)]
            },
            {
                "text": "Doston nima?",
                "choices": [("Katta hajmli she'riy asar", True), ("Qisqa hikoya", False), ("Roman", False), ("Esse", False)]
            },
            {
                "text": "Qissa nima?",
                "choices": [("Kichik hajmli hikoya", True), ("Katta roman", False), ("She'r", False), ("Doston", False)]
            },
            {
                "text": "Roman nima?",
                "choices": [("Katta hajmli nasriy asar", True), ("Qisqa hikoya", False), ("She'r", False), ("Maqola", False)]
            },
            {
                "text": "Lirika nima?",
                "choices": [("His-tuyg'u bildiruvchi adabiyot", True), ("Voqea hikoyasi", False), ("Komediya", False), ("Tragediya", False)]
            },
            {
                "text": "Epik asar nima?",
                "choices": [("Voqeali hikoya asari", True), ("His-tuyg'u she'ri", False), ("Drama", False), ("Esse", False)]
            },
            {
                "text": "Drama nima?",
                "choices": [("Sahna asari", True), ("She'r", False), ("Roman", False), ("Qissa", False)]
            },
            {
                "text": "Metafora nima?",
                "choices": [("Ko'chma ma'noli qo'llanish", True), ("To'g'ridan-to'g'ri ma'no", False), ("Antonim", False), ("Sinonim", False)]
            },
            {
                "text": "Tashbih nima?",
                "choices": [("O'xshatish", True), ("Qarama-qarshilash", False), ("Takrorlash", False), ("Savol", False)]
            },
            {
                "text": "Alisher Navoiy qachon yashagan?",
                "choices": [("XV asr", True), ("XX asr", False), ("X asr", False), ("XVIII asr", False)]
            },
            {
                "text": "'Xamsa' nechta dostondan iborat?",
                "choices": [("5 ta", True), ("3 ta", False), ("7 ta", False), ("10 ta", False)]
            },
            {
                "text": "She'rda qofiya nima?",
                "choices": [("Misralar oxiridagi uyg'unlik", True), ("Bosh qism", False), ("O'rta qism", False), ("Kirish qism", False)]
            },
            {
                "text": "Bayt nima?",
                "choices": [("Ikki misradan iborat she'riy parcha", True), ("Bitta misra", False), ("To'rt misra", False), ("She'r", False)]
            },
            {
                "text": "Ruba'iy nechta misradan iborat?",
                "choices": [("4 misra", True), ("2 misra", False), ("6 misra", False), ("8 misra", False)]
            },
            {
                "text": "G'azal nima?",
                "choices": [("Lirik she'r janri", True), ("Epik janr", False), ("Drama", False), ("Roman", False)]
            },
            {
                "text": "Mubolag'a nima?",
                "choices": [("Bo'rttirib ko'rsatish", True), ("Kamaytirib ko'rsatish", False), ("O'xshatish", False), ("Takrorlash", False)]
            },
            {
                "text": "Taqlid nima?",
                "choices": [("Tabiiy tovushlarni ifodalash", True), ("O'xshatish", False), ("Qarama-qarshilash", False), ("Savol", False)]
            },
            {
                "text": "Janr nima?",
                "choices": [("Adabiy tur", True), ("Yozuvchi", False), ("Kitob", False), ("She'r", False)]
            },
            {
                "text": "Satirik asar nima?",
                "choices": [("Masxara, tanqid asari", True), ("Maqtov asari", False), ("Qo'shiq", False), ("Hikoya", False)]
            },
            {
                "text": "Fantastik asar nima?",
                "choices": [("Xayoliy voqealar asari", True), ("Haqiqiy voqea", False), ("Tarixiy voqea", False), ("Kundalik hayot", False)]
            },
        ],
        
        "Fizika": [
            {
                "text": "Fizika nima haqidagi fan?",
                "choices": [("Tabiat hodisalari", True), ("Tirik organizmlar", False), ("Kimyoviy moddalar", False), ("Tarix", False)]
            },
            {
                "text": "Kuch birligi nima?",
                "choices": [("Nyuton (N)", True), ("Metr (m)", False), ("Kilogramm (kg)", False), ("Sekund (s)", False)]
            },
            {
                "text": "Tezlik formulasi?",
                "choices": [("v = s/t", True), ("v = m×a", False), ("v = s×t", False), ("v = m/t", False)]
            },
            {
                "text": "Massaning birligi?",
                "choices": [("Kilogramm (kg)", True), ("Metr (m)", False), ("Nyuton (N)", False), ("Sekundлари (s)", False)]
            },
            {
                "text": "Energiya birligi?",
                "choices": [("Joul (J)", True), ("Nyuton (N)", False), ("Vatt (W)", False), ("Volt (V)", False)]
            },
            {
                "text": "Quvvat birligi?",
                "choices": [("Vatt (W)", True), ("Joul (J)", False), ("Nyuton (N)", False), ("Amper (A)", False)]
            },
            {
                "text": "Yorug'lik tezligi qancha?",
                "choices": [("300,000 km/s", True), ("100,000 km/s", False), ("500,000 km/s", False), ("200,000 km/s", False)]
            },
            {
                "text": "Gravitatsiya nima?",
                "choices": [("Tortishish kuchi", True), ("Itarish kuchi", False), ("Elektr kuchi", False), ("Magnit kuchi", False)]
            },
            {
                "text": "Nyutonning birinchi qonuni?",
                "choices": [("Inertsiya qonuni", True), ("Harakat qonuni", False), ("Ta'sir-qarshi ta'sir", False), ("Gravitatsiya", False)]
            },
            {
                "text": "Issiqlik energiyasi qanday uzatiladi?",
                "choices": [("O'tkazuvchanlik, konvektsiya, nurlanish", True), ("Faqat o'tkazuvchanlik", False), ("Faqat konvektsiya", False), ("Faqat nurlanish", False)]
            },
            {
                "text": "Elektr toki nima?",
                "choices": [("Zaryadlar harakati", True), ("Magnit maydoni", False), ("Yorug'lik", False), ("Tovush", False)]
            },
            {
                "text": "Tok kuchi birligi?",
                "choices": [("Amper (A)", True), ("Volt (V)", False), ("Om (Ω)", False), ("Vatt (W)", False)]
            },
            {
                "text": "Kuchlanish birligi?",
                "choices": [("Volt (V)", True), ("Amper (A)", False), ("Om (Ω)", False), ("Joul (J)", False)]
            },
            {
                "text": "Qarshilik birligi?",
                "choices": [("Om (Ω)", True), ("Volt (V)", False), ("Amper (A)", False), ("Vatt (W)", False)]
            },
            {
                "text": "Om qonuni formulasi?",
                "choices": [("I = U/R", True), ("I = U×R", False), ("U = I×t", False), ("R = U+I", False)]
            },
            {
                "text": "Atmosfera bosimi taxminan?",
                "choices": [("101,325 Pa", True), ("50,000 Pa", False), ("200,000 Pa", False), ("10,000 Pa", False)]
            },
            {
                "text": "Archimed qonuni nima haqida?",
                "choices": [("Suyuqlikka cho'mgan jismga ta'sir etuvchi kuch", True), ("Gravitatsiya", False), ("Elektr toki", False), ("Yorug'lik", False)]
            },
            {
                "text": "Tovush qanday tarqaladi?",
                "choices": [("To'lqin shaklida", True), ("To'g'ri chiziq", False), ("Doira bo'ylab", False), ("Tarqalmaydi", False)]
            },
            {
                "text": "Tovush vakuumda tarqaladimi?",
                "choices": [("Yo'q", True), ("Ha", False), ("Ba'zan", False), ("Bilmayman", False)]
            },
            {
                "text": "Linza qanday qurilma?",
                "choices": [("Optik qurilma", True), ("Elektr qurilmasi", False), ("Mexanik qurilma", False), ("Kimyoviy qurilma", False)]
            },
            {
                "text": "Yorug'likning qaytishi nima?",
                "choices": [("Aks ettirish", True), ("Sinish", False), ("Yutilish", False), ("Tarqalish", False)]
            },
            {
                "text": "Spektr nima?",
                "choices": [("Yorug'likning ranglarga ajralishi", True), ("Tovush", False), ("Issiqlik", False), ("Elektr", False)]
            },
            {
                "text": "Magnit qutblari?",
                "choices": [("Shimoliy va Janubiy", True), ("Sharqiy va G'arbiy", False), ("Yuqori va Pastki", False), ("Chap va O'ng", False)]
            },
            {
                "text": "Atom nima?",
                "choices": [("Moddaning eng kichik zarrasi", True), ("Katta zarracha", False), ("Molekula", False), ("Ion", False)]
            },
            {
                "text": "Elektron qayerda joylashgan?",
                "choices": [("Atom orbitalida", True), ("Yadroda", False), ("Tashqarida", False), ("Molekulada", False)]
            },
            {
                "text": "Proton qanday zaryadga ega?",
                "choices": [("Musbat", True), ("Manfiy", False), ("Neytral", False), ("Yo'q", False)]
            },
            {
                "text": "Neytron qanday zaryadga ega?",
                "choices": [("Neytral (zaryadsiz)", True), ("Musbat", False), ("Manfiy", False), ("Ikkalasi ham", False)]
            },
            {
                "text": "Erkin tushish tezlanishi qancha?",
                "choices": [("9.8 m/s²", True), ("10 m/s²", False), ("5 m/s²", False), ("15 m/s²", False)]
            },
            {
                "text": "Ish formulasi (fizikada)?",
                "choices": [("A = F×s", True), ("A = m×v", False), ("A = P×t", False), ("A = F/s", False)]
            },
            {
                "text": "Quvvat nima?",
                "choices": [("Vaqt birligidagi ish", True), ("Kuch", False), ("Energiya", False), ("Tezlik", False)]
            },
        ],
        
        "Tabiiy fan": [
            {
                "text": "Yer nechta qatlamdan iborat?",
                "choices": [("3 ta (po'stloq, mantiya, yadro)", True), ("2 ta", False), ("4 ta", False), ("5 ta", False)]
            },
            {
                "text": "Fotosintez jarayoni nimani ishlab chiqaradi?",
                "choices": [("Kislorod", True), ("Karbonat angidrid", False), ("Azot", False), ("Vodorod", False)]
            },
            {
                "text": "Quyosh sistemasida nechta sayyora bor?",
                "choices": [("8 ta", True), ("9 ta", False), ("7 ta", False), ("10 ta", False)]
            },
            {
                "text": "Eng katta sayyora?",
                "choices": [("Yupiter", True), ("Saturn", False), ("Yer", False), ("Mars", False)]
            },
            {
                "text": "Yer Quyosh atrofida necha kunda aylanadi?",
                "choices": [("365 kun", True), ("360 kun", False), ("300 kun", False), ("400 kun", False)]
            },
            {
                "text": "Oy Yer atrofida necha kunda aylanadi?",
                "choices": [("28-29 kun", True), ("30 kun", False), ("7 kun", False), ("365 kun", False)]
            },
            {
                "text": "Suv qaysi haroratda qaynaydi?",
                "choices": [("100°C", True), ("0°C", False), ("50°C", False), ("200°C", False)]
            },
            {
                "text": "Suv qaysi haroratda muzlaydi?",
                "choices": [("0°C", True), ("100°C", False), ("-10°C", False), ("10°C", False)]
            },
            {
                "text": "Havoning asosiy qismi qaysi gaz?",
                "choices": [("Azot (78%)", True), ("Kislorod (78%)", False), ("Karbonat angidrid", False), ("Vodorod", False)]
            },
            {
                "text": "Fotosintez qayerda sodir bo'ladi?",
                "choices": [("O'simlik bargi (xloroplast)", True), ("Ildiz", False), ("Poya", False), ("Gul", False)]
            },
            {
                "text": "Inson tanasida nechta suyak bor?",
                "choices": [("206 ta", True), ("106 ta", False), ("306 ta", False), ("156 ta", False)]
            },
            {
                "text": "Yurak nima vazifa bajaradi?",
                "choices": [("Qonni haydaydi", True), ("Nafas oladi", False), ("Oziq hazm qiladi", False), ("Fikrlaydi", False)]
            },
            {
                "text": "O'pka nimaning organi?",
                "choices": [("Nafas olish tizimi", True), ("Ovqat hazm qilish", False), ("Qon aylanishi", False), ("Nerv tizimi", False)]
            },
            {
                "text": "Miya qayerda joylashgan?",
                "choices": [("Bosh suyagi ichida", True), ("Ko'krak qafasida", False), ("Qorin bo'shlig'ida", False), ("Orqa miya", False)]
            },
            {
                "text": "Qaysi vitamin D vitamini deb ataladi?",
                "choices": [("Quyosh vitamini", True), ("Suv vitamini", False), ("Havo vitamini", False), ("Yer vitamini", False)]
            },
            {
                "text": "Daraxt qanday o'simlik?",
                "choices": [("Ko'p yillik", True), ("Bir yillik", False), ("Ikki yillik", False), ("Yarim yillik", False)]
            },
            {
                "text": "Gul nimaning organi?",
                "choices": [("Ko'payish organi", True), ("Oziqlanish", False), ("Nafas olish", False), ("Himoya", False)]
            },
            {
                "text": "Ildiz nimaning organi?",
                "choices": [("Oziqlanish va mustahkamlash", True), ("Faqat nafas olish", False), ("Faqat ko'payish", False), ("Hech qanday", False)]
            },
            {
                "text": "Hayvonlar qanday organizmlar?",
                "choices": [("Heterotroflar", True), ("Avtotroflar", False), ("Produtsentlar", False), ("Hech biri", False)]
            },
            {
                "text": "O'simliklar qanday organizmlar?",
                "choices": [("Avtotroflar", True), ("Heterotroflar", False), ("Konsumentlar", False), ("Redusentlar", False)]
            },
            {
                "text": "DNK nima?",
                "choices": [("Irsiy ma'lumot tashuvchi", True), ("Vitamin", False), ("Gormon", False), ("Ferment", False)]
            },
            {
                "text": "Hujayraning bosh qismi?",
                "choices": [("Yadro", True), ("Sitoplazma", False), ("Membrana", False), ("Vakuola", False)]
            },
            {
                "text": "Bakteriyalar qanday organizmlar?",
                "choices": [("Bir hujayrali", True), ("Ko'p hujayrali", False), ("Hujayrali emas", False), ("Viruslar", False)]
            },
            {
                "text": "Ekologiya nima haqidagi fan?",
                "choices": [("Organizmlar va muhit munosabati", True), ("Faqat hayvonlar", False), ("Faqat o'simliklar", False), ("Faqat inson", False)]
            },
            {
                "text": "Biotsenoz nima?",
                "choices": [("Bir joyda yashovchi organizmlar", True), ("Bir hayvon", False), ("Bir o'simlik", False), ("Tuproq", False)]
            },
            {
                "text": "Siklning davomiyligi taxminan?",
                "choices": [("24 soat", True), ("12 soat", False), ("48 soat", False), ("6 soat", False)]
            },
            {
                "text": "Yil davomiyligi?",
                "choices": [("365.25 kun", True), ("365 kun", False), ("360 kun", False), ("366 kun", False)]
            },
            {
                "text": "Oyning fazalari nechta?",
                "choices": [("4 ta", True), ("2 ta", False), ("8 ta", False), ("12 ta", False)]
            },
            {
                "text": "Quyosh sistemasining markazi?",
                "choices": [("Quyosh", True), ("Yer", False), ("Yupiter", False), ("Mars", False)]
            },
            {
                "text": "Eng yaqin yulduz?",
                "choices": [("Quyosh", True), ("Sirius", False), ("Alfa Kentavr", False), ("Vega", False)]
            },
        ],
        
        "Geografiya": [
            {
                "text": "Eng katta okean?",
                "choices": [("Tinch okeani", True), ("Atlantika", False), ("Hind okeani", False), ("Shimoliy Muz okeani", False)]
            },
            {
                "text": "Eng uzun daryo?",
                "choices": [("Nil daryosi", True), ("Amazon", False), ("Missisipi", False), ("Yangtszы", False)]
            },
            {
                "text": "Eng baland tog'?",
                "choices": [("Everest (Jomolungma)", True), ("K2", False), ("Kanchenjunga", False), ("Elbrus", False)]
            },
            {
                "text": "O'zbekiston poytaxti?",
                "choices": [("Toshkent", True), ("Samarqand", False), ("Buxoro", False), ("Xiva", False)]
            },
            {
                "text": "O'zbekiston qaysi qit'ada joylashgan?",
                "choices": [("Osiyo", True), ("Yevropa", False), ("Afrika", False), ("Amerika", False)]
            },
            {
                "text": "Yerning necha foizi suv?",
                "choices": [("71%", True), ("50%", False), ("80%", False), ("60%", False)]
            },
            {
                "text": "Ekvator chizig'i qayerdan o'tadi?",
                "choices": [("Yer o'rtasidan", True), ("Shimoliy qutbdan", False), ("Janubiy qutbdan", False), ("Yo'q", False)]
            },
            {
                "text": "Qaysi qit'a eng katta?",
                "choices": [("Yevrosiyo", True), ("Afrika", False), ("Shimoliy Amerika", False), ("Avstraliya", False)]
            },
            {
                "text": "Qaysi qit'a eng kichik?",
                "choices": [("Avstraliya", True), ("Yevropa", False), ("Antarktida", False), ("Janubiy Amerika", False)]
            },
            {
                "text": "O'zbekistonning qo'shni davlatlari nechta?",
                "choices": [("5 ta", True), ("4 ta", False), ("6 ta", False), ("3 ta", False)]
            },
            {
                "text": "Sahro nima?",
                "choices": [("Quruq, issiq hudud", True), ("Sovuq hudud", False), ("Dengiz", False), ("Tog'", False)]
            },
            {
                "text": "Cho'l nima?",
                "choices": [("Qumli, quruq hudud", True), ("Dengiz bo'yi", False), ("Tog'li joy", False), ("O'rmon", False)]
            },
            {
                "text": "Tropik iqlim qayerda?",
                "choices": [("Ekvator yaqinida", True), ("Qutblarda", False), ("O'rta kenglikda", False), ("Hech qayerda", False)]
            },
            {
                "text": "Arktika qayerda?",
                "choices": [("Shimoliy qutb", True), ("Janubiy qutb", False), ("Ekvator", False), ("Osiyo", False)]
            },
            {
                "text": "Antarktida qayerda?",
                "choices": [("Janubiy qutb", True), ("Shimoliy qutb", False), ("Ekvator", False), ("Afrika", False)]
            },
            {
                "text": "Vulqon nima?",
                "choices": [("Yer qobig'idagi yorilish", True), ("Daryo", False), ("Dengiz", False), ("Cho'l", False)]
            },
            {
                "text": "Zilzila nima?",
                "choices": [("Yer qobig'ining silkinishi", True), ("Shamol", False), ("Yomg'ir", False), ("Qor", False)]
            },
            {
                "text": "Tsunami nima?",
                "choices": [("Dengiz to'lqini (zilziladan)", True), ("Shamol", False), ("Yomg'ir", False), ("Qor", False)]
            },
            {
                "text": "Iqlim nima?",
                "choices": [("Ko'p yillik o'rtacha ob-havo", True), ("Bugungi ob-havo", False), ("Harorat", False), ("Yomg'ir", False)]
            },
            {
                "text": "Ob-havo nima?",
                "choices": [("Hozirgi atmosfera holati", True), ("Ko'p yillik holat", False), ("Faqat harorat", False), ("Faqat shamol", False)]
            },
            {
                "text": "Meridian nima?",
                "choices": [("Shimoldan janubga chiziq", True), ("Sharqdan g'arbga", False), ("Ekvator", False), ("Doira", False)]
            },
            {
                "text": "Parallеl nima?",
                "choices": [("Sharqdan g'arbga chiziq", True), ("Shimoldan janubga", False), ("Vertikal chiziq", False), ("Diagonal", False)]
            },
            {
                "text": "Kenglik nima?",
                "choices": [("Ekvatordan masofa", True), ("Meridian", False), ("Balandlik", False), ("Masofa", False)]
            },
            {
                "text": "Uzunlik nima?",
                "choices": [("Boshlang'ich meridindan masofa", True), ("Ekvatordan masofa", False), ("Balandlik", False), ("Kenglik", False)]
            },
            {
                "text": "Atlas nima?",
                "choices": [("Xaritalar to'plami", True), ("Bitta xarita", False), ("Globus", False), ("Kitob", False)]
            },
            {
                "text": "Globus nima?",
                "choices": [("Yerning kichik modeli", True), ("Xarita", False), ("Atlas", False), ("Rasm", False)]
            },
            {
                "text": "Aholining eng ko'p yashaydigan qit'a?",
                "choices": [("Osiyo", True), ("Afrika", False), ("Yevropa", False), ("Amerika", False)]
            },
            {
                "text": "Orol nima?",
                "choices": [("Suv bilan o'ralgan quruqlik", True), ("Quruqlik bilan o'ralgan suv", False), ("Tog'", False), ("Daryo", False)]
            },
            {
                "text": "Yarim orol nima?",
                "choices": [("Uch tomondan suv bilan o'ralgan", True), ("To'rt tomondan suv", False), ("Ikki tomondan suv", False), ("Suv yo'q", False)]
            },
            {
                "text": "Qaysi okean eng kichik?",
                "choices": [("Shimoliy Muz okeani", True), ("Tinch okeani", False), ("Atlantika", False), ("Hind okeani", False)]
            },
        ],
        
        "Ingliz tili": [
            {
                "text": "Hello so'zining ma'nosi?",
                "choices": [("Salom", True), ("Xayr", False), ("Rahmat", False), ("Iltimos", False)]
            },
            {
                "text": "Thank you so'zining ma'nosi?",
                "choices": [("Rahmat", True), ("Salom", False), ("Xayr", False), ("Kechirasiz", False)]
            },
            {
                "text": "Good morning so'zining ma'nosi?",
                "choices": [("Xayrli tong", True), ("Xayrli kech", False), ("Xayrli kun", False), ("Xayrli tun", False)]
            },
            {
                "text": "What is your name? - Ma'nosi?",
                "choices": [("Ismingiz nima?", True), ("Yoshingiz necha?", False), ("Qayerdasiz?", False), ("Nima qilyapsiz?", False)]
            },
            {
                "text": "I am a student - Ma'nosi?",
                "choices": [("Men o'quvchiman", True), ("Men o'qituvchiman", False), ("Men talabaman", False), ("Men ishchiman", False)]
            },
            {
                "text": "How are you? - Ma'nosi?",
                "choices": [("Qalaysiz?", True), ("Ismingiz nima?", False), ("Qayerdasiz?", False), ("Necha yoshdasiz?", False)]
            },
            {
                "text": "I love you - Ma'nosi?",
                "choices": [("Men sizni yaxshi ko'raman", True), ("Men sizni yomon ko'raman", False), ("Men sizni taniyapman", False), ("Men sizni ko'ryapman", False)]
            },
            {
                "text": "Book so'zining ko'plik shakli?",
                "choices": [("Books", True), ("Bookes", False), ("Book's", False), ("Bookies", False)]
            },
            {
                "text": "I ____ a teacher (to'ldiring)",
                "choices": [("am", True), ("is", False), ("are", False), ("be", False)]
            },
            {
                "text": "She ____ beautiful (to'ldiring)",
                "choices": [("is", True), ("am", False), ("are", False), ("be", False)]
            },
            {
                "text": "They ____ students (to'ldiring)",
                "choices": [("are", True), ("is", False), ("am", False), ("be", False)]
            },
            {
                "text": "Cat so'zining ma'nosi?",
                "choices": [("Mushuk", True), ("It", False), ("Qush", False), ("Baliq", False)]
            },
            {
                "text": "Dog so'zining ma'nosi?",
                "choices": [("It", True), ("Mushuk", False), ("Qush", False), ("Ot", False)]
            },
            {
                "text": "Apple so'zining ma'nosi?",
                "choices": [("Olma", True), ("Nok", False), ("Banan", False), ("Apelsin", False)]
            },
            {
                "text": "Red so'zining ma'nosi?",
                "choices": [("Qizil", True), ("Ko'k", False), ("Yashil", False), ("Sariq", False)]
            },
            {
                "text": "Blue so'zining ma'nosi?",
                "choices": [("Ko'k", True), ("Qizil", False), ("Yashil", False), ("Qora", False)]
            },
            {
                "text": "One, two, three, ___?",
                "choices": [("four", True), ("five", False), ("six", False), ("ten", False)]
            },
            {
                "text": "Monday - qaysi kun?",
                "choices": [("Dushanba", True), ("Seshanba", False), ("Payshanba", False), ("Juma", False)]
            },
            {
                "text": "Friday - qaysi kun?",
                "choices": [("Juma", True), ("Shanba", False), ("Yakshanba", False), ("Dushanba", False)]
            },
            {
                "text": "January - qaysi oy?",
                "choices": [("Yanvar", True), ("Fevral", False), ("Mart", False), ("Aprel", False)]
            },
            {
                "text": "Summer - qaysi fasl?",
                "choices": [("Yoz", True), ("Qish", False), ("Bahor", False), ("Kuz", False)]
            },
            {
                "text": "Mother so'zining ma'nosi?",
                "choices": [("Ona", True), ("Ota", False), ("Opa", False), ("Aka", False)]
            },
            {
                "text": "Father so'zining ma'nosi?",
                "choices": [("Ota", True), ("Ona", False), ("Aka", False), ("Uka", False)]
            },
            {
                "text": "School so'zining ma'nosi?",
                "choices": [("Maktab", True), ("Uy", False), ("Do'kon", False), ("Bog'", False)]
            },
            {
                "text": "House so'zining ma'nosi?",
                "choices": [("Uy", True), ("Maktab", False), ("Kasalxona", False), ("Do'kon", False)]
            },
            {
                "text": "Water so'zining ma'nosi?",
                "choices": [("Suv", True), ("Non", False), ("Choy", False), ("Qahva", False)]
            },
            {
                "text": "Bread so'zining ma'nosi?",
                "choices": [("Non", True), ("Suv", False), ("Go'sht", False), ("Sabzavot", False)]
            },
            {
                "text": "Good so'zining antonimi?",
                "choices": [("Bad", True), ("Nice", False), ("Great", False), ("Beautiful", False)]
            },
            {
                "text": "Big so'zining antonimi?",
                "choices": [("Small", True), ("Large", False), ("Huge", False), ("Giant", False)]
            },
            {
                "text": "Happy so'zining ma'nosi?",
                "choices": [("Baxtli", True), ("G'amgin", False), ("Jahldor", False), ("Xafa", False)]
            },
        ],
        
        "Rus tili": [
            {
                "text": "Привет so'zining ma'nosi?",
                "choices": [("Salom", True), ("Xayr", False), ("Rahmat", False), ("Iltimos", False)]
            },
            {
                "text": "Спасибо so'zining ma'nosi?",
                "choices": [("Rahmat", True), ("Salom", False), ("Xayr", False), ("Kechirasiz", False)]
            },
            {
                "text": "Доброе утро so'zining ma'nosi?",
                "choices": [("Xayrli tong", True), ("Xayrli kech", False), ("Xayrli kun", False), ("Xayrli tun", False)]
            },
            {
                "text": "Как вас зовут? - Ma'nosi?",
                "choices": [("Ismingiz nima?", True), ("Yoshingiz necha?", False), ("Qayerdasiz?", False), ("Nima qilyapsiz?", False)]
            },
            {
                "text": "Я студент - Ma'nosi?",
                "choices": [("Men talabaman", True), ("Men o'quvchiman", False), ("Men o'qituvchiman", False), ("Men ishchiman", False)]
            },
            {
                "text": "Rus alifbosida nechta harf bor?",
                "choices": [("33 ta", True), ("26 ta", False), ("29 ta", False), ("30 ta", False)]
            },
            {
                "text": "Книга so'zining ma'nosi?",
                "choices": [("Kitob", True), ("Daftar", False), ("Qalam", False), ("Stol", False)]
            },
            {
                "text": "Стол so'zining ma'nosi?",
                "choices": [("Stol", True), ("Stul", False), ("Kitob", False), ("Daftar", False)]
            },
            {
                "text": "Я люблю - Ma'nosi?",
                "choices": [("Men yaxshi ko'raman", True), ("Men yomon ko'raman", False), ("Men bilaman", False), ("Men ko'raman", False)]
            },
            {
                "text": "Мама so'zining ma'nosi?",
                "choices": [("Ona", True), ("Ota", False), ("Opa", False), ("Aka", False)]
            },
            {
                "text": "Папа so'zining ma'nosi?",
                "choices": [("Ota", True), ("Ona", False), ("Aka", False), ("Uka", False)]
            },
            {
                "text": "Школа so'zining ma'nosi?",
                "choices": [("Maktab", True), ("Uy", False), ("Do'kon", False), ("Bog'", False)]
            },
            {
                "text": "Дом so'zining ma'nosi?",
                "choices": [("Uy", True), ("Maktab", False), ("Kasalxona", False), ("Do'kon", False)]
            },
            {
                "text": "Вода so'zining ma'nosi?",
                "choices": [("Suv", True), ("Non", False), ("Choy", False), ("Qahva", False)]
            },
            {
                "text": "Хлеб so'zining ma'nosi?",
                "choices": [("Non", True), ("Suv", False), ("Go'sht", False), ("Sabzavot", False)]
            },
            {
                "text": "Один, два, три, ___?",
                "choices": [("четыре", True), ("пять", False), ("шесть", False), ("десять", False)]
            },
            {
                "text": "Красный so'zining ma'nosi?",
                "choices": [("Qizil", True), ("Ko'k", False), ("Yashil", False), ("Sariq", False)]
            },
            {
                "text": "Синий so'zining ma'nosi?",
                "choices": [("Ko'k", True), ("Qizil", False), ("Yashil", False), ("Qora", False)]
            },
            {
                "text": "Большой so'zining antonimi?",
                "choices": [("Маленький", True), ("Огромный", False), ("Громадный", False), ("Великий", False)]
            },
            {
                "text": "Хороший so'zining antonimi?",
                "choices": [("Плохой", True), ("Отличный", False), ("Прекрасный", False), ("Замечательный", False)]
            },
            {
                "text": "Зима so'zining ma'nosi?",
                "choices": [("Qish", True), ("Yoz", False), ("Bahor", False), ("Kuz", False)]
            },
            {
                "text": "Лето so'zining ma'nosi?",
                "choices": [("Yoz", True), ("Qish", False), ("Bahor", False), ("Kuz", False)]
            },
            {
                "text": "Весна so'zining ma'nosi?",
                "choices": [("Bahor", True), ("Yoz", False), ("Qish", False), ("Kuz", False)]
            },
            {
                "text": "Осень so'zining ma'nosi?",
                "choices": [("Kuz", True), ("Bahor", False), ("Yoz", False), ("Qish", False)]
            },
            {
                "text": "Понедельник - qaysi kun?",
                "choices": [("Dushanba", True), ("Seshanba", False), ("Payshanba", False), ("Juma", False)]
            },
            {
                "text": "Пятница - qaysi kun?",
                "choices": [("Juma", True), ("Shanba", False), ("Yakshanba", False), ("Dushanba", False)]
            },
            {
                "text": "Январь - qaysi oy?",
                "choices": [("Yanvar", True), ("Fevral", False), ("Mart", False), ("Aprel", False)]
            },
            {
                "text": "Друг so'zining ma'nosi?",
                "choices": [("Do'st", True), ("Dushman", False), ("O'rtoq", False), ("Tanish", False)]
            },
            {
                "text": "Сестра so'zining ma'nosi?",
                "choices": [("Opa/Singil", True), ("Aka/Uka", False), ("Ona", False), ("Ota", False)]
            },
            {
                "text": "Брат so'zining ma'nosi?",
                "choices": [("Aka/Uka", True), ("Opa/Singil", False), ("Ona", False), ("Ota", False)]
            },
        ],
        
        "Tarix": [
            {
                "text": "O'zbekiston mustaqillikka qachon erishgan?",
                "choices": [("1991 yil 1 sentyabr", True), ("1990 yil", False), ("1992 yil", False), ("1989 yil", False)]
            },
            {
                "text": "Amir Temur qachon hukmronlik qilgan?",
                "choices": [("XIV-XV asr", True), ("X-XI asr", False), ("XVI-XVII asr", False), ("XX asr", False)]
            },
            {
                "text": "Samarqand qachon poytaxt bo'lgan?",
                "choices": [("Temuriylar davri", True), ("Hozir", False), ("Sovet davri", False), ("Hech qachon", False)]
            },
            {
                "text": "Buxoro qadimiy shahri nima bilan mashhur?",
                "choices": [("Madaniy markaz, savdo", True), ("Dengiz porti", False), ("Tog'lar", False), ("Cho'l", False)]
            },
            {
                "text": "Ulug'bek kim edi?",
                "choices": [("Olim, astronom", True), ("Shoir", False), ("Jangchi", False), ("Savdogar", False)]
            },
            {
                "text": "Ipak yo'li nima edi?",
                "choices": [("Qadimiy savdo yo'li", True), ("Daryo", False), ("Temir yo'l", False), ("Havo yo'li", False)]
            },
            {
                "text": "Movaraunnahrning qadimiy nomi?",
                "choices": [("Transokiana", True), ("Turkiston", False), ("Xorazm", False), ("Buxoro", False)]
            },
            {
                "text": "Xorazm qayerda joylashgan?",
                "choices": [("Amudaryo havzasi", True), ("Sirdaryo havzasi", False), ("Zarafshon havzasi", False), ("Cho'lda", False)]
            },
            {
                "text": "Qaysi shahar 'Sharq gavhari' deb atalgan?",
                "choices": [("Samarqand", True), ("Toshkent", False), ("Buxoro", False), ("Xiva", False)]
            },
            {
                "text": "Temurning poytaxti qayerda bo'lgan?",
                "choices": [("Samarqand", True), ("Toshkent", False), ("Buxoro", False), ("Xiva", False)]
            },
            {
                "text": "Ikkinchi jahon urushi qachon boshlangan?",
                "choices": [("1939 yil", True), ("1941 yil", False), ("1945 yil", False), ("1914 yil", False)]
            },
            {
                "text": "Ikkinchi jahon urushi qachon tugagan?",
                "choices": [("1945 yil", True), ("1941 yil", False), ("1939 yil", False), ("1950 yil", False)]
            },
            {
                "text": "Birinchi jahon urushi qachon boshlangan?",
                "choices": [("1914 yil", True), ("1918 yil", False), ("1939 yil", False), ("1941 yil", False)]
            },
            {
                "text": "Qadimgi Rim qayerda joylashgan?",
                "choices": [("Italiya", True), ("Gretsiya", False), ("Misr", False), ("Turkiya", False)]
            },
            {
                "text": "Piramidalar qayerda?",
                "choices": [("Misr", True), ("Gretsiya", False), ("Italiya", False), ("Hindiston", False)]
            },
            {
                "text": "Chingizxon kim edi?",
                "choices": [("Mo'g'ul xoni", True), ("Turkiy xon", False), ("Arab xon", False), ("Fors shoh", False)]
            },
            {
                "text": "Makedoniyalik Aleksandr kim edi?",
                "choices": [("Buyuk sardaq", True), ("Olim", False), ("Shoir", False), ("Savdogar", False)]
            },
            {
                "text": "Renaissance davri qaysi asrda?",
                "choices": [("XIV-XVII asr", True), ("X-XII asr", False), ("XVIII-XX asr", False), ("I-V asr", False)]
            },
            {
                "text": "O'rta asrlar qaysi davrni o'z ichiga oladi?",
                "choices": [("V-XV asrlar", True), ("I-V asrlar", False), ("XV-XX asrlar", False), ("Hozirgi davr", False)]
            },
            {
                "text": "Napoleon kim edi?",
                "choices": [("Frantsiya imperatori", True), ("Rus imperatori", False), ("Ingliz qiroli", False), ("Ispan qiroli", False)]
            },
            {
                "text": "Kolumb nima kashf etgan?",
                "choices": [("Amerika qit'asi", True), ("Avstraliya", False), ("Afrika", False), ("Osiyo", False)]
            },
            {
                "text": "Qadimgi Misr sivilizatsiyasi qaysi daryoda?",
                "choices": [("Nil daryosi", True), ("Tigr va Yevfrat", False), ("Amazon", False), ("Missisipi", False)]
            },
            {
                "text": "Qadimgi Gretsiya qayerda?",
                "choices": [("Balkan yarim oroli", True), ("Apeinin yarim oroli", False), ("Pireney yarim oroli", False), ("Skandinaviya", False)]
            },
            {
                "text": "Sovet Ittifoqi qachon tarqaldi?",
                "choices": [("1991 yil", True), ("1990 yil", False), ("1989 yil", False), ("1992 yil", False)]
            },
            {
                "text": "BМТ (Birlashgan Millatlar Tashkiloti) qachon tashkil topgan?",
                "choices": [("1945 yil", True), ("1939 yil", False), ("1950 yil", False), ("1960 yil", False)]
            },
            {
                "text": "Movaraunnahrda birinchi davlat?",
                "choices": [("Xorazm", True), ("Samarqand", False), ("Buxoro", False), ("Toshkent", False)]
            },
            {
                "text": "Qadimiy Xorazm poytaxti?",
                "choices": [("Katta", True), ("Urganch", False), ("Xiva", False), ("Buxoro", False)]
            },
            {
                "text": "Abu Ali ibn Sino (Avitsenna) qaysi asrda yashagan?",
                "choices": [("X-XI asr", True), ("XV asr", False), ("V asr", False), ("XX asr", False)]
            },
            {
                "text": "Beruniy qaysi fanning asoschilaridan?",
                "choices": [("Astronomiya, matematika", True), ("Kimyo", False), ("Biologiya", False), ("Fizika", False)]
            },
            {
                "text": "Samarqandda Registon qachon qurilgan?",
                "choices": [("XV-XVII asrlar", True), ("XX asr", False), ("X asr", False), ("V asr", False)]
            },
        ]
    }
    
    # Agar fan topilmasa, umumiy savollar
    if subject not in questions:
        questions[subject] = [
            {
                "text": f"{subject} fanidan savol {i+1}",
                "choices": [
                    (f"To'g'ri javob {i+1}", True),
                    (f"Noto'g'ri javob A", False),
                    (f"Noto'g'ri javob B", False),
                    (f"Noto'g'ri javob C", False)
                ]
            } for i in range(30)
        ]
    
    return questions[subject]


if __name__ == '__main__':
    print("🚀 Testlar yaratish boshlandi...")
    create_tests()
    print("\n✅ Tayyor! Admin paneldan yoki saytdan testlarni ko'ring.")

