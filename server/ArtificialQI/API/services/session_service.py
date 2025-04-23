"""
File che contiene i servizi riguardanti le sessioni.
"""

from API.repositories import SessionRepository
from API.models import Session, LLM
from .abstract_service import AbstractService


class SessionService(AbstractService):
    """
    Classe che contiene i servizi riguardanti le sessioni.
    """

    repository = SessionRepository

    @classmethod
    def get_llm(cls, session_id: int):
        """
        Funzione che ritorna tutti i LLM connessi ad una sessione.
        """
        try:
            return cls.repository.get_llm(session_id=session_id)
        except Session.DoesNotExist:
            return "Session not found"
        except LLM.DoesNotExist:
            return "LLM not found"

    @classmethod
    def add_llm(cls, session_id: int, llm_id: int) -> LLM | str:
        """
        Funzione che aggiunge un LLM ad una sessione.
        """
        try:
            session = Session.objects.get(id=session_id)
            llm = LLM.objects.get(id=llm_id)
            return cls.repository.add_llm(session, llm)
        except Session.DoesNotExist:
            return "Session not found"
        except LLM.DoesNotExist:
            return "LLM not found"

    @classmethod
    def delete_llm(cls, session_id: int, llm_id: int) -> None | str:
        """
        Funzione che rimuove un LLM da una sessione.
        """
        try:
            session = Session.objects.get(id=session_id)
            llm = LLM.objects.get(id=llm_id)
            return cls.repository.delete_llm(session, llm)
        except Session.DoesNotExist:
            return "Session not found"
        except LLM.DoesNotExist:
            return "LLM not found"
