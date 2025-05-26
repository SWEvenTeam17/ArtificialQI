import pytest
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework import status
from API.views_def.block_view import BlockView, BlockTestView

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def factory():
    return APIRequestFactory()

# ----------- BlockView POST -----------

@pytest.mark.django_db
def test_post_block_success(monkeypatch, client):
    class FakeService:
        @staticmethod
        def create(data):
            class Obj:
                id = 1
                name = data["name"]
                prompt = data.get("prompt", [])
                pk = 1
            return Obj()
    monkeypatch.setattr(BlockView, "service", FakeService)
    data = {"name": "block1", "prompt": []}
    response = client.post("/question_blocks/", data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "block1"

@pytest.mark.django_db
def test_post_block_duplicate(monkeypatch, client):
    class FakeService:
        @staticmethod
        def create(data):
            return False
    monkeypatch.setattr(BlockView, "service", FakeService)
    data = {"name": "block1", "prompt": []}
    response = client.post("/question_blocks/", data, format="json")
    assert response.status_code == 500
    assert "error" in response.data
    assert response.data["error"] == "Nome duplicato"

@pytest.mark.django_db
def test_post_block_exception(monkeypatch, client):
    class FakeService:
        @staticmethod
        def create(data):
            raise Exception("Errore finto")
    monkeypatch.setattr(BlockView, "service", FakeService)
    data = {"name": "block1", "prompt": []}
    response = client.post("/question_blocks/", data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data
    assert response.data["error"] == "Errore finto"

# ----------- BlockTestView GET -----------

@pytest.mark.django_db
def test_blocktestview_get_success(monkeypatch, factory):
    # Successo con blocchi e run
    class FakeLLM:
        def __init__(self, id):
            self.id = id
    class FakeBlock:
        def __init__(self, id, name):
            self.id = id
            self.name = name
    class FakePrompt:
        pass
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
    monkeypatch.setattr("API.views_def.block_view.BlockRepository.get_common_blocks_for_llms", lambda a, b: [FakeBlock(1, "block1")])
    monkeypatch.setattr("API.views_def.block_view.RunRepository.get_common_runs", lambda a, b, c: [FakeRun(FakeLLM(1), FakePrompt(), FakeEval(0.8, 0.9))])
    class FakeBlockManager:
        @staticmethod
        def filter(**kwargs):
            return [FakeBlock(1, "block1")]
    monkeypatch.setattr("API.views_def.block_view.Block", type("Block", (), {"objects": FakeBlockManager}))
    request = factory.get("/question_blocks/", {"first_llm_id": 1, "second_llm_id": 2})
    response = BlockTestView.as_view()(request)
    assert response.status_code == 200
    assert "common_blocks" in response.data
    assert response.data["common_blocks"][0]["block_id"] == 1

@pytest.mark.django_db
def test_blocktestview_get_missing_llm(monkeypatch, factory):
    # Uno dei due LLM non esiste
    monkeypatch.setattr("API.views_def.block_view.LLMService.read", lambda x: None)
    request = factory.get("/question_blocks/", {"first_llm_id": 1, "second_llm_id": 2})
    response = BlockTestView.as_view()(request)
    assert response.status_code == 400
    assert "error" in response.data

@pytest.mark.django_db
def test_blocktestview_get_no_common_blocks(monkeypatch, factory):
    # Nessun blocco comune
    class FakeLLM:
        def __init__(self, id):
            self.id = id
    monkeypatch.setattr("API.views_def.block_view.LLMService.read", lambda x: FakeLLM(x))
    monkeypatch.setattr("API.views_def.block_view.BlockRepository.get_common_blocks_for_llms", lambda a, b: [])
    monkeypatch.setattr("API.views_def.block_view.RunRepository.get_common_runs", lambda a, b, c: [])
    class FakeBlockManager:
        @staticmethod
        def filter(**kwargs):
            return []
    monkeypatch.setattr("API.views_def.block_view.Block", type("Block", (), {"objects": FakeBlockManager}))
    request = factory.get("/question_blocks/", {"first_llm_id": 1, "second_llm_id": 2})
    response = BlockTestView.as_view()(request)
    assert response.status_code == 200
    assert response.data["common_blocks"] == []

@pytest.mark.django_db
def test_blocktestview_get_multiple_runs(monkeypatch, factory):
    # Più run e blocchi, copre for annidati
    class FakeLLM:
        def __init__(self, id):
            self.id = id
    class FakeBlock:
        def __init__(self, id, name):
            self.id = id
            self.name = name
    class FakePrompt:
        pass
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
    monkeypatch.setattr("API.views_def.block_view.BlockRepository.get_common_blocks_for_llms", lambda a, b: [FakeBlock(1, "block1"), FakeBlock(2, "block2")])
    monkeypatch.setattr("API.views_def.block_view.RunRepository.get_common_runs", lambda a, b, c: [
        FakeRun(FakeLLM(1), FakePrompt(), FakeEval(0.8, 0.9)),
        FakeRun(FakeLLM(2), FakePrompt(), FakeEval(0.7, 0.6)),
    ])
    class FakeBlockManager:
        @staticmethod
        def filter(**kwargs):
            # Restituisce entrambi i blocchi
            return [FakeBlock(1, "block1"), FakeBlock(2, "block2")]
    monkeypatch.setattr("API.views_def.block_view.Block", type("Block", (), {"objects": FakeBlockManager}))
    request = factory.get("/question_blocks/", {"first_llm_id": 1, "second_llm_id": 2})
    response = BlockTestView.as_view()(request)
    assert response.status_code == 200
    assert len(response.data["common_blocks"]) == 2
    assert set([b["block_id"] for b in response.data["common_blocks"]]) == {1, 2}