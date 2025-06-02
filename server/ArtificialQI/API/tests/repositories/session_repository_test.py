import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ArtificialQI.settings")
django.setup()

from API.models import LLM, Session, Prompt, Evaluation, Block, Run
from API.repositories.session_repository import SessionRepository
from API.repositories.block_repository import BlockRepository
from API.repositories.block_test_repository import BlockTestRepository
from API.tests.repositories.abstract_repository_test import TestAbstractRepository
import pytest


class TestAnswerRepository(TestAbstractRepository):

    @pytest.fixture
    def setup_data(self, db):
        _llm = LLM.objects.create(name="llama3.2", n_parameters="3B")
        _llm2 = LLM.objects.create(name="gemma3", n_parameters="4B")
        return {"llm1": _llm, "llm2": _llm2}
    
    @pytest.fixture
    def setup_data_prev(self, db):
        _llm = LLM.objects.create(name="llama3.3", n_parameters="3B")
        _llm2 = LLM.objects.create(name="gemma4", n_parameters="4B")
        _llm3 = LLM.objects.create(name="llama3.1", n_parameters="1B")
        _session = Session.objects.create(title="Sessione 1", description="test 1")
        _session.llm.add(_llm)
        _session2 = Session.objects.create(title="Sessione 2", description="test 2")
        _session2.llm.add(_llm)
        _prompt = Prompt.objects.create(
            prompt_text="Domanda 1?",
            expected_answer="Risposta 1",
        )
        _evaluation = Evaluation.objects.create(
            semantic_evaluation=98, external_evaluation=98
        )
        _block = Block.objects.create(name="blocco1")
        BlockRepository.add_prompt(_block, _prompt)

        _block2 = Block.objects.create(name="blocco2")
        BlockRepository.add_prompt(_block2, _prompt)

        _run = Run.objects.create(
            llm=_llm,
            prompt=_prompt,
            evaluation=_evaluation,
            llm_answer="Risposta run 1",
        )
        _run2 = Run.objects.create(
            llm=_llm,
            prompt=_prompt,
            evaluation=_evaluation,
            llm_answer="Risposta run 2",
        )

        return {
            "llm": _llm,
            "llm2": _llm2,
            "llm3": _llm3,
            "session": _session,
            "session2": _session2,
            "prompt": _prompt,
            "evaluation": _evaluation,
            "block": _block,
            "block2": _block2,
            "run": _run,
            "run2": _run2,
        }

    @pytest.fixture
    def repository(self):
        return SessionRepository

    @pytest.fixture
    def valid_data(self, setup_data):
        return {
            "title": "Sessione 1",
            "description": "Descrizione",
        }
    
    @pytest.fixture
    def valid_data_prev(self, setup_data_prev):
        return {
            "session": setup_data_prev["session"],
            "block": setup_data_prev["block"],
        }

    @pytest.fixture
    def update_data(self, setup_data):
        return {
            "title": "Sessione 2",
            "description": "Descrizione 2",
        }
    
    @pytest.fixture
    def update_data_prev(self, setup_data_prev):
        return {
            "session": setup_data_prev["session2"],
            "block": setup_data_prev["block2"],
        }

    def test_get_remaining_llm(self, repository, valid_data, setup_data):
        # creazione session e aggiunta llm
        session = repository.create(valid_data)
        repository.add_llm(session, setup_data["llm2"])
        # test
        results = repository.get_remaining_llm(session.id)
        # verifica che llm usato non sia nella lista e che quello non usato sia in list
        assert setup_data["llm2"] not in results
        assert setup_data["llm1"] in results

    def test_get_llms(self, repository, valid_data, setup_data):
        # creazione session e aggiunta llm
        session = repository.create(valid_data)
        repository.add_llm(session, setup_data["llm2"])
        # test
        results = repository.get_llms(session)
        # verifica che llm usato non sia nella lista e che quello non usato sia in list
        assert setup_data["llm1"] not in results
        assert setup_data["llm2"] in results

    def test_add_llm(self, repository, valid_data, setup_data):
        # creazione session
        session = repository.create(valid_data)
        # verifica che il campo llm di session sia vuoto
        assert repository.get_by_id(session.id).llm.count() == 0
        # test: aggiunta llm
        repository.add_llm(session, setup_data["llm1"])
        # verifica che llm sia presente in session
        assert setup_data["llm1"] in repository.get_by_id(session.id).llm.all()

    def test_delete_llm(self, repository, valid_data, setup_data):
        # creazione session e aggiunta llm
        session = repository.create(valid_data)
        repository.add_llm(session, setup_data["llm1"])
        # test
        repository.delete_llm(session, setup_data["llm1"])
        # verifica che llm non sia più collegato
        assert repository.get_by_id(session.id).llm.count() == 0

    def test_get_tests_by_session(self, repository, valid_data, setup_data_prev):
        ptest = repository.create(valid_data)
        ptest2 = repository.create(
            {
                "session": setup_data_prev["session2"],
                "block": setup_data_prev["block"],
            }
        )
        assert repository is not SessionRepository
        BlockTestRepository.add_run(ptest, setup_data_prev["run"])
        results = repository.get_tests_by_session(setup_data_prev["session"])
        assert ptest in results
        assert ptest2 not in results
        assert len(results) == 1
