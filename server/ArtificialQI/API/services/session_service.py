"""
File che contiene i servizi riguardanti le sessioni.
"""

from API.repositories import SessionRepository, LLMRepository
from API.models import LLM
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
        return cls.repository.get_llm(session_id=session_id)

    @classmethod
    def add_llm(cls, session_id: int, llm_id: int) -> LLM | str:
        """
        Funzione che aggiunge un LLM ad una sessione.
        """
        session = cls.repository.get_by_id(session_id)
        llm = LLMRepository.get_by_id(llm_id)
        return cls.repository.add_llm(session, llm)

    @classmethod
    def delete_llm(cls, session_id: int, llm_id: int) -> None | str:
        """
        Funzione che rimuove un LLM da una sessione.
        """
        session = cls.repository.get_by_id(session_id)
        llm = LLMRepository.get_by_id(llm_id)
        return cls.repository.delete_llm(session, llm)
