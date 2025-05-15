import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ArtificialQI.settings")
django.setup()

from API.models import Answer, Prompt, LLM, Session
from API.repositories.llm_repository import LLMRepository
from API.tests.repositories.abstract_repository_test import TestAbstractRepository
import pytest

class TestLLMRepository(TestAbstractRepository):

    @pytest.fixture
    def repository(self):
        return LLMRepository

    @pytest.fixture
    def valid_data(self):
        return {
            "name": "llama3.2",
            "n_parameters": "3B"
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
        assert repository.get_by_id(1).n_parameters, "6B"