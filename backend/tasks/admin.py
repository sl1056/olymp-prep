from django.contrib import admin
from .models import Task
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
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
    # readonly_fields = ()
    ordering = ('-id',)