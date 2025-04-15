from .abstract_view import AbstractView
from API.serializers import TestSerializer
from API.services import TestService
from rest_framework.response import Response
from rest_framework import status

class TestView(AbstractView):
    serializer = TestSerializer
    service = TestService

    def post(self, request):
        data, session = self.service.get_data(request=request)
        if not data:
            return Response(
                {"error": "Domanda e risposta sono campi obbligatori"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            test = self.service.runtest(data, session)
        except (ConnectionError, FileNotFoundError) as e:
            if isinstance(e, ConnectionError):
                return Response(
                    {"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
            elif isinstance(e, FileNotFoundError):
                return Response(
                    {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(test, status=status.HTTP_200_OK)