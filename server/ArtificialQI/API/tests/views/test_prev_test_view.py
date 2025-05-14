from django.test import TestCase, Client
from unittest.mock import patch, MagicMock


class PrevTestViewTest(TestCase):

    @patch("API.views_def.prev_test_view.PromptService.filter_by_session")
    @patch("API.views_def.prev_test_view.SessionService.read")
    def test_get_previous_tests_success(self, mock_read, mock_filter_by_session):
        session_id = 1
        mock_session = MagicMock()
        mock_read.return_value = mock_session
        mock_filter_by_session.return_value = Mock()
        mock_filter_by_session.return_value.tolist.return_value = [mock_prompt]


        client = Client()
        response = client.get(f"/previous_tests/{session_id}/")

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    @patch("API.views_def.prev_test_view.PromptService.filter_by_session", side_effect=Exception("Errore"))
    @patch("API.views_def.prev_test_view.SessionService.read")
    def test_get_previous_tests_error(self, mock_read, mock_filter):
        mock_read.return_value = MagicMock()
        client = Client()
        response = client.get("/previous_tests/999/")

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    @mock.patch("API.views_def.prev_test_view.PromptService.delete")
    def test_delete_previous_tests_success(self, mock_delete):
        # Mocka la chiamata alla delete
        mock_delete.return_value = None  # O la risposta che desideri
        session_id = 1  # Usa un valore di test
        response = self.client.delete(f"/previous_tests/{session_id}/")
        
        # Verifica che la delete sia stata chiamata
        mock_delete.assert_called_once_with(instance_id=session_id)

        # Verifica che il codice di stato sia 204
        self.assertEqual(response.status_code, 204)


    @patch("API.views.prev_test_view.PromptService.delete", side_effect=Exception("Errore cancellazione"))
    def test_delete_previous_tests_error(self, mock_delete):
        client = Client()
        response = client.delete("/previous_tests/123/")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
