from .abstract_service import AbstractService
from API.repositories import EvaluationRepository

class EvaluationService(AbstractService):
    repository = EvaluationRepository