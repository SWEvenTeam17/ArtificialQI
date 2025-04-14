from API.models import Session, LLM
from API.serializers import SessionSerializer
from .abstract_repository import AbstractRepository

class SessionRepository(AbstractRepository):
    model = Session
    