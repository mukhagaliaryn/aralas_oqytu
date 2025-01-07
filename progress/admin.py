from django.contrib import admin
from .models import UserSubject, UserLesson, Comment, UserTest, UserAnswer


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


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'author', 'created_at', 'content')
    search_fields = ('author', 'content')
    list_filter = ('lesson', 'created_at')


class UserAnswerTab(admin.TabularInline):
    model = UserAnswer
    extra = 0


@admin.register(UserTest)
class UserTestAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'score', 'completed', 'submitted_at')
    list_filter = ('completed', 'submitted_at')
    search_fields = ('user__username', 'test__title')
