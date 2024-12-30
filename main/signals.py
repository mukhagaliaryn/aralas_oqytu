from django.db.models.signals import post_save
from django.dispatch import receiver
from progress.models import UserSubject, UserLesson
from .models import Lesson


@receiver(post_save, sender=Lesson)
def create_or_update_user_lessons(sender, instance, created, **kwargs):
    user_subjects = UserSubject.objects.filter(subject=instance.subject)

    for user_subject in user_subjects:
        user_lesson, lesson_created = UserLesson.objects.get_or_create(
            user_subject=user_subject,
            lesson=instance
        )
        if created or lesson_created:
            user_lesson.completed = False
            user_lesson.save()