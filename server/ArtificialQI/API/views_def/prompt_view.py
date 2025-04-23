"""
File che contiene la classe PromptView.
"""

from API.serializers import PromptSerializer
from API.services import PromptService
from .abstract_view import AbstractView

class PromptView(AbstractView):
    """
    Classe che contiene le definizioni delle viste dedicate alla gestione dei Prompt.
    """
    serializer = PromptSerializer
    service = PromptService
