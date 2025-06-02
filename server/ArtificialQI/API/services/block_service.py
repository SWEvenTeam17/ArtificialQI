"""
File che contiene i servizi riguardanti i blocchi.
"""

from typing import List
from API.repositories import BlockRepository, PromptRepository, AbstractRepository
from API.models import Block, LLM
from .abstract_service import AbstractService
from typing import ClassVar

class BlockService(AbstractService):
    """
    Classe che contiene i servizi riguardanti i blocchi.
    """

    _repository: ClassVar[AbstractRepository] = BlockRepository

    @classmethod
    def create(cls, data: dict) -> Block | bool:
        """
        Override della funzione create, crea un blocco e aggiunge tutti i prompt.
        """
        duplicate = cls._repository.get_by_name(data["name"])
        if duplicate == None:
            new_block = cls._repository.create({"name": data["name"]})
            for prompt in data["questions"]:
                instance = PromptRepository.get_or_create(
                    prompt_text=prompt["question"], expected_answer=prompt["answer"]
                )
                cls._repository.add_prompt(block=new_block, prompt=instance)
            return new_block
        return False

    @classmethod
    def is_duplicated(cls, name: str) -> bool:
        """
        Funzione che determina se un blocco è duplicato.
        """
        duplicated = cls._repository.get_by_name(name=name)
        return duplicated is not None

    @classmethod
    def retrieve_blocks(cls, blocks: List) -> List[Block]:
        """
        Funzione che ritorna le istanze in DB a partire da una lista.
        """
        retrieved: List[Block] = []
        for block in blocks:
            retrieved.append(cls.read(block["id"]))
        return retrieved

    @classmethod
    def get_common_blocks(cls, first_llm: LLM, second_llm: LLM) -> List[Block]:
        """
        Funzione che ritorna tutti i blocchi a cui hanno risposto due LLM.
        """
        blocks_ids_first = list(
            map(lambda b: b.id, cls._repository.filter_by_llm(first_llm))
        )
        blocks_ids_second = list(
            map(lambda b: b.id, cls._repository.filter_by_llm(second_llm))
        )

        common_block_ids = set(blocks_ids_first).intersection(set(blocks_ids_second))
        return cls._repository.filter_by_ids(common_block_ids)
