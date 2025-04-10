from abc import ABC
from django.db import models
from typing import ClassVar

class AbstractRepository(ABC):

    model: ClassVar[models.Model]

    @classmethod
    def get_all(cls):
        return cls.model.objects.all()
    
    @classmethod
    def get_by_id(cls, id: int):
        try:
            return cls.model.objects.get(pk=id)
        except cls.model.DoesNotExist:
            return None
    
    @classmethod
    def create(cls, data: dict):
        return cls.model.objects.create(**data)

    @classmethod
    def delete(cls, id: int)->bool:
        instance = cls.get_by_id(id)
        if instance:
            instance.delete()
            return True
        return False
        
    @classmethod
    def update(cls, id: int, data: dict):
        instance = cls.get_by_id(id)
        if instance is None:
            return None
        for key, value in data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


