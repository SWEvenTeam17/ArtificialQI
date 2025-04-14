from .abstract_service import AbstractService
from API.repositories import SessionRepository
from API.models import Session, LLM

class SessionService(AbstractService):
    repository = SessionRepository

    @classmethod
    def get_llm(cls, session_id: int):
        try:
            return cls.repository.get_llm(session_id=session_id)
        except Session.DoesNotExist:
            return "Session not found"
        except LLM.DoesNotExist:
            return "LLM not found"

    @classmethod
    def add_llm(cls, session_id: int, llm_id: int):
        try:
            session = Session.objects.get(id=session_id)
            llm = LLM.objects.get(id=llm_id)
            return cls.repository.add_llm(session, llm)
        except Session.DoesNotExist:
            return "Session not found"
        except LLM.DoesNotExist:
            return "LLM not found"
    
    @classmethod
    def delete_llm(cls, session_id: int, llm_id: int):
        try:
            session = Session.objects.get(id=session_id)
            llm = LLM.objects.get(id=llm_id)
            cls.repository.delete_llm(session, llm)
        except Session.DoesNotExist:
            return "Session not found"
        except LLM.DoesNotExist:
            return "LLM not found"
