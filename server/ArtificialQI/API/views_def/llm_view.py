from .abstract_view import AbstractView
from API.serializers import LLMSerializer
from API.services import LLMService
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class LLMView(AbstractView):
    serializer = LLMSerializer
    service = LLMService


class OllamaView(APIView):
    def post(self, request=None):
        try:
            LLMService.sync_ollama_llms()
            return Response(
                {"message": "LLM models loaded successfully from Ollama server"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
