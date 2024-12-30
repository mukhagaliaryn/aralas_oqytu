from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import UserSubject, UserLesson, UserHomework, Homework, Comment


@admin.register(UserSubject)
class UserSubjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'created_at')
    list_filter = ('user', 'subject')
    search_fields = ('user__username', 'subject__title')


@admin.register(UserLesson)
class UserLessonAdmin(admin.ModelAdmin):
    list_display = ('user_subject', 'lesson', 'lesson_score', 'completed', 'completed_at')
    list_filter = ('completed', )
    search_fields = ('user_subject__user__username', 'lesson__title')


class UserHomeworkTab(admin.TabularInline):
    model = UserHomework
    extra = 0

@admin.register(Homework)
class HomeworkAdmin(SummernoteModelAdmin):
    list_display = ('title', 'lesson', )
    search_fields = ('title',)
    list_filter = ('lesson', )

    inlines = (UserHomeworkTab, )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'author', 'created_at', 'content')
    search_fields = ('author', 'content')
    list_filter = ('lesson', 'created_at')