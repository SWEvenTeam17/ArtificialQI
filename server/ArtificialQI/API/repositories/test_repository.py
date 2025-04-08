from API.models import Test
from API.serializers import TestSerializer
from .abstract_repository import AbstractRepository

class TestRepository(AbstractRepository):
    model_class = Test
    serializer_class = TestSerializer