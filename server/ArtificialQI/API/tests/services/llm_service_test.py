from unittest.mock import patch, MagicMock
import pytest
import requests
from django.core.exceptions import ObjectDoesNotExist
from API.services.llm_service import LLMService
from API.tests.services.abstract_service_test import AbstractServiceTestCase


class TestLLMService(AbstractServiceTestCase):
    service_class = LLMService

    @patch("API.services.llm_service.requests.get")
    @patch("API.services.llm_service.os.getenv")
    @patch("API.services.llm_service.load_dotenv")
    def test_fetch_ollama_models(self, mock_load, mock_getenv, mock_get):
        """Test fetch dei modelli da Ollama"""
        mock_getenv.return_value = "http://ollama:11434"
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {"name": "llama2", "details": {"parameter_size": "7B"}}
        ]
        mock_get.return_value = mock_response

        result = LLMService._LLMService__fetch_ollama_models()

        mock_load.assert_called_once()
        mock_getenv.assert_called_with("LLM_SERVICE_URL")
        mock_get.assert_called_with("http://ollama:11434/interrogate/", timeout=5)
        assert result == [{"name": "llama2", "details": {"parameter_size": "7B"}}]

    @patch("API.services.llm_service.LLMService._LLMService__fetch_ollama_models")
    def test_sync_ollama_llms(self, mock_fetch):
        """Test sincronizzazione modelli nel database"""
        mock_fetch.return_value = [
            {"name": "llama2", "details": {"parameter_size": "7B"}},
            {"name": "mistral", "details": {"parameter_size": "7B"}},
        ]
        mock_repo = MagicMock()
        self.service_class.repository = (
            mock_repo  # <- Patch manuale dell'attributo di classe
        )

        self.service_class.sync_ollama_llms()

        mock_fetch.assert_called_once()
        assert mock_repo.update_or_create.call_count == 2
        mock_repo.update_or_create.assert_any_call(name="llama2", parameters="7B")
        mock_repo.update_or_create.assert_any_call(name="mistral", parameters="7B")

    @patch("API.services.llm_service.requests.get")
    @patch("API.services.llm_service.os.getenv", return_value="http://ollama:11434")
    def test_fetch_ollama_models_timeout(self, mock_getenv, mock_get):
        """Test gestione errori di timeout"""
        mock_get.side_effect = requests.exceptions.Timeout

        with pytest.raises(requests.exceptions.Timeout):
            LLMService._LLMService__fetch_ollama_models()

    @patch("API.services.llm_service.LLMService._LLMService__fetch_ollama_models")
    @patch("API.services.llm_service.LLMRepository")
    def test_sync_empty_models(self, mock_repo, mock_fetch):
        """Test con lista modelli vuota"""
        mock_fetch.return_value = []

        LLMService.sync_ollama_llms()

        mock_fetch.assert_called_once()
        mock_repo.update_or_create.assert_not_called()
