from API.models import Answer
from .abstract_repository import AbstractRepository

class AnswerRepository(AbstractRepository):
    model = Answer
