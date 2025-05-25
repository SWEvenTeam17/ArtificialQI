import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ArtificialQI.settings")
django.setup()

from API.models import Prompt, LLM, Session, Run, Evaluation, Block, Test
from API.repositories.prev_test_repository import PrevTestRepository
from API.repositories.block_repository import BlockRepository
from API.tests.repositories.abstract_repository_test import TestAbstractRepository
import pytest

@pytest.mark.django_db
class TestPrevTestRepository(TestAbstractRepository):
    
    @pytest.fixture
    def setup_data(self, db):
        _llm = LLM.objects.create(name="llama3.2", n_parameters="3B")
        _llm2 = LLM.objects.create(name="gemma4", n_parameters="4B")
        _llm3 = LLM.objects.create(name="llama3.1", n_parameters="1B")
        _session = Session.objects.create(title="Sessione 1", description="test 1")
        _session.llm.add(_llm)
        _session2 = Session.objects.create(title="Sessione 2", description="test 2")
        _session2.llm.add(_llm)
        _prompt = Prompt.objects.create(
            prompt_text="Domanda 1?",
            expected_answer="Risposta 1",
        )
        _evaluation = Evaluation.objects.create(
            semantic_evaluation = 98,
            external_evaluation = 98
        )
        _block = Block.objects.create(name="blocco1")
        BlockRepository.add_prompt(_block, _prompt)

        _run = Run.objects.create(llm = _llm, prompt = _prompt, evaluation = _evaluation, llm_answer = "Risposta run 1")
        _run2 = Run.objects.create(llm = _llm, prompt = _prompt, evaluation = _evaluation, llm_answer = "Risposta run 2")

        return {"llm": _llm, "llm2": _llm2, "llm3": _llm3, "session": _session, "session2": _session2, "prompt": _prompt, "evaluation": _evaluation, "block": _block, "run": _run, "run2": _run2}
    
    @pytest.fixture
    def repository(self):
        return PrevTestRepository()
    
    @pytest.fixture
    def valid_data(self, setup_data):
        return {
            "session": setup_data["session"],
            "block": setup_data["block"],
        }


    def test_get_tests_by_session(self, repository, valid_data, setup_data):
        ptest = repository.create(valid_data)
        assert repository is not PrevTestRepository
        repository.add_run(ptest, setup_data["run"])
        results = repository.get_tests_by_session(setup_data["session"])
        assert ptest in results
        assert len(results) == 100
        assert len(results) == 10
        assert results is None
        assert results is not None
        assert results is Test
        assert results is not Test