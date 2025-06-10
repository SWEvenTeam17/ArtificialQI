import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ArtificialQI.settings")
django.setup()

from typing import override

import pytest
from API.models import LLM, Block, Evaluation, Prompt, Run, Session
from API.repositories.block_repository import BlockRepository
from API.tests.repositories.abstract_repository_test import \
    TestAbstractRepository


@pytest.mark.django_db
class TestAnswerRepository(TestAbstractRepository):

    @pytest.fixture
    def setup_data(self, db):
        _llm = LLM.objects.create(name="llama3.2", n_parameters="3B")
        _llm2 = LLM.objects.create(name="gemma", n_parameters="4B")
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
            semantic_evaluation=90, external_evaluation=95
        )
        _evaluation = Evaluation.objects.create(
            semantic_evaluation=98, external_evaluation=99
        )
        _run = Run.objects.create(
            llm=_llm,
            prompt=_prompt,
            evaluation=_evaluation,
            llm_answer="Risposta run 1",
        )
        _run2 = Run.objects.create(
            llm=_llm2,
            prompt=_prompt2,
            evaluation=_evaluation,
            llm_answer="Risposta run 2",
        )
        _run3 = Run.objects.create(
            llm=_llm2,
            prompt=_prompt,
            evaluation=_evaluation,
            llm_answer="Risposta run 3",
        )
        return {
            "llm": _llm,
            "llm2": _llm2,
            "session": _session,
            "prompt": _prompt,
            "prompt2": _prompt2,
            _run: "run",
            _run2: "run2",
            _run3: "run3",
        }

    @pytest.fixture
    def repository(self):
        return BlockRepository

    @pytest.fixture
    def valid_data(self, setup_data):
        return {"name": "nome"}

    @pytest.fixture
    def update_data(self, setup_data):
        return {"name": "nome_update"}

    def test_add_prompt(self, repository, valid_data, setup_data):
        block = repository.create(valid_data)
        repository.add_prompt(block, setup_data["prompt"])
        assert setup_data["prompt"] in repository.get_by_id(block.id).prompt.all()

    def test_remove_prompt(self, repository, valid_data, setup_data):
        block = repository.create(valid_data)
        repository.add_prompt(block, setup_data["prompt"])
        assert setup_data["prompt"] in repository.get_by_id(block.id).prompt.all()
        repository.remove_prompt(block, setup_data["prompt"])
        assert setup_data["prompt"] not in repository.get_by_id(block.id).prompt.all()

    def test_get_by_name(self, repository, valid_data, setup_data):
        block = repository.create(valid_data)
        found = repository.get_by_name("nome")
        assert found is not None
        assert found.id == block.id
        assert found.name == "nome"
        found2 = repository.get_by_name("nome2")
        assert found2 is None

    def test_get_prompts(self, repository, valid_data, setup_data):
        block = repository.create(valid_data)
        repository.add_prompt(block, setup_data["prompt"])
        repository.add_prompt(block, setup_data["prompt2"])
        results = repository.get_prompts(block)
        assert setup_data["prompt"] in results
        assert setup_data["prompt2"] in results
        assert len(results) == 2

    def test_filter_by_llm(self, repository, valid_data, setup_data):
        block1 = repository.create(valid_data)
        block2 = repository.create({"name": "nome2"})
        repository.add_prompt(block1, setup_data["prompt"])
        repository.add_prompt(block2, setup_data["prompt2"])
        results = repository.filter_by_llm(setup_data["llm"])
        assert block1 in results
        assert block2 not in results

    def test_filter_by_ids(self, repository, valid_data, setup_data):
        block1 = repository.create(valid_data)
        block2 = repository.create({"name": "nome2"})
        repository.add_prompt(block1, setup_data["prompt"])
        repository.add_prompt(block2, setup_data["prompt2"])
        results = repository.filter_by_ids([1])
        assert block1 in results
        assert block2 not in results

    def test_get_common_blocks_for_llms(self, repository, valid_data, setup_data):
        block1 = repository.create(valid_data)
        block2 = repository.create({"name": "nome2"})
        repository.add_prompt(block1, setup_data["prompt"])
        repository.add_prompt(block2, setup_data["prompt2"])
        results = repository.get_common_blocks_for_llms(
            setup_data["llm"], setup_data["llm2"]
        )
        assert len(results) == 1
