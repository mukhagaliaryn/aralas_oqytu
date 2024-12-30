from email.policy import default

from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User


# Category model
class Category(models.Model):
    name = models.CharField(_('Атауы'), max_length=255)
    slug = models.SlugField(_('Кілттік атауы'), max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категориялар')


# Subject model
class Subject(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        verbose_name=_('Категория'), related_name="subjects"
    )
    title = models.CharField(_('Тақырыбы'), max_length=255)
    poster = models.ImageField(_('Постер'), blank=True, null=True, upload_to='main/subject/posters')
    description = models.TextField(_('Анықтамасы'), blank=True, null=True)
    observers = models.ManyToManyField(User, verbose_name=_('Жазылушылар'), related_name='access_subjects', blank=True)
    created_at = models.DateTimeField(_('Уақыты'), auto_now_add=True)
    view = models.PositiveIntegerField(_('Қаралым'), default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Курс')
        verbose_name_plural = _('Курстар')
        ordering = ('-created_at', )


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


# FrameContent model
class FrameContent(models.Model):
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE,
        verbose_name=_('Сабақ'), related_name="frame_contents"
    )
    url = models.TextField(_('URL сілтеме'))

    def __str__(self):
        return f"Фреймконтент: {self.lesson.title}"

    class Meta:
        verbose_name = _('Фрейм контент')
        verbose_name_plural = _('Фрейм контенттер')
