from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from API.models import LLM

class LLMViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.llm = LLM.objects.create(name="GPT-4", n_parameters="1T")
        self.base_url = "/llm_list/"
        self.detail_url = f"/llm_list/{self.llm.pk}/"

    def test_get_all_llms(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_llm_by_id(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.llm.id)

    def test_post_valid_llm(self):
        data = {
            "name": "Mistral-7B",
            "n_parameters": "7B"
        }
        response = self.client.post(self.base_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Mistral-7B")

    def test_put_valid_llm(self):
        updated_data = {
            "name": "GPT-4 Turbo",
            "n_parameters": "1.5T"
        }
        response = self.client.put(self.detail_url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "GPT-4 Turbo")

    def test_delete_llm(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
