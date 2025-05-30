import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ArtificialQI.settings")
django.setup()

from API.models import Prompt, LLM, Session, Run, Evaluation
from API.repositories.run_repository import RunRepository
from API.tests.repositories.abstract_repository_test import TestAbstractRepository
import pytest

@pytest.mark.django_db
class TestRunRepository(TestAbstractRepository):
    
    @pytest.fixture
    def setup_data(self, db):
        _llm = LLM.objects.create(name="llama3.2", n_parameters="3B")
        _llm2 = LLM.objects.create(name="gemma4", n_parameters="4B")
        _llm3 = LLM.objects.create(name="llama3.1", n_parameters="1B")
        _session = Session.objects.create(title="Sessione 1", description="test 1")
        _session.llm.add(_llm)
        _prompt = Prompt.objects.create(
            prompt_text="Domanda 1?",
            expected_answer="Risposta 1",
        )
        _prompt2 = Prompt.objects.create(
            prompt_text="Domanda 2?",
            expected_answer="Risposta 2",
        )
        _evaluation = Evaluation.objects.create(
            semantic_evaluation = 98,
            external_evaluation = 98
        )
        _evaluation2 = Evaluation.objects.create(
            semantic_evaluation = 95,
            external_evaluation = 95
        )
        return {"llm": _llm, "llm2": _llm2, "llm3": _llm3, "session": _session, "prompt": _prompt, "prompt2": _prompt2, "evaluation": _evaluation, "evaluation2": _evaluation2}
    
    @pytest.fixture
    def repository(self):
        return RunRepository()
    
    @pytest.fixture
    def valid_data(self, setup_data):
        return {
            "llm": setup_data["llm"],
            "prompt": setup_data["prompt"],
            "evaluation": setup_data["evaluation"],
            "llm_answer": "Risposta 1",
        }
    
    @pytest.fixture
    def update_data(self, setup_data):
        return {
            "llm": setup_data["llm2"],
            "prompt": setup_data["prompt2"],
            "evaluation": setup_data["evaluation2"],
            "llm_answer": "Risposta 2",
        }
    
    def test_commons_run(self, repository, valid_data, setup_data):
        run1 = repository.create(valid_data)
        run2 = repository.create({"llm": setup_data["llm2"],
            "prompt": setup_data["prompt"],
            "evaluation": setup_data["evaluation"],
            "llm_answer": "Risposta 2"})
        results = repository.get_common_runs(setup_data["llm"], setup_data["llm2"], [])
        assert len(repository.get_common_runs(setup_data["llm3"], setup_data["llm3"], [])) == 0
        assert len(repository.get_common_runs(setup_data["llm"], setup_data["llm2"], [])) == 2


    def test_get_by_prompt(self, repository, valid_data, setup_data):
        run1 = repository.create(valid_data)
        run2 = repository.create({"llm": setup_data["llm"],
            "prompt": setup_data["prompt"],
            "evaluation": setup_data["evaluation"],
            "llm_answer": "Risposta 2"})
        results = repository.get_by_prompt(1)
        assert len(results) == 2
        assert all(isinstance(r, Run) for r in results)
        assert results[0] == run1
        assert results[1] == run2
        assert isinstance(results[0].prompt, Prompt)
        assert results[0].prompt.id == setup_data["prompt"].id