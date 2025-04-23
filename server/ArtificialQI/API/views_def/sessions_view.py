"""
File che contiene la classe SessionsView, che gestisce le
richieste per effettuare operazioni sulle Sessioni.
"""
from API.serializers import SessionSerializer
from API.services import SessionService
from .abstract_view import AbstractView
class SessionsView(AbstractView):
    """
    Classe che contiene la definizione della vista dedicata
    alla gestione delle sessioni.
    """
    serializer = SessionSerializer
    service = SessionService
