import unittest
from unittest.mock import patch
from API.services.prev_test_service import PrevTestService
from API.tests.services.abstract_service_test import AbstractServiceTestCase


class TestPrevTestService(AbstractServiceTestCase):
    service_class = PrevTestService

    @patch.object(PrevTestService, "repository")
    def test_get_tests_by_session(self, mock_repository):
        mock_repository.get_tests_by_session.return_value = ["test1", "test2"]

        result = PrevTestService.get_tests_by_session(session_id=123)

        mock_repository.get_tests_by_session.assert_called_once_with(session_id=123)
        assert result == ["test1", "test2"]
