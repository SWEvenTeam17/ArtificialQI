from API.models import Test
from API.serializers import TestSerializer
from django.core.exceptions import ObjectDoesNotExist
from API.repositories import AbstractRepository

class TestRepository(AbstractRepository):
    @staticmethod
    def get_by_id(id: int):
        """Recupera l'oggetto con un dato id"""
        try:
            return TestSerializer(Test.objects.get(pk=id))
        except Test.DoesNotExist:
            return None

    @staticmethod
    def get_all():
        """Recupera tutte le istanze"""
        try:
            return TestSerializer(Test.objects.all())
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def create(data):
        """Creare una nuova istanza"""
        serializer = TestSerializer(data=data)
        if serializer.is_valid():
            return True, serializer.data
        return False, serializer.errors

    @staticmethod
    def delete(id: int)->bool:
        """Eliminare una istanza esistente"""
        try:
            Test.objects.get(pk=id).delete()
            return True
        except Test.DoesNotExist:
            return False

    @staticmethod
    def update(id: int, data)->bool:
        serializer = TestSerializer(Test.objects.get(pk=id), data=data)
        if serializer.is_valid():
            serializer.save()
            return True, serializer.data
        return False, serializer.errors