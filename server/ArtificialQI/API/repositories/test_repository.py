"""
File che contiene il repository che gestisce le istanze dei Test in DB.
"""

from API.models import Test
from .abstract_repository import AbstractRepository


class TestRepository(AbstractRepository):
    """
    Classe che contiene la definizione del repository che gestisce le istanze dei Test in DB.
    """

    model = Test
