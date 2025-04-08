from API.models import LLM
from API.serializers import LLMSerializer
from .abstract_repository import AbstractRepository

class LLMRepository(AbstractRepository):
    model_class = LLM
    serializer_class = LLMSerializer

    @staticmethod 
    def update_or_create(name, parameters)->bool:
        llm, exists = LLM.objects.get_or_create(name=name)
        if not exists or llm.n_parameters != parameters:
            llm.n_parameters = parameters
            llm.save()
        return True