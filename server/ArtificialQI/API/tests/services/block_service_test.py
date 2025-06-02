from unittest.mock import patch, MagicMock, call
import pytest
from API.models import Block, LLM
from API.services.block_service import BlockService
from API.tests.services.abstract_service_test import AbstractServiceTestCase


class TestBlockService(AbstractServiceTestCase):
    service_class = BlockService

    @patch("API.services.block_service.PromptRepository")
    @patch("API.services.block_service.BlockRepository")
    def test_create(self, mock_block_repo, mock_prompt_repo):
        mock_block_repo.get_by_name.return_value = None
        mock_block = MagicMock(spec=Block)
        mock_block_repo.create.return_value = mock_block

        mock_prompt = MagicMock()
        mock_prompt_repo.get_or_create.return_value = mock_prompt

        sample_data = {
            "name": "test_block",
            "questions": [{"question": "q1", "answer": "a1"}],
        }

        result = BlockService.create(sample_data)

        assert result == mock_block
        mock_block_repo.get_by_name.assert_called_once_with("test_block")
        mock_block_repo.create.assert_called_once_with({"name": "test_block"})
        mock_prompt_repo.get_or_create.assert_called_once_with(
            prompt_text="q1", expected_answer="a1"
        )
        mock_block_repo.add_prompt.assert_called_once_with(
            block=mock_block, prompt=mock_prompt
        )

    @patch("API.services.block_service.PromptRepository")
    @patch("API.services.block_service.BlockRepository")
    def test_create_no_duplicate(self, mock_block_repo, mock_prompt_repo):
        mock_block_repo.get_by_name.return_value = None
        mock_new_block = MagicMock(spec=Block)
        mock_block_repo.create.return_value = mock_new_block

        mock_prompt_instance = MagicMock()
        mock_prompt_repo.get_or_create.return_value = mock_prompt_instance

        test_data = {
            "name": "test_block",
            "questions": [
                {"question": "q1", "answer": "a1"},
                {"question": "q2", "answer": "a2"},
            ],
        }

        result = BlockService.create(test_data)

        assert result == mock_new_block
        mock_block_repo.get_by_name.assert_called_once_with("test_block")
        mock_block_repo.create.assert_called_once_with({"name": "test_block"})
        assert mock_prompt_repo.get_or_create.call_count == 2
        assert mock_block_repo.add_prompt.call_count == 2

    @patch("API.services.block_service.BlockRepository")
    def test_create_duplicate(self, mock_block_repo):
        mock_existing_block = MagicMock(spec=Block)
        mock_block_repo.get_by_name.return_value = mock_existing_block

        test_data = {"name": "existing_block", "questions": []}

        result = BlockService.create(test_data)

        assert result is False
        mock_block_repo.get_by_name.assert_called_once_with("existing_block")
        mock_block_repo.create.assert_not_called()

    @patch("API.services.block_service.BlockRepository")
    def test_is_duplicated_true(self, mock_block_repo):
        mock_block_repo.get_by_name.return_value = MagicMock(spec=Block)

        result = BlockService.is_duplicated("existing_name")

        assert result is True
        mock_block_repo.get_by_name.assert_called_once_with(name="existing_name")

    @patch("API.services.block_service.BlockRepository")
    def test_is_duplicated_false(self, mock_block_repo):
        mock_block_repo.get_by_name.return_value = None

        result = BlockService.is_duplicated("non_existing_name")

        assert result is False
        mock_block_repo.get_by_name.assert_called_once_with(name="non_existing_name")

    @patch("API.services.block_service.BlockRepository")
    def test_retrieve_blocks(self, mock_block_repo):
        mock_block1 = MagicMock(spec=Block)
        mock_block2 = MagicMock(spec=Block)

        with patch("API.services.block_service.BlockService.read") as mock_read:
            mock_read.side_effect = [mock_block1, mock_block2]

            result = BlockService.retrieve_blocks([{"id": 1}, {"id": 2}])

            assert len(result) == 2
            assert result[0] is mock_block1
            assert result[1] is mock_block2

            mock_read.assert_any_call(1)
            mock_read.assert_any_call(2)

    @patch("API.services.block_service.BlockRepository")
    def test_get_common_blocks(self, mock_block_repo):
        mock_llm1 = MagicMock(spec=LLM)
        mock_llm2 = MagicMock(spec=LLM)

        mock_block1 = MagicMock(spec=Block)
        mock_block1.id = 1
        mock_block2 = MagicMock(spec=Block)
        mock_block2.id = 2
        mock_block3 = MagicMock(spec=Block)
        mock_block3.id = 3

        mock_block_repo.filter_by_llm.return_value = [mock_block1, mock_block2]
        mock_block_repo.filter_by_llm.side_effect = [
            [mock_block1, mock_block2],
            [mock_block2, mock_block3],
        ]

        mock_block_repo.filter_by_ids.return_value = [mock_block2]

        result = BlockService.get_common_blocks(mock_llm1, mock_llm2)

        assert len(result) == 1
        assert mock_block2 in result
        mock_block_repo.filter_by_ids.assert_called_once_with({2})
        assert mock_block_repo.filter_by_llm.call_count == 2
