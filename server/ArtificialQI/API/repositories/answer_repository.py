"""
File che contiene il repository che gestisce le istanze delle Risposte in DB.
"""

from API.models import Answer
from .abstract_repository import AbstractRepository


class AnswerRepository(AbstractRepository):
    """
    Classe che contiene la definizione del repository che gestisce le istanze delle Risposte in DB.
    """

    model = Answer
