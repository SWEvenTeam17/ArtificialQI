"""
File che contiene la vista dedicata alla gestione dei
test precedentemente eseguiti in una sessione.
"""

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from API.models import Test
from API.serializers import TestSerializer
from API.services import PrevTestService, TestService


class PrevTestView(APIView):
    """
    Classe che contiene la definizione della vista dedicata
    alla gestione dei test precedentemente eseguiti in una sessione.
    """

    serializer = TestSerializer
    service = PrevTestService

    def get(self, request, instance_id: int) -> Response:
        """
        Funzione che ritorna tutti i prompt precedenti di una sessione.
        """
        test_id = request.GET.get("test_id")
        try:
            if test_id is not None:
                test = self.service.read(instance_id=test_id)
                data = TestService.format_results(test)
                return Response(data)
            tests = self.service.get_tests_by_session(instance_id)
            serializer = self.serializer(tests, many=True)
            return Response(serializer.data)
        except Test.DoesNotExist:
            return Response({"error": "Test not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
