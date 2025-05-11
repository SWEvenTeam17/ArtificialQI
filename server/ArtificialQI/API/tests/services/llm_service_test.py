import pytest
import os
import requests
from unittest.mock import patch, MagicMock
from API.services.llm_service import LLMService
from API.tests.services.abstract_service_test import AbstractServiceTestCase

class TestLLMService(AbstractServiceTestCase):
    service_class = LLMService


    @pytest.fixture(autouse=True)
    def setup(self, mocker):
        self.mock_repository = mocker.MagicMock()
        LLMService.repository = self.mock_repository

    @patch("API.services.llm_service.requests.get")
    @patch("API.services.llm_service.load_dotenv")
    def test_fetch_ollama_models(self, mock_load_dotenv, mock_get):
        # Simula la variabile di ambiente con l'URL fittizio di Ollama
        os.environ["OLLAMA_URL"] = "http://fake-url.com"

        # Crea una finta risposta del server
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "models": [
                {"name": "llama2", "details": {"parameter_size": "7B"}},
                {"name": "mistral", "details": {"parameter_size": "13B"}}
            ]
        }
        mock_get.return_value = mock_response

        # Chiama la funzione
        models = LLMService.fetch_ollama_models()

        # Verifiche
        assert len(models) == 2
        assert models[0]["name"] == "llama2"
        mock_load_dotenv.assert_called_once()
        mock_get.assert_called_once_with("http://fake-url.com/api/tags", timeout=5)

    @patch.object(LLMService, "fetch_ollama_models")
    def test_sync_ollama_llms(self, mock_fetch):
        # Restituisce due modelli finti
        mock_fetch.return_value = [
            {"name": "llama2", "details": {"parameter_size": "7B"}},
            {"name": "mistral", "details": {"parameter_size": "13B"}},
        ]
        # Chiama il metodo per sincronizzare
        LLMService.sync_ollama_llms()

        # Verifica che siano stati chiamati correttamente i metodi del repository
        assert self.mock_repository.update_or_create.call_count == 2
        self.mock_repository.update_or_create.assert_any_call(name="llama2", parameters="7B")
        self.mock_repository.update_or_create.assert_any_call(name="mistral", parameters="13B")