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
      # Configurazione degli oggetti mock
      session = MagicMock(spec=Session)
      block = MagicMock(spec=Block)
      block.id = 1
      block.name = "Block 1"

      llm = MagicMock()
      llm.name = "LLM-1"
    
      prompt = MagicMock()
      prompt.prompt_text = "Domanda?"
      prompt.expected_answer = "Risposta attesa"

      # Crea mock completi per gli oggetti restituiti
      test_mock = MagicMock()
      evaluation_mock = MagicMock()
      run_mock = MagicMock()
      run_mock.id = 123  # Aggiungi l'attributo id necessario

      # Configura i return value
      mock_get_llms.return_value = [llm]
      mock_get_prompts.return_value = [prompt]
      mock_test_create.return_value = test_mock
      mock_eval_create.return_value = evaluation_mock
      mock_run_create.return_value = run_mock

      # Esegui il test
      result = self.service_class.runtest(session, [block])

      # Verifiche
      mock_get_llms.assert_called_once_with(session=session)
      mock_get_prompts.assert_called_once_with(block=block)
      mock_test_create.assert_called_once_with({"session": session, "block": block})
      mock_interrogate.assert_called_once_with("LLM-1", "Domanda?")
      mock_semantic_eval.assert_called_once_with("Risposta attesa", "Risposta LLM")
      mock_external_eval.assert_called_once_with("google", "Risposta attesa", "Risposta LLM")
    
      # Verifica che create sia chiamato con i parametri corretti
      mock_eval_create.assert_called_once_with({
        "semantic_evaluation": 0.8,
        "external_evaluation": 0.9
      })
    
      mock_run_create.assert_called_once_with({
        "llm": llm,
        "prompt": prompt,
        "evaluation": evaluation_mock,
        "llm_answer": "Risposta LLM"
      })
    
      mock_add_run.assert_called_once_with(test_mock, run_mock)

      # Verifica la struttura del risultato
      assert isinstance(result, dict)
      assert len(result["results"]) == 1
      assert result["results"][0]["block_id"] == 1
      assert result["results"][0]["block_name"] == "Block 1"
      assert len(result["results"][0]["results"]) == 1
      assert result["results"][0]["averages_by_llm"]["LLM-1"]["avg_semantic_scores"] == 0.8
      assert result["results"][0]["averages_by_llm"]["LLM-1"]["avg_external_scores"] == 0.9