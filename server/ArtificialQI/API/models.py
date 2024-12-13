from django.db import models

# Create your models here.
class Question(models.Model):
    question = models.TextField()
    expected_answer = models.TextField()

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    LLM_answer = models.TextField()