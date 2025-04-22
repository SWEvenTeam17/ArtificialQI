from .abstract_view import AbstractView
from API.serializers import PromptSerializer
from API.services import TestService, SessionService, PromptService
from rest_framework.response import Response
from rest_framework import status


class PrevTestView(AbstractView):
    serializer = PromptSerializer
    service = TestService

    def get(self, request, pk):
        try:
            previous_prompts = PromptService.filter_by_session(
                session=SessionService.read(id=pk)
            )
            serializer = self.serializer(previous_prompts, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            PromptService.delete(id=pk)
            return Response(status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
