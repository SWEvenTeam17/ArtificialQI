from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.services import LLMService

class LLMView(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request):
        pass
    def post(self, request):
        llm_name = request.data.get("llm_name")
        prompt = request.data.get("prompt")
        answer = LLMService.interrogate(llm=LLMService.get_llm(llm_name), prompt=prompt)
        return Response({"llm_name":llm_name,"prompt":prompt,"answer":answer})

        
