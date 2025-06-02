"""
File che contiene la classe SessionsView, che gestisce le
richieste per effettuare operazioni sulle Sessioni.
"""

from typing import ClassVar

from rest_framework import serializers

from API.serializers import SessionSerializer
from API.services import AbstractService, SessionService

from .abstract_view import AbstractView


class SessionsView(AbstractView):
    """
    Classe che contiene la definizione della vista dedicata
    alla gestione delle sessioni.
    """

    serializer: ClassVar[type[serializers.Serializer]] = SessionSerializer
    service: ClassVar[type[AbstractService]] = SessionService
