from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from main.models import Subject, Lesson, Chapter, Test, Question, Option, TextContent, VideoContent, FrameContent, Task
from progress.models import UserSubject, UserLesson, UserTest, UserAnswer, UseTask


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
        total_user_subject_score = 0
        user_percent = 0
        for user_subject in user_subjects:
            total_user_subject_score += user_subject.total_percent
        try:
            user_percent = total_user_subject_score / user_subjects.count()
        except:
            pass

        completed_tasks = UseTask.objects.filter(user=user, is_done=True)
        pending_tasks = UseTask.objects.filter(user=user, is_done=False)

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
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'user_type': 'student'
        }
        return render(request, 'home/index.html', context)

    elif user.user_type == 'teacher':
        return redirect('/admin/')


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
        if user_lessons:
            first_user_lesson = user_lessons.first()
            first_user_lesson.is_open = True
            first_user_lesson.save()

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



# lesson_detail view
@login_required(login_url='/accounts/login/')
def lesson_detail(request, user_subject_pk, chapter_pk, user_lesson_pk):
    user = request.user

    if user.user_type == 'student':
        user_subject = get_object_or_404(UserSubject, pk=user_subject_pk)
        chapter = get_object_or_404(Chapter, pk=chapter_pk)
        user_lesson = get_object_or_404(UserLesson, pk=user_lesson_pk)
        chapters = Chapter.objects.filter(subject=user_subject.subject)
        chapters_with_lessons = []
        for item in chapters:
            lessons = UserLesson.objects.filter(
                user_subject=user_subject,
                lesson__chapter=item
            ).order_by('lesson__order')
            chapters_with_lessons.append({
                'chapter': item,
                'user_lessons': lessons
            })

        # lesson contents
        text_contents = TextContent.objects.filter(lesson=user_lesson.lesson)
        video_contents = VideoContent.objects.filter(lesson=user_lesson.lesson)
        frame_contents = FrameContent.objects.filter(lesson=user_lesson.lesson)
        user_tasks = UseTask.objects.filter(user_lesson=user_lesson, user=user)
        user_tests = UserTest.objects.filter(user_lesson=user_lesson, user=user)

        if request.method == 'POST':
            action = request.POST.get('action')

            if action == 'submit_task':
                task_id = request.POST.get('task_id')
                task = get_object_or_404(Task, pk=task_id)
                submission = request.FILES.get('submission')
                feedback = request.POST.get('feedback')

                user_task, created = UseTask.objects.get_or_create(
                    user=user,
                    user_lesson=user_lesson,
                    task=task
                )
                if submission:
                    user_task.submission = submission
                    user_task.feedback = feedback
                    user_task.save()
                    messages.success(request, f"'{user_task.task.title}' тапсырмасы сәтті жіберілді!")
                else:
                    messages.error(request, "Тапсырманы жіберу үшін құжатты тіркеу қажет!")

            elif action == 'submit_test':
                test_id = request.POST.get('test_id')
                test = get_object_or_404(Test, pk=test_id)
                user_test, created = UserTest.objects.get_or_create(
                    user=user,
                    user_lesson=user_lesson,
                    test=test
                )

                total_test_score = 0
                for question in Question.objects.filter(test=test):
                    selected_option_ids = request.POST.getlist(f'question_{question.id}')
                    user_answer, created = UserAnswer.objects.get_or_create(
                        user_test=user_test,
                        question=question
                    )
                    user_answer.answers.set(Option.objects.filter(id__in=selected_option_ids))
                    user_answer.score = sum(option.score for option in user_answer.answers.all())
                    user_answer.save()

                    total_test_score += user_answer.score

                user_test.score = (total_test_score * 100)/user_test.test.total_score
                user_test.completed = True
                user_test.save()
                messages.success(request, f"Тест аяқталды! Нәтижені сабақ аяқталғаннан соң көресіз!")

            elif action == 'complete_lesson':
                total_task_score = sum(user_task.grade for user_task in user_tasks.filter(is_done=True))
                task_count = user_tasks.filter(is_done=True).count()
                avg_task_score = (total_task_score / task_count) if task_count > 0 else 0

                total_test_score = sum(user_test.score for user_test in user_tests.filter(completed=True))
                test_count = user_tests.filter(completed=True).count()
                avg_test_score = (total_test_score / test_count) if test_count > 0 else 0

                user_lesson.lesson_score = (avg_task_score + avg_test_score) / (task_count + test_count)
                user_lesson.completed = True
                user_lesson.completed_at = timezone.now()
                user_lesson.save()

                next_lesson = UserLesson.objects.filter(
                    user_subject=user_subject,
                    lesson__order=user_lesson.lesson.order + 1
                ).first()

                if next_lesson:
                    next_lesson.is_open = True
                    next_lesson.save()

                completed_lessons = UserLesson.objects.filter(user_subject=user_subject, completed=True)
                total_score = sum(lesson.lesson_score for lesson in completed_lessons)
                total_lessons = UserLesson.objects.filter(user_subject=user_subject).count()
                user_subject.total_percent = total_score / total_lessons if total_lessons > 0 else 0
                user_subject.save()
                messages.success(request, 'Сабақ аяқталды!')

        next_lesson = UserLesson.objects.filter(
            user_subject=user_subject,
            lesson__order=user_lesson.lesson.order + 1
        ).first()

        context = {
            'user_subject': user_subject,
            'chapter': chapter,
            'user_lesson': user_lesson,
            'chapters_with_lessons': chapters_with_lessons,

            # lesson contents
            'text_contents': text_contents,
            'video_contents': video_contents,
            'frame_contents': frame_contents,
            'user_tasks': user_tasks,
            'user_tests': user_tests,
            'next_lesson': next_lesson
        }

        user_tasks = UseTask.objects.filter(user=user, user_lesson=user_lesson, is_done=True)
        task_results = []
        for user_task in user_tasks:
            task_results.append({
                'task': user_task.task,
                'submission': user_task.submission,
                'grade': user_task.grade,
                'feedback': user_task.feedback,
            })
        context['task_results'] = task_results


        user_test = UserTest.objects.filter(user=user, user_lesson=user_lesson, completed=True).first()
        if user_test:
            user_answers = UserAnswer.objects.filter(user_test=user_test)
            test_results = []
            for user_answer in user_answers:
                correct_options = Option.objects.filter(question=user_answer.question, is_correct=True)
                user_selected_options = user_answer.answers.all()

                test_results.append({
                    'question': user_answer.question,
                    'correct_options': correct_options,
                    'user_selected_options': user_selected_options,
                })

            context['test_results'] = test_results
            context['user_test'] = user_test

        return render(request, 'subjects/lesson_detail.html', context)

    elif user.user_type == 'teacher':
        raise Http404('Оқытушыларға бұл бет қолжетімді емес.')
