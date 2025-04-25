"""
File che contiene la classe SessionLLMView.
"""

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from API.serializers import LLMSerializer
from API.services import SessionService
from API.models import Session, LLM

class SessionLLMView(APIView):
    """
    Classe che contiene la definizione della vista dedicata
    alla gestione della connessione sessione-llm.
    """
    serializer = LLMSerializer
    service = SessionService

    def get(self, request, instance_id: int)->Response:
        """
        Ritorna tutti i modelli collegati ad una sessione.
        """
        try:
            result = self.service.get_llm(session_id=instance_id)
            serializer = self.serializer(result, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Session.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
        except LLM.DoesNotExist:
            return Response({"error": "LLM not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request)->Response:
        """
        Collega un LLM ad una sessione.
        """
        try:
            session_id = request.data.get("sessionId")
            llm_id = request.data.get("llmId")
            serializer = self.serializer(
                self.service.add_llm(session_id=session_id, llm_id=llm_id)
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Session.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
        except LLM.DoesNotExist:
            return Response({"error": "LLM not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, session_id: int, llm_id: int)->Response:
        """
        Rimuove un LLM da una sessione.
        """
        try:
            self.service.delete_llm(session_id, llm_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Session.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
        except LLM.DoesNotExist:
            return Response({"error": "LLM not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
