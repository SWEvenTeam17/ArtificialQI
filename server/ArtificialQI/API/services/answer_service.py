from API.services import AbstractService
from API.repositories import AnswerRepository

class AnswerService(AbstractService):
    repository = AnswerRepository