"""
File che contiene il repository che gestisce le istanze
delle Run in DB.
"""

from typing import ClassVar, List

from django.db import models

from API.models import LLM, Run

from .abstract_repository import AbstractRepository


class RunRepository(AbstractRepository):
    """
    Classe che contiene la definizione del repository
    che gestisce le istanze delle Run in DB.
    """

    _model: ClassVar[models.Model] = Run

    @classmethod
    def get_common_runs(
        cls, first_llm: LLM, second_llm: LLM, tables_to_join: List[str]
    ) -> List[Run]:
        return list(
            cls._model.objects.filter(
                llm__id__in=[first_llm.id, second_llm.id]
            ).select_related(*tables_to_join)
        )

    @classmethod
    def get_by_prompt(cls, prompt_id: int):
        return cls._model.objects.filter(prompt__id=prompt_id).select_related(
            "llm", "prompt", "evaluation"
        )
