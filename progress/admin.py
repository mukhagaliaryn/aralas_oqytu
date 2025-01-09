from django.contrib import admin
from main.models import Task
from .models import UserSubject, UserLesson, Comment, UserTest, UserAnswer, UseTask


# UserSubject admin
@admin.register(UserSubject)
class UserSubjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'created_at')
    list_filter = ('user', 'subject')
    search_fields = ('user__username', 'subject__title')


# UserLesson admin
@admin.register(UserLesson)
class UserLessonAdmin(admin.ModelAdmin):
    list_display = ('user_subject', 'lesson', 'lesson_score', 'completed', 'completed_at')
    list_filter = ('completed', )
    search_fields = ('user_subject__user__username', 'lesson__title')


# Comment admin
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'author', 'created_at', 'content')
    search_fields = ('author', 'content')
    list_filter = ('lesson', 'created_at')


# Task admin
class UserTaskTab(admin.TabularInline):
    model = UseTask
    extra = 0


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'total_score', )
    inlines = (UserTaskTab, )


# UserTest admin
class UserAnswerTab(admin.TabularInline):
    model = UserAnswer
    extra = 0


@admin.register(UserTest)
class UserTestAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'score', 'completed',)
    list_filter = ('completed',)
    search_fields = ('user__username', 'test__title')
