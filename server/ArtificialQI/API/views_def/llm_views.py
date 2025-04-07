"""
File che contiene le viste relative ai LLM.
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from API.models import LLM
from API.repositories import LLMRepository
import requests
from API.serializers import LLMSerializer
import os
from dotenv import load_dotenv

# LLM
@api_view(["GET", "POST"])
def llm_list(request):
    """
    Vista che restituisce la lista dei LLM collegati oppure ne crea uno nuovo.
    """
    if request.method == "GET":
        return Response(LLMRepository.get_all(), status=status.HTTP_200_OK)
    if request.method == "POST":
        status, instance = LLMRepository.create(data=request.data)
        if status == False:
            return Response(
                {"error": "Esiste già un LLM con lo stesso nome."}, status=status.HTTP_409_CONFLICT
            )
        return Response(instance, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def llm_detail(request, pk):
    """
    Vista che ritorna le informazioni su un LLM specifico oppure lo modifica/elimina.
    """
    try:
        llm = LLM.objects.get(pk=pk)
    except LLM.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = LLMSerializer(llm)
        return Response(serializer.data)
    if request.method == "PUT":
        data = request.data
        serializer = LLMSerializer(llm, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "DELETE":
        llm.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def load_ollama_llms(request):
    try:
        load_dotenv()
        url = os.getenv("OLLAMA_URL")+"/api/tags"
        response = requests.get(url)
        data = response.json()
        models = data.get("models", [])
        for model in models:
            name = model.get("name")
            size = model.get("details", {}).get("parameter_size")
            llm, _ = LLM.objects.get_or_create(name=name)
            llm.n_parameters = size
            llm.save()
        return Response(
            {"message": "LLM models loaded successfully from Ollama server"},
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
