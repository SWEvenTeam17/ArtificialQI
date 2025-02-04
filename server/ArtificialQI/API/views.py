from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
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


@api_view(['GET'])
def test(request):
    llm = LLMController("llama3.2")
    output = llm.getAnswer("Ciao come stai?")
    return Response(output)

@api_view(['POST'])
def runtest(request):
    question = request.data.get('question', None)
    if not question:
        return Response({"error": "Question is required"}, status=status.HTTP_400_BAD_REQUEST)
    session = Session.objects.get(id = request.data.get('sessionId'))
    llms = session.llm.all()
    responses = []
    for llm in llms:
        llmObj = LLMController(llm.name)
        output = llmObj.getAnswer(question)
        responses.append({
            "llm_name": llm.name,
            "answer": output
        })
    return Response({"responses": responses}, status=status.HTTP_200_OK)


# ADD LLM TO SESSION
@api_view(['POST'])
def add_llm_session(request):
    try:
        session = Session.objects.get(id = request.data.get('sessionId'))
        llm = LLM.objects.get(id = request.data.get('llmId'))
        session.llm.add(llm)
        session.save()
        serializer = LLMSerializer(llm)
        content = serializer.data;
        return Response(content, status=status.HTTP_201_CREATED)
    except Session.DoesNotExist:
        return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
    except LLM.DoesNotExist:
        return Response({"error": "LLM not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_llm_session(request, pk):
    try:
        result = LLM.objects.exclude(session__id=pk).all()
        serializer = LLMSerializer(result, many=True)
        content = serializer.data;
        return Response(content, status=status.HTTP_200_OK)
    except Session.DoesNotExist:
        return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
    except LLM.DoesNotExist:
        return Response({"error": "LLM not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_llm_session(request, session_id, llm_id):
    try:
        session = Session.objects.get(id=session_id)
        llm = LLM.objects.get(id=llm_id)
        session.llm.remove(llm)
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Session.DoesNotExist:
        return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
    except LLM.DoesNotExist:
        return Response({"error": "LLM not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)