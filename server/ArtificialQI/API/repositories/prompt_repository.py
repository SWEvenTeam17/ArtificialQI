from API.models import Prompt
from API.serializers import PromptSerializer
from .abstract_repository import AbstractRepository

class PromptRepository(AbstractRepository):
    model = Prompt
