from .abstract_view import AbstractView
from API.serializers import PromptSerializer
from API.services import TestService
from rest_framework.response import Response
from rest_framework import status

class PrevTestView(AbstractView):
    serializer = PromptSerializer
    service = TestService

    def get(self, request, pk):
        try:
            previous_prompts = self.service.get_prev(pk)
            serializer = self.serializer(previous_prompts, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        try:
            self.service.delete_prompt(request)
            return Response(status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        