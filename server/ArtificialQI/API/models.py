"""
File contenente tutti i modelli utilizzati nel progetto
ArtificialQI, ogni modello corrisponde ad una tabella in database.
"""

from django.db import models


class LLM(models.Model):
    """
    Modello che rappresenta un LLM collegato ad ArtificialQI
    """

    name = models.CharField(max_length=255, unique=True)
    n_parameters = models.TextField(default="")
    # session = models.ForeignKey(Session, on_delete=models.CASCADE)


class Session(models.Model):
    """
    Modello che rappresenta una sessione creata in ArtificialQI,
    una sessione è un insieme di massimo 3 modelli collegati e utilizzati a scopi di benchmark.
    """

    title = models.CharField(max_length=255, unique=True)
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


class Evaluation(models.Model):
    """
    Modello che rappresenta una valutazione data da ArtificialQI
    ad una determinata risposta di un determinato modello.
    """

    semantic_evaluation = models.DecimalField(max_digits=5, decimal_places=2)
    external_evaluation = models.DecimalField(max_digits=5, decimal_places=2)


class Block(models.Model):
    """
    Modello che rappresenta un blocco di domande, è associato con i prompt tramite relazione N:N.
    """

    name = models.CharField(
        max_length=255, null=False, default="Blocco senza nome", unique=True
    )
    prompt = models.ManyToManyField(Prompt)


class Run(models.Model):
    """
    Rappresenta una singola istanza del test.
    """

    llm = models.ForeignKey(LLM, on_delete=models.CASCADE)
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE)
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
    llm_answer = models.TextField()


class BlockTest(models.Model):
    """
    Modello che rappresenta un test richiesto da un utente.
    Rappresenta la sessione di test, il blocco di domande inviato ed è collegato
    a Run tramite relazione N:N.
    """

    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    run = models.ManyToManyField(Run)
    timestamp = models.DateTimeField(auto_now_add=True)
