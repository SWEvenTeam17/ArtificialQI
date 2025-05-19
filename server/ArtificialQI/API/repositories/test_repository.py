"""
File che contiene il repository che gestisce le istanze dei Test in DB.
"""

from API.models import Test, Run
from .abstract_repository import AbstractRepository


class TestRepository(AbstractRepository):
    """
    Classe che contiene la definizione del repository che gestisce le istanze dei Test in DB.
    """

    model = Test

    @staticmethod
    def add_run(test: Test, run: Run) -> Test:
        test.run.add(run)
        return test

    @staticmethod
    def remove_run(test: Test, run: Run) -> Test:
        test.run.remove(run)
        return test
