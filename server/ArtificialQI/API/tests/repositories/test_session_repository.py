import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ArtificialQI.settings")
django.setup()

from API.models import Answer, Prompt, LLM, Session
from API.repositories.session_repository import SessionRepository
from API.tests.repositories.abstract_repository_test import AbstractRepository
import pytest

class AnswerRepositoryTest(AbstractRepository):

    def setUp(self):
        self.llm  = LLM.objects.create(name="llama3.2", n_parameters="3B")
        self.llm2 = LLM.objects.create(name="gemma3", n_parameters="4B")

    @property
    def repository(self):
        return SessionRepository

    @property
    def valid_data(self):
        return {
            "title": "Sessione 1",
            "description": "Descrizione",
        }
    
    def test_add_llm(self):
        # creazione session
        session = self.repository.create(self.valid_data)
        # verifica che il campo llm di session sia vuoto
        assert self.repository.get_by_id(session.id).llm.count() != 0
        # test: aggiunta llm
        self.repository.add_llm(session, self.llm)
        # verifica che llm sia presente in session
        assert self.llm in self.repository.get_by_id(session.id).llm.all()
    
    def test_get_llm(self):
        # creazione session e aggiunta llm
        session = self.repository.create(self.valid_data)
        self.repository.add_llm(session, self.llm)
        # test
        results = self.repository.get_llm(session.id)
        # verifica che llm usato non sia nella lista e che quello non usato sia in list
        assert session.llm not in results
        assert self.llm2 in results
    
    def test_delete_llm(self):
        # creazione session e aggiunta llm
        session = self.repository.create(self.valid_data)
        self.repository.add_llm(session, self.llm)
        #test
        self.repository.delete_llm(session, self.llm)
        # verifica che llm non sia più collegato
        assert self.repository.get_by_id(session.id).llm.count() == 0