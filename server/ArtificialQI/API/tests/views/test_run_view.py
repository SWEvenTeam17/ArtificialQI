import pytest
from rest_framework.test import APIClient
from unittest.mock import patch
from API.models import LLM, Prompt, Run, Evaluation

RUN_URL = "/runs/"
RUN_DETAIL_URL = lambda pk: f"/runs/{pk}/"

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def llm(db):
    return LLM.objects.create(name="GPT-4", n_parameters="1T")

@pytest.fixture
def prompt(db):
    return Prompt.objects.create(prompt_text="prompt test", expected_answer="risposta attesa")

@pytest.fixture
def evaluation(db):
    return Evaluation.objects.create(semantic_evaluation=4.5, external_evaluation=3.0)

@pytest.fixture
def run_obj(db, llm, prompt, evaluation):
    return Run.objects.create(llm=llm, prompt=prompt, evaluation=evaluation, llm_answer="Risposta generata")

@pytest.mark.django_db
class TestRunView:

    @patch("API.views_def.run_view.RunService")
    def test_get_all_runs(self, mock_service, api_client, run_obj, llm, prompt, evaluation):
        run_dict = {
            "id": run_obj.id,
            "llm": llm.id,
            "prompt": prompt.id,
            "evaluation": evaluation.id,
            "llm_answer": "Risposta generata"
        }
        mock_service.read_all.return_value = [run_dict]
        response = api_client.get(RUN_URL)
        assert response.status_code == 200
        assert isinstance(response.data, list)
        assert response.data[0]["llm"] == llm.id

    @patch("API.views_def.run_view.RunService")
    def test_get_run_by_id(self, mock_service, api_client, run_obj, llm, prompt, evaluation):
        run_dict = {
            "id": run_obj.id,
            "llm": llm.id,
            "prompt": prompt.id,
            "evaluation": evaluation.id,
            "llm_answer": "Risposta generata"
        }
        mock_service.read.return_value = run_dict
        response = api_client.get(RUN_DETAIL_URL(run_obj.id))
        assert response.status_code == 200
        assert response.data["llm"] == llm.id

    @patch("API.views_def.run_view.RunService")
    def test_post_run_valid(self, mock_service, api_client, llm, prompt, evaluation):
        run_dict = {
            "id": 1,
            "llm": llm.id,
            "prompt": prompt.id,
            "evaluation": evaluation.id,
            "llm_answer": "Risposta generata"
        }
        mock_service.create.return_value = run_dict
        data = {
            "llm": llm.id,
            "prompt": prompt.id,
            "evaluation": evaluation.id,
            "llm_answer": "Risposta generata"
        }
        response = api_client.post(RUN_URL, data=data, format="json")
        assert response.status_code == 201
        assert response.data["llm"] == llm.id

    @patch("API.views_def.run_view.RunService")
    def test_post_run_invalid(self, mock_service, api_client):
        invalid_data = {"llm": 1}
        response = api_client.post(RUN_URL, data=invalid_data, format="json")
        assert response.status_code == 400
        assert "prompt" in response.data or "evaluation" in response.data

    @patch("API.views_def.run_view.RunService")
    def test_put_run(self, mock_service, api_client, run_obj, llm, prompt, evaluation):
        run_dict = {
            "id": run_obj.id,
            "llm": llm.id,
            "prompt": prompt.id,
            "evaluation": evaluation.id,
            "llm_answer": "Risposta generata"
        }
        mock_service.update.return_value = run_dict
        data = {
            "llm": llm.id,
            "prompt": prompt.id,
            "evaluation": evaluation.id,
            "llm_answer": "Risposta generata"
        }
        response = api_client.put(RUN_DETAIL_URL(run_obj.id), data=data, format="json")
        assert response.status_code == 200
        assert response.data["llm"] == llm.id

    @patch("API.views_def.run_view.RunService")
    def test_delete_run(self, mock_service, api_client, run_obj):
        mock_service.delete.return_value = None
        response = api_client.delete(RUN_DETAIL_URL(run_obj.id))
        assert response.status_code == 204