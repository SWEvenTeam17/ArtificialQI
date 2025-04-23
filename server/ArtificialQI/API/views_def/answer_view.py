"""
File che contiene le definizioni della vista AnswerView.
"""
from API.serializers import AnswerSerializer
from API.services import AnswerService
from .abstract_view import AbstractView

class AnswerView(AbstractView):
    """
    Classe che definisce le operazioni disponibili per le risposte.
    """
    serializer = AnswerSerializer
    service = AnswerService
