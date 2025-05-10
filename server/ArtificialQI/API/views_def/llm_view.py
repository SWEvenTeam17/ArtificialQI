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
        
class LLMComparisonView(APIView):
    def get(self, request):
        first_llm_id = request.query_params.get("first_llm_id")
        second_llm_id = request.query_params.get("second_llm_id")
        session_id = request.query_params.get("session_id")

        result = LLMService.compare_llms(
            int(first_llm_id),
            int(second_llm_id),
            int(session_id)
        )

        serialized_tests = TestSerializer(result["common_tests"], many=True).data

        return Response({
            "common_tests": serialized_tests,
            "first_llm_averages": result["first_llm_averages"],
            "second_llm_averages": result["second_llm_averages"]
        }, status=status.HTTP_200_OK)

class PromptComparisonView(APIView):
    def get(self, request):
        llm_id = request.query_params.get("llm_id")
        session_id = request.query_params.get("session_id")

        result = LLMService.compare_prompts(
            int(llm_id),
            int(session_id)
        )

        serialized_tests = TestSerializer(result["tests"], many=True).data

        return Response({
            "tests": serialized_tests,
            "averages": result["averages"]
        }, status=status.HTTP_200_OK)
