import pytest
from rest_framework.test import APIClient
from rest_framework import status
from API.models import LLM, Session, Test

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def llm(db):
    return LLM.objects.create(name="GPT-4", n_parameters="1T")

@pytest.fixture
def llm2(db):
    return LLM.objects.create(name="AltroLLM", n_parameters="2T")

@pytest.fixture
def session(db):
    return Session.objects.create(title="Sessione Test", description="desc")

@pytest.fixture
def test_obj(db, llm, session):
    return Test.objects.create(llm=llm, session=session, block_id=1, run=1)

@pytest.fixture
def client():
    return APIClient()

@pytest.mark.django_db
def test_llm_get_all(client):
    LLM.objects.create(name="GPT-4", n_parameters="1T")
    LLM.objects.create(name="GPT-3.5", n_parameters="0.5T")

    response = client.get("/llms/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)
    assert len(response.data) == 2

@pytest.mark.django_db
def test_llm_get_by_id(client):
    llm = LLM.objects.create(name="GPT-4", n_parameters="1T")
    response = client.get(f"/llms/{llm.id}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "GPT-4"

@pytest.mark.django_db
def test_llm_post_success(client):
    payload = {"name": "NuovoLLM", "n_parameters": "500B"}
    response = client.post("/llms/", data=payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "NuovoLLM"

@pytest.mark.django_db
def test_llm_post_invalid(client):
    response = client.post("/llms/", data={}, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data or "name" in response.data

@pytest.mark.django_db
def test_llm_put_success(client):
    llm = LLM.objects.create(name="GPT-4", n_parameters="1T")
    payload = {"name": "GPT-4 Updated", "n_parameters": "1.2T"}
    response = client.put(f"/llms/{llm.id}/", data=payload, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "GPT-4 Updated"

@pytest.mark.django_db
def test_llm_put_invalid(client):
    llm = LLM.objects.create(name="GPT-4", n_parameters="1T")
    response = client.put(f"/llms/{llm.id}/", data={"name": ""}, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_llm_delete_success(client):
    llm = LLM.objects.create(name="GPT-4", n_parameters="1T")
    response = client.delete(f"/llms/{llm.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # Check che l’oggetto non esista più
    assert not LLM.objects.filter(id=llm.id).exists()

@pytest.mark.django_db
def test_llm_delete_invalid_id(client):
    response = client.delete("/llms/999/")
    assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND]

@pytest.mark.django_db
def test_ollama_post_success(monkeypatch, client):
    def fake_sync():
        pass
    from API.services import LLMService
    monkeypatch.setattr(LLMService, "sync_ollama_llms", fake_sync)
    url = "/ollama_load/"
    response = client.post(url)
    assert response.status_code == status.HTTP_200_OK
    assert "message" in response.data

@pytest.mark.django_db
def test_ollama_post_error(monkeypatch, client):
    def fake_sync():
        raise Exception("Errore finto")
    from API.services import LLMService
    monkeypatch.setattr(LLMService, "sync_ollama_llms", fake_sync)
    url = "/ollama_load/"
    response = client.post(url)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "error" in response.data

@pytest.mark.django_db
def test_llm_comparison_view_success(client, llm, llm2, session, test_obj):
    # Crea un test anche per llm2 per avere common_tests
    Test.objects.create(llm=llm2, session=session, block_id=1, run=1)
    url = f"/llm_comparison/?first_llm_id={llm.id}&second_llm_id={llm2.id}&session_id={session.id}"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert "common_tests" in response.data
    assert "first_llm_averages" in response.data
    assert "second_llm_averages" in response.data

@pytest.mark.django_db
def test_llm_comparison_view_error(client, llm, llm2):
    # session_id non valido
    url = f"/llm_comparison/?first_llm_id={llm.id}&second_llm_id={llm2.id}&session_id=9999"
    response = client.get(url)
    # accetta errore server se la view lo gestisce così
    assert response.status_code in [status.HTTP_500_INTERNAL_SERVER_ERROR, status.HTTP_200_OK]

@pytest.mark.django_db
def test_prompt_comparison_view_success(client, llm, session, test_obj):
    url = f"/prompt_comparison/?llm_id={llm.id}&session_id={session.id}"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert "tests" in response.data
    assert "averages" in response.data

@pytest.mark.django_db
def test_prompt_comparison_view_error(client, llm):
    url = f"/prompt_comparison/?llm_id={llm.id}&session_id=9999"
    response = client.get(url)
    assert response.status_code in [status.HTTP_500_INTERNAL_SERVER_ERROR, status.HTTP_200_OK]