"""
File che contiene i servizi riguardanti i prompt.
"""

from API.repositories import PromptRepository, AbstractRepository
from typing import ClassVar
from .abstract_service import AbstractService


class PromptService(AbstractService):
    """
    Classe che contiene i servizi riguardanti i prompt.
    """

    _repository: ClassVar[AbstractRepository] = PromptRepository