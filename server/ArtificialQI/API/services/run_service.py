"""
File che contiene i servizi riguardanti i prompt.
"""

from API.repositories import RunRepository
from API.models import Session
from .abstract_service import AbstractService


class RunService(AbstractService):
    """
    Classe che contiene i servizi riguardanti i prompt.
    """

    repository = RunRepository
