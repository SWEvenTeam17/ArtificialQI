from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.services import LLMService

class LLMView(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request):
        result = LLMService.get_ollama_llms()
        if result == None:
            return Response({"error":"Connessione con Ollama fallita"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(result)

    def post(self, request):
        llm_name = request.data.get("llm_name")
        prompt = request.data.get("prompt")
        llm_object = LLMService.get_llm(llm_name)
        if llm_object == None:
            return Response({"error":"Connessione con Ollama fallita"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        answer = LLMService.interrogate(llm=llm_object, prompt=prompt)
        return Response({"llm_name":llm_name,"prompt":prompt,"answer":answer})

        
