import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from unittest.mock import MagicMock, patch

import pytest
from api.views import LLMServiceView
from rest_framework.test import APIRequestFactory


@pytest.fixture
def factory():
    return APIRequestFactory()


# --- Test GET ---


@patch("api.services.OllamaLLMIntegrationService.get_ollama_llms")
def test_llmserviceview_get_success(mock_get_ollama_llms, factory):
    mock_get_ollama_llms.return_value = [{"name": "llm1"}]
    request = factory.get("/llms/")
    view = LLMServiceView.as_view()
    response = view(request)
    assert response.status_code == 200
    assert response.data == [{"name": "llm1"}]


@patch("api.services.OllamaLLMIntegrationService.get_ollama_llms", return_value=None)
def test_llmserviceview_get_failure(mock_get_ollama_llms, factory):
    request = factory.get("/llms/")
    view = LLMServiceView.as_view()
    response = view(request)
    assert response.status_code == 500
    assert "error" in response.data


# --- Test POST ---


@patch("api.services.OllamaLLMIntegrationService.interrogate")
@patch("api.services.OllamaLLMIntegrationService.get_llm")
def test_llmserviceview_post_success(mock_get_llm, mock_interrogate, factory):
    mock_get_llm.return_value = MagicMock()
    mock_interrogate.return_value = "Risposta"
    data = {"llm_name": "llm1", "prompt": "ciao"}
    request = factory.post("/llms/", data, format="json")
    view = LLMServiceView.as_view()
    response = view(request)
    assert response.status_code == 200
    assert response.data["llm_name"] == "llm1"
    assert response.data["prompt"] == "ciao"
    assert response.data["answer"] == "Risposta"


@patch("api.services.OllamaLLMIntegrationService.get_llm", return_value=None)
def test_llmserviceview_post_failure(mock_get_llm, factory):
    data = {"llm_name": "llm1", "prompt": "ciao"}
    request = factory.post("/llms/", data, format="json")
    view = LLMServiceView.as_view()
    response = view(request)
    assert response.status_code == 500
    assert "error" in response.data
