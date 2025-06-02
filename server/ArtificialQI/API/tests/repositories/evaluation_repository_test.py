import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ArtificialQI.settings")
django.setup()

import pytest

from API.models import LLM, Evaluation, Prompt, Session
from API.repositories.evaluation_repository import EvaluationRepository
from API.tests.repositories.abstract_repository_test import TestAbstractRepository


@pytest.mark.django_db
class TestEvaluationRepository(TestAbstractRepository):

    @pytest.fixture
    def setup_data(self, db):
        _llm = LLM.objects.create(name="llama3.2", n_parameters="3B")
        _session = Session.objects.create(title="Sessione 1", description="test 1")
        _session.llm.add(_llm)
        _prompt = Prompt.objects.create(
            prompt_text="Domanda 1?",
            expected_answer="Risposta 1",
        )
        return {"llm": _llm, "prompt": _prompt}

    @pytest.fixture
    def repository(self):
        return EvaluationRepository()

    @pytest.fixture
    def valid_data(self, setup_data):
        return {
            "semantic_evaluation": 98,
            "external_evaluation": 98,
        }

    @pytest.fixture
    def update_data(self, setup_data):
        return {
            "semantic_evaluation": 90,
            "external_evaluation": 91,
        }
