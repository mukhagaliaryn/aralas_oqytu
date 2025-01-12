from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_TYPE = (
        ('student', _('Білім алушы')),
        ('teacher', _('Оқытушы')),
    )

    avatar = models.ImageField(
        _('Пайдаланушы суреті'), upload_to='accounts/avatars/', null=True, blank=True,
        help_text=_('Сурет шаршы форматта болуы керек. Мысалы: (512x512)px')
    )
    user_type = models.CharField(_('Пайдаланушы түрі'), choices=USER_TYPE, default='student', max_length=128)
    profession = models.CharField(_('Профессия'), max_length=128, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = _('Пайдаланушы')
        verbose_name_plural = _('Пайдаланушылар')


# Content model
class Content(models.Model):
    title = models.CharField(_('Тақырыбы'), max_length=128)
    video = models.FileField(_('Видео'), upload_to='accounts/content/videos/', blank=True, null=True)
    body = models.TextField(_('Мәтіні'), blank=True, null=True)
    order = models.PositiveSmallIntegerField(_('Реттілік'), default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Контент')
        verbose_name_plural = _('Контенттер')
        ordering = ('order', )
