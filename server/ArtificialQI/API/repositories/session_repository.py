"""
Repository che gestisce le istanze delle Sessioni in DB.
"""

from typing import ClassVar

from django.db import models

from API.models import LLM, BlockTest, Session

from .abstract_repository import AbstractRepository


class SessionRepository(AbstractRepository):
    """
    Classe del repository che gestisce le istanze delle Sessioni in DB.
    """

    _model: ClassVar[models.Model] = Session

    @classmethod
    def get_remaining_llm(cls, session_id: int):
        """
        Ritorna tutti i LLM non collegati ad una determinata sessione.
        """
        return LLM.objects.exclude(session__id=session_id).all()

    @staticmethod
    def get_llms(session: Session):
        return list(session.llm.all())

    @classmethod
    def add_llm(cls, session: Session, llm: LLM) -> LLM:
        """
        Aggiunge un collegamento LLM-Sessione.
        """
        session.llm.add(llm)
        session.save()
        return llm

    @classmethod
    def delete_llm(cls, session: Session, llm: LLM) -> None:
        """
        Rimuove un collegamento LLM-Sessione.
        """
        session.llm.remove(llm)

    @classmethod
    def get_tests_by_session(cls, session_id: int):
        return BlockTest.objects.filter(session_id=session_id)
