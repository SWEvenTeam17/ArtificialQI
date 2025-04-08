from API.models import Answer
from django.core.exceptions import ObjectDoesNotExist
from API.repositories import AbstractRepository
from API.serializers import AnswerSerializer

class AnswerRepository(AbstractRepository):
    @staticmethod
    def get_all():
        try:
            return AnswerSerializer(Answer.objects.all(), many=True).data
        except ObjectDoesNotExist:
            return None
        
    @staticmethod
    def get_by_id(id: int):
        try:
            answer = Answer.objects.get(pk=id)
            return AnswerSerializer(answer)
        except Answer.DoesNotExist:
            return None
        
    @staticmethod    
    def create(data):
        serializer = AnswerSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return True, serializer.data
        return False, serializer.errors
    
    @staticmethod
    def delete(id: int)->bool:
        try:
            Answer.objects.get(pk=id).delete()
            return True
        except Answer.DoesNotExist:
            return False
        
    @staticmethod     
    def update(id: int, data):
        serializer = AnswerSerializer(Answer.objects.get(pk=id),data=data)
        if serializer.is_valid():
            serializer.save()
            return True, serializer.data
        return False, serializer.errors


