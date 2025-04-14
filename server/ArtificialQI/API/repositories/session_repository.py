from API.models import Session, LLM
from .abstract_repository import AbstractRepository

class SessionRepository(AbstractRepository):
    model = Session

    @classmethod
    def get_llm(cls, session_id: int):
        return LLM.objects.exclude(session__id=session_id).all()

    @classmethod
    def add_llm(cls, session: Session, llm: LLM):
        session.llm.add(llm)
        session.save()
        return llm
    
    @classmethod
    def delete_llm(cls, session: Session, llm: LLM):
        session.llm.remove(llm)