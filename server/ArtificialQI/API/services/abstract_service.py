from abc import ABC
from typing import ClassVar
from API.repositories import AbstractRepository


class AbstractService(ABC):
    repository: ClassVar[AbstractRepository]

    @classmethod
    def create(cls, data: dict):
        return cls.repository.create(data)

    @classmethod
    def read(cls, id: int):
        return cls.repository.get_by_id(id=id)

    @classmethod
    def read_all(cls):
        return cls.repository.get_all()

    @classmethod
    def update(cls, id: int, data: dict):
        return cls.repository.update(id=id, data=data)

    @classmethod
    def delete(cls, id: int):
        return cls.repository.delete(id=id)
