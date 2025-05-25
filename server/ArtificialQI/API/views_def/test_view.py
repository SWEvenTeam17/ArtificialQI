"""
File che contiene la classe TestView, che gestisce le
richieste per effettuare operazioni sui Test.
"""

from rest_framework.response import Response
from rest_framework import status
from API.serializers import BlockTestSerializer
from API.services import BlockTestService, SessionService, BlockService
from API.models import Block
from typing import List
from .abstract_view import AbstractView


class TestView(AbstractView):
    """
    Classe che contiene la definizione della vista dedicata
    alla gestione dei test precedentemente eseguiti in una sessione..
    """

    serializer = BlockTestSerializer
    service = BlockTestService

    def post(self, request) -> Response:
        session = SessionService.read(request.data.get("sessionId"))
        blocks: List[Block] = BlockService.retrieve_blocks(request.data.get("blocks"))
        try:
            test = self.service.runtest(session=session, blocks=blocks)
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
        except Exception as e:
            return Response(
                {"error": f"Errore inatteso: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
