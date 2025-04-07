from API.models import Answer
from django.core.exceptions import ObjectDoesNotExist
from .abstract_repository import AbstractRepository
from API.serializers import AnswerSerializer

class AnswerRepository(AbstractRepository):
    def get_all():
        try:
            return AnswerSerializer(Answer.objects.all(), many=True).data
        except ObjectDoesNotExist:
            return None
    
    def get_by_id(id: int):
        try:
            answer = Answer.objects.get(pk=id)
            return AnswerSerializer(answer).data
        except Answer.DoesNotExist:
            return None
        
    def create(data):
        serializer = AnswerSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return True, serializer.data
        return False, serializer.errors
    
    def delete(id: int)->bool:
        try:
            answer = Answer.objects.get(pk=id)
            answer.delete()
            return True
        except Answer.DoesNotExist:
            return False


