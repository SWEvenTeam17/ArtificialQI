"""
File che contiene la definizione del repository
che gestisce le istanze dei blocchi in DB.
"""

from typing import List
from API.models import Block, Prompt, LLM
from django.db.models import Count, Q
from .abstract_repository import AbstractRepository


class BlockRepository(AbstractRepository):
    """
    Classe che contiene la definizione del repository
    che gestisce le istanze dei blocchi in DB.
    """

    model = Block

    @staticmethod
    def add_prompt(block: Block, prompt: Prompt) -> Block:
        """
        Aggiunge un prompt ad un blocco.
        """
        block.prompt.add(prompt)
        return block

    @staticmethod
    def remove_prompt(block: Block, prompt: Prompt) -> Block:
        """
        Rimuove un prompt da un blocco.
        """
        block.prompt.remove(prompt)
        return block

    @staticmethod
    def get_by_name(name: str) -> Block | None:
        """
        Trova un blocco tramite il suo nome.
        """
        return Block.objects.filter(name=name).first()

    @staticmethod
    def get_prompts(block: Block) -> List[Prompt]:
        """
        Ritorna tutti i prompt di un blocco sotto forma di lista.
        """
        return list(block.prompt.all())

    @staticmethod
    def filter_by_llm(llm: LLM) -> List[Block]:
        """
        Ritorna tutti i blocchi eseguiti da un LLM sotto forma di lista.
        """
        return list(Block.objects.filter(prompt__run__llm__id=llm.id))

    @staticmethod
    def filter_by_ids(ids: List[int]) -> List[Block]:
        """
        Filtra i blocchi prendendo quelli con id all'interno della lista di id passata.
        """
        return list(Block.objects.filter(id__in=ids))

    @staticmethod
    def get_common_blocks_for_llms(first_llm: LLM, second_llm: LLM) -> List[Block]:
        """
        Restituisce i blocchi che hanno prompt usati in Run da entrambi gli LLM.
        """
        return (
            Block.objects
            .filter(
                Q(prompt__run__llm=first_llm) | Q(prompt__run__llm=second_llm)
            )
            .annotate(
                llm_count=Count('prompt__run__llm', distinct=True)
            )
            .filter(llm_count=2)
            .distinct()
        )