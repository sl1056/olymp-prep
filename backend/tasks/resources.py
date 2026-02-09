from import_export import resources
from import_export.fields import Field
from .models import Task

class TaskResource(resources.ModelResource):
    subject_display = Field(attribute='get_subject_display', readonly=True)
    difficulty_display = Field(attribute='get_difficulty_display', readonly=True)

    class Meta:
        model = Task
        fields = (
            'id',
            'subject',
            'subject_display',
            'topic',
            'difficulty',
            'difficulty_display',
            'text',
            'correct_answer',
            'hints',
        )
        export_order = fields