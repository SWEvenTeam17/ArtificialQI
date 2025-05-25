from .abstract_repository import AbstractRepository
from API.models import BlockTest

class PrevTestRepository(AbstractRepository):

    model = BlockTest

    @classmethod
    def get_tests_by_session(cls, session_id: int):
        return cls.model.objects.filter(session_id=session_id)