"""
Repository che gestisce le istanze dei Prompt in DB.
"""

from API.models import Prompt, Session
from .abstract_repository import AbstractRepository
from typing import ClassVar
from django.db import models


class PromptRepository(AbstractRepository):
    """
    Classe del repository che gestisce le istanze dei Prompt in DB.
    """

    _model: ClassVar[models.Model] = Prompt

    @classmethod
    def filter_one(cls, prompt_text: str, expected_answer: str):
        """
        Restituisce un singolo prompt che corrisponde esattamente a
        prompt_text, expected_answer. Ritorna None se non trovato.
        """
        return cls._model.objects.filter(
            prompt_text=prompt_text,
            expected_answer=expected_answer,
        ).first()

    @classmethod
    def get_or_create(cls, prompt_text: str, expected_answer: str) -> Prompt:
        instance, _ = cls._model.objects.get_or_create(
            prompt_text=prompt_text, expected_answer=expected_answer
        )
        return instance
