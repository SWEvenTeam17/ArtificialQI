import pytest
from rest_framework.test import APIClient
from rest_framework import status
from API.models import Prompt, Session, LLM

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def llm(db):
    return LLM.objects.create(name="GPT-3.5", n_parameters="175B")

@pytest.fixture
def session(db, llm):
    session = Session.objects.create(title="Sessione di test")
    session.llm.add(llm)
    return session

@pytest.fixture
def prompt(db, session):
    return Prompt.objects.create(
        prompt_text="Cosa fa il photosistema II?",
        expected_answer="Produce ossigeno",
        session=session,
    )

@pytest.fixture
def base_url():
    return "/prompt_list/"

@pytest.fixture
def detail_url(prompt):
    return f"/prompt_list/{prompt.pk}/"

def test_get_all_prompts(client, base_url, prompt):
    response = client.get(base_url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) >= 1

def test_get_prompt_by_id(client, detail_url, prompt):
    response = client.get(detail_url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == prompt.id

def test_post_valid_prompt(client, base_url, session):
    data = {
        "prompt_text": "Qual è la capitale dell’Italia?",
        "expected_answer": "Roma",
        "session": session.id,
    }
    response = client.post(base_url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED

def test_put_valid_prompt(client, detail_url, session):
    updated_data = {
        "prompt_text": "Qual è la capitale dell’Italia aggiornata?",
        "expected_answer": "Roma",
        "session": session.id,
    }
    response = client.put(detail_url, updated_data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["prompt_text"] == updated_data["prompt_text"]

def test_delete_prompt(client, detail_url):
    response = client.delete(detail_url)
    assert response.status_code == status.HTTP_204_NO_CONTENT