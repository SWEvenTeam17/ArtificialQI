from API.repositories import PrevTestRepository, AbstractRepository
from .abstract_service import AbstractService
from typing import ClassVar


class PrevTestService(AbstractService):

    _repository: ClassVar[AbstractRepository] = PrevTestRepository

    @classmethod
    def get_tests_by_session(cls, session_id: int):
        return cls._repository.get_tests_by_session(session_id=session_id)
