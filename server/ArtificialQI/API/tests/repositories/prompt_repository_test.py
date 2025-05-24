# import django
# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ArtificialQI.settings")
# django.setup()

# from API.models import Prompt, LLM, Session
# from API.repositories.prompt_repository import PromptRepository
# from API.tests.repositories.abstract_repository_test import TestAbstractRepository
# import pytest

# @pytest.mark.django_db
# class TestAnswerRepository(TestAbstractRepository):

#     @pytest.fixture
#     def setup_data(self, db):
#         _llm = LLM.objects.create(name="llama3.2", n_parameters="3B")
#         _session = Session.objects.create(title="Sessione 1", description="test 1")
#         _session.llm.add(_llm)
#         return {"llm": _llm, "session": _session}

#     @pytest.fixture
#     def repository(self):
#         return PromptRepository

#     @pytest.fixture
#     def valid_data(self, setup_data):
#         return {
#             "prompt_text":"Domanda 1?",
#             "expected_answer": "Risposta 1",
#         }
    
#     def test_filter_by_session(self, repository, valid_data, setup_data):
