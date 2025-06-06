"""
File che contiene la classe PromptView.
"""

from typing import ClassVar

from rest_framework import serializers

from API.serializers import PromptSerializer
from API.services import AbstractService, PromptService

from .abstract_view import AbstractView


class PromptView(AbstractView):
    """
    Classe che contiene le definizioni delle viste dedicate alla gestione dei Prompt.
    """

    _serializer: ClassVar[type[serializers.Serializer]] = PromptSerializer
    _service: ClassVar[type[AbstractService]] = PromptService
