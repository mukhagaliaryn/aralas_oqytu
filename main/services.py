import os
import io
from datetime import timezone
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from openpyxl.utils import get_column_letter
from openpyxl.workbook import Workbook
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from pdfrw import PdfReader, PdfWriter, PageMerge
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from openpyxl.styles import Font, Alignment, Border, Side
from main.models import Subject
from progress.models import UserSubject


# Generate certificate
# ----------------------------------------------------------------------------------------------------------------------
@login_required
def generate_certificate_view(request, subject_pk):
    user = request.user
    subject = get_object_or_404(Subject, pk=subject_pk)
    user_subject = UserSubject.objects.filter(user=request.user, subject=subject).order_by('id').first()

    if request.method == 'POST':
        packet = io.BytesIO()

        font_path = os.path.join(settings.BASE_DIR, 'templates', 'static', 'fonts', 'Georgia', 'GeorgiaPro-Bold.ttf')
        pdfmetrics.registerFont(TTFont('GeorgiaPro', font_path))

        page_width, page_height = landscape(A4)
        can = canvas.Canvas(packet, pagesize=(page_width, page_height))

        # Full name
        # --------------------------------------------------------------------------------------------------------------
        can.setFont('GeorgiaPro', 36)
        can.setFillColor(HexColor("#a17b41"))

        full_name = f'{user.first_name} {user.last_name}'
        can.drawCentredString(page_width / 2, 340, full_name)


        # Course name
        # --------------------------------------------------------------------------------------------------------------
        course_name = f'{subject.title}'
        can.setFont('GeorgiaPro', 24)
        can.setFillColor(HexColor("#0d491d"))
        can.drawCentredString(page_width / 2, 280, course_name)

        # Course number
        # --------------------------------------------------------------------------------------------------------------
        course_name = f'N00{user_subject.id}'
        can.setFont('GeorgiaPro', 18)
        can.setFillColor(HexColor("#000000"))
        can.drawCentredString(224, 116, course_name)

        # Save all
        can.save()
        packet.seek(0)

        cert_path = os.path.join(settings.BASE_DIR, 'templates', 'static', 'images', 'cert.pdf')
        template_pdf = PdfReader(cert_path)
        overlay_pdf = PdfReader(packet)

        for page, overlay in zip(template_pdf.pages, overlay_pdf.pages):
            merger = PageMerge(page)
            merger.add(overlay).render()

        output = io.BytesIO()
        PdfWriter(output, trailer=template_pdf).write()
        output.seek(0)
        return HttpResponse(output, content_type='application/pdf')

    return HttpResponse("GET сұраныс рұқсат етілмейді.", status=405)


# Export excel user_subject
# ----------------------------------------------------------------------------------------------------------------------
def export_user_course_report_excel(request, user_subject_id):
    user_subject = UserSubject.objects.select_related('user', 'subject').get(id=user_subject_id)

    wb = Workbook()
    ws = wb.active
    ws.title = f'{user_subject.user.first_name} {user_subject.user.last_name}'

    thin_border = Border(left=Side(style='thin'), right=Side(style='thin'),
                         top=Side(style='thin'), bottom=Side(style='thin'))

    # ===== HEADER =====
    ws.merge_cells('A2:G2')
    ws['A2'] = '“Өзбекәлі Жәнібеков атындағы Оңтүстік Қазақстан педагогикалық университеті”'
    ws['A2'].font = Font(name='Times New Roman', size=12, bold=True)
    ws['A2'].alignment = Alignment(horizontal='center', wrap_text=True)

    ws.merge_cells('A3:G3')
    ws['A3'] = 'Некоммерческое акционерное общество "Южно-Казахстанский педагогический университет имени Өзбекали Жанибекова"'
    ws['A3'].font = Font(name='Times New Roman', size=11, bold=True)
    ws['A3'].alignment = Alignment(horizontal='center', wrap_text=True)

    ws.merge_cells('A5:G5')
    ws['A5'] = 'ЖЕКЕ БІЛІМАЛУШЫ ВЕДОМОСІ'
    ws['A5'].font = Font(size=14, bold=True)
    ws['A5'].alignment = Alignment(horizontal='center')

    # ===== STUDENT INFO =====
    info = {
        'Аты-жөні:': f'{user_subject.user.last_name} {user_subject.user.first_name}',
        'Факультеті:': '',
        'Білім беру бағдарламасы:': '',
        'Тобы:': '',
        'Тапсырған күні:': '',
        'Оқытушы:': '',
    }

    row_idx = 7
    for label, value in info.items():
        ws[f'A{row_idx}'] = label
        ws[f'B{row_idx}'] = value
        row_idx += 1

    # ===== TABLE HEADER =====
    table_row = row_idx + 2
    headers = ['Сабақ', 'Сабақ уақыты', 'Тапсырма бағасы', 'Тестілеу бағасы', 'Жалпы бағалау', 'Статус', 'Орындалған уақыты']

    for col_idx, header in enumerate(headers, 1):  # A=1
        cell = ws.cell(row=table_row, column=col_idx, value=header)
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal='center')
        cell.border = thin_border

    # ===== TABLE CONTENT =====
    for i, user_lesson in enumerate(user_subject.user_lessons.all(), 1):
        title = user_lesson.lesson.title
        duration = user_lesson.lesson.duration
        task_score = sum([t.grade for t in user_lesson.user_tasks.all()])
        test_score = sum([t.score for t in user_lesson.user_tests.all()])
        lesson_score = user_lesson.lesson_score
        status = 'Орындалды' if user_lesson.completed else '-'
        submitted_at = (
            user_lesson.completed_at.astimezone(timezone.utc).replace(tzinfo=None)
            if user_lesson.completed_at else '-'
        )

        values = [title, duration, task_score, test_score, lesson_score, status, submitted_at]

        for j, val in enumerate(values, 1):
            cell = ws.cell(row=table_row + i, column=j, value=val)
            cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            cell.border = thin_border

    # ===== FOOTER =====
    footer_row = table_row + i + 3
    ws[f'A{footer_row}'] = 'Мұғалімнің қолы: _______________________'

    # ===== AUTO WIDTH (MAX 42 units ≈ 300px) =====
    for col_idx in range(1, 1 + len(headers)):
        max_len = 0
        col_letter = get_column_letter(col_idx)
        for row in range(table_row, table_row + i + 1):
            val = ws.cell(row=row, column=col_idx).value
            if val:
                max_len = max(max_len, len(str(val)))
        ws.column_dimensions[col_letter].width = min(max(max_len + 2, 12), 42)

    # ===== GRID OFF =====
    ws.sheet_view.showGridLines = False

    # ===== HIDE UNUSED COLUMNS/ROWS =====
    for col_idx in range(8, 100):
        ws.column_dimensions[get_column_letter(col_idx)].hidden = True
    for row in range(footer_row + 2, 100):
        ws.row_dimensions[row].hidden = True

    # ===== LIMIT VISIBLE AREA =====
    ws.sheet_view.selection[0].sqref = f"A1:G{footer_row+1}"
    ws.print_area = f"A1:G{footer_row+1}"

    # ===== EXPORT =====
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    filename = f'user_subject_{user_subject.id}_report.xlsx'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    wb.save(response)
    return response
