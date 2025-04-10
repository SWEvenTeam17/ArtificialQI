from API.services import AbstractService
from API.repositories import SessionRepository

class SessionService(AbstractService):
    repository = SessionRepository