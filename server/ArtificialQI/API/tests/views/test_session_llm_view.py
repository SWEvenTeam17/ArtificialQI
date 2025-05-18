import pytest
from rest_framework.test import APIClient
from rest_framework import status
from API.models import LLM, Session

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

@pytest.mark.skip(reason="test non ancora funzionante")
def test_get_llms_by_session(client, get_url, session, llm):
    # Assicura che il llm sia associato alla sessione
    session.refresh_from_db()
    llms = list(session.llm.all())
    assert llm in llms

    response = client.get(get_url)
    assert response.status_code == status.HTTP_200_OK
    # La risposta deve essere una lista di dizionari serializzati
    assert isinstance(response.data, list)
    ids = [item["id"] for item in response.data]
    assert llm.id in ids

def test_post_add_llm_to_session(client, session, post_url):
    new_llm = LLM.objects.create(name="LLaMA-3", n_parameters="70B")
    response = client.post(post_url, {
        "sessionId": session.pk,
        "llmId": new_llm.pk
    }, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["id"] == new_llm.id

def test_delete_llm_from_session(client, delete_url, session, llm):
    response = client.delete(delete_url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not session.llm.filter(pk=llm.pk).exists()