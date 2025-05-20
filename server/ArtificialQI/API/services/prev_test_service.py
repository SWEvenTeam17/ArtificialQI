from API.repositories import PrevTestRepository
from .abstract_service import AbstractService

class PrevTestService(AbstractService):

    repository = PrevTestRepository

    @classmethod
    def get_tests_by_session(cls, session_id: int):
        return cls.repository.get_tests_by_session(session_id=session_id)