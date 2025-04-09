from abc import ABC, abstractmethod
from django.db import models
from rest_framework.serializers import Serializer
from typing import Type

class AbstractRepository(ABC):

    model_class = Type[models.Model]
    serializer_class = Type[Serializer]

    @classmethod
    @abstractmethod
    def get_all(cls):
        return cls.serializer_class(cls.model_class.objects.all(), many=True)
    
    @classmethod
    @abstractmethod
    def get_by_id(cls, id: int):
        try:
            instance = cls.model_class.objects.get(pk=id)
            return cls.serializer_class(instance)
        except cls.model_class.DoesNotExist:
            return None
    
    @classmethod
    @abstractmethod   
    def create(cls, data):
        serializer = cls.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return True, serializer.data
        return False, serializer.errors

    @classmethod
    @abstractmethod
    def delete(cls, id: int)->bool:
        try:
            cls.model_class.objects.get(pk=id).delete()
            return True
        except cls.model_class.DoesNotExist:
            return False
        
    @classmethod
    @abstractmethod    
    def update(cls, id: int, data):
        serializer = cls.serializer_class(cls.model_class.objects.get(pk=id),data=data)
        if serializer.is_valid():
            serializer.save()
            return True, serializer.data
        return False, serializer.errors


