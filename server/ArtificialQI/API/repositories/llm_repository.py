from API.models import LLM
from API.serializers import LLMSerializer
from .abstract_repository import AbstractRepository

class LLMRepository(AbstractRepository):
    model = LLM
