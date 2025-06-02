import pytest
from unittest.mock import patch, MagicMock
from API.services import EvaluationService


class TestEvaluationService:

    @patch("API.services.evaluation_service.SentenceTransformer")
    def test_get_semantic_evaluation_exact_match(self, mock_st):
        assert (
            EvaluationService.get_semantic_evaluation("Risposta.", "risposta.") == 100
        )

    @patch("API.services.evaluation_service.SentenceTransformer")
    def test_get_semantic_evaluation_similarity(self, mock_st):
        mock_model = MagicMock()
        mock_st.return_value = mock_model
        mock_model.encode.side_effect = lambda x: [[1.0]]
        mock_model.similarity.return_value = [[MagicMock(item=lambda: 0.42)]]
        result = EvaluationService.get_semantic_evaluation("a", "b")
        assert isinstance(result, float)

    @patch("API.services.evaluation_service.load_dotenv", return_value=False)
    def test_get_external_evaluation_env_missing(self, mock_dotenv):
        with pytest.raises(FileNotFoundError):
            EvaluationService.get_external_evaluation("google", "a", "b")

    @patch("API.services.evaluation_service.load_dotenv", return_value=True)
    @patch("API.services.evaluation_service.os.getenv", return_value=None)
    def test_get_external_evaluation_no_key(self, mock_getenv, mock_dotenv):
        result = EvaluationService.get_external_evaluation("google", "a", "b")
        assert result == "API key not found."

    @patch("API.services.evaluation_service.load_dotenv", return_value=True)
    @patch("API.services.evaluation_service.os.getenv", return_value="fake-key")
    @patch("API.services.evaluation_service.ChatGoogleGenerativeAI")
    def test_get_external_evaluation_percentage_found(
        self, mock_chat, mock_getenv, mock_dotenv
    ):
        mock_llm = MagicMock()
        mock_chat.return_value = mock_llm
        mock_stream = iter([MagicMock(content="La risposta è 87.5%")])
        mock_llm.stream.return_value = mock_stream
        result = EvaluationService.get_external_evaluation("google", "a", "b")
        assert result == "87.5"

    @patch("API.services.evaluation_service.load_dotenv", return_value=True)
    @patch("API.services.evaluation_service.os.getenv", return_value="fake-key")
    @patch("API.services.evaluation_service.ChatGoogleGenerativeAI")
    def test_get_external_evaluation_percentage_not_found(
        self, mock_chat, mock_getenv, mock_dotenv
    ):
        mock_llm = MagicMock()
        mock_chat.return_value = mock_llm
        mock_stream = iter([MagicMock(content="No number here")])
        mock_llm.stream.return_value = mock_stream
        result = EvaluationService.get_external_evaluation("google", "a", "b")
        assert result == "Percentage not found."

    @patch("API.services.evaluation_service.load_dotenv", return_value=True)
    @patch("API.services.evaluation_service.os.getenv", return_value="fake-key")
    @patch(
        "API.services.evaluation_service.ChatGoogleGenerativeAI",
        side_effect=Exception("fail"),
    )
    def test_get_external_evaluation_generic_exception(
        self, mock_chat, mock_getenv, mock_dotenv
    ):
        result = EvaluationService.get_external_evaluation("google", "a", "b")
        assert result == "Errore interno durante la valutazione"

    @patch("API.services.evaluation_service.load_dotenv", return_value=True)
    @patch("API.services.evaluation_service.os.getenv", return_value="fake-key")
    @patch(
        "API.services.evaluation_service.ChatGoogleGenerativeAI",
        side_effect=ImportError("fail"),
    )
    def test_get_external_evaluation_google_api_exception(
        self, mock_chat, mock_getenv, mock_dotenv
    ):
        result = EvaluationService.get_external_evaluation("google", "a", "b")
        assert result in ["Errore API Gemini", "Errore interno durante la valutazione"]

    def test_get_external_evaluation_unsupported(self):
        result = EvaluationService.get_external_evaluation("altro", "a", "b")
        assert result == "Unsupported provider"
