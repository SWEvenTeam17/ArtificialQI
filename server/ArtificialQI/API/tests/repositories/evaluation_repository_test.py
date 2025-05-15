import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ArtificialQI.settings")
django.setup()

from API.models import Answer, Prompt, LLM, Session, Evaluation
from API.repositories.evaluation_repository import EvaluationRepository
from API.tests.repositories.abstract_repository_test import TestAbstractRepository
import pytest

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
            session=_session
        )
        return {"llm": _llm, "session": _session, "prompt": _prompt}

    @pytest.fixture
    def repository(self):
        return EvaluationRepository()

    @pytest.fixture
    def valid_data(self, setup_data):
        return {
            "prompt": setup_data["prompt"],
            "semantic_evaluation": 98,
            "external_evaluation": 98,
        }