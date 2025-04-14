from .abstract_view import AbstractView
from API.serializers import LLMSerializer
from API.services import SessionService
from rest_framework.response import Response
from rest_framework import status

class SessionLLMView(AbstractView):
    serializer = LLMSerializer
    service = SessionService

    def get(self, request, pk: int):
        try:
            result = self.service.get_llm(session_id=pk)
            serializer = self.serializer(result, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            session_id = request.data.get("sessionId")
            llm_id = request.data.get("llmId")
            serializer = self.serializer(self.service.add_llm(session_id=session_id, llm_id=llm_id))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, session_id: int, llm_id: int):
        try:
            self.service.delete_llm(session_id, llm_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)