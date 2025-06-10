import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from unittest.mock import MagicMock, patch

import pytest
from api.services.ollama_llm_integration_service import \
    OllamaLLMIntegrationService
from requests.exceptions import RequestException

# --- Test get_llm ---


@patch("api.services.ollama_llm_integration_service.requests.get")
@patch("api.services.ollama_llm_integration_service.OllamaLLM")
@patch(
    "api.services.ollama_llm_integration_service.os.getenv",
    return_value="http://fake-url",
)
def test_get_llm_success(mock_getenv, mock_ollama, mock_requests_get):
    mock_response = MagicMock()
    mock_requests_get.return_value = mock_response
    mock_response.raise_for_status.return_value = None
    llm = OllamaLLMIntegrationService.get_llm("test-model")
    assert llm == mock_ollama.return_value
    mock_requests_get.assert_called_once_with("http://fake-url/api/version", timeout=5)
    mock_ollama.assert_called_once_with(model="test-model", base_url="http://fake-url")


@patch(
    "api.services.ollama_llm_integration_service.requests.get",
    side_effect=RequestException,
)
@patch(
    "api.services.ollama_llm_integration_service.os.getenv",
    return_value="http://fake-url",
)
def test_get_llm_failure(mock_getenv, mock_requests_get):
    llm = OllamaLLMIntegrationService.get_llm("test-model")
    assert llm is None


# --- Test interrogate ---


def test_interrogate():
    mock_llm = MagicMock()
    mock_stream = iter(["Hello", " world!"])
    mock_llm.stream.return_value = mock_stream
    result = OllamaLLMIntegrationService.interrogate(mock_llm, "prompt")
    assert result == "Hello world!"
    mock_llm.stream.assert_called_once_with("prompt")


# --- Test get_ollama_llms ---


@patch("api.services.ollama_llm_integration_service.requests.get")
@patch(
    "api.services.ollama_llm_integration_service.os.getenv",
    return_value="http://fake-url",
)
def test_get_ollama_llms_success(mock_getenv, mock_requests_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"models": [{"name": "llm1"}, {"name": "llm2"}]}
    mock_requests_get.return_value = mock_response
    result = OllamaLLMIntegrationService.get_ollama_llms()
    assert result == [{"name": "llm1"}, {"name": "llm2"}]
    mock_requests_get.assert_called_once_with("http://fake-url/api/tags")


@patch(
    "api.services.ollama_llm_integration_service.requests.get",
    side_effect=RequestException,
)
@patch(
    "api.services.ollama_llm_integration_service.os.getenv",
    return_value="http://fake-url",
)
def test_get_ollama_llms_failure(mock_getenv, mock_requests_get):
    result = OllamaLLMIntegrationService.get_ollama_llms()
    assert result is None
