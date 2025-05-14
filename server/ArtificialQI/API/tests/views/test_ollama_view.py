from django.test import TestCase
from unittest.mock import patch
from rest_framework.test import APIClient
from rest_framework import status

class OllamaViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = "/llm_list/load_ollama/"

    @patch("API.services.LLMService.sync_ollama_llms")
    def test_sync_success(self, mock_sync):
        mock_sync.return_value = None  # simuliamo il successo
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "LLM models loaded successfully from Ollama server")

    @patch("API.services.LLMService.sync_ollama_llms")
    def test_sync_failure(self, mock_sync):
        mock_sync.side_effect = Exception("Errore di connessione")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("error", response.data)
