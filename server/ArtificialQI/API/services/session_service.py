from .abstract_service import AbstractService
from API.repositories import SessionRepository

class SessionService(AbstractService):
    repository = SessionRepository