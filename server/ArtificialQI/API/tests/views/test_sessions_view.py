import pytest
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def base_url():
    return "/session_list/"

@pytest.fixture
def session(db):
    from API.models import Session
    return Session.objects.create(title="Sessione Test", description="Descrizione test")

@pytest.fixture
def detail_url(session):
    return f"/session_list/{session.pk}/"

# --- GET ALL SUCCESS ---
def test_get_all_sessions(client, base_url, session):
    response = client.get(base_url)
    assert response.status_code == status.HTTP_200_OK
    assert any(s["id"] == session.id for s in response.data)

# --- GET BY ID SUCCESS ---
def test_get_session_by_id(client, detail_url, session):
    response = client.get(detail_url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == session.id

# --- GET EXCEPTION ---
@patch("API.views_def.sessions_view.SessionService.read_all", side_effect=Exception("Errore get all"))
def test_get_all_sessions_exception(mock_read_all, client, base_url):
    response = client.get(base_url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data

# --- POST SUCCESS ---
@pytest.mark.django_db
def test_post_valid_session(client, base_url):
    data = {"title": "Nuova Sessione", "description": "Descrizione"}
    response = client.post(base_url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == "Nuova Sessione"

# --- POST INVALID SERIALIZER ---
def test_post_invalid_session(client, base_url):
    data = {}  # manca title e description
    response = client.post(base_url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "title" in response.data

# --- POST EXCEPTION ---
@pytest.mark.django_db
@patch("API.views_def.sessions_view.SessionService.create", side_effect=Exception("Errore post"))
def test_post_session_exception(mock_create, client, base_url):
    data = {"title": "Nuova Sessione", "description": "Descrizione"}
    response = client.post(base_url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data

# --- PUT SUCCESS ---
def test_put_valid_session(client, detail_url, session):
    updated_data = {"title": "Sessione Aggiornata", "description": "Descrizione modificata"}
    response = client.put(detail_url, updated_data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == "Sessione Aggiornata"

# --- PUT INVALID SERIALIZER ---
def test_put_invalid_session(client, detail_url):
    updated_data = {}  # manca title e description
    response = client.put(detail_url, updated_data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "title" in response.data

# --- PUT EXCEPTION ---
@patch("API.views_def.sessions_view.SessionService.update", side_effect=Exception("Errore put"))
def test_put_session_exception(mock_update, client, detail_url, session):
    updated_data = {"title": "Sessione Aggiornata", "description": "Descrizione modificata"}
    response = client.put(detail_url, updated_data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data

# --- DELETE SUCCESS ---
def test_delete_session(client, detail_url):
    response = client.delete(detail_url)
    assert response.status_code == status.HTTP_204_NO_CONTENT

# --- DELETE EXCEPTION ---
@patch("API.views_def.sessions_view.SessionService.delete", side_effect=Exception("Errore delete"))
def test_delete_session_exception(mock_delete, client, detail_url):
    response = client.delete(detail_url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data