"""
Repository che gestisce le istanze dei LLM in DB.
"""

from API.models import LLM, BlockTest
from .abstract_repository import AbstractRepository


class LLMRepository(AbstractRepository):
    """
    Classe del repository che gestisce le istanze dei LLM in DB.
    """

    model = LLM

    @staticmethod
    def update_or_create(name: str, parameters: str) -> bool:
        """
        Cerca un LLM con stesso nome, aggiorna i parametri se esiste
        altrimenti ne crea uno nuovo.
        """
        llm, exists = LLM.objects.get_or_create(name=name)
        if not exists or llm.n_parameters != parameters:
            llm.n_parameters = parameters
            llm.save()
        return True