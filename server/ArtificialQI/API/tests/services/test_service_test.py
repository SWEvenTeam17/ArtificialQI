from unittest.mock import patch, MagicMock
import pytest
from API.services.test_service import TestService
from API.tests.services.abstract_service_test import AbstractServiceTestCase
from API.models import Session

class TestTestService(AbstractServiceTestCase):
    service_class = TestService

    @patch('API.services.test_service.PromptRepository')
    @patch('API.services.test_service.PromptService')
    
    def test_save_data_new_prompt(self, mock_prompt_service, mock_prompt_repo):
        # Setup
        mock_session = MagicMock(spec=Session)
        test_data = [{
            "prompt_text": "Test question?",
            "expected_answer": "Test answer"
        }]
        
        # Mock: no existing prompt found
        mock_prompt_repo.filter_one.return_value = None
        mock_prompt_service.create.return_value = MagicMock(id=1)
        
        # Test
        TestService.save_data(data=test_data, session=mock_session)
        
        # Assert
        mock_prompt_repo.filter_one.assert_called_once_with(
            prompt_text="Test question?",
            expected_answer="Test answer",
            session=mock_session
        )
        mock_prompt_service.create.assert_called_once_with({
            "prompt_text": "Test question?",
            "expected_answer": "Test answer",
            "session": mock_session,
        })
        assert test_data[0]["id"] == 1

    @patch('API.services.test_service.PromptRepository')
    
    def test_save_data_existing_prompt(self, mock_prompt_repo):
        # Setup
        mock_session = MagicMock(spec=Session)
        mock_existing_prompt = MagicMock(id=42)
        test_data = [{
            "prompt_text": "Existing question?",
            "expected_answer": "Existing answer"
        }]
        
        # Mock: existing prompt found
        mock_prompt_repo.filter_one.return_value = mock_existing_prompt
        
        # Test
        TestService.save_data(data=test_data, session=mock_session)
        
        # Assert
        mock_prompt_repo.filter_one.assert_called_once_with(
            prompt_text="Existing question?",
            expected_answer="Existing answer",
            session=mock_session
        )
        assert test_data[0]["id"] == 42

    @patch('API.services.test_service.requests.post')
    @patch('API.services.test_service.os.getenv')
   
    def test_interrogate(self, mock_getenv, mock_post):
        # Setup
        mock_getenv.return_value = "http://llm-service/"
        mock_response = MagicMock()
        mock_response.json.return_value = {"answer": "Test response"}
        mock_post.return_value = mock_response
        
        # Test
        result = TestService.interrogate("test-llm", "Test question?")
        
        # Assert
        mock_getenv.assert_called_once_with("LLM_SERVICE_URL")
        mock_post.assert_called_once_with(
            "http://llm-service/interrogate/",
            {"llm_name": "test-llm", "prompt": "Test question?"}
        )
        assert result == "Test response"

    @patch('API.services.test_service.LLMController')
    @patch('API.services.test_service.EvaluationService')
    @patch('API.services.test_service.PromptService')
    @patch('API.services.test_service.TestService.interrogate')
   
    def test_evaluate(self, mock_interrogate, mock_prompt_service, mock_eval_service, mock_llm_controller):
        # Setup
        mock_llm1 = MagicMock()
        mock_llm1.name = "llm1" 
        mock_llm2 = MagicMock()
        mock_llm2.name = "llm2"
        mock_llms = [mock_llm1, mock_llm2]
    
        test_data = [{
         "id": 1,
         "prompt_text": "Q1",
         "expected_answer": "A1"
         }]
        
        # Mocks
        mock_prompt = MagicMock()
        mock_prompt.prompt_text = "Q1"
        mock_prompt.session = MagicMock()
        mock_prompt_service.read.return_value = mock_prompt
        
        mock_interrogate.return_value = "LLM response"
        mock_llm_controller.get_semantic_evaluation.return_value = 0.85
        mock_llm_controller.get_external_evaluation.return_value = 0.9
        mock_eval_service.create.return_value = MagicMock()
        
        # Test
        results = TestService.evaluate(mock_llms, test_data)
        
        # Assert
        assert len(results) == 2  
        assert results[0]["llm_name"] == "llm1"
        assert results[0]["question"] == "Q1"
        assert results[0]["expected_answer"] == "A1"
        assert results[0]["answer"] == "LLM response"
        assert results[0]["semantic_evaluation"] == 0.85
        assert results[0]["external_evaluation"] == 0.9

    def test_get_formatted(self):
        # Test with ID
        input_data = [{
            "id": 1,
            "prompt_text": "Question?",
            "expected_answer": "Answer"
        }]
        result = TestService.get_formatted(input_data)
        assert result == input_data
        
        # Test without ID
        input_data = [{
            "prompt_text": "New question?",
            "expected_answer": "New answer"
        }]
        expected = [{
            "prompt_text": "New question?",
            "expected_answer": "New answer"
        }]
        result = TestService.get_formatted(input_data)
        assert result == expected

    @patch('API.services.test_service.SessionRepository')
    @patch('API.services.test_service.TestService.get_formatted')
    
    def test_get_data(self, mock_get_formatted, mock_session_repo):
        # Setup
        mock_session = MagicMock()
        mock_session_repo.get_by_id.return_value = mock_session
        mock_get_formatted.return_value = ["formatted_data"]
        
        # Test
        formatted_data, session = TestService.get_data("raw_data", 123)
        
        # Assert
        mock_session_repo.get_by_id.assert_called_once_with(123)
        mock_get_formatted.assert_called_once_with("raw_data")
        assert formatted_data == ["formatted_data"]
        assert session == mock_session