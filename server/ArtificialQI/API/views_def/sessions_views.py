from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from API.models import LLM, Session
from API.serializers import (
    LLMSerializer,
    SessionSerializer,
)

@csrf_exempt
# Sessions
@api_view(["GET", "POST"])
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


@api_view(["GET", "PUT", "DELETE"])
def session_detail(request, pk):
    try:
        session = Session.objects.get(pk=pk)
    except Session.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = SessionSerializer(session)
        return Response(serializer.data)
    elif request.method == "PUT":
        data = request.data
        serializer = SessionSerializer(session, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        session.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def add_llm_session(request):
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
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_llm_session(request, pk):
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
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_llm_session(request, session_id, llm_id):
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
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
