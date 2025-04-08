from API.models import LLM
from API.serializers import LLMSerializer
from django.core.exceptions import ObjectDoesNotExist
from API.repositories import AbstractRepository

class LLMRepository(AbstractRepository):
    @staticmethod
    def get_all():
        try:
            return LLMSerializer(LLM.objects.all(), many=True).data
        except ObjectDoesNotExist:
            return None
        
    @staticmethod
    def get_by_id(id: int):
        try:
            llm = LLM.objects.get(pk=id)
            return LLMSerializer(llm)
        except LLM.DoesNotExist:
            return None

    @staticmethod
    def create(data):
        # Controlla se esiste già un LLM con lo stesso nome
        if LLM.objects.all().filter(name=data.get("name")).first():
            return False, {"error":"Name already in use"}
        serializer = LLMSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return True, serializer.data
        return False, serializer.errors

    @staticmethod
    def delete(id: int)->bool:
        try:
            LLM.objects.get(pk=id).delete()
            return True
        except LLM.DoesNotExist:
            return False

    @staticmethod     
    def update(id: int, data):
        serializer = LLMSerializer(LLM.objects.get(pk=id),data=data)
        if serializer.is_valid():
            serializer.save()
            return True, serializer.data
        return False, serializer.errors

    @staticmethod 
    def update_or_create(name, parameters)->bool:
        llm, exists = LLM.objects.get_or_create(name=name)
        if not exists or llm.n_parameters != parameters:
            llm.n_parameters = parameters
            llm.save()
        return True

