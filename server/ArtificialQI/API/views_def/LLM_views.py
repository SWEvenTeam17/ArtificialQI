from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from API.models import LLM
from API.serializers import LLMSerializer

@csrf_exempt
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