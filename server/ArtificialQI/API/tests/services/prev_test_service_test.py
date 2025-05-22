from unittest.mock import patch
from API.services.prev_test_service import PrevTestService
from API.tests.services.abstract_service_test import AbstractServiceTestCase


class TestPrevTestService(AbstractServiceTestCase):
    service_class = PrevTestService

    @patch("API.services.prev_test.PrevTestRepository.get_tests_by_session")
    def test_get_tests_by_session(self, mock_get_tests_by_session):
        """Test get_tests_by_session restituisce i test associati alla sessione"""

        # Arrange
        mock_get_tests_by_session.return_value = ["test1", "test2"]

        # Act
        result = self.service_class.get_tests_by_session(session_id=123)

        # Assert
        mock_get_tests_by_session.assert_called_once_with(session_id=123)
        self.assertEqual(result, ["test1", "test2"])
