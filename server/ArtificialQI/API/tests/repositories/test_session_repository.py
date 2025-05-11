from API.models import Answer, Prompt, LLM, Session
from API.repositories.session_repository import SessionRepository
from API.tests.repositories.abstract_repository import AbstractRepository
from django.test import TestCase

class AnswerRepositoryTest(AbstractRepository, TestCase):

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
        self.assertEqual(self.repository.get_by_id(session.id).llm.count(), 0)
        # test: aggiunta llm
        self.repository.add_llm(session, self.llm)
        # verifica che llm sia presente in session
        self.assertIn(self.llm, self.repository.get_by_id(session.id).llm.all())
    
    def test_get_llm(self):
        # creazione session e aggiunta llm
        session = self.repository.create(self.valid_data)
        self.repository.add_llm(session, self.llm)
        # test
        results = self.repository.get_llm(session.id)
        # verifica che llm usato non sia nella lista e che quello non usato sia in list
        self.assertNotIn(session.llm, results)
        self.assertIn(self.llm2, results)
    
    def test_delete_llm(self):
        # creazione session e aggiunta llm
        session = self.repository.create(self.valid_data)
        self.repository.add_llm(session, self.llm)
        #test
        self.repository.delete_llm(session, self.llm)
        # verifica che llm non sia più collegato
        self.assertEqual(self.repository.get_by_id(session.id).llm.count(), 0)