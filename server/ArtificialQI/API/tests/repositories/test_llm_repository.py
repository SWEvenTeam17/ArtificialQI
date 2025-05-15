import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ArtificialQI.settings")
django.setup()

from API.models import Answer, Prompt, LLM, Session
from API.repositories.llm_repository import LLMRepository
from API.tests.repositories.abstract_repository_test import AbstractRepository
import pytest

class LLMRepositoryTest(AbstractRepository):

      #def setUp(self):
        #self.llm = LLM.objects.create(name="llama3.2", n_parameters="3B")

    @property
    def repository(self):
        return LLMRepository

    @property
    def valid_data(self):
        return {
            "name": "llama3.2",
            "n_parameters": "3B"
        }

    def test_update_or_create(self):
        # test: aggiungere modello non esistente
        self.repository.update_or_create("mod1", "3B")
        results = self.repository.get_all()
        self.assertEqual(len(results),1)
        self.assertEqual(self.repository.get_by_id(1).name, "mod1")
        self.assertEqual(self.repository.get_by_id(1).n_parameters, "3B")
        # test: aggiornare modello
        self.repository.update_or_create("mod1", "6B")
        self.assertEqual(self.repository.get_by_id(1).name, "mod1")
        self.assertEqual(self.repository.get_by_id(1).n_parameters, "6B")
        # test: aggiornare modello con gli stessi dati
        self.repository.update_or_create("mod1", "6B")
        self.assertEqual(self.repository.get_by_id(1).name, "mod1")
        self.assertEqual(self.repository.get_by_id(1).n_parameters, "6B")