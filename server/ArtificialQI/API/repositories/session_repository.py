"""
Repository che gestisce le istanze delle Sessioni in DB.
"""

from API.models import Session, LLM
from .abstract_repository import AbstractRepository
from typing import ClassVar
from django.db import models


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
