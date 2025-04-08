from API.models import Prompt
from API.serializers import PromptSerializer
from .abstract_repository import AbstractRepository

class PromptRepository(AbstractRepository):
    model_class = Prompt
    serializer_class = PromptSerializer