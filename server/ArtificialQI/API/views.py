from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from API.models import Prompt, Answer
from API.serializers import PromptSerializer


@csrf_exempt
def prompt_text_list(request):
    if request.method == "GET":
        prompt_texts = Prompt.objects.all()
        serializer = PromptSerializer(prompt_texts, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = PromptSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def prompt_text_detail(request, pk):
    try:
        prompt_text = Prompt.objects.get(pk=pk)
    except Prompt.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = PromptSerializer(prompt_text)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = PromptSerializer(prompt_text, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method=='DELETE':
        prompt_text.delete()
        return HttpResponse(status=204)