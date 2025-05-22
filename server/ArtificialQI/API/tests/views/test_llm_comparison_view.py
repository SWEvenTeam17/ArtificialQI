import sys
sys.path.append("C:/Users/Alessandro/OneDrive/Desktop/progetto swe/ArtificialQI/server")
import pytest
from unittest.mock import patch, MagicMock
from rest_framework.test import APIClient
from rest_framework import status

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def url():
    return "/llm_comparison/"

@patch("API.views_def.llm_view.LLMService.compare_llms")
@patch("API.views_def.llm_view.TestSerializer")
def test_llm_comparison_view_success(mock_serializer, mock_compare, client, url):
    mock_common_tests = [MagicMock(), MagicMock()]
    mock_compare.return_value = {
        "common_tests": mock_common_tests,
        "first_llm_averages": {"semantic_average": 0.8, "external_average": 0.7},
        "second_llm_averages": {"semantic_average": 0.6, "external_average": 0.5},
    }
    mock_serializer.return_value.data = [
        {"id": 1, "field": "value1"},
        {"id": 2, "field": "value2"},
    ]

    params = {
        "first_llm_id": 1,
        "second_llm_id": 2,
        "session_id": 3,
    }
    response = client.get(url, params)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "common_tests" in data
    assert "first_llm_averages" in data
    assert "second_llm_averages" in data

@patch("API.views_def.llm_view.LLMService.compare_llms", side_effect=Exception("Errore confronto"))
def test_llm_comparison_view_error(mock_compare, client, url):
    params = {
        "first_llm_id": 1,
        "second_llm_id": 2,
        "session_id": 3,
    }
    with pytest.raises(Exception) as excinfo:
        client.get(url, params)
    assert str(excinfo.value) == "Errore confronto"