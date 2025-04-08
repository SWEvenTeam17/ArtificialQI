from API.models import Answer
from API.serializers import AnswerSerializer
from .abstract_repository import AbstractRepository

class AnswerRepository(AbstractRepository):
    model_class = Answer
    serializer_class = AnswerSerializer