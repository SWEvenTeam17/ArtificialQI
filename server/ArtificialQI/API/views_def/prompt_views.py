"""
File che contiene le viste relative ai prompt.
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from API.models import Prompt, Session
from API.serializers import PromptSerializer
from API.repositories import PromptRepository

@api_view(["GET", "POST"])
def prompt_list(request):
    """
    Funzione che ritorna la lista dei prompt oppure
    ne crea uno
    """
    if request.method == "GET":
        return Response(PromptRepository.get_all().data)
    if request.method == "POST":
        data = request.data
        session_id = data.get("sessionId")
        try:
            session = Session.objects.get(id=session_id)
        except Session.DoesNotExist:
            return Response(
                {"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND
            )
        save_data = {
            "prompt_text": data.get("prompt_text"),
            "expected_answer": data.get("expected_answer"),
            "session": session.id,
        }
        serializer = PromptSerializer(data=save_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def prompt_detail(request, pk):
    """
    Funzione che ritorna i dettagli relativi ad un prompt
    oppure ne crea o modifica uno
    """
    if request.method == "GET":
        data = PromptRepository.get_by_id(id=pk).data
        if data != None:
            return Response(data)
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "PUT":
        result, data = PromptRepository.update(id=pk, data=request.data)
        if result == True:
            return Response(data, status=status.HTTP_200_OK)
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "DELETE":
        if PromptRepository.delete(id=pk):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_400_BAD_REQUEST)
