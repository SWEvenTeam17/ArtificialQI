import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ArtificialQI.settings")
django.setup()
import pytest
from unittest.mock import patch, MagicMock
from rest_framework.test import APIClient
from rest_framework import status


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def base_url():
    return "/prompt_list/"


@pytest.fixture
def session(db):
    from API.models import Session

    return Session.objects.create(title="Test Session")


@pytest.fixture
def prompt(db, session):
    from API.models import Prompt

    return Prompt.objects.create(prompt_text="Test?", expected_answer="42")


# --- GET ALL SUCCESS ---
@patch("API.views_def.prompt_view.PromptService.read_all")
@patch("API.views_def.prompt_view.PromptSerializer")
def test_get_all_prompts_success(
    mock_serializer, mock_service, client, base_url, prompt
):
    # Aggiungi anche 'expected_answer' e 'timestamp'
    mock_service.return_value = [
        {
            "id": prompt.id,
            "prompt_text": "Test?",
            "expected_answer": "42",
            "timestamp": str(prompt.timestamp),  # deve essere una stringa ISO
            "evaluation_set": [],
        }
    ]

    class FakeSerializer:
        def __init__(self, data, many=False):
            self._data = data

        @property
        def data(self):
            return self._data

    mock_serializer.side_effect = FakeSerializer
    response = client.get(base_url)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)


# --- GET ALL EXCEPTION ---
@patch(
    "API.views_def.prompt_view.PromptService.read_all",
    side_effect=Exception("Errore get all"),
)
def test_get_all_prompts_exception(mock_service, client, base_url):
    response = client.get(base_url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data


# --- GET BY ID SUCCESS ---
@patch("API.views_def.prompt_view.PromptService.read")
@patch("API.views_def.prompt_view.PromptSerializer")
def test_get_prompt_by_id_success(mock_serializer, mock_service, client, prompt):
    mock_service.return_value = {
        "id": prompt.id,
        "prompt_text": "Test?",
        "expected_answer": "42",
        "timestamp": str(prompt.timestamp),
        "evaluation_set": [],
    }

    class FakeSerializer:
        def __init__(self, data, many=False):
            self._data = data

        @property
        def data(self):
            return self._data

    mock_serializer.side_effect = FakeSerializer
    url = f"/prompt_list/{prompt.id}/"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == prompt.id


# --- GET BY ID EXCEPTION ---
@patch(
    "API.views_def.prompt_view.PromptService.read",
    side_effect=Exception("Errore get by id"),
)
def test_get_prompt_by_id_exception(mock_service, client, prompt):
    url = f"/prompt_list/{prompt.id}/"
    response = client.get(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data


# --- POST SUCCESS ---
@patch("API.views_def.prompt_view.PromptService.create")
@patch("API.views_def.prompt_view.PromptSerializer")
def test_post_prompt_success(mock_serializer, mock_service, client, session):
    valid_data = {
        "prompt_text": "Test?",
        "expected_answer": "42",
        "session": session.id,
    }
    instance = mock_serializer.return_value
    instance.is_valid.return_value = True
    instance.validated_data = valid_data
    instance.data = valid_data
    response = client.post("/prompt_list/", data=valid_data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["prompt_text"] == "Test?"


# --- POST INVALID SERIALIZER ---
@patch("API.views_def.prompt_view.PromptSerializer")
def test_post_prompt_invalid_serializer(mock_serializer, client):
    instance = mock_serializer.return_value
    instance.is_valid.return_value = False
    instance.errors = {"prompt_text": ["Questo campo è obbligatorio."]}
    response = client.post("/prompt_list/", data={}, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "prompt_text" in response.data


# --- POST EXCEPTION ---
@patch(
    "API.views_def.prompt_view.PromptService.create",
    side_effect=Exception("Errore post"),
)
@patch("API.views_def.prompt_view.PromptSerializer")
def test_post_prompt_exception(mock_serializer, mock_service, client, session):
    valid_data = {
        "prompt_text": "Test?",
        "expected_answer": "42",
        "session": session.id,
    }
    instance = mock_serializer.return_value
    instance.is_valid.return_value = True
    instance.validated_data = valid_data
    instance.data = valid_data
    response = client.post("/prompt_list/", data=valid_data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data


# --- PUT SUCCESS ---
@patch("API.views_def.prompt_view.PromptService.update")
@patch("API.views_def.prompt_view.PromptSerializer")
def test_put_prompt_success(mock_serializer, mock_service, client, prompt, session):
    updated_data = {
        "prompt_text": "Updated?",
        "expected_answer": "43",
        "session": session.id,
    }
    instance = mock_serializer.return_value
    instance.is_valid.return_value = True
    instance.validated_data = updated_data
    instance.data = updated_data
    url = f"/prompt_list/{prompt.id}/"
    response = client.put(url, data=updated_data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["prompt_text"] == "Updated?"


# --- PUT INVALID SERIALIZER ---
@patch("API.views_def.prompt_view.PromptSerializer")
def test_put_prompt_invalid_serializer(mock_serializer, client, prompt):
    instance = mock_serializer.return_value
    instance.is_valid.return_value = False
    instance.errors = {"prompt_text": ["Questo campo è obbligatorio."]}
    url = f"/prompt_list/{prompt.id}/"
    response = client.put(url, data={}, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "prompt_text" in response.data


# --- PUT EXCEPTION ---
@patch(
    "API.views_def.prompt_view.PromptService.update",
    side_effect=Exception("Errore put"),
)
@patch("API.views_def.prompt_view.PromptSerializer")
def test_put_prompt_exception(mock_serializer, mock_service, client, prompt, session):
    updated_data = {
        "prompt_text": "Updated?",
        "expected_answer": "43",
        "session": session.id,
    }
    instance = mock_serializer.return_value
    instance.is_valid.return_value = True
    instance.validated_data = updated_data
    instance.data = updated_data
    url = f"/prompt_list/{prompt.id}/"
    response = client.put(url, data=updated_data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data


# --- DELETE SUCCESS ---
@patch("API.views_def.prompt_view.PromptService.delete")
def test_delete_prompt_success(mock_service, client, prompt):
    url = f"/prompt_list/{prompt.id}/"
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT


# --- DELETE EXCEPTION ---
@patch(
    "API.views_def.prompt_view.PromptService.delete",
    side_effect=Exception("Errore delete"),
)
def test_delete_prompt_exception(mock_service, client, prompt):
    url = f"/prompt_list/{prompt.id}/"
    response = client.delete(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data
