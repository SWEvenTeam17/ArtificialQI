from .abstract_service import AbstractService
from API.repositories import PromptRepository
from API.models import Session


class PromptService(AbstractService):
    repository = PromptRepository

    @classmethod
    def filter_by_session(cls, session: Session):
        return cls.repository.filter_by_session(session)
