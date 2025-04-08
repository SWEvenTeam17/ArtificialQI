from API.models import Session
from API.serializers import SessionSerializer
from API.repositories import AbstractRepository
from django.core.exceptions import ObjectDoesNotExist

class SessionRepository(AbstractRepository):
    @staticmethod
    def get_by_id(id: int):
        try:
            session = Session.objects.get(pk=id)
            return SessionSerializer(session)
        except Session.DoesNotExist:
            return None

    @staticmethod
    def get_all():
        try:
            return SessionSerializer(Session.objects.all(), many=True).data
        except ObjectDoesNotExist:
            return None

    @staticmethod    
    def create(data):
        serializer = SessionSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return True, serializer.data
        return False, serializer.errors
    
    @staticmethod
    def delete(id: int)->bool:
        try:
            Session.objects.get(pk=id).delete()
            return True
        except Session.DoesNotExist:
            return False

    @staticmethod     
    def update(id: int, data):
        serializer = SessionSerializer(Session.objects.get(pk=id),data=data)
        if serializer.is_valid():
            serializer.save()
            return True, serializer.data
        return False, serializer.errors