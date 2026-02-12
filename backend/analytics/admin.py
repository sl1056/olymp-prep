from django.contrib import admin
from .models import TaskAttempt
from tasks.models import Task

@admin.register(TaskAttempt)
class TaskAttemptAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'task', 'is_correct',
        'get_subject_display', 'get_difficulty_display', 'submitted_at'
    )
    list_filter = ('user', 'subject', 'difficulty', 'is_correct', 'submitted_at')
    search_fields = ('user__username', 'task__text')
    readonly_fields = ('submitted_at',)
    ordering = ('-submitted_at',)

    def get_subject_display(self, obj):
        return dict(Task.SUBJECTS).get(obj.subject, obj.subject)

    get_subject_display.short_description = 'Предмет'

    def get_difficulty_display(self, obj):
        return dict(Task.DIFFICULTY_CHOICES).get(obj.difficulty, obj.difficulty)

    get_difficulty_display.short_description = 'Сложность'