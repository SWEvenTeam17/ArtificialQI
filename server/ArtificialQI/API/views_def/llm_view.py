"""
File che contiene le definizioni delle viste LLMView e OllamaView.
"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from API.serializers import LLMSerializer, TestSerializer
from API.services import LLMService
from .abstract_view import AbstractView


class LLMView(AbstractView):
    """
    Classe che gestisce le richieste per creare,modificare e cancellare LLM.
    """

    serializer = LLMSerializer
    service = LLMService


class OllamaView(APIView):
    """
    Classe che gestisce le richieste per caricare i modelli di Ollama nell'applicativo.
    """

    def post(self, request=None):
        """
        Funzione che sincronizza i modelli di Ollama con il DB.
        """
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
