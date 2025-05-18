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

    @classmethod
    def filter_one(cls, prompt_text: str, expected_answer: str):
        """
        Restituisce un singolo prompt che corrisponde esattamente a
        prompt_text, expected_answer e session. Ritorna None se non trovato.
        """
        return cls.model.objects.filter(
            prompt_text=prompt_text,
            expected_answer=expected_answer,
        ).first()

    @classmethod
    def get_or_create(cls, prompt_text: str, expected_answer: str) -> Prompt:
        instance, _ = cls.model.objects.get_or_create(
            prompt_text=prompt_text, expected_answer=expected_answer
        )
        return instance
