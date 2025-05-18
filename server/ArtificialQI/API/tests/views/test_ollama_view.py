import pytest
from unittest.mock import patch
from rest_framework.test import APIClient
from rest_framework import status

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def url():
    return "/llm_list/load_ollama/"

@patch("API.services.LLMService.sync_ollama_llms")
def test_sync_success(mock_sync, client, url):
    mock_sync.return_value = None  # simuliamo il successo
    response = client.post(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["message"] == "LLM models loaded successfully from Ollama server"

@patch("API.services.LLMService.sync_ollama_llms")
def test_sync_failure(mock_sync, client, url):
    mock_sync.side_effect = Exception("Errore di connessione")
    response = client.post(url)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "error" in response.data