from django.db import models
from accounts.models import User
from main.models import Subject, Lesson, Test, Question, Option
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
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'subject')
        verbose_name = _('Қолданушының курсы')
        verbose_name_plural = _('Қолданушының курстары')

    def __str__(self):
        return f"{self.user} - {self.subject.title}"


# UserLesson model
class UserLesson(models.Model):
    user_subject = models.ForeignKey(
        UserSubject, on_delete=models.CASCADE,
        verbose_name=_('Қолданушының курсы'), related_name="user_lessons")
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE,
        verbose_name=_('Сабақ'), related_name="user_lessons"
    )
    lesson_score = models.DecimalField(_('Сабақтың баллы'), max_digits=5, decimal_places=2, default=0)
    completed = models.BooleanField(_('Орындалды'), default=False)
    completed_at = models.DateTimeField(_('Орындалған уақыты'), blank=True, null=True)

    class Meta:
        unique_together = ('user_subject', 'lesson')
        verbose_name = _('Қолданушының сабағы')
        verbose_name_plural = _('Қолданушылардың сабақтары')

    def __str__(self):
        return f"{self.user_subject.user} - {self.lesson.title} - {'Орындалды' if self.completed else 'Процессте'}"


# Homework model
class Homework(models.Model):
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE,
        verbose_name=_('Сабақ'), related_name='homeworks'
    )
    title = models.CharField(_('Тақырыбы'), max_length=255)
    content = models.TextField(_('Тапсырма мәтіні'), blank=True, null=True)
    file = models.FileField(_('Тапсырма құжаты'), upload_to='main/subject/homeworks/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.lesson.title} тақырыбындағы үй тапсырмасы"

    class Meta:
        verbose_name = _('Үй жұмысы')
        verbose_name_plural = _('Үй жұмыстары')


# UserHomework model
class UserHomework(models.Model):
    homework = models.ForeignKey(
        Homework, on_delete=models.PROTECT, related_name='user_homeworks',
        verbose_name=_('Үй жұмысы')
    )
    user_lesson = models.ForeignKey(
        UserLesson, on_delete=models.CASCADE, related_name='user_homeworks',
        verbose_name=_('Үй жұмысы')
    )
    student = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name=_('Білім алушы'), related_name='homeworks'
    )
    submission = models.FileField(_('Тапсырма'), upload_to='main/subject/user/homeworks/')
    grade = models.DecimalField(_('Балл'), max_digits=5, decimal_places=2, default=0)
    feedback = models.TextField(_('Пікір'), blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_done = models.BooleanField(_('Орындалды'), default=False)

    def __str__(self):
        return f"{self.student} {self.homework.title} тақырыбындағы үй жұмысы"

    class Meta:
        verbose_name = _('Қолданушының үй жұмысы')
        verbose_name_plural = _('Қолданушылардың үй жұмыстары')


# 🧑‍🎓 UserTest model
class UserTest(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='user_tests', verbose_name=_('Қолданушы')
    )
    test = models.ForeignKey(
        Test, on_delete=models.CASCADE,
        related_name='user_tests', verbose_name=_('Тест')
    )
    score = models.PositiveIntegerField(_('Балл'), default=0)
    completed = models.BooleanField(_('Аяқталды'), default=False)
    submitted_at = models.DateTimeField(_('Жіберілген уақыт'), auto_now_add=True)

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
    answers = models.ManyToManyField(Option, verbose_name=_('Жауаптар'))
    score = models.PositiveSmallIntegerField(_('Балл'), default=0)

    def calculate_score(self):
        correct_answers = self.question.options.filter(is_correct=True)
        selected_correct_answers = self.answers.filter(is_correct=True)

        if set(correct_answers) == set(selected_correct_answers):
            self.score = self.question.test.total_score // self.question.test.questions.count()
        else:
            self.score = 0

        self.save()

    def __str__(self):
        return f"{self.user_test.user.username} - {self.question.text} ({self.score} ұпай)"


    class Meta:
        verbose_name = _('Қолданушының жауабы')
        verbose_name_plural = _('Қолданушылардың жауаптары')


# Comment model
class Comment(models.Model):
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE,
        verbose_name=_('Сабақ'), related_name='comments'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name=_('Авторы'), related_name='comments'
    )
    content = models.TextField(_('Пікір'))
    score = models.PositiveSmallIntegerField(_('Балл'), default=0)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.author} {self.lesson.title} сабағына берген пікірі"

    class Meta:
        verbose_name = _('Қолданушы пікірі')
        verbose_name_plural = _('Қолданушылар пікірлері')
