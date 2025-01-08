from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.models import User
from main.models import Subject, Lesson, Chapter, Test, Question, Option
from progress.models import UserSubject, UserLesson, Comment, UserTest, UserAnswer


# main
# ----------------------------------------------------------------------------------------------------------------------
def main(request):
    return render(request, 'index.html', {})


# home
# ----------------------------------------------------------------------------------------------------------------------
@login_required(login_url='/accounts/login/')
def home(request):
    user = request.user

    if user.user_type == 'student':
        user_subjects = UserSubject.objects.filter(user=user)
        started_subjects = UserSubject.objects.filter(user=user, completed=False)
        finished_subjects = UserSubject.objects.filter(user=user, completed=True)
        user_percent = 60

        if request.method == 'POST':
            user_subject_id = request.POST.get('delete_user_subject_id')
            if user_subject_id:
                user_subject = get_object_or_404(UserSubject, id=user_subject_id, user=user)
                user_subject.delete()
                return redirect('home')

        context = {
            'user_subjects': user_subjects,
            'started_subjects': started_subjects,
            'finished_subjects': finished_subjects,
            'started_subjects_count': started_subjects.count(),
            'finished_subjects_count': finished_subjects.count(),
            'user_percent': user_percent,
            'user_type': 'student'
        }
        return render(request, 'home/index.html', context)

    elif user.user_type == 'teacher':
        all_subjects = Subject.objects.all()
        user_subjects = UserSubject.objects.all()

        context = {
            'all_subjects': all_subjects,
            'user_subjects': user_subjects,
            'user_type': 'teacher'
        }
        return render(request, 'home/index.html', context)


# subjects
# ----------------------------------------------------------------------------------------------------------------------
@login_required(login_url='/accounts/login/')
def subjects(request):
    user = request.user

    if user.user_type == 'student':
        user_subjects = UserSubject.objects.filter(user=user)
        all_subjects = Subject.objects.all()
        context = {
            'user_subjects': user_subjects,
            'all_subjects': all_subjects
        }
        return render(request, 'subjects/index.html', context)
    elif user.user_type == 'teacher':
        raise Http404("Оқытушыларға бұл бет қолжетімді емес.")


# subject_detail
# ----------------------------------------------------------------------------------------------------------------------
@login_required(login_url='/accounts/login/')
def subject_detail(request, subject_pk):
    user = request.user

    if user.user_type == 'student':
        user_subjects = UserSubject.objects.filter(user=user)
        subject = get_object_or_404(Subject, pk=subject_pk)
        subject.view += 1
        subject.save()

        first_user_subject = UserSubject.objects.filter(user=request.user, subject=subject).order_by('id').first()
        first_user_lesson = None
        if first_user_subject:
            first_user_lesson = UserLesson.objects.filter(
                user_subject=first_user_subject
            ).order_by('lesson__order').first()
        my_subjects = request.user.user_subjects.all()
        add_subjects = [user_subject.subject for user_subject in my_subjects]

        if request.method == 'POST':
            subject_id = request.POST.get('subject_id')
            if not subject_id or not subject_id.isdigit():
                messages.error(request, 'Қате сұрау: элемент идентификаторы жоқ.')
                return redirect('subject_detail', subject_pk=subject.id)

            has_lessons = Lesson.objects.filter(chapter__subject=subject).exists()
            if not has_lessons:
                messages.error(request, f'"{subject.title}" пәнінде сабақтар жоқ, оны қосу мүмкін емес.')
                return redirect('subject_detail', subject_pk=subject.id)

            if UserSubject.objects.filter(user=request.user, subject=subject).exists():
                messages.error(request, 'Сіз бұл пәнді қосып қойғансыз.')
            else:
                user_subject = UserSubject.objects.create(user=request.user, subject=subject)
                messages.success(request, f'"{subject.title}" пәні қосылды!')
                lessons = Lesson.objects.filter(chapter__subject=subject)
                user_lessons = [
                    UserLesson(user_subject=user_subject, lesson=lesson, completed=False)
                    for lesson in lessons
                ]
                UserLesson.objects.bulk_create(user_lessons)
                messages.success(request, f'"{subject.title}" пәнінің сабақтары қосылды!')

            return redirect('home')

        context = {
            'user_subjects': user_subjects,
            'subject': subject,
            'add_subjects': add_subjects,
            'first_user_subject': first_user_subject,
            'first_user_lesson': first_user_lesson
        }
        return render(request, 'subjects/subject_detail.html', context)

    elif user.user_type == 'teacher':
        raise Http404("Оқытушыларға бұл бет қолжетімді емес.")


# chapter_detail
# ----------------------------------------------------------------------------------------------------------------------
@login_required(login_url='/accounts/login/')
def chapter_detail(request, user_subject_pk, chapter_pk):
    user = request.user
    active_subject_id = None

    if user.user_type == 'student':
        user_subjects = UserSubject.objects.filter(user=user)
        for user_subject in user_subjects:
            for chapter in user_subject.subject.chapters.all():
                chapter_url = f"/subject/{user_subject.id}/chapter/{chapter.id}/"
                if request.path == chapter_url:
                    active_subject_id = user_subject.subject.id

        user_subject = get_object_or_404(UserSubject, pk=user_subject_pk)
        chapter = get_object_or_404(Chapter, pk=chapter_pk)
        user_lessons = user_subject.user_lessons.filter(lesson__chapter=chapter)

        context = {
            'user_subjects': user_subjects,
            'active_subject_id': active_subject_id,
            'user_subject': user_subject,
            'chapter': chapter,
            'user_lessons': user_lessons
        }
        return render(request, 'subjects/chapter_detail.html', context)

    elif user.user_type == 'teacher':
        raise Http404("Оқытушыларға бұл бет қолжетімді емес.")



# UserCourse detail view
@login_required(login_url='/accounts/login/')
def lesson_detail(request, user_subject_pk, chapter_pk, user_lesson_pk):
    user = request.user

    if user.user_type == 'student':
        user_subjects = UserSubject.objects.filter(user=user)

        user_subject = get_object_or_404(UserSubject, pk=user_subject_pk)
        chapter = get_object_or_404(Chapter, pk=chapter_pk)
        user_lesson = get_object_or_404(UserLesson, pk=user_lesson_pk)

        context = {
            'user_subjects': user_subjects,
            'user_subject': user_subject,
            'chapter': chapter,
            'user_lesson': user_lesson
        }
        return render(request, 'subjects/lesson/index.html', context)

    elif user.user_type == 'teacher':
        raise Http404('Оқытушыларға бұл бет қолжетімді емес.')


# # UserCourse detail view
# @login_required(login_url='/accounts/login/')
# def lesson_detail(request, user_subject_pk, user_lesson_pk):
#     user_subject = get_object_or_404(UserSubject, pk=user_subject_pk, user=request.user)
#     user_lesson = get_object_or_404(UserLesson, pk=user_lesson_pk, user_subject=user_subject)
#     chapters = Chapter.objects.filter(subject=user_subject.subject).order_by('order')
#     comments = Comment.objects.filter(lesson=user_lesson.lesson).order_by('created_at')
#     homeworks = Homework.objects.filter(lesson=user_lesson.lesson)
#     user_homeworks_done = UserHomework.objects.filter(student=request.user, homework__in=homeworks, is_done=True)
#     send_homeworks = [user_homework.homework for user_homework in request.user.homeworks.filter(homework__in=homeworks)]
#     tests = Test.objects.filter(lesson=user_lesson.lesson)
#
#     if request.method == 'POST':
#         action = request.POST.get('action')
#
#         # 1️⃣ Пікір жіберу
#         if action == 'submit_comment':
#             content = request.POST.get('content')
#             rating = request.POST.get('score')
#             if not content:
#                 messages.error(request, 'Пікір мәтіні бос болмауы керек!')
#             elif not rating or not rating.isdigit() or int(rating) not in range(1, 6):
#                 messages.error(request, 'Баға 1-ден 5-ке дейін болуы керек!')
#             else:
#                 Comment.objects.create(
#                     author=request.user,
#                     lesson=user_lesson.lesson,
#                     content=content,
#                     score=int(rating)
#                 )
#                 messages.success(request, 'Пікіріңіз сәтті жіберілді!')
#
#         # 2️⃣ Үй тапсырмасын жіберу
#         elif action == 'submit_homework':
#             homework_id = request.POST.get('homework_id')
#             homework = get_object_or_404(Homework, pk=homework_id)
#             submission = request.FILES.get('submission')
#
#             user_homework, created = UserHomework.objects.get_or_create(
#                 student=request.user,
#                 user_lesson=user_lesson,
#                 homework=homework
#             )
#             if submission:
#                 user_homework.submission = submission
#                 user_homework.save()
#                 messages.success(request, f"Үй жұмысы '{homework.title}' сәтті жіберілді!")
#             else:
#                 messages.error(request, "Тапсырманы жіберу үшін құжатты тіркеу қажет!")
#
#         # 3️⃣ Тестті аяқтау және бағалау
#         elif action == 'submit_test':
#             user_test, created = UserTest.objects.get_or_create(
#                 user=request.user,
#                 test__lesson=user_lesson.lesson
#             )
#
#             total_test_score = 0
#             for question in Question.objects.filter(test__lesson=user_lesson.lesson):
#                 selected_option_ids = request.POST.getlist(f'question_{question.id}')
#                 user_answer, created = UserAnswer.objects.get_or_create(
#                     user_test=user_test,
#                     question=question
#                 )
#                 user_answer.answers.set(Option.objects.filter(id__in=selected_option_ids))
#                 user_answer.score = sum(option.is_correct for option in user_answer.answers.all()) * 10
#                 user_answer.save()
#                 total_test_score += user_answer.score
#
#             user_test.score = total_test_score
#             user_test.completed = True
#             user_test.save()
#
#             messages.success(request, f"Тест аяқталды! Сіздің ұпайыңыз: {user_test.score}")
#
#         # 4️⃣ Сабақты аяқтау
#         elif action == 'complete_lesson':
#             # Үй жұмысының орташа баллы
#             total_homework_score = sum(uh.grade for uh in user_homeworks_done)
#             homework_count = user_homeworks_done.count()
#             avg_homework_score = (total_homework_score / homework_count) if homework_count > 0 else 0
#
#             # Тесттің орташа баллы
#             user_test = UserTest.objects.filter(user=request.user, test__lesson=user_lesson.lesson).first()
#             test_score = user_test.score if user_test else 0
#
#             # Жалпы ортақ балл
#             user_lesson.lesson_score = (avg_homework_score + test_score) / 2
#             user_lesson.completed = True
#             user_lesson.completed_at = timezone.now()
#             user_lesson.save()
#
#             # Жалпы пәннің ортақ пайызы
#             completed_lessons = UserLesson.objects.filter(user_subject=user_subject, completed=True)
#             total_score = sum(lesson.lesson_score for lesson in completed_lessons)
#             total_lessons = UserLesson.objects.filter(user_subject=user_subject).count()
#
#             user_subject.total_percent = total_score / total_lessons if total_lessons > 0 else 0
#             user_subject.save()
#
#             messages.success(request, 'Сабақ аяқталды!')
#
#     chapters_with_lessons = []
#     for chapter in chapters:
#         lessons = UserLesson.objects.filter(
#             user_subject=user_subject,
#             lesson__chapter=chapter
#         ).order_by('lesson__order')
#         chapters_with_lessons.append({
#             'chapter': chapter,
#             'user_lessons': lessons
#         })
#
#     context = {
#         'user_lesson': user_lesson,
#         'user_subject': user_subject,
#         'chapters_with_lessons': chapters_with_lessons,
#         'comments': comments,
#         'send_homeworks': send_homeworks,
#         'homeworks': homeworks,
#         'user_homeworks_done': user_homeworks_done,
#         'tests': tests
#     }
#     return render(request, 'home/lesson_detail.html', context)
#
#




