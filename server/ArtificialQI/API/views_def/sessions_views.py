"""
File contenente le viste relative alla gestione delle sessioni
"""
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from API.models import LLM, Session, Prompt
from API.serializers import (
    LLMSerializer,
    SessionSerializer,
    PromptSerializer
)


# Sessions
@api_view(["GET", "POST"])
def session_list(request):
    """"
    Vista che restituisce la lista delle sessioni
    oppure ne crea una nuova
    """
    if request.method == "GET":
        sessions = Session.objects.all()
        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data)
    if request.method == "POST":
        data = request.data
        serializer = SessionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)
@api_view(["GET", "PUT", "DELETE"])
def session_detail(request, pk):
    """
    Vista che restituisce i dettagli di una sessione
    oppure ne modifica/cancella una
    """
    try:
        session = Session.objects.get(pk=pk)
    except Session.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = SessionSerializer(session)
        return Response(serializer.data)
    if request.method == "PUT":
        data = request.data
        serializer = SessionSerializer(session, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "DELETE":
        session.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)
@api_view(["POST"])
def add_llm_session(request):
    """
    Vista che crea un nuovo collegamento tra LLM e sessione
    """
    try:
        session = Session.objects.get(id=request.data.get("sessionId"))
        llm = LLM.objects.get(id=request.data.get("llmId"))
        session.llm.add(llm)
        session.save()
        serializer = LLMSerializer(llm)
        content = serializer.data
        return Response(content, status=status.HTTP_201_CREATED)
    except Session.DoesNotExist:
        return Response(
            {"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except LLM.DoesNotExist:
        return Response({"error": "LLM not found"}, status=status.HTTP_404_NOT_FOUND)
@api_view(["GET"])
def get_llm_session(request, pk):
    """
    Vista che ritorna tutti i LLM connessi ad una sessione
    """
    try:
        result = LLM.objects.exclude(session__id=pk).all()
        serializer = LLMSerializer(result, many=True)
        content = serializer.data
        return Response(content, status=status.HTTP_200_OK)
    except Session.DoesNotExist:
        return Response(
            {"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except LLM.DoesNotExist:
        return Response({"error": "LLM not found"}, status=status.HTTP_404_NOT_FOUND)
@api_view(["DELETE"])
def delete_llm_session(request, session_id, llm_id):
    """
    Vista che elimina una connessione tra LLM e sessione
    """
    try:
        session = Session.objects.get(id=session_id)
        llm = LLM.objects.get(id=llm_id)
        session.llm.remove(llm)
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Session.DoesNotExist:
        return Response(
            {"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except LLM.DoesNotExist:
        return Response({"error": "LLM not found"}, status=status.HTTP_404_NOT_FOUND)
@api_view(["GET","DELETE"])
def get_previous_tests(request, pk):
    """
    Vista che restituisce i test precedenti relativi ad una sessione
    oppure ne elimina uno
    """
    if request.method == "GET":
        session = Session.objects.get(id=pk)
        previous_prompts = Prompt.objects.filter(session=session)
        serializer = PromptSerializer(previous_prompts, many=True)
        return Response(serializer.data)
    if request.method == "DELETE":
        target = Prompt.objects.get(id=request.data.get("previousPromptId"))
        target.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)
