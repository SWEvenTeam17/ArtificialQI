"""
File che contiene i servizi riguardanti i prompt.
"""

from typing import ClassVar

from API.repositories import AbstractRepository, PromptRepository

from .abstract_service import AbstractService


class PromptService(AbstractService):
    """
    Classe che contiene i servizi riguardanti i prompt.
    """

    _repository: ClassVar[AbstractRepository] = PromptRepository
