"""
File che contiene il repository che gestisce le istanze
delle Valutazioni in DB.
"""

from API.models import Evaluation
from .abstract_repository import AbstractRepository
from typing import ClassVar
from django.db import models

class EvaluationRepository(AbstractRepository):
    """
    Classe che contiene la definizione del repository
    che gestisce le istanze delle Valutazioni in DB.
    """

    _model: ClassVar[models.Model] = Evaluation
