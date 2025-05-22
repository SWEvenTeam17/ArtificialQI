import pytest
from unittest.mock import MagicMock
from API.services.prompt_service import PromptService
from API.tests.services.abstract_service_test import AbstractServiceTestCase


class TestPromptService(AbstractServiceTestCase):
    service_class = PromptService

    @pytest.fixture(autouse=True)
    def setup(self, mocker):
        self.mock_repository = mocker.MagicMock()
        self.service_class.repository = self.mock_repository

    def test_filter_by_session(self):
        fake_session = MagicMock()
        expected_prompts = [{"id": 1, "text": "prompt 1"}, {"id": 2, "text": "prompt 2"}]
        self.mock_repository.filter_by_session.return_value = expected_prompts

        result = self.service_class.filter_by_session(fake_session)

        assert result == expected_prompts
        self.mock_repository.filter_by_session.assert_called_once_with(fake_session)