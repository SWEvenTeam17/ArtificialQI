import pytest
from rest_framework.test import APIClient
from API.models import Prompt, LLM, Answer, Session

@pytest.fixture
def setup_data(db):
    client = APIClient()
    llm = LLM.objects.create(name="llama3.2", n_parameters="3B")
    session = Session.objects.create(title="Test session")
    session.llm.add(llm)
    prompt = Prompt.objects.create(
        prompt_text="Qual è la capitale della Francia?",
        expected_answer="Parigi",
        session=session,
    )
    answer = Answer.objects.create(
        prompt=prompt,
        LLM=llm,
        LLM_answer="Parigi",
    )
    base_url = "/answer_list/"
    detail_url = f"/answer_list/{answer.pk}/"
    return {
        "client": client,
        "llm": llm,
        "session": session,
        "prompt": prompt,
        "answer": answer,
        "base_url": base_url,
        "detail_url": detail_url,
    }

def test_get_all_answers(setup_data):
    client = setup_data["client"]
    base_url = setup_data["base_url"]
    response = client.get(base_url)
    assert response.status_code == 200
    assert len(response.data) == 1

def test_get_answer_by_id(setup_data):
    client = setup_data["client"]
    detail_url = setup_data["detail_url"]
    answer = setup_data["answer"]
    response = client.get(detail_url)
    assert response.status_code == 200
    assert response.data["id"] == answer.id

def test_post_valid_answer(setup_data):
    client = setup_data["client"]
    base_url = setup_data["base_url"]
    prompt = setup_data["prompt"]
    llm = setup_data["llm"]
    data = {
        "prompt": prompt.id,
        "LLM": llm.id,
        "LLM_answer": "Parigi"
    }
    response = client.post(base_url, data, format="json")
    assert response.status_code == 201

def test_put_valid_answer(setup_data):
    client = setup_data["client"]
    detail_url = setup_data["detail_url"]
    prompt = setup_data["prompt"]
    llm = setup_data["llm"]
    updated_data = {
        "prompt": prompt.id,
        "LLM": llm.id,
        "LLM_answer": "Parigi aggiornata"
    }
    response = client.put(detail_url, updated_data, format="json")
    assert response.status_code == 200
    assert response.data["LLM_answer"] == "Parigi aggiornata"

def test_delete_answer(setup_data):
    client = setup_data["client"]
    detail_url = setup_data["detail_url"]
    response = client.delete(detail_url)
    assert response.status_code == 204