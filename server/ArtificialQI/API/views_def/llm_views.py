"""
File che contiene le viste relative ai LLM.
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from API.repositories import LLMRepository
from API.services import LLMService

# LLM
@api_view(["GET", "POST"])
def llm_list(request):
    """
    Vista che restituisce la lista dei LLM collegati oppure ne crea uno nuovo.
    """
    if request.method == "GET":
        return Response(LLMRepository.get_all().data)
    if request.method == "POST":
        result, instance = LLMRepository.create(data=request.data)
        if result == False:
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
    if request.method == "GET":
        data = LLMRepository.get_by_id(id=pk).data
        if data != None:
            return Response(data)
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "PUT":
        result, data = LLMRepository.update(id=pk, data=request.data)
        if result == True:
            return Response(data, status=status.HTTP_200_OK)
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "DELETE":
        if LLMRepository.delete(id=pk):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def load_ollama_llms(request):
    try:
        LLMService.sync_ollama_llms()
        return Response(
            {"message": "LLM models loaded successfully from Ollama server"},
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
