"""
File che contiene i servizi riguardanti le sessioni.
"""

from typing import ClassVar

from API.models import LLM
from API.repositories import (AbstractRepository, LLMRepository,
                              SessionRepository)

from .abstract_service import AbstractService


class SessionService(AbstractService):
    """
    Classe che contiene i servizi riguardanti le sessioni.
    """

    _repository: ClassVar[AbstractRepository] = SessionRepository

    @classmethod
    def get_excluded_llm(cls, session_id: int):
        """
        Funzione che ritorna tutti i LLM  non connessi ad una sessione.
        """
        return cls._repository.get_remaining_llm(session_id=session_id)

    @classmethod
    def add_llm(cls, session_id: int, llm_id: int) -> LLM | str:
        """
        Funzione che aggiunge un LLM ad una sessione.
        """
        session = cls._repository.get_by_id(session_id)
        llm = LLMRepository.get_by_id(llm_id)
        return cls._repository.add_llm(session, llm)

    @classmethod
    def delete_llm(cls, session_id: int, llm_id: int) -> None | str:
        """
        Funzione che rimuove un LLM da una sessione.
        """
        session = cls._repository.get_by_id(session_id)
        llm = LLMRepository.get_by_id(llm_id)
        return cls._repository.delete_llm(session, llm)

    @classmethod
    def get_tests_by_session(cls, session_id: int):
        return cls._repository.get_tests_by_session(session_id=session_id)
