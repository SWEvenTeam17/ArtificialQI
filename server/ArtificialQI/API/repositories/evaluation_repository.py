from API.models import Evaluation
from API.serializers import EvaluationSerializer
from .abstract_repository import AbstractRepository

class EvaluationRepository(AbstractRepository):
    model_class = Evaluation
    serializer_class = EvaluationSerializer