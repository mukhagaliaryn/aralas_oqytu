from django.contrib import admin
from progress.models import Homework
from .models import Category, Subject, Chapter, Lesson, TextContent, VideoContent, FrameContent, \
    LessonDocs
from django_summernote.admin import SummernoteModelAdmin, SummernoteModelAdminMixin


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', )
    search_fields = ('name', 'slug', )
    ordering = ('name',)


# Subject admin
class ChapterTab(admin.TabularInline):
    model = Chapter
    extra = 1

@admin.register(Subject)
class SubjectAdmin(SummernoteModelAdmin):
    list_display = ('title', 'category', 'created_at', 'view', )
    list_filter = ('category',)
    search_fields = ('title', 'description')
    filter_horizontal = ('observers', )
    inlines = (ChapterTab, )


# Chapter admin
class LessonTab(SummernoteModelAdminMixin, admin.StackedInline):
    model = Lesson
    extra = 1

@admin.register(Chapter)
class ChapterAdmin(SummernoteModelAdmin):
    list_display = ('title', 'subject', 'order')
    list_filter = ('subject',)
    ordering = ('order',)
    inlines = (LessonTab, )


# Lesson admin
class TextContentTab(SummernoteModelAdminMixin, admin.TabularInline):
    model = TextContent
    extra = 0

class VideoContentTab(admin.TabularInline):
    model = VideoContent
    extra = 0

class FrameContentTab(admin.TabularInline):
    model = FrameContent
    extra = 0


class FileDocTab(admin.TabularInline):
    model = LessonDocs
    extra = 0


class HomeworkTab(SummernoteModelAdminMixin, admin.TabularInline):
    model = Homework
    extra = 0


@admin.register(Lesson)
class LessonAdmin(SummernoteModelAdmin):
    list_display = ('title', 'chapter', 'lesson_type', 'order')
    list_filter = ('subject', 'chapter', 'lesson_type', )
    ordering = ('chapter', 'order')
    inlines = (TextContentTab, VideoContentTab, FrameContentTab, FileDocTab, HomeworkTab, )
