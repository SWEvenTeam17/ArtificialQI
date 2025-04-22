from API.models import Evaluation
from API.serializers import EvaluationSerializer
from .abstract_repository import AbstractRepository


class EvaluationRepository(AbstractRepository):
    model = Evaluation
