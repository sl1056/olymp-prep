from django.contrib import admin

<<<<<<< Updated upstream
# Register your models here.
=======
@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'player1', 'player2', 'get_subject', 'status',
        'questions_count', 'current_question_index',
        'timer_enabled', 'hints_enabled', 'random_order', 'is_private',
        'player1_score', 'player2_score',
        'created_at', 'finished_at'
    )
    list_filter = ('status', 'created_at', 'task__subject')
    search_fields = ('player1__username', 'player2__username', 'task__topic')
    readonly_fields = ('created_at', 'started_at', 'finished_at')
    fields = (
        'player1', 'player2', 'status',
        'task', 'questions_count', 'current_question_index',
        'question_task_ids',
        'timer_enabled', 'time_limit_seconds', 'current_question_started_at',
        'hints_enabled', 'random_order', 'is_private', 'private_token',
        'player1_score', 'player2_score',
        'created_at', 'started_at', 'finished_at',
        'player1_answer', 'player2_answer',
        'player1_correct', 'player2_correct'
    )

    def get_subject(self, obj):
        return obj.task.get_subject_display() if obj.task else "-"
    get_subject.short_description = 'Предмет'
    get_subject.admin_order_field = 'task__subject'
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
