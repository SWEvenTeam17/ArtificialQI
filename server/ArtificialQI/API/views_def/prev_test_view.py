"""
File che contiene la vista dedicata alla gestione dei
test precedentemente eseguiti in una sessione.
"""

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from API.serializers import PromptSerializer
from API.services import TestService, SessionService, PromptService


class PrevTestView(APIView):
    """
    Classe che contiene la definizione della vista dedicata
    alla gestione dei test precedentemente eseguiti in una sessione.
    """

    serializer = PromptSerializer
    service = TestService

    def get(self, request, instance_id: int) -> Response:
        """
        Funzione che ritorna tutti i test precedenti.
        """
        try:
            previous_prompts = PromptService.filter_by_session(
                session=SessionService.read(instance_id=instance_id)
            )
            serializer = self.serializer(previous_prompts, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, instance_id: int) -> Response:
        """
        Funzione che cancella un test precdente.
        """
        try:
            PromptService.delete(instance_id=instance_id)
            return Response(status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
