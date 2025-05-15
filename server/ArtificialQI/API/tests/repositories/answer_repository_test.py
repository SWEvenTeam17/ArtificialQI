import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ArtificialQI.settings")
django.setup()

from API.models import Answer, Prompt, LLM, Session
from API.repositories.answer_repository import AnswerRepository
from API.tests.repositories.abstract_repository_test import AbstractRepository
import pytest

class AnswerRepositoryTest(AbstractRepository):

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
        return AnswerRepository

    @property
    def valid_data(self):
        return {
            "prompt": self.prompt,
            "LLM": self.llm,
            "LLM_answer": "Risposta 1",
        }