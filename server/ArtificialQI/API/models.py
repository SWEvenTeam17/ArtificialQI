from django.db import models


class Session(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Prompt(models.Model):
    prompt_text = models.TextField()
    expected_answer = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)


class LLM(models.Model):
    name = models.TextField()
    n_parameters = models.TextField(default="")
    session = models.ForeignKey(Session, on_delete=models.CASCADE)


class Answer(models.Model):
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE)
    LLM = models.ForeignKey(LLM, on_delete=models.CASCADE)
    LLM_answer = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
