from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from API.models import Prompt, LLM, Answer, Session

class AnswerViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.llm = LLM.objects.create(name="llama3.2", n_parameters="3B")
        self.session = Session.objects.create(title="Test session")
        self.session.llm.add(self.llm)
        self.prompt = Prompt.objects.create(
            prompt_text="Qual è la capitale della Francia?",
            expected_answer="Parigi",
            session=self.session,
        )
        self.answer = Answer.objects.create(
            prompt=self.prompt,
            LLM=self.llm,
            LLM_answer="Parigi",
        )
        self.base_url = "/answer_list/"
        self.detail_url = f"/answer_list/{self.answer.pk}/"
    def test_get_all_answers(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_answer_by_id(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.answer.id)

    def test_post_valid_answer(self):
        data = {
            "prompt": self.prompt.id,
            "LLM": self.llm.id,
            "LLM_answer": "Parigi"
        }
        response = self.client.post(self.base_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_valid_answer(self):
        updated_data = {
            "prompt": self.prompt.id,
            "LLM": self.llm.id,
            "LLM_answer": "Parigi aggiornata"
        }
        response = self.client.put(self.detail_url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["LLM_answer"], "Parigi aggiornata")

    def test_delete_answer(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
