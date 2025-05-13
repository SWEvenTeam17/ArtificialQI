"""
File che contiene i servizi riguardanti i blocchi.
"""

from API.repositories import BlockRepository
from API.models import Block
from .abstract_service import AbstractService


class BlockService(AbstractService):
    """
    Classe che contiene i servizi riguardanti i blocchi.
    """

    repository = BlockRepository

    @classmethod
    def create(cls, data: dict)->Block|bool:
        duplicate = BlockRepository.get_by_name(data["name"])
        if duplicate==None:
            return BlockRepository.create(data)
        return False

    @staticmethod
    def is_duplicated(name: str)->bool:
        duplicated = BlockRepository.get_by_name(name=name)
        return duplicated is not None

