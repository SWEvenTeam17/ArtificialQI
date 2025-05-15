import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ArtificialQI.settings")
django.setup()

from API.models import Answer, Prompt, LLM, Session
from API.repositories.session_repository import SessionRepository
from API.tests.repositories.abstract_repository_test import TestAbstractRepository
import pytest

class TestAnswerRepository(TestAbstractRepository):

    @pytest.fixture
    def setup_data(self, db):
        _llm  = LLM.objects.create(name="llama3.2", n_parameters="3B")
        _llm2 = LLM.objects.create(name="gemma3", n_parameters="4B")
        return {"llm1": _llm, "llm2": _llm2}

    @pytest.fixture
    def repository(self):
        return SessionRepository

    @pytest.fixture
    def valid_data(self, setup_data):
        return {
            "title": "Sessione 1",
            "description": "Descrizione",
        }
    
    def test_add_llm(self, repository, valid_data, setup_data):
        # creazione session
        session = repository.create(valid_data)
        # verifica che il campo llm di session sia vuoto
        assert repository.get_by_id(session.id).llm.count() == 0
        # test: aggiunta llm
        repository.add_llm(session, setup_data["llm1"])
        # verifica che llm sia presente in session
        assert setup_data["llm1"] in repository.get_by_id(session.id).llm.all()
    
    def test_get_llm(self, repository, valid_data, setup_data):
        # creazione session e aggiunta llm
        session = repository.create(valid_data)
        repository.add_llm(session, setup_data["llm2"])
        # test
        results = repository.get_llm(session.id)
        # verifica che llm usato non sia nella lista e che quello non usato sia in list
        assert session.llm not in results
        assert setup_data["llm1"] in results
    
    def test_delete_llm(self, repository, valid_data, setup_data):
        # creazione session e aggiunta llm
        session = repository.create(valid_data)
        repository.add_llm(session, setup_data["llm1"])
        #test
        repository.delete_llm(session, setup_data["llm1"])
        # verifica che llm non sia più collegato
        assert repository.get_by_id(session.id).llm.count() == 0