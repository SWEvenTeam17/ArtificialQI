"""
File che contiene la vista dedicata alla gestione dei
test precedentemente eseguiti in una sessione.
"""

from API.serializers import BlockSerializer
from API.services import BlockService
from .abstract_view import AbstractView
from rest_framework.response import Response
from rest_framework import status

class BlockView(AbstractView):
    """
    Classe che contiene la definizione della vista dedicata
    alla gestione dei blocchi di domande.
    """

    serializer = BlockSerializer
    service = BlockService

    def post(self, request)->Response:
        """
        Metodo che risponde alle richieste di tipo POST.
        Valida i dati tramite il serializer corretto
        e crea una nuova istanza del Model in DB utilizzando
        il service corrispondente.
        """
        data: dict = {
            "name":request.data.get("name"),
            "questions":request.data.get("questions")
        }
        try:
            result = self.service.create(data=data)
            if result == False:
                 return Response({"error":"Nome duplicato"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(
                data, status=status.HTTP_201_CREATED
            )
        except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
