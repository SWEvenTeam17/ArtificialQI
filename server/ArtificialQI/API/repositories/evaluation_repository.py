"""
File che contiene il repository che gestisce le istanze
delle Valutazioni in DB.
"""

from API.models import Evaluation
from .abstract_repository import AbstractRepository


class EvaluationRepository(AbstractRepository):
    """
    Classe che contiene la definizione del repository
    che gestisce le istanze delle Valutazioni in DB.
    """

    model = Evaluation
