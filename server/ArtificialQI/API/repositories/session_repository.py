from API.models import Session
from API.serializers import SessionSerializer
from .abstract_repository import AbstractRepository

class SessionRepository(AbstractRepository):
    model = Session
