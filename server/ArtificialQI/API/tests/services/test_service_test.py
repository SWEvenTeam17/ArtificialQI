import unittest
from unittest.mock import patch, MagicMock
from API.services.test_service import TestService
from API.tests.services.abstract_service_test import AbstractServiceTestCase
from API.models import Block, Session


class TestTestService(AbstractServiceTestCase):

    service_class = TestService

    @patch("API.services.test_service.requests.post")
    @patch("API.services.test_service.os.getenv", return_value="http://fake-llm-service/")
    def test_interrogate(self, mock_getenv, mock_post):
        """Test interrogate chiama correttamente il microservizio"""
        mock_post.return_value.json.return_value = {"answer": "test response"}

        response = self.service_class.interrogate("GPT-4", "Che ore sono?")

        mock_getenv.assert_called_once_with("LLM_SERVICE_URL")
        mock_post.assert_called_once_with(
            "http://fake-llm-service/interrogate/",
            {"llm_name": "GPT-4", "prompt": "Che ore sono?"}
        )
        assert response == "test response"

    @patch("API.services.test_service.TestRepository.add_run")
    @patch("API.services.test_service.RunService.create")
    @patch("API.services.test_service.EvaluationService.create")
    @patch("API.services.test_service.LLMController.get_external_evaluation", return_value=0.9)
    @patch("API.services.test_service.LLMController.get_semantic_evaluation", return_value=0.8)
    @patch("API.services.test_service.TestService.interrogate", return_value="Risposta LLM")
    @patch("API.services.test_service.BlockRepository.get_prompts")
    @patch("API.services.test_service.SessionRepository.get_llms")
    @patch("API.services.test_service.TestService.create")
    def test_runtest(
        self,
        mock_test_create,
        mock_get_llms,
        mock_get_prompts,
        mock_interrogate,
        mock_semantic_eval,
        mock_external_eval,
        mock_eval_create,
        mock_run_create,
        mock_add_run,
    ):
        """Test runtest elabora correttamente le risposte e calcola medie"""
        session = MagicMock(spec=Session)
        block = MagicMock(spec=Block)
        block.id = 1
        block.name = "Block 1"

        llm = MagicMock()
        llm.name = "LLM-1"
        prompt = MagicMock()
        prompt.prompt_text = "Domanda?"
        prompt.expected_answer = "Risposta attesa"

        mock_get_llms.return_value = [llm]
        mock_get_prompts.return_value = [prompt]
        mock_test_create.return_value = "test-obj"
        mock_eval_create.return_value = "evaluation-obj"
        mock_run_create.return_value = "run-obj"

        result = self.service_class.runtest(session, [block])

        mock_get_llms.assert_called_once_with(session=session)
        mock_get_prompts.assert_called_once_with(block=block)
        mock_test_create.assert_called_once()
        mock_interrogate.assert_called_once_with("LLM-1", "Domanda?")
        mock_semantic_eval.assert_called_once_with("Risposta attesa", "Risposta LLM")
        mock_external_eval.assert_called_once_with("google", "Risposta attesa", "Risposta LLM")
        mock_eval_create.assert_called_once()
        mock_run_create.assert_called_once()
        mock_add_run.assert_called_once_with("test-obj", "run-obj")

        assert "results" in result
        assert len(result["results"]) == 1
        block_result = result["results"][0]
        assert block_result["block_id"] == 1
        assert block_result["block_name"] == "Block 1"
        assert len(block_result["results"]) == 1
        assert "averages_by_llm" in block_result
        assert "LLM-1" in block_result["averages_by_llm"]
        assert block_result["averages_by_llm"]["LLM-1"]["avg_semantic_scores"] == 0.8
        assert block_result["averages_by_llm"]["LLM-1"]["avg_external_scores"] == 0.9
