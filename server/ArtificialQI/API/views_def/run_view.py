"""
File che contiene la classe PromptView.
"""

from API.serializers import RunSerializer
from API.services import RunService
from .abstract_view import AbstractView


class PromptView(AbstractView):
    """
    Classe che contiene le definizioni delle viste dedicate alla gestione dei Prompt.
    """

    serializer = RunSerializer
    service = RunService
