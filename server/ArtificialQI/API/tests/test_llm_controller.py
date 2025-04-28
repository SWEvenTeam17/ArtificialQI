from django.test import TestCase
from API.classes.llm_controller import LLMController
from unittest.mock import patch

class LLMControllerTests(TestCase):
    def test_semantic_evaluation_exact_match(self):
        """Verifica che risposte identiche abbiano score 100."""
        llm = LLMController("llama3")
        score = llm.get_semantic_evaluation("Hello", "Hello")
        self.assertEqual(score, 100)

    def test_semantic_evaluation_no_match(self):
        """Verifica che risposte diverse abbiano score basso."""
        llm = LLMController("llama3") 
        score = llm.get_semantic_evaluation("Hello", "Goodbye")
        self.assertTrue(0 <= score < 50) 
  
  "patch simula chiamate API esterne"
    @patch("requests.get")  # Mock della chiamata API a Ollama
    def test_get_answer_from_llm(self, mock_get):
        """Testa che get_answer() restituisca una risposta valida."""
        mock_get.return_value.json.return_value = {"output": "Mocked answer"}
        llm = LLMController("llama3")
        answer = llm.get_answer("Test question")
        self.assertEqual(answer, "Mocked answer")