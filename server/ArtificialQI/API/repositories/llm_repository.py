from API.models import LLM
from API.serializers import LLMSerializer
from .abstract_repository import AbstractRepository

class LLMRepository(AbstractRepository):
    model = LLM

    @staticmethod 
    def update_or_create(name: str, parameters: str)->bool:
        llm, exists = LLM.objects.get_or_create(name=name)
        if not exists or llm.n_parameters != parameters:
            llm.n_parameters = parameters
            llm.save()
        return True
