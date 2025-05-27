"""
File che contiene i servizi riguardanti i blocchi.
"""

from typing import List
from API.repositories import BlockRepository, PromptRepository
from API.models import Block, LLM
from .abstract_service import AbstractService


class BlockService(AbstractService):
    """
    Classe che contiene i servizi riguardanti i blocchi.
    """

    repository = BlockRepository

    @classmethod
    def create(cls, data: dict) -> Block | bool:
        """
        Override della funzione create, crea un blocco e aggiunge tutti i prompt.
        """
        duplicate = BlockRepository.get_by_name(data["name"])
        if duplicate == None:
            new_block = BlockRepository.create({"name": data["name"]})
            for prompt in data["questions"]:
                instance = PromptRepository.get_or_create(
                    prompt_text=prompt["question"], expected_answer=prompt["answer"]
                )
                BlockRepository.add_prompt(block=new_block, prompt=instance)
            return new_block
        return False

    @staticmethod
    def is_duplicated(name: str) -> bool:
        """
        Funzione che determina se un blocco è duplicato.
        """
        duplicated = BlockRepository.get_by_name(name=name)
        return duplicated is not None

    @staticmethod
    def retrieve_blocks(blocks: List) -> List[Block]:
        """
        Funzione che ritorna le istanze in DB a partire da una lista.
        """
        retrieved: List[Block] = []
        for block in blocks:
            retrieved.append(BlockService.read(block["id"]))
        return retrieved

    @classmethod
    def get_common_blocks(cls, first_llm: LLM, second_llm: LLM) -> List[Block]:
        """
        Funzione che ritorna tutti i blocchi a cui hanno risposto due LLM.
        """
        # Prendo tutti gli id dei blocchi a cui hanno risposto i LLM passati come parametri
        blocks_ids_first = list(
            map(lambda b: b.id, BlockRepository.filter_by_llm(first_llm))
        )
        blocks_ids_second = list(
            map(lambda b: b.id, BlockRepository.filter_by_llm(second_llm))
        )

        # Eseguo intersezione tra i due per capire gli ID comuni, poi eseguo il fetch di tutti i blocchi in comune
        common_block_ids = set(blocks_ids_first).intersection(set(blocks_ids_second))
        return BlockRepository.filter_by_ids(common_block_ids)
