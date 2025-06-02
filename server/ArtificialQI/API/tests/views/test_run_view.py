import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ArtificialQI.settings")
django.setup()
from unittest.mock import patch

import pytest
from rest_framework.test import APIClient

RUNPROMPT_URL = "/prompt_runs"


@pytest.fixture
def api_client():
    return APIClient()


# --- GET: prompt_id mancante ---
def test_runpromptview_get_missing_prompt_id(api_client):
    response = api_client.get(RUNPROMPT_URL)
    assert response.status_code == 400
    assert response.data["error"] == "Missing prompt_id."


# --- GET: prompt_id non intero ---
def test_runpromptview_get_invalid_prompt_id(api_client):
    response = api_client.get(RUNPROMPT_URL, {"prompt_id": "abc"})
    assert response.status_code == 400
    assert response.data["error"] == "Invalid prompt_id."


# --- GET: prompt non trovato ---
@patch("API.views_def.run_view.RunService.get_formatted_by_prompt")
def test_runpromptview_get_prompt_not_found(mock_get, api_client):
    mock_get.return_value = None
    response = api_client.get(RUNPROMPT_URL, {"prompt_id": "1"})
    assert response.status_code == 404
    assert response.data["error"] == "Prompt not found."
    mock_get.assert_called_once_with(prompt_id=1)


# --- GET: successo ---
@patch("API.views_def.run_view.RunService.get_formatted_by_prompt")
def test_runpromptview_get_success(mock_get, api_client):
    mock_get.return_value = [{"run": 1}]
    response = api_client.get(RUNPROMPT_URL, {"prompt_id": "1"})
    assert response.status_code == 200
    assert response.data == [{"run": 1}]
    mock_get.assert_called_once_with(prompt_id=1)


# --- DELETE: run_id mancante ---
def test_runpromptview_delete_missing_run_id(api_client):
    response = api_client.delete(RUNPROMPT_URL)
    assert response.status_code == 400
    assert response.data["error"] == "Missing run_id."


# --- DELETE: run_id non intero ---
def test_runpromptview_delete_invalid_run_id(api_client):
    response = api_client.delete(f"{RUNPROMPT_URL}?run_id=abc")
    assert response.status_code == 400
    assert response.data["error"] == "Invalid run_id."


# --- DELETE: successo ---
@patch("API.views_def.run_view.RunService.delete")
def test_runpromptview_delete_success(mock_delete, api_client):
    response = api_client.delete(f"{RUNPROMPT_URL}?run_id=5")
    assert response.status_code == 204
    mock_delete.assert_called_once_with(5)


# --- DELETE: ValueError (run non trovato) ---
@patch(
    "API.views_def.run_view.RunService.delete", side_effect=ValueError("Run not found")
)
def test_runpromptview_delete_not_found(mock_delete, api_client):
    response = api_client.delete(f"{RUNPROMPT_URL}?run_id=5")
    assert response.status_code == 404
    assert response.data["error"] == "Run not found"
    mock_delete.assert_called_once_with(5)


# --- DELETE: generic Exception ---
@patch(
    "API.views_def.run_view.RunService.delete", side_effect=Exception("Errore generico")
)
def test_runpromptview_delete_generic_error(mock_delete, api_client):
    response = api_client.delete(f"{RUNPROMPT_URL}?run_id=5")
    assert response.status_code == 400
    assert response.data["error"] == "Errore generico"
    mock_delete.assert_called_once_with(5)
