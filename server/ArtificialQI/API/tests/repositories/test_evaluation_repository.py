import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ArtificialQI.settings")
django.setup()

from API.models import Answer, Prompt, LLM, Session, Evaluation
from API.repositories.evaluation_repository import EvaluationRepository
from API.tests.repositories.abstract_repository_test import AbstractRepository
import pytest

class EvaluationRepositoryTest(AbstractRepository):

    def setUp(self):
        self.llm = LLM.objects.create(name="llama3.2", n_parameters="3B")
        self.session = Session.objects.create(title="Sessione 1", description="test 1")
        self.session.llm.add(self.llm)
        self.prompt = Prompt.objects.create(
            prompt_text="Domanda 1?",
            expected_answer="Risposta 1",
            session=self.session
        )

    @property
    def repository(self):
        return EvaluationRepository

    @property
    def valid_data(self):
        return {
            "prompt": self.prompt,
            "semantic_evaluation": 98,
            "external_evaluation": 98,
        }