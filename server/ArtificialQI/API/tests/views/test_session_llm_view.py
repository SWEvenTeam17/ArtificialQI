from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from API.models import LLM, Session

class TestSessionLLMView(TestCase):

    def setUp(self):
        
        self.client = APIClient()
        self.llm = LLM.objects.create(name="GPT-4", n_parameters="1T")
        self.session = Session.objects.create(title="Benchmark Session")

        self.session.save()
        self.session.llm.set([self.llm])  # <-- usa set invece di add
        self.session.refresh_from_db()

        self.get_url = f"/llm_list_by_session/{self.session.pk}/"
        self.post_url = "/llm_add/"
        self.delete_url = f"/llm_delete/{self.session.pk}/{self.llm.pk}"

    #def test_get_llms_by_session(self):
    #    response = self.client.get(self.get_url)
    #    self.assertEqual(response.status_code, status.HTTP_200_OK)
    #    self.assertGreaterEqual(len(response.data), 1)
    #    self.assertEqual(response.data[0]["id"], self.llm.id)

    def test_post_add_llm_to_session(self):
        new_llm = LLM.objects.create(name="LLaMA-3", n_parameters="70B")
        response = self.client.post(self.post_url, {
            "sessionId": self.session.pk,
            "llmId": new_llm.pk
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["id"], new_llm.id)

    def test_delete_llm_from_session(self):
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.session.llm.filter(pk=self.llm.pk).exists())
