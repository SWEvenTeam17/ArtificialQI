import pytest
from rest_framework.test import APIClient
from rest_framework import status
from API.models import Session

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def session(db):
    return Session.objects.create(
        title="Sessione Test",
        description="Questa è una sessione di prova"
    )

@pytest.fixture
def base_url():
    return "/session_list/"

@pytest.fixture
def detail_url(session):
    return f"/session_list/{session.pk}/"

def test_get_all_sessions(client, base_url, session):
    response = client.get(base_url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) >= 1

def test_get_session_by_id(client, detail_url, session):
    response = client.get(detail_url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == session.id

@pytest.mark.django_db
def test_post_valid_session(client, base_url):
    data = {
        "title": "Nuova Sessione",
        "description": "Descrizione della sessione"
    }
    response = client.post(base_url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == "Nuova Sessione"

def test_put_valid_session(client, detail_url, session):
    updated_data = {
        "title": "Sessione Aggiornata",
        "description": "Descrizione modificata"
    }
    response = client.put(detail_url, updated_data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == "Sessione Aggiornata"

def test_delete_session(client, detail_url):
    response = client.delete(detail_url)
    assert response.status_code == status.HTTP_204_NO_CONTENT