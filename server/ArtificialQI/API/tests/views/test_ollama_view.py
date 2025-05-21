import pytest
from unittest.mock import patch
from rest_framework.test import APIClient

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def url():
    return "/llm_list/load_ollama/"

@patch("API.views_def.llm_view.LLMService.sync_ollama_llms")
def test_ollama_view_post_success(mock_sync, client, url):
    mock_sync.return_value = None
    response = client.post(url)
    assert response.status_code == 200
    assert response.json()["message"] == "LLM models loaded successfully from Ollama server"
    mock_sync.assert_called_once()

@patch("API.views_def.llm_view.LLMService.sync_ollama_llms", side_effect=Exception("Errore Ollama"))
def test_ollama_view_post_error(mock_sync, client, url):
    response = client.post(url)
    assert response.status_code == 500
    assert "error" in response.json()
    assert response.json()["error"] == "Errore Ollama"