"""
Admin panel uchun alohida view'lar
"""
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from accounts.models import User


@staff_member_required
def export_teachers_credentials_view(request):
    """O'qituvchilar login va parollarini yuklab olish (parol faqat admin uchun)"""
    teachers = User.objects.filter(role='teacher', is_verified=True).order_by('first_name', 'last_name')
    
    if not teachers.exists():
        return HttpResponse('O\'qituvchilar topilmadi!', status=404)
    
    # Faqat admin parolni ko'ra oladi
    is_admin = hasattr(request.user, 'role') and request.user.role == 'admin'
    
    wb = Workbook()
    ws = wb.active
    ws.title = "O'qituvchilar"
    
    # Headers va ustunlar soni admin/staff ga qarab o'zgaradi
    if is_admin:
        headers = ['№', 'Ism', 'Familiya', 'Login (Username)', 'Email', 'Parol', 'Fan']
        merge_range = 'A1:G1'
        merge_range_info = 'A2:G2'
    else:
        headers = ['№', 'Ism', 'Familiya', 'Login (Username)', 'Email', 'Fan']
        merge_range = 'A1:F1'
        merge_range_info = 'A2:F2'
    
    # Title
    ws.merge_cells(merge_range)
    title_cell = ws['A1']
    if is_admin:
        title_cell.value = "O'QITUVCHILAR LOGIN VA PAROLLARI"
    else:
        title_cell.value = "O'QITUVCHILAR LOGINLARI"
    title_cell.font = Font(size=16, bold=True, color="FFFFFF")
    title_cell.fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    title_cell.alignment = Alignment(horizontal='center', vertical='center')
    ws.row_dimensions[1].height = 30
    
    # Info
    ws.merge_cells(merge_range_info)
    info_cell = ws['A2']
    info_cell.value = f"Export qilingan sana: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')} | Jami: {teachers.count()} ta"
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
    
    ws.row_dimensions[header_row].height = 25
    
    # Data
    for idx, user in enumerate(teachers, 1):
        row = header_row + idx
        
        if is_admin:
            # Admin uchun parol bilan
            password = user.temporary_password if user.temporary_password else '(Parol hash qilingan - qayta tiklash kerak)'
            data = [
                idx,
                user.first_name or '',
                user.last_name or '',
                user.username,
                user.email,
                password,
                user.subject or '',
            ]
        else:
            # Staff uchun parolsiz
            data = [
                idx,
                user.first_name or '',
                user.last_name or '',
                user.username,
                user.email,
                user.subject or '',
            ]
        
        for col, value in enumerate(data, 1):
            cell = ws.cell(row=row, column=col, value=value)
            cell.alignment = Alignment(horizontal='left', vertical='center')
            # Parol ustuni uchun maxsus format (faqat admin uchun)
            if is_admin and col == 6:  # Parol ustuni (F)
                if not user.temporary_password:
                    cell.font = Font(italic=True, color="FF0000")  # Qizil va italic
            if row % 2 == 0:
                cell.fill = PatternFill(start_color="E7E6E6", end_color="E7E6E6", fill_type="solid")
    
    # Column widths
    ws.column_dimensions['A'].width = 8
    ws.column_dimensions['B'].width = 20
    ws.column_dimensions['C'].width = 20
    ws.column_dimensions['D'].width = 25
    ws.column_dimensions['E'].width = 30
    if is_admin:
        ws.column_dimensions['F'].width = 40  # Parol ustuni kengroq
        ws.column_dimensions['G'].width = 20
    else:
        ws.column_dimensions['F'].width = 20  # Fan ustuni
    
    # Save to response
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    
    if is_admin:
        filename = f"oqituvchilar_login_parol_{timezone.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    else:
        filename = f"oqituvchilar_login_{timezone.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


@staff_member_required
def export_students_credentials_view(request):
    """O'quvchilar login va parollarini yuklab olish (parol faqat admin uchun)"""
    students = User.objects.filter(role='student', is_verified=True).order_by('grade', 'class_name', 'first_name', 'last_name')
    
    if not students.exists():
        return HttpResponse('O\'quvchilar topilmadi!', status=404)
    
    # Faqat admin parolni ko'ra oladi
    is_admin = hasattr(request.user, 'role') and request.user.role == 'admin'
    
    wb = Workbook()
    ws = wb.active
    ws.title = "O'quvchilar"
    
    # Headers va ustunlar soni admin/staff ga qarab o'zgaradi
    if is_admin:
        headers = ['№', 'Ism', 'Familiya', 'Login (Username)', 'Email', 'Parol', 'Sinf', 'Sinif']
        merge_range = 'A1:H1'
        merge_range_info = 'A2:H2'
    else:
        headers = ['№', 'Ism', 'Familiya', 'Login (Username)', 'Email', 'Sinf', 'Sinif']
        merge_range = 'A1:G1'
        merge_range_info = 'A2:G2'
    
    # Title
    ws.merge_cells(merge_range)
    title_cell = ws['A1']
    if is_admin:
        title_cell.value = "O'QUVCHILAR LOGIN VA PAROLLARI"
    else:
        title_cell.value = "O'QUVCHILAR LOGINLARI"
    title_cell.font = Font(size=16, bold=True, color="FFFFFF")
    title_cell.fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    title_cell.alignment = Alignment(horizontal='center', vertical='center')
    ws.row_dimensions[1].height = 30
    
    # Info
    ws.merge_cells(merge_range_info)
    info_cell = ws['A2']
    info_cell.value = f"Export qilingan sana: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')} | Jami: {students.count()} ta"
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
    
    ws.row_dimensions[header_row].height = 25
    
    # Data
    for idx, user in enumerate(students, 1):
        row = header_row + idx
        
        if is_admin:
            # Admin uchun parol bilan
            password = user.temporary_password if user.temporary_password else '(Parol hash qilingan - qayta tiklash kerak)'
            data = [
                idx,
                user.first_name or '',
                user.last_name or '',
                user.username,
                user.email,
                password,
                user.grade or '',
                user.class_name or '',
            ]
        else:
            # Staff uchun parolsiz
            data = [
                idx,
                user.first_name or '',
                user.last_name or '',
                user.username,
                user.email,
                user.grade or '',
                user.class_name or '',
            ]
        
        for col, value in enumerate(data, 1):
            cell = ws.cell(row=row, column=col, value=value)
            cell.alignment = Alignment(horizontal='left', vertical='center')
            # Parol ustuni uchun maxsus format (faqat admin uchun)
            if is_admin and col == 6:  # Parol ustuni (F)
                if not user.temporary_password:
                    cell.font = Font(italic=True, color="FF0000")  # Qizil va italic
            if row % 2 == 0:
                cell.fill = PatternFill(start_color="E7E6E6", end_color="E7E6E6", fill_type="solid")
    
    # Column widths
    ws.column_dimensions['A'].width = 8
    ws.column_dimensions['B'].width = 20
    ws.column_dimensions['C'].width = 20
    ws.column_dimensions['D'].width = 25
    ws.column_dimensions['E'].width = 30
    if is_admin:
        ws.column_dimensions['F'].width = 40  # Parol ustuni kengroq
        ws.column_dimensions['G'].width = 10
        ws.column_dimensions['H'].width = 15
    else:
        ws.column_dimensions['F'].width = 10  # Sinf ustuni
        ws.column_dimensions['G'].width = 15  # Sinif ustuni
    
    # Save to response
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    
    if is_admin:
        filename = f"oquvchilar_login_parol_{timezone.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    else:
        filename = f"oquvchilar_login_{timezone.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response
