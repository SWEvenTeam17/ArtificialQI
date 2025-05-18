"""
File che contiene il repository che gestisce le istanze
delle Run in DB.
"""

from API.models import Run, LLM
from .abstract_repository import AbstractRepository
from typing import List


class RunRepository(AbstractRepository):
    """
    Classe che contiene la definizione del repository
    che gestisce le istanze delle Run in DB.
    """

    model = Run

    @classmethod
    def get_common_runs(cls, first_llm: LLM, second_llm: LLM, tables_to_join: List[str] )->List[Run]:
        return list(cls.model.objects.filter(
            llm__id__in=[first_llm.id, second_llm.id]
        ).select_related(*tables_to_join))
