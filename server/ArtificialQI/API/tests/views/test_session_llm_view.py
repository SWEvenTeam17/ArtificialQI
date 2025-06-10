import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ArtificialQI.settings")
django.setup()
from unittest.mock import patch

import pytest
from API.models import LLM, Session
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def llm(db):
    return LLM.objects.create(name="GPT-4", n_parameters="1T")


@pytest.fixture
def session(db, llm):
    session = Session.objects.create(title="Benchmark Session")
    session.llm.set([llm])
    session.save()
    session.refresh_from_db()
    return session


@pytest.fixture
def get_url(session):
    return f"/llm_list_by_session/{session.pk}/"


@pytest.fixture
def post_url():
    return "/llm_add/"


@pytest.fixture
def delete_url(session, llm):
    return f"/llm_delete/{session.pk}/{llm.pk}"


@patch("API.views_def.session_llm_view.SessionService.get_excluded_llm")
def test_get_llms_by_session(mock_get_excluded_llm, client, get_url, llm):
    mock_get_excluded_llm.return_value = [{"id": 2, "name": "Fake LLM"}]
    response = client.get(get_url)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)
    ids = [item["id"] for item in response.data]
    assert llm.id not in ids
    mock_get_excluded_llm.assert_called_once()


def test_get_llms_by_session(client, get_url, session, llm):
    session.refresh_from_db()
    response = client.get(get_url)
    print("RESPONSE DATA:", response.data)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)
    ids = [item["id"] for item in response.data]
    assert llm.id not in ids


@patch(
    "API.views_def.session_llm_view.SessionService.get_excluded_llm",
    side_effect=Session.DoesNotExist,
)
def test_get_llms_by_session_not_found(mock_get_llm, client, session):
    url = f"/llm_list_by_session/9999/"
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["error"] == "Session not found"


@patch(
    "API.views_def.session_llm_view.SessionService.get_excluded_llm",
    side_effect=LLM.DoesNotExist,
)
def test_get_llms_by_session_llm_not_found(mock_get_llm, client, session):
    url = f"/llm_list_by_session/{session.pk}/"
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["error"] == "LLM not found"


@patch(
    "API.views_def.session_llm_view.SessionService.get_excluded_llm",
    side_effect=Exception("Errore generico"),
)
def test_get_llms_by_session_generic_error(mock_get_llm, client, session):
    url = f"/llm_list_by_session/{session.pk}/"
    response = client.get(url)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "error" in response.data


@patch("API.views_def.session_llm_view.SessionService.add_llm")
def test_post_add_llm_to_session(mock_add_llm, client, post_url):
    llm = LLM(id=123, name="Fake LLM", n_parameters="1T")
    mock_add_llm.return_value = llm
    response = client.post(post_url, {"sessionId": 1, "llmId": 123}, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["id"] == 123
    mock_add_llm.assert_called_once_with(session_id=1, llm_id=123)


@patch(
    "API.views_def.session_llm_view.SessionService.add_llm",
    side_effect=Session.DoesNotExist,
)
def test_post_add_llm_session_not_found(mock_add_llm, client, post_url):
    response = client.post(post_url, {"sessionId": 9999, "llmId": 1}, format="json")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["error"] == "Session not found"


@patch(
    "API.views_def.session_llm_view.SessionService.add_llm",
    side_effect=LLM.DoesNotExist,
)
def test_post_add_llm_llm_not_found(mock_add_llm, client, post_url, session):
    response = client.post(
        post_url, {"sessionId": session.pk, "llmId": 9999}, format="json"
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["error"] == "LLM not found"


@patch(
    "API.views_def.session_llm_view.SessionService.add_llm",
    side_effect=Exception("Errore generico"),
)
def test_post_add_llm_generic_error(mock_add_llm, client, post_url, session):
    response = client.post(
        post_url, {"sessionId": session.pk, "llmId": 1}, format="json"
    )
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "error" in response.data


@patch("API.views_def.session_llm_view.SessionService.delete_llm")
def test_delete_llm_from_session_unit(mock_delete_llm, client, delete_url):
    mock_delete_llm.return_value = None
    response = client.delete(delete_url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    mock_delete_llm.assert_called_once()


@patch(
    "API.views_def.session_llm_view.SessionService.delete_llm",
    side_effect=Session.DoesNotExist,
)
def test_delete_llm_session_not_found(mock_delete_llm, client, session, llm):
    url = f"/llm_delete/9999/{llm.pk}"
    response = client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["error"] == "Session not found"


@patch(
    "API.views_def.session_llm_view.SessionService.delete_llm",
    side_effect=LLM.DoesNotExist,
)
def test_delete_llm_llm_not_found(mock_delete_llm, client, session, llm):
    url = f"/llm_delete/{session.pk}/9999"
    response = client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["error"] == "LLM not found"


@patch(
    "API.views_def.session_llm_view.SessionService.delete_llm",
    side_effect=Exception("Errore generico"),
)
def test_delete_llm_generic_error(mock_delete_llm, client, session, llm):
    url = f"/llm_delete/{session.pk}/{llm.pk}"
    response = client.delete(url)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "error" in response.data
