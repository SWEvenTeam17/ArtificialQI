"""
File che contiene la classe TestView, che gestisce le
richieste per effettuare operazioni sui Test.
"""

from rest_framework.response import Response
from rest_framework import status
from API.serializers import TestSerializer
from API.services import TestService
from .abstract_view import AbstractView
class TestView(AbstractView):
    """
    Classe che contiene la definizione della vista dedicata
    alla gestione dei test precedentemente eseguiti in una sessione..
    """
    serializer = TestSerializer
    service = TestService

    def post(self, request)->Response:
        """
        Override della funzione che gestisce le richieste di tipo POST.
        """
        data, session = self.service.get_data(request.data, request.data.get("sessionId"))
        if not data:
            return Response(
                {"error": "Domanda e risposta sono campi obbligatori"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            test = self.service.runtest(data, session)
            return Response(test, status=status.HTTP_200_OK)
        except (ConnectionError, FileNotFoundError) as e:
            if isinstance(e, ConnectionError):
                return Response(
                    {"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
            if isinstance(e, FileNotFoundError):
                return Response(
                    {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(
        {"error": "Errore sconosciuto."},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
