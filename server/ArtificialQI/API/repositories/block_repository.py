from .abstract_repository import AbstractRepository
from API.models import Block, Prompt

class BlockRepository(AbstractRepository):
    model = Block

    @staticmethod
    def add_prompt(block: Block,prompt: Prompt)->Block:
        block.prompt.add(prompt)
        block.save()
        return block

    @staticmethod
    def remove_prompt(block: Block,prompt: Prompt)->Block:
        block.prompt.remove(prompt)
        block.save()
        return block
    
    @staticmethod
    def get_by_name(name: str)->Block | None:
        return Block.objects.filter(name=name).first()
    

    