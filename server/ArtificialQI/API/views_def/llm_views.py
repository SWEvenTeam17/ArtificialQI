"""
File che contiene le viste relative ai LLM.
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from API.models import LLM
import requests
from API.serializers import LLMSerializer


#LLM
@api_view(['GET', 'POST'])
def llm_list(request):
    """
    Vista che restituisce la lista dei LLM collegati oppure ne crea uno nuovo.
    """
    if request.method == "GET":
        llm_all = LLM.objects.all()
        serializer = LLMSerializer(llm_all, many=True)
        return Response(serializer.data)
    if request.method == "POST":
        data = request.data
        # Controlla se esiste già un LLM con lo stesso nome
        if LLM.objects.all().filter(name=data.get("name")).first():
            return Response({"error": "LLM already exists"}, status=status.HTTP_409_CONFLICT)
        serializer = LLMSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
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

@api_view(['POST'])
def load_ollama_llms(request):
    try:
        url = "http://localhost:11434/api/tags"
        response = requests.get(url)
        data = response.json()
        models = data.get("models", [])
        for model in models:
            name = model.get("name")
            size = model.get("details", {}).get("parameter_size")
            llm, _ = LLM.objects.get_or_create(name=name)
            llm.n_parameters = size
            llm.save()
        return Response({"message":"LLM models loaded successfully from Ollama server"},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
