"""
File che contiene il repository astratto che definisce metodi comuni
per tutte le classi derivate.
"""

from abc import ABC
from typing import ClassVar

from django.db import models


class AbstractRepository(ABC):
    """
    Classe che contiene la definizione del repository astratto che definisce metodi comuni
    per tutte le classi derivate. Ogni repository è collegato ad una classe Model specifica.
    """

    _model: ClassVar[models.Model]

    @classmethod
    def get_all(cls):
        """
        Ritorna tutte le istanze presenti in DB del model.
        """
        return cls._model.objects.all()

    @classmethod
    def get_by_id(cls, instance_id: int) -> models.Model | None:
        """
        Ritorna una istanza specifica del model, filtrandolo per id.
        """
        try:
            return cls._model.objects.get(pk=instance_id)
        except cls._model.DoesNotExist:
            return None

    @classmethod
    def create(cls, data: dict) -> models.Model:
        """
        Crea una nuova istanza del Model in DB.
        """
        return cls._model.objects.create(**data)

    @classmethod
    def delete(cls, instance_id: int) -> bool:
        """
        Elimina una istanza del Model in DB.
        """
        instance = cls.get_by_id(instance_id)
        if instance:
            instance.delete()
            return True
        return False

    @classmethod
    def update(cls, instance_id: int, data: dict) -> models.Model | None:
        """
        Aggiorna una istanza del Model in DB.
        """
        instance = cls.get_by_id(instance_id)
        if instance is None:
            return None
        for key, value in data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
