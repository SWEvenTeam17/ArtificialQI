"""
File che contiene la definizione della classe astratta da cui derivano tutti i service.
"""

from abc import ABC
from typing import ClassVar
from API.repositories import AbstractRepository


class AbstractService(ABC):
    """
    Classe astratta da cui derivano tutti i service.
    """

    _repository: ClassVar[AbstractRepository]

    @classmethod
    def create(cls, data: dict):
        """
        Funzione che gestisce la creazione di una istanza in DB.
        """
        return cls._repository.create(data)

    @classmethod
    def read(cls, instance_id: int):
        """
        Funzione che gestisce la lettura di una istanza in DB.
        """
        return cls._repository.get_by_id(instance_id=instance_id)

    @classmethod
    def read_all(cls):
        """
        Funzione che gestisce la lettura di tutte le istanze in DB.
        """
        return cls._repository.get_all()

    @classmethod
    def update(cls, instance_id: int, data: dict):
        """
        Funzione che gestisce l'aggiornamento di una istanza in DB.
        """
        return cls._repository.update(instance_id=instance_id, data=data)

    @classmethod
    def delete(cls, instance_id: int):
        """
        Funzione che gestisce la canellazione di una istanza in DB.
        """
        return cls._repository.delete(instance_id=instance_id)
