from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import UserSubject, UserLesson, UserTest, UserAnswer, UseTask


# UserSubject admin
# ----------------------------------------------------------------------------------------------------------------------
@admin.register(UserSubject)
class UserSubjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'created_at', 'completed', 'total_percent', )
    list_filter = ('user', 'subject', 'completed', )
    search_fields = ('user__username', 'subject__title')


# UserLesson admin
# ----------------------------------------------------------------------------------------------------------------------
@admin.register(UserLesson)
class UserLessonAdmin(admin.ModelAdmin):
    list_display = ('user_subject', 'lesson', 'lesson_score', 'completed', 'completed_at', 'is_open',)
    list_filter = ('user_subject', 'lesson', 'completed', )
    search_fields = ('user_subject__user__username', 'lesson__title')



# UserTask admin
# ----------------------------------------------------------------------------------------------------------------------
@admin.register(UseTask)
class UserTaskAdmin(SummernoteModelAdmin):
    list_display = ('user', 'task', 'grade', 'is_done',)
    list_filter = ('task', 'user', 'is_done',)
    search_fields = ('user__username', 'task__title')


# UserTest admin
# ----------------------------------------------------------------------------------------------------------------------
class UserAnswerTab(admin.TabularInline):
    model = UserAnswer
    extra = 0


@admin.register(UserTest)
class UserTestAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'score', 'completed',)
    list_filter = ('completed',)
    search_fields = ('user__username', 'test__title')
    inlines = (UserAnswerTab, )



