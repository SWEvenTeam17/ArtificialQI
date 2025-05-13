"""
File che contiene i servizi riguardanti i blocchi.
"""

from API.repositories import BlockRepository, PromptRepository
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
            new_block = BlockRepository.create({"name":data["name"]})
            print(data)
            for prompt in data["questions"]:
                instance = PromptRepository.get_or_create(prompt_text=prompt["question"], expected_answer=prompt["answer"])
                BlockRepository.add_prompt(block=new_block, prompt=instance)
            return new_block
        return False

    @staticmethod
    def is_duplicated(name: str)->bool:
        duplicated = BlockRepository.get_by_name(name=name)
        return duplicated is not None
    


