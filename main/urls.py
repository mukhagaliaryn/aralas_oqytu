from django.urls import path
from . import views
from .services import generate_certificate_view, export_user_course_report_excel

urlpatterns = [
    path('', views.main, name='main'),
    path('content/<pk>/', views.content_detail, name='content_detail'),
    path('home/', views.home, name='home'),
    path('subjects/', views.subjects, name='subjects'),
    path('subject/<subject_pk>/', views.subject_detail, name='subject_detail'),
    path('subject/<user_subject_pk>/chapter/<chapter_pk>/', views.chapter_detail, name='chapter_detail'),
    path('subject/<user_subject_pk>/chapter/<chapter_pk>/lesson/<user_lesson_pk>/', views.lesson_detail, name='lesson_detail'),

    path('subject/<subject_pk>/cert/', generate_certificate_view, name='generate_cert'),
    path('export/user-course/<int:user_subject_id>/report/', export_user_course_report_excel, name='export_user_course_report_excel'),
]