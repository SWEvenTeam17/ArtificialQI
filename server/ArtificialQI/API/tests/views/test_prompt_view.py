from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from API.models import Prompt, Session, LLM

class PromptViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.llm = LLM.objects.create(name="GPT-3.5", n_parameters="175B")
        self.session = Session.objects.create(title="Sessione di test")
        self.session.llm.add(self.llm)
        self.prompt = Prompt.objects.create(
            prompt_text="Cosa fa il photosistema II?",
            expected_answer="Produce ossigeno",
            session=self.session,
        )
        self.base_url = "/prompt_list/"
        self.detail_url = f"/prompt_list/{self.prompt.pk}/"

    def test_get_all_prompts(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_prompt_by_id(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.prompt.id)

    def test_post_valid_prompt(self):
        data = {
            "prompt_text": "Qual è la capitale dell’Italia?",
            "expected_answer": "Roma",
            "session": self.session.id,
        }
        response = self.client.post(self.base_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_valid_prompt(self):
        updated_data = {
            "prompt_text": "Qual è la capitale dell’Italia aggiornata?",
            "expected_answer": "Roma",
            "session": self.session.id,
        }
        response = self.client.put(self.detail_url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["prompt_text"], updated_data["prompt_text"])

    def test_delete_prompt(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
