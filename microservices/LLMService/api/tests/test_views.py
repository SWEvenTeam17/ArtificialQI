import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import pytest
from rest_framework.test import APIRequestFactory
from unittest.mock import patch, MagicMock
from api.views import LLMView


@pytest.fixture
def factory():
    return APIRequestFactory()


# --- Test GET ---


@patch("api.views.LLMService.get_ollama_llms")
def test_llmview_get_success(mock_get_ollama_llms, factory):
    mock_get_ollama_llms.return_value = [{"name": "llm1"}]
    request = factory.get("/llms/")
    view = LLMView.as_view()
    response = view(request)
    assert response.status_code == 200
    assert response.data == [{"name": "llm1"}]


@patch("api.views.LLMService.get_ollama_llms", return_value=None)
def test_llmview_get_failure(mock_get_ollama_llms, factory):
    request = factory.get("/llms/")
    view = LLMView.as_view()
    response = view(request)
    assert response.status_code == 500
    assert "error" in response.data


# --- Test POST ---


@patch("api.views.LLMService.interrogate")
@patch("api.views.LLMService.get_llm")
def test_llmview_post_success(mock_get_llm, mock_interrogate, factory):
    mock_get_llm.return_value = MagicMock()
    mock_interrogate.return_value = "Risposta"
    data = {"llm_name": "llm1", "prompt": "ciao"}
    request = factory.post("/llms/", data, format="json")
    view = LLMView.as_view()
    response = view(request)
    assert response.status_code == 200
    assert response.data["llm_name"] == "llm1"
    assert response.data["prompt"] == "ciao"
    assert response.data["answer"] == "Risposta"


@patch("api.views.LLMService.get_llm", return_value=None)
def test_llmview_post_failure(mock_get_llm, factory):
    data = {"llm_name": "llm1", "prompt": "ciao"}
    request = factory.post("/llms/", data, format="json")
    view = LLMView.as_view()
    response = view(request)
    assert response.status_code == 500
    assert "error" in response.data
