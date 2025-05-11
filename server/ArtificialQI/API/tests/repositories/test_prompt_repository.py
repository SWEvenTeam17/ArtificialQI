from API.models import Answer, Prompt, LLM, Session
from API.repositories.prompt_repository import PromptRepository
from API.tests.repositories.abstract_repository import AbstractRepository
from django.test import TestCase

class AnswerRepositoryTest(AbstractRepository, TestCase):

    def setUp(self):
        self.llm = LLM.objects.create(name="llama3.2", n_parameters="3B")
        self.session = Session.objects.create(title="Sessione 1", description="test 1")
        self.session.llm.add(self.llm)

    @property
    def repository(self):
        return PromptRepository

    @property
    def valid_data(self):
        return {
            "prompt_text":"Domanda 1?",
            "expected_answer": "Risposta 1",
            "session": self.session
        }