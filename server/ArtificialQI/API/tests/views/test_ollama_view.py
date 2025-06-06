import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ArtificialQI.settings")
django.setup()
from unittest.mock import patch

import pytest
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def url():
    return "/llm_list/load_ollama/"


@patch("API.views_def.llm_view.LLMService.sync_ollama_llms")
def test_ollama_view_post_success(mock_sync, client, url):
    print("test_ollama_view_post_success")
    mock_sync.return_value = None
    response = client.post(url)
    assert response.status_code == status.HTTP_200_OK
    assert (
        response.json()["message"]
        == "LLM models loaded successfully from Ollama server"
    )
    mock_sync.assert_called_once()


@patch(
    "API.views_def.llm_view.LLMService.sync_ollama_llms",
    side_effect=Exception("Errore Ollama"),
)
def test_ollama_view_post_error(mock_sync, client, url):
    print("test_ollama_view_post_error")
    response = client.post(url)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "error" in response.json()
    assert response.json()["error"] == "Errore Ollama"
