from api.serializers import LLMRequestSerializer, LLMResponseSerializer
from api.services import OllamaLLMIntegrationService
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class LLMServiceView(APIView):

    authentication_classes = []
    permission_classes = []

    @extend_schema(
        responses=LLMResponseSerializer,
        description="Restituisce la lista degli LLM disponibili",
    )
    def get(self, request):
        result = OllamaLLMIntegrationService.get_ollama_llms()
        if result is None:
            return Response(
                {"error": "Connessione con Ollama fallita"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(result)

    @extend_schema(
        request=LLMRequestSerializer,
        responses=LLMResponseSerializer,
        description="Interroga un LLM specifico con un prompt",
    )
    def post(self, request):
        serializer = LLMRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        llm_name = serializer.validated_data["llm_name"]
        prompt = serializer.validated_data["prompt"]

        llm_object = OllamaLLMIntegrationService.get_llm(llm_name)
        if llm_object is None:
            return Response(
                {"error": "Connessione con Ollama fallita"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        answer = OllamaLLMIntegrationService.interrogate(llm=llm_object, prompt=prompt)
        response_data = {"llm_name": llm_name, "prompt": prompt, "answer": answer}
        return Response(response_data)
