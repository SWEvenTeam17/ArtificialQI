import pytest
from rest_framework.test import APIClient
from rest_framework import status
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ArtificialQI.settings")
from API.views_def.block_view import BlockView

@pytest.fixture
def client():
    return APIClient()

@pytest.mark.django_db
def test_post_block_success(monkeypatch, client):
    # Finto service che simula la creazione avvenuta con successo
    class FakeService:
        @staticmethod
        def create(data):
            return True

    # Applica la patch sul service della view
    monkeypatch.setattr(BlockView, "service", FakeService)

    data = {"name": "block1", "questions": []}  # Nessuna domanda per evitare problemi di validazione
    response = client.post("/question_blocks/", data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "block1"
    assert response.data["questions"] == []

@pytest.mark.django_db
def test_post_block_duplicate(monkeypatch, client):
    # Finto service che simula fallimento per nome duplicato
    class FakeService:
        @staticmethod
        def create(data):
            return False  # Simula duplicato

    monkeypatch.setattr(BlockView, "service", FakeService)

    data = {"name": "block1", "questions": []}
    response = client.post("/question_blocks/", data, format="json")

    assert response.status_code == 500
    assert "error" in response.data
    assert response.data["error"] == "Nome duplicato"
    
@pytest.mark.django_db
def test_post_block_exception(monkeypatch, client):
    # Mock BlockService.create per eccezione
    class FakeService:
        @staticmethod
        def create(data):
            raise Exception("Errore finto")
    monkeypatch.setattr("API.views_def.block_view.BlockService", FakeService)
    data = {"name": "block1", "questions": [1, 2, 3]}
    response = client.post("/question_blocks/", data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data

@pytest.mark.django_db
def test_get_block_success(monkeypatch, client):
    # Mock LLMService, BlockService, RunRepository per successo
    class FakeLLM:
        def __init__(self, id):
            self.id = id
    class FakeBlock:
        def __init__(self, id, name):
            self.id = id
            self.name = name
    class FakeBlockSet:
        def __init__(self, blocks):
            self.blocks = blocks
        def all(self):
            return self.blocks

    class FakePrompt:
        def __init__(self, blocks):
            self.block_set = FakeBlockSet(blocks)

    class FakeEval:
        def __init__(self, sem, ext):
            self.semantic_evaluation = sem
            self.external_evaluation = ext
    class FakeRun:
        def __init__(self, llm, prompt, evaluation):
            self.llm = llm
            self.prompt = prompt
            self.evaluation = evaluation

    monkeypatch.setattr("API.views_def.block_view.LLMService.read", lambda x: FakeLLM(x))
    monkeypatch.setattr("API.views_def.block_view.BlockService.get_common_blocks", lambda a, b: [FakeBlock(1, "block1")])
    # prompt.block_set.all() deve restituire una lista di blocchi
    fake_prompt = FakePrompt(blocks=[FakeBlock(1, "block1")])
    fake_eval = FakeEval(0.8, 0.9)
    fake_run = FakeRun(FakeLLM(1), fake_prompt, fake_eval)
    monkeypatch.setattr("API.views_def.block_view.RunRepository.get_common_runs", lambda a, b, c: [fake_run])

    url = "/question_blocks/?first_llm_id=1&second_llm_id=2"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert "common_blocks" in response.data
    assert response.data["common_blocks"][0]["block_id"] == 1

@pytest.mark.django_db
def test_get_block_missing_llm(monkeypatch, client):
    # Uno dei due LLM non esiste
    monkeypatch.setattr("API.views_def.block_view.LLMService.read", lambda x: None)
    url = "/question_blocks/?first_llm_id=1&second_llm_id=2"
    response = client.get(url)
    assert response.status_code == 400
    assert "error" in response.data

@pytest.mark.django_db
def test_get_block_no_common_blocks(monkeypatch, client):
    # Nessun blocco comune
    class FakeLLM:
        def __init__(self, id):
            self.id = id
    monkeypatch.setattr("API.views_def.block_view.LLMService.read", lambda x: FakeLLM(x))
    monkeypatch.setattr("API.views_def.block_view.BlockService.get_common_blocks", lambda a, b: [])
    monkeypatch.setattr("API.views_def.block_view.RunRepository.get_common_runs", lambda a, b, c: [])
    url = "/question_blocks/?first_llm_id=1&second_llm_id=2"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["common_blocks"] == []
