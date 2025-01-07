from django.db import models
from django.utils.translation import gettext_lazy as _


# Subject model
class Subject(models.Model):
    title = models.CharField(_('Тақырыбы'), max_length=255)
    poster = models.ImageField(_('Постер'), blank=True, null=True, upload_to='main/subject/posters')
    description = models.TextField(_('Анықтамасы'), blank=True, null=True)
    created_at = models.DateTimeField(_('Уақыты'), auto_now_add=True)
    view = models.PositiveIntegerField(_('Қаралым'), default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Курс')
        verbose_name_plural = _('Курстар')
        ordering = ('created_at', )


# Chapter model
class Chapter(models.Model):
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE,
        verbose_name=_('Курс'), related_name="chapters"
    )
    title = models.CharField(_('Тақырыбы'), max_length=255)
    order = models.PositiveIntegerField(_('Order'))

    def __str__(self):
        return f"{self.subject.title}: {self.order}-модуль:{self.title}"

    class Meta:
        verbose_name = _('Модуль')
        verbose_name_plural = _('Модульдер')


# Lesson model
class Lesson(models.Model):
    LESSON_TYPE = (
        ('theory', _('Теориялық сабақ')),
        ('practice', _('Практикалық сабақ')),
    )
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE,
        verbose_name=_('Курс'), related_name="lessons", null=True, blank=True
    )
    chapter = models.ForeignKey(
        Chapter, on_delete=models.CASCADE,
        verbose_name=_('Модуль'), related_name="lessons"
    )
    title = models.CharField(_('Тақырыбы'), max_length=255)
    lesson_type = models.CharField(_('Сабақтың түрі'), choices=LESSON_TYPE, max_length=255)
    description = models.TextField(_('Анықтамасы'), blank=True, null=True)
    order = models.PositiveIntegerField(_('Order'), default=0)
    duration = models.PositiveSmallIntegerField(_('Сабақтың уақыты (мин)'), default=0)

    def __str__(self):
        return f"{self.title} ({self.chapter.title})"

    class Meta:
        verbose_name = _('Сабақ')
        verbose_name_plural = _('Сабақтар')


# LessonDoc model
class LessonDocs(models.Model):
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE,
        verbose_name=_('Сабақ'), related_name="docs"
    )
    title = models.CharField(_('Тақырыбы'), max_length=255)
    file = models.FileField(_('Файл'), upload_to='main/lesson/docs/', blank=True, null=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = _('Сабақ құжаты')
        verbose_name_plural = _('Сабақ құжаттары')


# TextContent model
class TextContent(models.Model):
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE,
        verbose_name=_('Сабақ'), related_name="text_contents"
    )
    content = models.TextField(_('Мәтін'))

    def __str__(self):
        return f"Мәтінді контент: {self.lesson.title}"

    class Meta:
        verbose_name = _('Мәтін контент')
        verbose_name_plural = _('Мәтін контенттер')


# VideoContent model
class VideoContent(models.Model):
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE,
        verbose_name=_('Сабақ'), related_name="video_contents"
    )
    url = models.URLField(_('URL сілтеме'))
    duration = models.PositiveSmallIntegerField(_('Видео уақыт'), default=0)

    def __str__(self):
        return f"Видеоконтент: {self.lesson.title}"

    class Meta:
        verbose_name = _('Видео контент')
        verbose_name_plural = _('Видео контенттер')


# Test content
class Test(models.Model):
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE,
        related_name='tests', verbose_name=_('Сабақ')
    )
    title = models.CharField(_('Тақырыбы'), max_length=255)
    description = models.TextField(_('Тест сипаттамасы'), blank=True, null=True)
    total_score = models.PositiveIntegerField(_('Жалпы балл'), default=100)

    def __str__(self):
        return f"{self.title} ({self.lesson.title})"

    class Meta:
        verbose_name = _('Тест')
        verbose_name_plural = _('Тесттер')


# Question model
class Question(models.Model):
    test = models.ForeignKey(
        Test, on_delete=models.CASCADE,
        related_name='questions', verbose_name=_('Тест')
    )
    text = models.CharField(_('Сұрақ мәтіні'), max_length=500)
    order = models.PositiveIntegerField(_('Реті'), default=0)

    def __str__(self):
        return f"{self.text} ({self.test.title})"

    class Meta:
        verbose_name = _('Сұрақ')
        verbose_name_plural = _('Сұрақтар')
        ordering = ['order']


# Option model
class Option(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE,
        related_name='options', verbose_name=_('Сұрақ')
    )
    text = models.TextField(_('Жауап мәтіні'), max_length=255)
    is_correct = models.BooleanField(_('Дұрыс жауап'), default=False)

    def __str__(self):
        return f"{self.text} ({'Дұрыс' if self.is_correct else 'Қате'})"

    class Meta:
        verbose_name = _('Жауап нұсқасы')
        verbose_name_plural = _('Жауап нұсқалары')
