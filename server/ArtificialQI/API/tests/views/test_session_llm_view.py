from rest_framework.test import APITestCase
from rest_framework import status
from API.models import Session, LLM
from API.serializers import LLMSerializer


class SessionLLMViewTestCase(APITestCase):
    def setUp(self):
        # Crea una sessione e due LLM
        self.session = Session.objects.create(title="Sessione Test", description="Descrizione")
        self.llm1 = LLM.objects.create(name="LLM-A", n_parameters="500M")
        self.llm2 = LLM.objects.create(name="LLM-B", n_parameters="1B")
        self.session.llm.add(self.llm1)

        # URL corrispondenti al tuo urls.py
        self.get_url = f"/api/llm_remaining/{self.session.id}"
        self.post_url = "/api/llm_add/"
        self.delete_url = f"/api/llm_delete/{self.session.id}/{self.llm1.id}"

    def test_get_llms_connected_to_session(self):
        response = self.client.get(self.get_url)
        expected_data = LLMSerializer([self.llm1], many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_add_llm_to_session(self):
        response = self.client.post(self.post_url, {
            "sessionId": self.session.id,
            "llmId": self.llm2.id
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.session.llm.filter(id=self.llm2.id).exists())

    def test_add_llm_invalid_id(self):
        response = self.client.post(self.post_url, {
            "sessionId": self.session.id,
            "llmId": 9999  # ID inesistente
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)

    def test_delete_llm_from_session(self):
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.session.llm.filter(id=self.llm1.id).exists())

    def test_delete_llm_invalid_id(self):
        response = self.client.delete(f"/api/llm_delete/{self.session.id}/9999")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)

    def test_get_llms_invalid_session(self):
        response = self.client.get("/api/llm_remaining/9999")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)
