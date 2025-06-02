"""
File che contiene la classe TestView, che gestisce le
richieste per effettuare operazioni sui Test.
"""

from typing import ClassVar, List

from rest_framework import serializers, status
from rest_framework.response import Response

from API.models import Block
from API.serializers import BlockTestSerializer
from API.services import AbstractService, BlockService, BlockTestService, SessionService

from .abstract_view import AbstractView


class RunBlockTestView(AbstractView):
    """
    Classe che contiene la definizione della vista dedicata
    alla esecuzione dei test.
    """

    _serializer: ClassVar[type[serializers.Serializer]] = BlockTestSerializer
    _service: ClassVar[type[AbstractService]] = BlockTestService

    def post(self, request) -> Response:
        session = SessionService.read(request.data.get("sessionId"))
        blocks: List[Block] = BlockService.retrieve_blocks(request.data.get("blocks"))
        try:
            test = self._service.runtest(session=session, blocks=blocks)
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
