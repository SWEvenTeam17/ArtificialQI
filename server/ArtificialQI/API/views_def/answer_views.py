"""
File che contiene tutte le viste relative
alla gestione delle risposte dei LLM
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from API.repositories import AnswerRepository

@api_view(["GET", "POST"])
def answer_list(request):
    """
    Funzione che ritorna la lista delle risposte
    oppure ne crea una nuova
    """
    if request.method == "GET":
        return Response(AnswerRepository.get_all(), status=status.HTTP_200_OK)
    if request.method == "POST":
        result, data = AnswerRepository.create(request.data)
        if result:
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "DELETE"])
def answer_detail(request, pk):
    """
    Funzione che ritorna le informazioni su una risposta
    oppure ne cancella una
    """
    if request.method == "GET":
        data = AnswerRepository.get_by_id(id=pk).data
        if data != None:
            return Response(data)
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "DELETE":
        if AnswerRepository.delete(id=pk):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_400_BAD_REQUEST)
