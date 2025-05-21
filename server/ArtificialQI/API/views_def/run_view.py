"""
File che contiene la classe PromptView.
"""

from API.serializers import RunSerializer
from API.services import RunService
from .abstract_view import AbstractView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

class PromptView(AbstractView):
    """
    Classe che contiene le definizioni delle viste dedicate alla gestione dei Prompt.
    """
    serializer = RunSerializer
    service = RunService

class RunPromptView(APIView):
    service = RunService
    def get(self, request):
        prompt_id = request.GET.get("prompt_id")
        if not prompt_id:
            return Response({"error": "Missing prompt_id."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            prompt_id = int(prompt_id)
        except ValueError:
            return Response({"error": "Invalid prompt_id."}, status=status.HTTP_400_BAD_REQUEST)
        
        data = RunService.get_formatted_by_prompt(prompt_id=prompt_id)
        if data is None:
            return Response({"error": "Prompt not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(data, status=status.HTTP_200_OK)
    
    def delete(self, request):
        run_id = request.GET.get("run_id")
        if not run_id:
            return Response({"error": "Missing run_id."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            run_id = int(run_id)
        except ValueError:
            return Response({"error": "Invalid run_id."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            RunService.delete(run_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
