from django.urls import path
from . import views


urlpatterns = [
    path('', views.main, name='main'),
    path('home/', views.home, name='home'),
    path('subject/<subject_pk>/', views.subject_detail, name='subject_detail'),
    # path('user/subject/<user_subject_pk>/lesson/<user_lesson_pk>/', views.lesson_detail, name='lesson_detail')
]