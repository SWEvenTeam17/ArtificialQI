"""
File che contiene il repository che gestisce le istanze dei Test in DB.
"""

from API.models import BlockTest, Run
from .abstract_repository import AbstractRepository


class BlockTestRepository(AbstractRepository):
    """
    Classe che contiene la definizione del repository che gestisce le istanze dei Test in DB.
    """

    model = BlockTest

    @staticmethod
    def add_run(test: BlockTest, run: Run) -> BlockTest:
        """
        Funzione che aggiunge una run ad un test.
        """
        test.run.add(run)
        return test

    @staticmethod
    def remove_run(test: BlockTest, run: Run) -> BlockTest:
        """
        Funzione che rimuove una run da un test.
        """
        test.run.remove(run)
        return test
