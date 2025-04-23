"""
Repository che gestisce le istanze dei Prompt in DB.
"""

from API.models import Prompt, Session
from .abstract_repository import AbstractRepository


class PromptRepository(AbstractRepository):
    """
    Classe del repository che gestisce le istanze dei Prompt in DB.
    """

    model = Prompt

    @classmethod
    def filter_by_session(cls, session: Session):
        """
        Funzione che filtra i prompt per sessione, ritorna tutti i prompt
        usati in una determinata sessione.
        """
        return cls.model.objects.filter(session=session)
