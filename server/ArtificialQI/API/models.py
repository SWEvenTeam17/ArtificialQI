"""
File contenente tutti i modelli utilizzati nel progetto
ArtificialQI, ogni modello corrisponde ad una tabella in database.
"""
from django.db import models

class LLM(models.Model):
    """
    Modello che rappresenta un LLM collegato ad ArtificialQI
    """
    name = models.TextField()
    n_parameters = models.TextField(default="")
    # session = models.ForeignKey(Session, on_delete=models.CASCADE)


class Session(models.Model):
    """
    Modello che rappresenta una sessione creata in ArtificialQI,
    una sessione è un insieme di massimo 3 modelli collegati e utilizzati a scopi di benchmark.
    """
    title = models.CharField(max_length=255)
    description = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    llm = models.ManyToManyField(LLM)


class Prompt(models.Model):
    """
    Modello che rappresenta una coppia domanda/risposta attesa.
    """
    prompt_text = models.TextField()
    expected_answer = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)


class Answer(models.Model):
    """
    Modello che rappresenta una risposta di un LLM ad un determinato prompt.
    """
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE)
    LLM = models.ForeignKey(LLM, on_delete=models.CASCADE)
    LLM_answer = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Evaluation(models.Model):
    """
    Modello che rappresenta una valutazione data da ArtificialQI
    ad una determinata risposta di un determinato modello.
    """
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE)
    llm = models.ForeignKey(LLM, on_delete=models.CASCADE)
    semantic_evaluation = models.DecimalField(max_digits=5, decimal_places=2)
    external_evaluation = models.DecimalField(max_digits=5, decimal_places=2)
