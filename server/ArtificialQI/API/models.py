from django.db import models


# Create your models here.
class Prompt(models.Model):
    prompt_text = models.TextField()
    expected_answer = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class LLM(models.Model):
    name = models.TextField()
    n_parameters = models.TextField(default="")


class Answer(models.Model):
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE)
    LLM = models.ForeignKey(LLM, on_delete=models.CASCADE)
    LLM_answer = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
