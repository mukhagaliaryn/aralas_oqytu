import os
import io
from datetime import timezone
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from openpyxl.workbook import Workbook
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape, A4
from pdfrw import PdfReader, PdfWriter, PageMerge
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from main.models import Subject, Lesson
from progress.models import UserSubject, UserLesson, UserTest, UserAnswer, UseTask


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



def export_user_course_report_excel(request, user_subject_id):
    user_subject = UserSubject.objects.select_related('user', 'subject').get(id=user_subject_id)

    wb = Workbook()
    ws = wb.active
    ws.title = f'{user_subject.user.first_name} {user_subject.user.last_name} - {user_subject.subject.title[:16]}'

    ws.append([f'{user_subject.user.first_name} {user_subject.user.last_name} - {user_subject.subject.title}'])
    ws.append(['Сабақ', 'Сабақ уақыты', 'Тапсырма бағасы', 'Тестілеу бағасы', 'Жалпы бағалау', 'Статус', 'Орындалған уақыты'])

    for user_lesson in user_subject.user_lessons.all():
        title = user_lesson.lesson.title
        duration = user_lesson.lesson.duration
        task_score = sum([user_task.grade for user_task in user_lesson.user_tasks.all()])
        test_score = sum([user_test.score for user_test in user_lesson.user_tests.all()])
        lesson_score = user_lesson.lesson_score
        status = user_lesson.completed
        submitted_at = user_lesson.completed_at.astimezone(timezone.utc).replace(tzinfo=None) if user_lesson.completed_at else '-'

        ws.append([
            title,
            duration,
            task_score,
            test_score,
            lesson_score,
            'Орындалды' if status else '-',
            submitted_at
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename=user_subject_{user_subject.id}_report.xlsx'
    wb.save(response)
    return response