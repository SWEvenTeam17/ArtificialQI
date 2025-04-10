from API.services import AbstractService
from API.repositories import AnswerRepository

class PromptService(AbstractService):
    repository = AnswerRepository