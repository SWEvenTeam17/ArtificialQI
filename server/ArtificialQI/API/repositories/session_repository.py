"""
Repository che gestisce le istanze delle Sessioni in DB.
"""

from API.models import Session, LLM
from .abstract_repository import AbstractRepository


class SessionRepository(AbstractRepository):
    """
    Classe del repository che gestisce le istanze delle Sessioni in DB.
    """

    model = Session

    @classmethod
    def get_llm(cls, session_id: int):
        """
        Ritorna tutti i LLM non collegati ad una determinata sessione.
        """
        return LLM.objects.exclude(session__id=session_id).all()

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
