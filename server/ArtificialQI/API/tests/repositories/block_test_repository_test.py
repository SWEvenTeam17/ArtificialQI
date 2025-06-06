import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ArtificialQI.settings")
django.setup()

import pytest

from API.models import LLM, Block, Evaluation, Prompt, Run, Session
from API.repositories.block_repository import BlockRepository
from API.repositories.block_test_repository import BlockTestRepository
from API.tests.repositories.abstract_repository_test import TestAbstractRepository


@pytest.mark.django_db
class TestBlockTestRepository(TestAbstractRepository):

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
            semantic_evaluation=98, external_evaluation=98
        )
        _block = Block.objects.create(name="blocco1")
        BlockRepository.add_prompt(_block, _prompt)
        _block2 = Block.objects.create(name="blocco2")
        BlockRepository.add_prompt(_block2, _prompt)

        _run = Run.objects.create(
            llm=_llm,
            prompt=_prompt,
            evaluation=_evaluation,
            llm_answer="Risposta run 1",
        )
        _run2 = Run.objects.create(
            llm=_llm,
            prompt=_prompt,
            evaluation=_evaluation,
            llm_answer="Risposta run 2",
        )

        return {
            "llm": _llm,
            "llm2": _llm2,
            "llm3": _llm3,
            "session": _session,
            "session2": _session2,
            "prompt": _prompt,
            "evaluation": _evaluation,
            "block": _block,
            "block2": _block2,
            "run": _run,
            "run2": _run2,
        }

    @pytest.fixture
    def repository(self):
        return BlockTestRepository()

    @pytest.fixture
    def valid_data(self, setup_data):
        return {
            "session": setup_data["session"],
            "block": setup_data["block"],
        }

    @pytest.fixture
    def update_data(self, setup_data):
        return {
            "session": setup_data["session2"],
            "block": setup_data["block2"],
        }

    def test_add_run(self, repository, valid_data, setup_data):
        test = repository.create(valid_data)
        result = repository.add_run(test, setup_data["run"])
        assert setup_data["run"] in result.run.all()
        result = repository.add_run(test, setup_data["run2"])
        assert setup_data["run"] in result.run.all()
        assert setup_data["run2"] in result.run.all()

    def test_remove_run(self, repository, valid_data, setup_data):
        test = repository.create(valid_data)
        repository.add_run(test, setup_data["run"])
        repository.add_run(test, setup_data["run2"])
        result = repository.remove_run(test, setup_data["run"])
        assert setup_data["run"] not in result.run.all()
        assert setup_data["run2"] in result.run.all()
        result = repository.remove_run(test, setup_data["run2"])
        assert setup_data["run2"] not in result.run.all()
