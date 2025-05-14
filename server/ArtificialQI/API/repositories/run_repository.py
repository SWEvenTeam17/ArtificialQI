"""
File che contiene il repository che gestisce le istanze
delle Run in DB.
"""

from API.models import Run
from .abstract_repository import AbstractRepository


class RunRepository(AbstractRepository):
    """
    Classe che contiene la definizione del repository
    che gestisce le istanze delle Run in DB.
    """

    model = Run
