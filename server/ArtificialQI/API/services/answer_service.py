"""
File che contiene i servizi riguardanti le risposte.
"""

from API.repositories import AnswerRepository
from .abstract_service import AbstractService


class AnswerService(AbstractService):
    """
    Classe che contiene i servizi riguardanti le risposte.
    """

    repository = AnswerRepository
