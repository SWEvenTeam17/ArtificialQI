import pytest
from unittest.mock import patch, MagicMock
from rest_framework.test import APIClient
from API.models import Session, Prompt

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def url():
    return "/previous_tests/"

@pytest.fixture
def session(db):
    return Session.objects.create(title="Test session")

@pytest.fixture
def prompt(db, session):
    return Prompt.objects.create(
        prompt_text="Domanda?",
        expected_answer="Risposta",
        session=session
    )

@patch("API.views_def.prev_test_view.PromptService.filter_by_session")
@patch("API.views_def.prev_test_view.SessionService.read")
def test_get_previous_tests_success(mock_read, mock_filter_by_session, client, url, session, prompt):
    mock_read.return_value = session
    mock_filter_by_session.return_value = [prompt]

    response = client.get(f"{url}{session.id}/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["prompt_text"] == "Domanda?"

@patch("API.views_def.prev_test_view.PromptService.filter_by_session", side_effect=Exception("Errore"))
@patch("API.views_def.prev_test_view.SessionService.read")
def test_get_previous_tests_error(mock_read, mock_filter, client, url):
    mock_read.return_value = MagicMock()
    response = client.get(f"{url}999/")
    assert response.status_code == 400
    assert "error" in response.json()

@patch("API.views_def.prev_test_view.PromptService.delete")
def test_delete_previous_tests_success(mock_delete, client, url):
    mock_delete.return_value = None
    session_id = 1
    response = client.delete(f"{url}{session_id}/")
    mock_delete.assert_called_once_with(instance_id=session_id)
    assert response.status_code == 204

@patch("API.views_def.prev_test_view.PromptService.delete", side_effect=Exception("Errore cancellazione"))
def test_delete_previous_tests_error(mock_delete, client, url):
    response = client.delete(f"{url}123/")
    assert response.status_code == 400
    assert "error" in response.json()