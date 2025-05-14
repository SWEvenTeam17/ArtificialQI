from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from API.models import Session

class TestSessionsView(TestCase):


    def setUp(self):
        self.client = APIClient()
        self.session = Session.objects.create(
            title="Sessione Test",
            description="Questa è una sessione di prova"
        )
        self.base_url = "/session_list/"
        self.detail_url = f"/session_list/{self.session.pk}/"

    def test_get_all_sessions(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_session_by_id(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.session.id)

    def test_post_valid_session(self):
        data = {
            "title": "Nuova Sessione",
            "description": "Descrizione della sessione"
        }
        response = self.client.post(self.base_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Nuova Sessione")

    def test_put_valid_session(self):
        updated_data = {
            "title": "Sessione Aggiornata",
            "description": "Descrizione modificata"
        }
        response = self.client.put(self.detail_url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Sessione Aggiornata")

    def test_delete_session(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)