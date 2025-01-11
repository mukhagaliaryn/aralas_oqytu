from django.db import models
from accounts.models import User
from main.models import Subject, Lesson, Test, Option, Task, Question
from django.utils.translation import gettext_lazy as _


# UserSubject model
class UserSubject(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name=_('Қолданушы'), related_name="user_subjects")
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE,
        verbose_name=_('Пән'), related_name="user_subjects"
    )
    total_percent = models.PositiveSmallIntegerField(_('Жалпы ұпай пайызы'), default=0)
    completed = models.BooleanField(_('Орындалды'), default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'subject')
        verbose_name = _('Қолданушының пәні')
        verbose_name_plural = _('Қолданушылардың пәндері')

    def __str__(self):
        return f"{self.user} - {self.subject.title}"


# UserLesson model
class UserLesson(models.Model):
    user_subject = models.ForeignKey(
        UserSubject, on_delete=models.CASCADE,
        verbose_name=_('Қолданушының пәні'), related_name="user_lessons")
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE,
        verbose_name=_('Сабақ'), related_name="user_lessons"
    )
    lesson_score = models.DecimalField(_('Сабақтың баллы'), max_digits=5, decimal_places=2, default=0)
    completed = models.BooleanField(_('Орындалды'), default=False)
    is_open = models.BooleanField(_('Ашық сабақ'), default=False)
    completed_at = models.DateTimeField(_('Орындалған уақыты'), blank=True, null=True)

    class Meta:
        unique_together = ('user_subject', 'lesson')
        verbose_name = _('Қолданушының сабағы')
        verbose_name_plural = _('Қолданушылардың сабақтары')

    def __str__(self):
        return f"{self.user_subject.user} - {self.lesson.title} - {'Орындалды' if self.completed else 'Процессте'}"


# UserTask model
class UseTask(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='user_tasks', verbose_name=_('Қолданушы')
    )
    user_lesson = models.ForeignKey(
        UserLesson, on_delete=models.CASCADE, related_name='user_tasks',
        verbose_name=_('Қолданушының сабағы')
    )
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE,
        related_name='user_tasks', verbose_name=_('Тапсырма')
    )
    submission = models.FileField(_('Тапсырма'), upload_to='main/subject/user/tasks/')
    grade = models.PositiveSmallIntegerField(_('Балл'), default=0)
    feedback = models.TextField(_('Пікір'), blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_done = models.BooleanField(_('Орындалды'), default=False)

    def __str__(self):
        return f"{self.user} {self.task.title} тақырыбындағы тапсырма"


    class Meta:
        verbose_name = _('Қолданушының тапсырмасы')
        verbose_name_plural = _('Қолданушылардың тапсырмалары')


# 🧑‍🎓 UserTest model
class UserTest(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='user_tests', verbose_name=_('Қолданушы')
    )
    user_lesson = models.ForeignKey(
        UserLesson, on_delete=models.CASCADE, related_name='user_tests',
        verbose_name=_('Қолданушының сабағы')
    )
    test = models.ForeignKey(
        Test, on_delete=models.CASCADE,
        related_name='user_tests', verbose_name=_('Тест')
    )
    score = models.PositiveIntegerField(_('Балл'), default=0)
    completed = models.BooleanField(_('Аяқталды'), default=False)

    def __str__(self):
        return f"{self.user.username} - {self.test.title} ({self.score} ұпай)"

    class Meta:
        verbose_name = _('Қолданушының тесті')
        verbose_name_plural = _('Қолданушылардың тесттері')


# UserAnswer model
class UserAnswer(models.Model):
    user_test = models.ForeignKey(
        UserTest, on_delete=models.CASCADE,
        related_name='answers', verbose_name=_('Қолданушы тесті')
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name=_('Сұрақ'), blank=True, null=True)
    answers = models.ManyToManyField(Option, verbose_name=_('Жауаптар'))
    score = models.PositiveSmallIntegerField(_('Балл'), default=0)


    class Meta:
        verbose_name = _('Қолданушының жауабы')
        verbose_name_plural = _('Қолданушылардың жауаптары')
