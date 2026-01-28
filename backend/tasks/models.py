from django.db import models
class Task(models.Model):
    subject = models.CharField(max_length=100)
    topic = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=20)
    text=models.TextField()
    correct_answer = models.CharField(max_length=255)
    hints = models.JSONField(default=list, blank=True, null=True)

def __str__(self):
    return f"{self.subject}: {self.topics}"
