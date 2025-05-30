import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ArtificialQI.settings")
django.setup()

from API.models import LLM, Prompt, Session, Evaluation, Block, Run, BlockTest
from API.repositories.llm_repository import LLMRepository
from API.repositories.block_repository import BlockRepository
from API.repositories.block_test_repository import BlockTestRepository
from API.tests.repositories.abstract_repository_test import TestAbstractRepository
import pytest

class TestLLMRepository(TestAbstractRepository):
    
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
        _evaluation = Evaluation.objects.create(
            semantic_evaluation = 98,
            external_evaluation = 98
        )
        _block = Block.objects.create(name="blocco1")
        BlockRepository.add_prompt(_block, _prompt)

        _run = Run.objects.create(llm = _llm, prompt = _prompt, evaluation = _evaluation, llm_answer = "Risposta run 1")
        _run2 = Run.objects.create(llm = _llm, prompt = _prompt, evaluation = _evaluation, llm_answer = "Risposta run 2")

        _test = BlockTest.objects.create(session = _session, block = _block)
        BlockTestRepository.add_run(_test, _run)

        return {"llm": _llm, "llm2": _llm2, "llm3": _llm3, "session": _session, "prompt": _prompt, "evaluation": _evaluation, "block": _block, "run": _run, "run2": _run2}
    
    @pytest.fixture
    def repository(self):
        return LLMRepository
    
    @pytest.fixture
    def valid_data(self):
        return {
            "name": "llama3.2",
            "n_parameters": "3B"
        }
    
    @pytest.fixture
    def update_data(self):
        return {
            "name": "gemma4",
            "n_parameters": "4B"
        }

    def test_update_or_create(self, repository, valid_data):
        # test: aggiungere modello non esistente
        repository.update_or_create("mod1", "3B")
        results = repository.get_all()
        assert len(results) == 1
        assert repository.get_by_id(1).name == "mod1"
        assert repository.get_by_id(1).n_parameters == "3B"
        # test: aggiornare modello
        repository.update_or_create("mod1", "6B")
        assert repository.get_by_id(1).name == "mod1"
        assert repository.get_by_id(1).n_parameters == "6B"
        # test: aggiornare modello con gli stessi dati
        repository.update_or_create("mod1", "6B")
        assert repository.get_by_id(1).name == "mod1"
        assert repository.get_by_id(1).n_parameters == "6B"