from unittest.mock import MagicMock, patch

from API.services.session_service import SessionService
from API.tests.services.abstract_service_test import AbstractServiceTestCase


class TestSessionService(AbstractServiceTestCase):
    service_class = SessionService

    @patch("API.services.session_service.SessionService._repository")
    def test_get_llm(self, mock_repo):
        """Test get_excluded_llm restituisce i LLM associati a una sessione"""
        mock_repo.get_remaining_llm.return_value = ["llm1", "llm2"]

        result = self.service_class.get_excluded_llm(session_id=1)

        mock_repo.get_remaining_llm.assert_called_once_with(session_id=1)
        assert result == ["llm1", "llm2"]

    @patch("API.services.session_service.LLMRepository.get_by_id")
    @patch("API.services.session_service.SessionService._repository")
    def test_add_llm(self, mock_repo, mock_get_llm):
        """Test add_llm aggiunge un LLM alla sessione"""
        mock_session = MagicMock()
        mock_llm = MagicMock()
        mock_repo.get_by_id.return_value = mock_session
        mock_get_llm.return_value = mock_llm
        mock_repo.add_llm.return_value = "success"

        result = self.service_class.add_llm(session_id=1, llm_id=42)

        mock_repo.get_by_id.assert_called_once_with(1)
        mock_get_llm.assert_called_once_with(42)
        mock_repo.add_llm.assert_called_once_with(mock_session, mock_llm)
        assert result == "success"

    @patch("API.services.session_service.LLMRepository.get_by_id")
    @patch("API.services.session_service.SessionService._repository")
    def test_delete_llm(self, mock_repo, mock_get_llm):
        """Test delete_llm rimuove un LLM dalla sessione"""
        mock_session = MagicMock()
        mock_llm = MagicMock()
        mock_repo.get_by_id.return_value = mock_session
        mock_get_llm.return_value = mock_llm
        mock_repo.delete_llm.return_value = None

        result = self.service_class.delete_llm(session_id=1, llm_id=42)

        mock_repo.get_by_id.assert_called_once_with(1)
        mock_get_llm.assert_called_once_with(42)
        mock_repo.delete_llm.assert_called_once_with(mock_session, mock_llm)
        assert result is None

    @patch("API.services.session_service.SessionService._repository")
    def test_get_tests_by_session(self, mock_repository):
        mock_repository.get_tests_by_session.return_value = ["test1", "test2"]

        result = self.service_class.get_tests_by_session(session_id=123)

        mock_repository.get_tests_by_session.assert_called_once_with(session_id=123)
        assert result == ["test1", "test2"]
