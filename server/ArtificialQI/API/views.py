from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from API.models import Prompt, Answer, LLM, Session
from API.serializers import PromptSerializer, AnswerSerializer, LLMSerializer, SessionSerializer
from API.classes.LLMController import LLMController

@csrf_exempt
# PROMPT
@api_view(['GET', 'POST'])
def prompt_list(request):
    if request.method == "GET":
        prompt_texts = Prompt.objects.all()
        serializer = PromptSerializer(prompt_texts, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        data = request.data
        serializer = PromptSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def prompt_detail(request, pk):
    try:
        prompt_text = Prompt.objects.get(pk=pk)
    except Prompt.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = PromptSerializer(prompt_text)
        return Response(serializer.data)
    elif request.method == 'PUT':
        data = request.data
        serializer = PromptSerializer(prompt_text, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method=='DELETE':
        prompt_text.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# ANSWER
@api_view(['GET', 'POST'])
def answer_list(request):
    if request.method == "GET":
        answer_texts = Answer.objects.all()
        serializer = AnswerSerializer(answer_texts, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        data = request.data
        serializer = AnswerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def answer_detail(request, pk):
    try:
        answer = Answer.objects.get(pk=pk)
    except Answer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = AnswerSerializer(answer)
        return Response(serializer.data)
    elif request.method == "DELETE":
        answer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#LLM
@api_view(['GET', 'POST'])
def llm_list(request):
    if request.method == "GET":
        llm_all = LLM.objects.all()
        serializer = LLMSerializer(llm_all, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        data = request.data
        serializer = LLMSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def llm_detail(request, pk):
    try:
        llm = LLM.objects.get(pk=pk)
    except LLM.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = LLMSerializer(llm)
        return Response(serializer.data)
    elif request.method == "PUT":
        data = request.data
        serializer = LLMSerializer(llm, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        llm.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def test(request):
    llm = LLMController("llama3.2")
    output = llm.getAnswer("Ciao come stai?")
    return Response(output)

#Sessions
@api_view(['GET', 'POST'])
def session_list(request):
    if request.method == "GET":
        sessions = Session.objects.all()
        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        data = request.data
        serializer = SessionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def session_detail(request, pk):
    try:
        session = Session.objects.get(pk=pk)
    except Session.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = SessionSerializer(session)
        return Response(serializer.data)
    elif request.method == 'PUT':
        data = request.data
        serializer = SessionSerializer(session, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method=='DELETE':
        session.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



