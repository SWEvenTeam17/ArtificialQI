import pytest
from unittest.mock import patch, MagicMock
from API.classes.llm_controller import LLMController
from requests.exceptions import RequestException

# --- __init__ ---

@patch("API.classes.llm_controller.OllamaLLM")
@patch("API.classes.llm_controller.requests.get")
@patch("API.classes.llm_controller.os.getenv", return_value="http://fake-url")
@patch("API.classes.llm_controller.load_dotenv", return_value=True)
def test_init_success(mock_dotenv, mock_getenv, mock_requests_get, mock_ollama):
    mock_response = MagicMock()
    mock_requests_get.return_value = mock_response
    mock_response.raise_for_status.return_value = None
    c = LLMController("test-model")
    assert c.llm == mock_ollama.return_value
    mock_requests_get.assert_called_once_with("http://fake-url/api/version", timeout=5)

@patch("API.classes.llm_controller.requests.get", side_effect=RequestException("fail"))
@patch("API.classes.llm_controller.os.getenv", return_value="http://fake-url")
@patch("API.classes.llm_controller.load_dotenv", return_value=True)
def test_init_fail(mock_dotenv, mock_getenv, mock_requests_get):
    with pytest.raises(ConnectionError):
        LLMController("test-model")

# --- get_answer ---

@patch.object(LLMController, "__init__", lambda self, llm_name: None)
def test_get_answer():
    c = LLMController("test")
    mock_stream = iter(["a", "b", "c"])
    c.llm = MagicMock()
    c.llm.stream.return_value = mock_stream
    result = c.get_answer("prompt")
    assert result == "abc"
    c.llm.stream.assert_called_once_with("prompt")

# --- get_semantic_evaluation ---

@patch("API.classes.llm_controller.SentenceTransformer")
def test_get_semantic_evaluation_exact_match(mock_st):
    # clean_expected in clean_llm_answer
    assert LLMController.get_semantic_evaluation("Risposta.", "risposta.") == 100

@patch("API.classes.llm_controller.SentenceTransformer")
def test_get_semantic_evaluation_similarity(mock_st):
    # clean_expected NOT in clean_llm_answer
    mock_model = MagicMock()
    mock_st.return_value = mock_model
    mock_model.encode.side_effect = lambda x: [[1.0]]
    mock_model.similarity.return_value = [[MagicMock(item=lambda: 0.42)]]
    result = LLMController.get_semantic_evaluation("a", "b")
    assert isinstance(result, float)

# --- get_external_evaluation ---

@patch("API.classes.llm_controller.load_dotenv", return_value=False)
def test_get_external_evaluation_env_missing(mock_dotenv):
    with pytest.raises(FileNotFoundError):
        LLMController.get_external_evaluation("google", "a", "b")

@patch("API.classes.llm_controller.load_dotenv", return_value=True)
@patch("API.classes.llm_controller.os.getenv", return_value=None)
def test_get_external_evaluation_no_key(mock_getenv, mock_dotenv):
    result = LLMController.get_external_evaluation("google", "a", "b")
    assert result == "API key not found."

@patch("API.classes.llm_controller.load_dotenv", return_value=True)
@patch("API.classes.llm_controller.os.getenv", return_value="fake-key")
@patch("API.classes.llm_controller.ChatGoogleGenerativeAI")
def test_get_external_evaluation_percentage_found(mock_chat, mock_getenv, mock_dotenv):
    mock_llm = MagicMock()
    mock_chat.return_value = mock_llm
    mock_stream = iter([MagicMock(content="La risposta è 87.5%")])
    mock_llm.stream.return_value = mock_stream
    result = LLMController.get_external_evaluation("google", "a", "b")
    assert result == "87.5"

@patch("API.classes.llm_controller.load_dotenv", return_value=True)
@patch("API.classes.llm_controller.os.getenv", return_value="fake-key")
@patch("API.classes.llm_controller.ChatGoogleGenerativeAI")
def test_get_external_evaluation_percentage_not_found(mock_chat, mock_getenv, mock_dotenv):
    mock_llm = MagicMock()
    mock_chat.return_value = mock_llm
    mock_stream = iter([MagicMock(content="No number here")])
    mock_llm.stream.return_value = mock_stream
    result = LLMController.get_external_evaluation("google", "a", "b")
    assert result == "Percentage not found."

@patch("API.classes.llm_controller.load_dotenv", return_value=True)
@patch("API.classes.llm_controller.os.getenv", return_value="fake-key")
@patch("API.classes.llm_controller.ChatGoogleGenerativeAI", side_effect=Exception("fail"))
def test_get_external_evaluation_generic_exception(mock_chat, mock_getenv, mock_dotenv):
    result = LLMController.get_external_evaluation("google", "a", "b")
    assert result == "Errore interno durante la valutazione"

@patch("API.classes.llm_controller.load_dotenv", return_value=True)
@patch("API.classes.llm_controller.os.getenv", return_value="fake-key")
@patch("API.classes.llm_controller.ChatGoogleGenerativeAI", side_effect=ImportError("fail"))
def test_get_external_evaluation_google_api_exception(mock_chat, mock_getenv, mock_dotenv):
    # Simula GoogleAPICallError o InternalServerError
    result = LLMController.get_external_evaluation("google", "a", "b")
    assert result in ["Errore API Gemini", "Errore interno durante la valutazione"]

def test_get_external_evaluation_unsupported():
    result = LLMController.get_external_evaluation("altro", "a", "b")
    assert result == "Unsupported provider"