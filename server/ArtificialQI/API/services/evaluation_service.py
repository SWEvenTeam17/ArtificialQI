"""
File che contiene i servizi riguardanti le valutazioni.
"""
from API.repositories import EvaluationRepository
from .abstract_service import AbstractService
class EvaluationService(AbstractService):
    """
    Classe che contiene i servizi riguardanti le valutazioni.
    """
    repository = EvaluationRepository
