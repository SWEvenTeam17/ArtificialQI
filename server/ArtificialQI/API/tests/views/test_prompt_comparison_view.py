# import pytest
# from unittest.mock import patch, MagicMock
# from rest_framework.test import APIClient

# @pytest.fixture
# def client():
#     return APIClient()

# @pytest.fixture
# def url():
#     # Assicurati che sia la route corretta nel tuo urls.py
#     return "/prompt_comparison/"

# @patch("API.views_def.llm_view.LLMService.compare_prompts")
# @patch("API.views_def.llm_view.BlockTestSerializer")
# def test_prompt_comparison_view_success(mock_serializer, mock_compare, client, url):
#     # Mock dei dati restituiti dal service
#     mock_tests = [MagicMock(), MagicMock()]
#     mock_compare.return_value = {
#         "tests": mock_tests,
#         "averages": {"semantic_average": 0.9, "external_average": 0.8},
#     }
#     # Mock del serializer
#     mock_serializer.return_value.data = [
#         {"id": 1, "field": "value1"},
#         {"id": 2, "field": "value2"},
#     ]

#     params = {
#         "llm_id": 1,
#         "session_id": 2,
#     }
#     response = client.get(url, params)
#     assert response.status_code == 200
#     data = response.json()
#     assert "tests" in data
#     assert "averages" in data
#     assert data["tests"] == [
#         {"id": 1, "field": "value1"},
#         {"id": 2, "field": "value2"},
#     ]
#     assert data["averages"] == {"semantic_average": 0.9, "external_average": 0.8}

# @patch("API.views_def.llm_view.LLMService.compare_prompts", side_effect=Exception("Errore confronto prompt"))
# def test_prompt_comparison_view_error(mock_compare, client, url):
#     params = {
#         "llm_id": 1,
#         "session_id": 2,
#     }
#     with pytest.raises(Exception) as excinfo:
#         client.get(url, params)
#     assert "Errore confronto prompt" in str(excinfo.value)