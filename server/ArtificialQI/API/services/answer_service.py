from .abstract_service import AbstractService
from API.repositories import AnswerRepository

class AnswerService(AbstractService):
    repository = AnswerRepository