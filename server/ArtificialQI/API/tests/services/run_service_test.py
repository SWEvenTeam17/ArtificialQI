import unittest
from unittest.mock import patch, MagicMock
from API.services.run_service import RunService
from API.tests.services.abstract_service_test import AbstractServiceTestCase
from API.models import Prompt


class TestRunService(AbstractServiceTestCase):
    service_class = RunService

    @patch("API.services.run_service.RunService._repository.get_by_prompt")
    @patch("API.services.run_service.PromptRepository.get_by_id")
    def test_get_formatted_by_prompt(self, mock_prompt_get, mock_get_by_prompt):
        prompt = MagicMock(spec=Prompt)
        prompt.id = 1
        prompt.prompt_text = "Qual è la capitale della Francia?"
        prompt.expected_answer = "Parigi"

        block = MagicMock()
        block.id = 10
        block.name = "Geography"

        prompt.block_set.all.return_value = [block]
        mock_prompt_get.return_value = prompt

        run = MagicMock()
        run.id = 123
        run.llm.name = "GPT-Test"
        run.prompt = prompt
        run.llm_answer = "Parigi"
        run.evaluation.semantic_evaluation = 0.95
        run.evaluation.external_evaluation = 0.90

        mock_get_by_prompt.return_value = [run]

        result = self.service_class.get_formatted_by_prompt(prompt_id=1)

        mock_prompt_get.assert_called_once_with(instance_id=1)
        mock_get_by_prompt.assert_called_once_with(prompt_id=1)

        assert isinstance(result, dict)
        assert len(result["results"]) == 1

        res = result["results"][0]
        assert res["block_id"] == 10
        assert res["block_name"] == "Geography"
        assert len(res["results"]) == 1

        run_result = res["results"][0]
        assert run_result["run_id"] == 123
        assert run_result["llm_name"] == "GPT-Test"
        assert run_result["question"] == "Qual è la capitale della Francia?"
        assert run_result["expected_answer"] == "Parigi"
        assert run_result["answer"] == "Parigi"
        assert run_result["semantic_evaluation"] == 0.95
        assert run_result["external_evaluation"] == 0.90

        assert res["averages_by_llm"]["GPT-Test"]["avg_semantic_scores"] == 0.95
        assert res["averages_by_llm"]["GPT-Test"]["avg_external_scores"] == 0.90

    @patch("API.services.run_service.PromptRepository.get_by_id", side_effect=Prompt.DoesNotExist)
    def test_get_formatted_by_prompt_prompt_not_found(self, mock_prompt_get):
        result = self.service_class.get_formatted_by_prompt(prompt_id=999)

        mock_prompt_get.assert_called_once_with(instance_id=999)
        assert result is None
