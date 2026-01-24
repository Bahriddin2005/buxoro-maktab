"""
Admin panel uchun alohida view'lar
"""
from django.http import HttpResponse, HttpResponseForbidden
from django.utils import timezone
from functools import wraps
from io import BytesIO
import secrets
import string
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from accounts.models import User


def admin_required(view_func):
    """Faqat admin roli bo'lgan foydalanuvchilar uchun decorator"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden('Tizimga kiring!')
        
        # Superuser yoki admin rolida bo'lishi kerak
        is_admin = (
            request.user.is_superuser or 
            (hasattr(request.user, 'role') and request.user.role == 'admin')
        )
        
        if not is_admin:
            return HttpResponseForbidden('Bu funksiya faqat adminlar uchun!')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def generate_secure_password(length=12):
    """Xavfsiz tasodifiy parol generatsiya qilish"""
    # Parol tarkibi: harflar, raqamlar, maxsus belgilar
    alphabet = string.ascii_letters + string.digits
    # Kamida bitta katta harf, bitta kichik harf, bitta raqam bo'lishini ta'minlash
    password = [
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.digits),
    ]
    # Qolgan belgilarni qo'shish
    password += [secrets.choice(alphabet) for _ in range(length - 3)]
    # Aralashtirish
    secrets.SystemRandom().shuffle(password)
    return ''.join(password)


@admin_required
def export_teachers_credentials_view(request):
    """
    O'qituvchilar login va parollarini yuklab olish (FAQAT ADMIN UCHUN)
    
    GET parametrlari:
    - reset_missing=1 : Parolsiz foydalanuvchilarga yangi parol berish
    """
    teachers = User.objects.filter(role='teacher', is_verified=True).order_by('first_name', 'last_name')
    
    if not teachers.exists():
        return HttpResponse('O\'qituvchilar topilmadi!', status=404)
    
    # Parolsiz foydalanuvchilarga yangi parol berish kerakmi?
    reset_missing = request.GET.get('reset_missing', '0') == '1'
    reset_count = 0
    
    if reset_missing:
        for user in teachers:
            if not user.temporary_password:
                new_password = generate_secure_password()
                user.set_password(new_password)  # Bu temporary_password ni ham saqlaydi
                user.save()
                reset_count += 1
        # Queryset ni yangilash
        teachers = User.objects.filter(role='teacher', is_verified=True).order_by('first_name', 'last_name')
    
    wb = Workbook()
    ws = wb.active
    ws.title = "O'qituvchilar"
    
    # Thin border
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    # Admin uchun parol bilan
    headers = ['№', 'Ism', 'Familiya', 'Login (Username)', 'Email', 'Parol', 'Fan', 'Parol holati']
    merge_range = 'A1:H1'
    merge_range_info = 'A2:H2'
    
    # Title
    ws.merge_cells(merge_range)
    title_cell = ws['A1']
    title_cell.value = "O'QITUVCHILAR LOGIN VA PAROLLARI"
    title_cell.font = Font(size=16, bold=True, color="FFFFFF")
    title_cell.fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    title_cell.alignment = Alignment(horizontal='center', vertical='center')
    ws.row_dimensions[1].height = 30
    
    # Info
    ws.merge_cells(merge_range_info)
    info_cell = ws['A2']
    info_text = f"Export qilingan sana: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')} | Jami: {teachers.count()} ta"
    if reset_missing and reset_count > 0:
        info_text += f" | Yangi parol berilgan: {reset_count} ta"
    info_cell.value = info_text
    info_cell.font = Font(size=10, italic=True)
    info_cell.alignment = Alignment(horizontal='center')
    ws.row_dimensions[2].height = 20
    
    # Headers
    header_row = 3
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=header_row, column=col, value=header)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill(start_color="70AD47", end_color="70AD47", fill_type="solid")
        cell.alignment = Alignment(horizontal='center', vertical='center')
        cell.border = thin_border
    
    ws.row_dimensions[header_row].height = 25
    
    # Data
    for idx, user in enumerate(teachers, 1):
        row = header_row + idx
        
        if user.temporary_password:
            password = user.temporary_password
            password_status = "✓ Mavjud"
            status_color = "00AA00"  # Yashil
        else:
            password = "(Parol saqlanmagan)"
            password_status = "✗ Saqlanmagan"
            status_color = "FF0000"  # Qizil
        
        data = [
            idx,
            user.first_name or '',
            user.last_name or '',
            user.username,
            user.email,
            password,
            user.subject or '',
            password_status,
        ]
        
        for col, value in enumerate(data, 1):
            cell = ws.cell(row=row, column=col, value=value)
            cell.alignment = Alignment(horizontal='left', vertical='center')
            cell.border = thin_border
            
            # Parol ustuni uchun maxsus format
            if col == 6 and not user.temporary_password:
                cell.font = Font(italic=True, color="FF0000")
            
            # Parol holati ustuni
            if col == 8:
                cell.font = Font(bold=True, color=status_color)
                cell.alignment = Alignment(horizontal='center', vertical='center')
            
            if row % 2 == 0:
                cell.fill = PatternFill(start_color="E7E6E6", end_color="E7E6E6", fill_type="solid")
    
    # Column widths
    ws.column_dimensions['A'].width = 8
    ws.column_dimensions['B'].width = 20
    ws.column_dimensions['C'].width = 20
    ws.column_dimensions['D'].width = 25
    ws.column_dimensions['E'].width = 35
    ws.column_dimensions['F'].width = 20
    ws.column_dimensions['G'].width = 20
    ws.column_dimensions['H'].width = 18
    
    # Save to response
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    
    filename = f"oqituvchilar_login_parol_{timezone.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


@admin_required
def export_students_credentials_view(request):
    """
    O'quvchilar login va parollarini yuklab olish (FAQAT ADMIN UCHUN)
    
    GET parametrlari:
    - reset_missing=1 : Parolsiz foydalanuvchilarga yangi parol berish
    """
    students = User.objects.filter(role='student', is_verified=True).order_by('grade', 'class_name', 'first_name', 'last_name')
    
    if not students.exists():
        return HttpResponse('O\'quvchilar topilmadi!', status=404)
    
    # Parolsiz foydalanuvchilarga yangi parol berish kerakmi?
    reset_missing = request.GET.get('reset_missing', '0') == '1'
    reset_count = 0
    
    if reset_missing:
        for user in students:
            if not user.temporary_password:
                new_password = generate_secure_password()
                user.set_password(new_password)  # Bu temporary_password ni ham saqlaydi
                user.save()
                reset_count += 1
        # Queryset ni yangilash
        students = User.objects.filter(role='student', is_verified=True).order_by('grade', 'class_name', 'first_name', 'last_name')
    
    wb = Workbook()
    ws = wb.active
    ws.title = "O'quvchilar"
    
    # Thin border
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    # Admin uchun parol bilan
    headers = ['№', 'Ism', 'Familiya', 'Login (Username)', 'Email', 'Parol', 'Sinf', 'Guruh', 'Parol holati']
    merge_range = 'A1:I1'
    merge_range_info = 'A2:I2'
    
    # Title
    ws.merge_cells(merge_range)
    title_cell = ws['A1']
    title_cell.value = "O'QUVCHILAR LOGIN VA PAROLLARI"
    title_cell.font = Font(size=16, bold=True, color="FFFFFF")
    title_cell.fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    title_cell.alignment = Alignment(horizontal='center', vertical='center')
    ws.row_dimensions[1].height = 30
    
    # Info
    ws.merge_cells(merge_range_info)
    info_cell = ws['A2']
    info_text = f"Export qilingan sana: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')} | Jami: {students.count()} ta"
    if reset_missing and reset_count > 0:
        info_text += f" | Yangi parol berilgan: {reset_count} ta"
    info_cell.value = info_text
    info_cell.font = Font(size=10, italic=True)
    info_cell.alignment = Alignment(horizontal='center')
    ws.row_dimensions[2].height = 20
    
    # Headers
    header_row = 3
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=header_row, column=col, value=header)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill(start_color="70AD47", end_color="70AD47", fill_type="solid")
        cell.alignment = Alignment(horizontal='center', vertical='center')
        cell.border = thin_border
    
    ws.row_dimensions[header_row].height = 25
    
    # Data
    for idx, user in enumerate(students, 1):
        row = header_row + idx
        
        if user.temporary_password:
            password = user.temporary_password
            password_status = "✓ Mavjud"
            status_color = "00AA00"  # Yashil
        else:
            password = "(Parol saqlanmagan)"
            password_status = "✗ Saqlanmagan"
            status_color = "FF0000"  # Qizil
        
        data = [
            idx,
            user.first_name or '',
            user.last_name or '',
            user.username,
            user.email,
            password,
            user.grade or '',
            user.class_name or '',
            password_status,
        ]
        
        for col, value in enumerate(data, 1):
            cell = ws.cell(row=row, column=col, value=value)
            cell.alignment = Alignment(horizontal='left', vertical='center')
            cell.border = thin_border
            
            # Parol ustuni uchun maxsus format
            if col == 6 and not user.temporary_password:
                cell.font = Font(italic=True, color="FF0000")
            
            # Parol holati ustuni
            if col == 9:
                cell.font = Font(bold=True, color=status_color)
                cell.alignment = Alignment(horizontal='center', vertical='center')
            
            if row % 2 == 0:
                cell.fill = PatternFill(start_color="E7E6E6", end_color="E7E6E6", fill_type="solid")
    
    # Column widths
    ws.column_dimensions['A'].width = 8
    ws.column_dimensions['B'].width = 20
    ws.column_dimensions['C'].width = 20
    ws.column_dimensions['D'].width = 25
    ws.column_dimensions['E'].width = 35
    ws.column_dimensions['F'].width = 20
    ws.column_dimensions['G'].width = 10
    ws.column_dimensions['H'].width = 15
    ws.column_dimensions['I'].width = 18
    
    # Save to response
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    
    filename = f"oquvchilar_login_parol_{timezone.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response
