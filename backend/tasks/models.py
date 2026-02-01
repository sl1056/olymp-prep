from django.db import models
class Task(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Лёгкий'),
        ('medium', 'Средний'),
        ('hard', 'Сложный'),
    ]
    SUBJECTS = [
        ('math', 'Математика')
        ('geom', 'Геометрия')
        ('d_math', 'Дискретная Математика')
        ('phys', 'Физика')
        ('chem', 'Химия')
        ('bio', 'Биология')
        ('eco', 'Экология')
        ('geo', 'География')
        ('astro', 'Астрономия')
        ('rus_lang', 'Русский язык')
        ('rus_lit', 'Литература')
        ('eng_lang', 'Английский язык')
        ('d_lang', 'Немецкий язык')
        ('fr_lang', 'Французский язык')
        ('chi_lang', 'Китайский язык')
        ('sp_lang', 'Испанский язык')
        ('lat_lang', 'Латинский язык')
        ('hist', 'История')
        ('s_st', 'Обществознание')
        ('law', 'Право')
        ('econ', 'Экономика')
        ('fin_lit', 'Финансовая грамотность')
        ('arts', 'Искусство (МХК)')
        ('tech', 'Технология')
        ('pc_sci', 'Информатика')
        ('robot', 'Робототехника')
        ('ai', 'Искусственный интеллект')
        ('pe', 'Физкультура')
        ('obzr', 'ОБЖ')
    ]
    subject = models.CharField(max_length=100, choices=SUBJECTS, default='math')
    topic = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='medium')
    text=models.TextField()
    correct_answer = models.CharField(max_length=255)
    hints = models.JSONField(default=list, blank=True, null=True)

def __str__(self):
    return f"{self.subject}: {self.topic}"


