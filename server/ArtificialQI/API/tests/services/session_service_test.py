import pytest
from unittest.mock import MagicMock
from API.services.session_service import SessionService
from API.tests.services.abstract_service_test import AbstractServiceTestCase


class TestSessionService(AbstractServiceTestCase):
    service_class = SessionService

    @pytest.fixture(autouse=True)
    def setup(self, mocker):
        self.mock_repository = mocker.MagicMock()
        self.mock_llm_repository = mocker.MagicMock()
        self.service_class.repository = self.mock_repository

        patcher = mocker.patch("API.services.session_service.LLMRepository", self.mock_llm_repository)
        self._patcher = patcher
    
    #Chiama il repository e restituisca i LLM 
    def test_get_llm(self):
        self.mock_repository.get_llm.return_value = [{"id": 1, "name": "llama2"}]

        result = self.service_class.get_llm(42)

        assert result == [{"id": 1, "name": "llama2"}]
        self.mock_repository.get_llm.assert_called_once_with(session_id=42)

    #Verifica che ad una sessione venga aggiunto un LLM   
    def test_add_llm(self):
        fake_session = MagicMock()
        fake_llm = MagicMock()
        self.mock_repository.get_by_id.return_value = fake_session
        self.mock_llm_repository.get_by_id.return_value = fake_llm
        self.mock_repository.add_llm.return_value = "LLM added"

        result = self.service_class.add_llm(1, 10)

        assert result == "LLM added"
        self.mock_repository.get_by_id.assert_called_once_with(1)
        self.mock_llm_repository.get_by_id.assert_called_once_with(10)
        self.mock_repository.add_llm.assert_called_once_with(fake_session, fake_llm)
    
    #Verifica la rimozione di LLM da una sessione
    def test_delete_llm(self):
        fake_session = MagicMock()
        fake_llm = MagicMock()
        self.mock_repository.get_by_id.return_value = fake_session
        self.mock_llm_repository.get_by_id.return_value = fake_llm
        self.mock_repository.delete_llm.return_value = None
        
        result = self.service_class.delete_llm(2, 5)

        assert result is None
        self.mock_repository.get_by_id.assert_called_once_with(2)
        self.mock_llm_repository.get_by_id.assert_called_once_with(5)
        self.mock_repository.delete_llm.assert_called_once_with(fake_session, fake_llm)