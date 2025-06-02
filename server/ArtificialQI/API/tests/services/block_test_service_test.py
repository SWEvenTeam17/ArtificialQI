from unittest.mock import patch, MagicMock
from API.services.block_test_service import BlockTestService
from API.tests.services.abstract_service_test import AbstractServiceTestCase
from API.models import Block, Session, BlockTest


class TestBlockTestService(AbstractServiceTestCase):
    service_class = BlockTestService

    @patch("API.services.block_test_service.requests.post")
    @patch(
        "API.services.block_test_service.os.getenv",
        return_value="http://fake-llm-service/",
    )
    def test_interrogate(self, mock_getenv, mock_post):
        """Test che verifica l'interrogazione al microservizio LLM"""
        mock_post.return_value.json.return_value = {"answer": "test response"}

        response = self.service_class.interrogate("GPT-4", "Che ore sono?")

        mock_getenv.assert_called_once_with("LLM_SERVICE_URL")
        mock_post.assert_called_once_with(
            "http://fake-llm-service/interrogate/",
            {"llm_name": "GPT-4", "prompt": "Che ore sono?"},
        )
        assert response == "test response"

    @patch("API.services.block_test_service.BlockTestRepository.add_run")
    @patch("API.services.block_test_service.RunService.create")
    @patch("API.services.block_test_service.EvaluationService.create")
    @patch(
        "API.services.block_test_service.EvaluationService.get_external_evaluation",
        return_value=0.9,
    )
    @patch(
        "API.services.block_test_service.EvaluationService.get_semantic_evaluation",
        return_value=0.8,
    )
    @patch(
        "API.services.block_test_service.BlockTestService.interrogate",
        return_value="Risposta LLM",
    )
    @patch("API.services.block_test_service.BlockRepository.get_prompts")
    @patch("API.services.block_test_service.SessionRepository.get_llms")
    @patch("API.services.block_test_service.BlockTestService.create")
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

        test_mock = MagicMock()
        evaluation_mock = MagicMock()
        run_mock = MagicMock()
        run_mock.id = 123

        mock_get_llms.return_value = [llm]
        mock_get_prompts.return_value = [prompt]
        mock_test_create.return_value = test_mock
        mock_eval_create.return_value = evaluation_mock
        mock_run_create.return_value = run_mock

        result = self.service_class.runtest(session, [block])

        mock_get_llms.assert_called_once_with(session=session)
        mock_get_prompts.assert_called_once_with(block=block)
        mock_test_create.assert_called_once_with({"session": session, "block": block})
        mock_interrogate.assert_called_once_with("LLM-1", "Domanda?")
        mock_semantic_eval.assert_called_once_with("Risposta attesa", "Risposta LLM")
        mock_external_eval.assert_called_once_with(
            "google", "Risposta attesa", "Risposta LLM"
        )
        mock_eval_create.assert_called_once()
        mock_run_create.assert_called_once()
        mock_add_run.assert_called_once_with(test_mock, run_mock)

        assert isinstance(result, dict)
        assert result["results"][0]["block_id"] == 1
        assert result["results"][0]["block_name"] == "Block 1"
        assert len(result["results"][0]["results"]) == 1
        assert (
            result["results"][0]["averages_by_llm"]["LLM-1"]["avg_semantic_scores"]
            == 0.8
        )
        assert (
            result["results"][0]["averages_by_llm"]["LLM-1"]["avg_external_scores"]
            == 0.9
        )

    @patch("API.services.block_test_service.BlockTest.run")
    def test_format_results(self, mock_run_related):
        """Test che verifica la formattazione dei risultati da un test"""
        test = MagicMock(spec=BlockTest)
        block = MagicMock()
        block.id = 42
        block.name = "Test Block"
        test.block = block

        evaluation = MagicMock()
        evaluation.semantic_evaluation = 0.6
        evaluation.external_evaluation = 0.4

        llm = MagicMock()
        llm.name = "LLM-Test"

        prompt = MagicMock()
        prompt.prompt_text = "Che cos'è il cielo?"
        prompt.expected_answer = "Una cosa blu"

        run = MagicMock()
        run.id = 77
        run.evaluation = evaluation
        run.llm = llm
        run.prompt = prompt
        run.llm_answer = "Una cosa celeste"

        mock_run_related.all.return_value.select_related.return_value = [run]
        test.run = mock_run_related

        result = self.service_class.format_results(test)

        assert isinstance(result, dict)
        assert "results" in result
        res_data = result["results"][0]
        assert res_data["block_id"] == 42
        assert res_data["block_name"] == "Test Block"
        assert res_data["averages_by_llm"]["LLM-Test"]["avg_semantic_scores"] == 0.6
        assert res_data["averages_by_llm"]["LLM-Test"]["avg_external_scores"] == 0.4
