import pytest
from unittest.mock import patch, MagicMock
from rest_framework.test import APIClient

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def url():
    return "/previous_tests/"

@patch("API.views_def.prev_test_view.PromptService.filter_by_session")
@patch("API.views_def.prev_test_view.SessionService.read")
def test_get_previous_tests_success(mock_read, mock_filter_by_session, client, url):
    mock_read.return_value = MagicMock()
    mock_prompt = {"prompt_text": "Domanda?", "expected_answer": "Risposta"}
    mock_filter_by_session.return_value = [mock_prompt]
    response = client.get(f"{url}1/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    # Il serializer potrebbe restituire dict, quindi controlla la chiave
    assert response.json()[0].get("prompt_text") == "Domanda?"

@patch("API.views_def.prev_test_view.PromptService.filter_by_session", side_effect=Exception("Errore"))
@patch("API.views_def.prev_test_view.SessionService.read")
def test_get_previous_tests_error(mock_read, mock_filter, client, url):
    mock_read.return_value = MagicMock()
    response = client.get(f"{url}999/")
    assert response.status_code == 400
    assert "error" in response.json()

@patch("API.views_def.prev_test_view.PromptService.filter_by_session")
@patch("API.views_def.prev_test_view.SessionService.read")
def test_get_previous_tests_returns_empty_list(mock_read, mock_filter_by_session, client, url):
    mock_read.return_value = MagicMock()
    mock_filter_by_session.return_value = []
    response = client.get(f"{url}1/")
    assert response.status_code == 200
    assert response.json() == []

@patch("API.views_def.prev_test_view.PromptService.filter_by_session")
@patch("API.views_def.prev_test_view.SessionService.read")
def test_get_previous_tests_multiple_prompts(mock_read, mock_filter_by_session, client, url):
    mock_read.return_value = MagicMock()
    prompt1 = {"prompt_text": "Q1", "expected_answer": "A1"}
    prompt2 = {"prompt_text": "Q2", "expected_answer": "A2"}
    mock_filter_by_session.return_value = [prompt1, prompt2]
    response = client.get(f"{url}1/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0].get("prompt_text") == "Q1"
    assert data[1].get("prompt_text") == "Q2"

@patch("API.views_def.prev_test_view.PromptService.delete")
def test_delete_previous_tests_success(mock_delete, client, url):
    mock_delete.return_value = None
    session_id = 1
    response = client.delete(f"{url}{session_id}/")
    mock_delete.assert_called_once_with(instance_id=session_id)
    # La tua view restituisce status 200, quindi testiamo quello
    assert response.status_code == 200 or response.status_code == 204

@patch("API.views_def.prev_test_view.PromptService.delete", side_effect=Exception("Errore cancellazione"))
def test_delete_previous_tests_error(mock_delete, client, url):
    response = client.delete(f"{url}123/")
    assert response.status_code == 400
    assert "error" in response.json()