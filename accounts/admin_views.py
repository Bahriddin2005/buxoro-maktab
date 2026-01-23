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
    """O'qituvchilar login va parollarini yuklab olish"""
    teachers = User.objects.filter(role='teacher', is_verified=True).order_by('first_name', 'last_name')
    
    if not teachers.exists():
        return HttpResponse('O\'qituvchilar topilmadi!', status=404)
    
    wb = Workbook()
    ws = wb.active
    ws.title = "O'qituvchilar"
    
    # Title
    ws.merge_cells('A1:G1')
    title_cell = ws['A1']
    title_cell.value = "O'QITUVCHILAR LOGIN VA PAROLLARI"
    title_cell.font = Font(size=16, bold=True, color="FFFFFF")
    title_cell.fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    title_cell.alignment = Alignment(horizontal='center', vertical='center')
    ws.row_dimensions[1].height = 30
    
    # Info
    ws.merge_cells('A2:G2')
    info_cell = ws['A2']
    info_cell.value = f"Export qilingan sana: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')} | Jami: {teachers.count()} ta"
    info_cell.font = Font(size=10, italic=True)
    info_cell.alignment = Alignment(horizontal='center')
    ws.row_dimensions[2].height = 20
    
    # Headers
    headers = ['№', 'Ism', 'Familiya', 'Login (Username)', 'Email', 'Parol', 'Fan']
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
        # Parolni olish - agar temporary_password bo'lsa, uni ko'rsat, aks holda "Parol hash qilingan (qayta tiklash kerak)"
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
        
        for col, value in enumerate(data, 1):
            cell = ws.cell(row=row, column=col, value=value)
            cell.alignment = Alignment(horizontal='left', vertical='center')
            # Parol ustuni uchun maxsus format
            if col == 6:  # Parol ustuni (F)
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
    ws.column_dimensions['F'].width = 40  # Parol ustuni kengroq
    ws.column_dimensions['G'].width = 20
    
    # Title va Info uchun merge cells yangilash
    ws.merge_cells('A1:G1')
    ws.merge_cells('A2:G2')
    
    # Save to response
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    
    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="oqituvchilar_login_parol_{timezone.now().strftime("%Y%m%d_%H%M%S")}.xlsx"'
    
    return response


@staff_member_required
def export_students_credentials_view(request):
    """O'quvchilar login va parollarini yuklab olish"""
    students = User.objects.filter(role='student', is_verified=True).order_by('grade', 'class_name', 'first_name', 'last_name')
    
    if not students.exists():
        return HttpResponse('O\'quvchilar topilmadi!', status=404)
    
    wb = Workbook()
    ws = wb.active
    ws.title = "O'quvchilar"
    
    # Title
    ws.merge_cells('A1:H1')
    title_cell = ws['A1']
    title_cell.value = "O'QUVCHILAR LOGIN VA PAROLLARI"
    title_cell.font = Font(size=16, bold=True, color="FFFFFF")
    title_cell.fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    title_cell.alignment = Alignment(horizontal='center', vertical='center')
    ws.row_dimensions[1].height = 30
    
    # Info
    ws.merge_cells('A2:H2')
    info_cell = ws['A2']
    info_cell.value = f"Export qilingan sana: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')} | Jami: {students.count()} ta"
    info_cell.font = Font(size=10, italic=True)
    info_cell.alignment = Alignment(horizontal='center')
    ws.row_dimensions[2].height = 20
    
    # Headers
    headers = ['№', 'Ism', 'Familiya', 'Login (Username)', 'Email', 'Parol', 'Sinf', 'Sinif']
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
        # Parolni olish - agar temporary_password bo'lsa, uni ko'rsat, aks holda "Parol hash qilingan (qayta tiklash kerak)"
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
        
        for col, value in enumerate(data, 1):
            cell = ws.cell(row=row, column=col, value=value)
            cell.alignment = Alignment(horizontal='left', vertical='center')
            # Parol ustuni uchun maxsus format
            if col == 6:  # Parol ustuni (F)
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
    ws.column_dimensions['F'].width = 40  # Parol ustuni kengroq
    ws.column_dimensions['G'].width = 10
    ws.column_dimensions['H'].width = 15
    
    # Save to response
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    
    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="oquvchilar_login_parol_{timezone.now().strftime("%Y%m%d_%H%M%S")}.xlsx"'
    
    return response
