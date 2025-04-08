from API.models import Prompt
from API.serializers import PromptSerializer
from API.repositories import AbstractRepository
from django.core.exceptions import ObjectDoesNotExist

class PromptRepository(AbstractRepository):
    @staticmethod
    def get_by_id(id: int):
        try:
            session = Prompt.objects.get(pk=id)
            return PromptSerializer(session)
        except Prompt.DoesNotExist:
            return None

    @staticmethod
    def get_all():
        try:
            return PromptSerializer(Prompt.objects.all(), many=True).data
        except ObjectDoesNotExist:
            return None

    @staticmethod    
    def create(data):
        serializer = PromptSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return True, serializer.data
        return False, serializer.errors
    
    @staticmethod
    def delete(id: int)->bool:
        try:
            Prompt.objects.get(pk=id).delete()
            return True
        except Prompt.DoesNotExist:
            return False

    @staticmethod     
    def update(id: int, data):
        serializer = PromptSerializer(Prompt.objects.get(pk=id),data=data)
        if serializer.is_valid():
            serializer.save()
            return True, serializer.data
        return False, serializer.errors