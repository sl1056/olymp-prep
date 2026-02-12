# tasks/admin.py
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin  # ← импорт
from .models import Task
from .resources import TaskResource


@admin.register(Task)
class TaskAdmin(ImportExportModelAdmin):
    resource_class = TaskResource

    list_display = ('id', 'subject', 'topic', 'difficulty')
    list_filter = ('subject', 'topic', 'difficulty')
    search_fields = ('text', 'topic', 'subject')

    fields = (
        'subject',
        'topic',
        'difficulty',
        'text',
        'correct_answer',
        'hints'
    )
    ordering = ('-id',)