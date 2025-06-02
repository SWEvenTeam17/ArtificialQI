import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ArtificialQI.settings")
django.setup()
from unittest.mock import MagicMock, patch

import pytest
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def url():
    return "/runtest"


# --- POST SUCCESS ---
@patch("API.views_def.test_view.BlockTestService.runtest")
@patch("API.views_def.test_view.BlockService.retrieve_blocks")
@patch("API.views_def.test_view.SessionService.read")
def test_post_test_success(
    mock_session_read, mock_block_retrieve, mock_runtest, client, url
):
    mock_session_read.return_value = MagicMock()
    mock_block_retrieve.return_value = [MagicMock()]
    mock_runtest.return_value = {"result": "ok"}
    data = {"sessionId": 1, "blocks": [1, 2]}
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {"result": "ok"}


# --- POST ConnectionError ---
@patch(
    "API.views_def.test_view.BlockTestService.runtest",
    side_effect=ConnectionError("Connessione persa"),
)
@patch("API.views_def.test_view.BlockService.retrieve_blocks")
@patch("API.views_def.test_view.SessionService.read")
def test_post_test_connection_error(
    mock_session_read, mock_block_retrieve, mock_runtest, client, url
):
    mock_session_read.return_value = MagicMock()
    mock_block_retrieve.return_value = [MagicMock()]
    data = {"sessionId": 1, "blocks": [1, 2]}
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert response.data["error"] == "Connessione persa"


# --- POST FileNotFoundError ---
@patch(
    "API.views_def.test_view.BlockTestService.runtest",
    side_effect=FileNotFoundError("File mancante"),
)
@patch("API.views_def.test_view.BlockService.retrieve_blocks")
@patch("API.views_def.test_view.SessionService.read")
def test_post_test_file_not_found_error(
    mock_session_read, mock_block_retrieve, mock_runtest, client, url
):
    mock_session_read.return_value = MagicMock()
    mock_block_retrieve.return_value = [MagicMock()]
    data = {"sessionId": 1, "blocks": [1, 2]}
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.data["error"] == "File mancante"


# --- POST errore sconosciuto ---
@patch(
    "API.views_def.test_view.BlockTestService.runtest",
    side_effect=Exception("Errore generico"),
)
@patch("API.views_def.test_view.BlockService.retrieve_blocks")
@patch("API.views_def.test_view.SessionService.read")
def test_post_test_generic_error(
    mock_session_read, mock_block_retrieve, mock_runtest, client, url
):
    mock_session_read.return_value = MagicMock()
    mock_block_retrieve.return_value = [MagicMock()]
    data = {"sessionId": 1, "blocks": [1, 2]}
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.data["error"] == "Errore inatteso: Errore generico"
