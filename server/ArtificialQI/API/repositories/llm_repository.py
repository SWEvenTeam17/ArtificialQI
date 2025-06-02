"""
Repository che gestisce le istanze dei LLM in DB.
"""

from API.models import LLM
from .abstract_repository import AbstractRepository
from typing import ClassVar
from django.db import models

class LLMRepository(AbstractRepository):
    """
    Classe del repository che gestisce le istanze dei LLM in DB.
    """

    _model: ClassVar[models.Model] = LLM

    @classmethod
    def update_or_create(cls, name: str, parameters: str) -> bool:
        """
        Cerca un LLM con stesso nome, aggiorna i parametri se esiste
        altrimenti ne crea uno nuovo.
        """
        llm, exists = cls._model.objects.get_or_create(name=name)
        if not exists or llm.n_parameters != parameters:
            llm.n_parameters = parameters
            llm.save()
        return True