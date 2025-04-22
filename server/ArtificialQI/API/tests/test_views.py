from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from API.models import LLM, Session

class ViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.llm = LLM.objects.create(name="llama3", n_parameters="7B")
        self.session = Session.objects.create(title="Test Session")

    def test_llm_list_api(self):
        """Testa l'endpoint di lista LLM."""
        url = reverse("llm-list")  # Assicurati di avere un 'name' in urls.py
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)  # Verifica che restituisca l'LLM creato

    def test_create_prompt_api(self):
        """Testa la creazione di un Prompt via API."""
        url = reverse("prompt-list")
        data = {
            "prompt_text": "Test prompt",
            "expected_answer": "Test answer",
            "session": self.session.id
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)  # 201 = Created
        self.assertEqual(response.data["prompt_text"], "Test prompt")