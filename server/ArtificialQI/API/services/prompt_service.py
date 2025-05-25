"""
File che contiene i servizi riguardanti i prompt.
"""

from API.repositories import PromptRepository
from API.models import Session
from .abstract_service import AbstractService


class PromptService(AbstractService):
    """
    Classe che contiene i servizi riguardanti i prompt.
    """

    repository = PromptRepository