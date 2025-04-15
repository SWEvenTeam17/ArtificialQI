from .abstract_service import AbstractService
from API.repositories import PromptRepository

class PromptService(AbstractService):
    repository = PromptRepository