import pytest
from rest_framework.test import APIClient
from rest_framework import status
from API.models import LLM

@pytest.fixture
def setup_llm(db):
    client = APIClient()
    llm = LLM.objects.create(name="GPT-4", n_parameters="1T")
    base_url = "/llm_list/"
    detail_url = f"/llm_list/{llm.pk}/"
    return {
        "client": client,
        "llm": llm,
        "base_url": base_url,
        "detail_url": detail_url,
    }

def test_get_all_llms(setup_llm):
    client = setup_llm["client"]
    base_url = setup_llm["base_url"]
    response = client.get(base_url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) >= 1

def test_get_llm_by_id(setup_llm):
    client = setup_llm["client"]
    detail_url = setup_llm["detail_url"]
    llm = setup_llm["llm"]
    response = client.get(detail_url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == llm.id

def test_post_valid_llm(setup_llm):
    client = setup_llm["client"]
    base_url = setup_llm["base_url"]
    data = {
        "name": "Mistral-7B",
        "n_parameters": "7B"
    }
    response = client.post(base_url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "Mistral-7B"

def test_put_valid_llm(setup_llm):
    client = setup_llm["client"]
    detail_url = setup_llm["detail_url"]
    updated_data = {
        "name": "GPT-4 Turbo",
        "n_parameters": "1.5T"
    }
    response = client.put(detail_url, updated_data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "GPT-4 Turbo"

def test_delete_llm(setup_llm):
    client = setup_llm["client"]
    detail_url = setup_llm["detail_url"]
    response = client.delete(detail_url)
    assert response.status_code == status.HTTP_204_NO_CONTENT