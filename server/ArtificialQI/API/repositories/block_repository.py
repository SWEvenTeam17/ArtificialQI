from .abstract_repository import AbstractRepository
from API.models import Block, Prompt, LLM
from typing import List

class BlockRepository(AbstractRepository):
    model = Block

    @staticmethod
    def add_prompt(block: Block,prompt: Prompt)->Block:
        block.prompt.add(prompt)
        return block

    @staticmethod
    def remove_prompt(block: Block,prompt: Prompt)->Block:
        block.prompt.remove(prompt)
        return block
    
    @staticmethod
    def get_by_name(name: str)->Block | None:
        return Block.objects.filter(name=name).first()

    @staticmethod
    def get_prompts(block: Block) -> List[Prompt]:
        return list(block.prompt.all())
    
    @staticmethod
    def filter_by_llm(llm: LLM)->List[Block]:
        return list(Block.objects.filter(prompt__run__llm__id=llm.id))
    
    @staticmethod
    def filter_by_ids(id: List[int])->List[Block]:
        return list(Block.objects.filter(id__in=id))

    

    