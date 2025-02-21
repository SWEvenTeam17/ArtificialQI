"""
File che contiene le viste relative ai prompt.
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from API.models import Prompt, Session
from API.serializers import PromptSerializer


@api_view(['GET', 'POST'])
def prompt_list(request):
    """
    Funzione che ritorna la lista dei prompt oppure
    ne crea uno
    """
    if request.method == "GET":
        prompt_texts = Prompt.objects.all()
        serializer = PromptSerializer(prompt_texts, many=True)
        return Response(serializer.data)
    if request.method == "POST":
        data = request.data
        session_id = data.get("sessionId")
        try:
            session = Session.objects.get(id = session_id)
        except Session.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
        save_data = {
            "prompt_text": data.get("prompt_text"),
            "expected_answer": data.get("expected_answer"),
            "session": session.id
        }
        serializer = PromptSerializer(data=save_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET', 'PUT', 'DELETE'])
def prompt_detail(request, pk):
    """
    Funzione che ritorna i dettagli relativi ad un prompt
    oppure ne crea o modifica uno
    """
    try:
        prompt_text = Prompt.objects.get(pk=pk)
    except Prompt.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = PromptSerializer(prompt_text)
        return Response(serializer.data)
    if request.method == 'PUT':
        data = request.data
        serializer = PromptSerializer(prompt_text, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method=='DELETE':
        prompt_text.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
