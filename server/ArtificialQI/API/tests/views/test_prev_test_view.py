import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ArtificialQI.settings")
django.setup()
import pytest
from unittest.mock import patch, MagicMock
from rest_framework.test import APIClient

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def url():
    return "/previous_tests/"

# --- GET con test_id (ramo TestService.format_results) ---
@patch("API.views_def.prev_test_view.BlockTestService.format_results")
@patch("API.views_def.prev_test_view.PrevTestService.read")
def test_get_previous_tests_with_test_id(mock_read, mock_format_results, client, url):
    mock_read.return_value = MagicMock()
    mock_format_results.return_value = {"result": "ok"}
    response = client.get(f"{url}1/?test_id=5")
    assert response.status_code == 200
    assert response.json() == {"result": "ok"}
    mock_read.assert_called_once_with(instance_id='5')  # test_id è una stringa da GET
    mock_format_results.assert_called_once()

@patch("API.views_def.prev_test_view.BlockTestSerializer")
@patch("API.views_def.prev_test_view.PrevTestService.get_tests_by_session")
def test_get_previous_tests_by_session(mock_get_tests, mock_serializer, client, url):
    mock_get_tests.return_value = [
        {"id": 1, "session": None, "block": None, "timestamp": "2024-01-01T00:00:00Z", "run": []},
        {"id": 2, "session": None, "block": None, "timestamp": "2024-01-01T00:00:00Z", "run": []}
    ]
    class FakeSerializer:
        def __init__(self, data, many=False):
            self._data = data
        @property
        def data(self):
            return self._data
    mock_serializer.side_effect = FakeSerializer
    response = client.get(f"{url}1/")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "session": None, "block": None, "timestamp": "2024-01-01T00:00:00Z", "run": []},
        {"id": 2, "session": None, "block": None, "timestamp": "2024-01-01T00:00:00Z", "run": []}
    ]
    mock_get_tests.assert_called_once_with(1)
    
# --- GET: Test.DoesNotExist ---
@patch("API.views_def.prev_test_view.PrevTestService.get_tests_by_session", side_effect=Exception("Test not found"))
def test_get_previous_tests_not_found(mock_get_tests, client, url):
    response = client.get(f"{url}999/")
    assert response.status_code == 400
    assert "error" in response.json()

# --- GET: generic Exception ---
@patch("API.views_def.prev_test_view.PrevTestService.get_tests_by_session", side_effect=Exception("Errore generico"))
def test_get_previous_tests_generic_error(mock_get_tests, client, url):
    response = client.get(f"{url}999/")
    assert response.status_code == 400
    assert "error" in response.json()

# --- DELETE successo ---
@patch("API.views_def.prev_test_view.BlockTestService.delete")
def test_delete_previous_tests_success(mock_delete, client, url):
    mock_delete.return_value = None
    session_id = 1
    response = client.delete(f"{url}{session_id}/")
    mock_delete.assert_called_once_with(instance_id=session_id)
    assert response.status_code == 204

# --- DELETE: Test.DoesNotExist ---
@patch("API.views_def.prev_test_view.BlockTestService.delete", side_effect=Exception("Test not found"))
def test_delete_previous_tests_not_found(mock_delete, client, url):
    response = client.delete(f"{url}999/")
    assert response.status_code == 400
    assert "error" in response.json()

# --- DELETE: generic Exception ---
@patch("API.views_def.prev_test_view.BlockTestService.delete", side_effect=Exception("Errore cancellazione"))
def test_delete_previous_tests_error(mock_delete, client, url):
    response = client.delete(f"{url}123/")
    assert response.status_code == 400
    assert "error" in response.json()