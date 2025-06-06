"""
File che contiene la vista dedicata alla gestione dei
test precedentemente eseguiti in una sessione.
"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from API.models import BlockTest
from API.serializers import BlockTestSerializer
from API.services import BlockTestService, SessionService


class PrevTestView(APIView):
    """
    Classe che contiene la definizione della vista dedicata
    alla gestione dei test precedentemente eseguiti in una sessione.
    """

    def get(self, request, instance_id: int) -> Response:
        """
        Funzione che ritorna tutti i prompt precedenti di una sessione.
        """
        test_id = request.GET.get("test_id")
        try:
            if test_id is not None:
                test = BlockTestService.read(instance_id=test_id)
                data = BlockTestService.format_results(test)
                return Response(data)
            tests = SessionService.get_tests_by_session(instance_id)
            serializer = BlockTestSerializer(tests, many=True)
            return Response(serializer.data)
        except BlockTest.DoesNotExist:
            return Response(
                {"error": "Test not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, instance_id: int) -> Response:
        try:
            BlockTestService.delete(instance_id=instance_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except BlockTest.DoesNotExist:
            return Response(
                {"error": "Test not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
