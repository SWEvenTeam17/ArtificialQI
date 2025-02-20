"""
File che contiene tutte le viste relative
alla gestione delle risposte dei LLM
"""
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from API.models import Answer
from API.serializers import AnswerSerializer

@csrf_exempt
@api_view(['GET', 'POST'])
def answer_list(request):
    """
    Funzione che ritorna la lista delle risposte 
    oppure ne crea una nuova
    """
    if request.method == "GET":
        answer_texts = Answer.objects.all()
        serializer = AnswerSerializer(answer_texts, many=True)
        return Response(serializer.data)
    if request.method == "POST":
        data = request.data
        serializer = AnswerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET', 'DELETE'])
def answer_detail(request, pk):
    """
    Funzione che ritorna le informazioni su una risposta
    oppure ne cancella una
    """
    try:
        answer = Answer.objects.get(pk=pk)
    except Answer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = AnswerSerializer(answer)
        return Response(serializer.data)
    if request.method == "DELETE":
        answer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
