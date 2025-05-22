import sys
sys.path.append("C:/Users/Alessandro/OneDrive/Desktop/progetto swe/ArtificialQI/server")
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
    print("TEST POST BLOCK SUCCESS")  # Per debug
    class FakeService:
        @staticmethod
        def create(data):
            return {"id": 1, "name": data["name"], "prompt": data.get("prompt", [])}

    monkeypatch.setattr(BlockView, "service", FakeService)

    data = {"name": "block1", "prompt": []}
    response = client.post("/question_blocks/", data, format="json")

    print("RESPONSE DATA:", response.data)  # Per debug
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "block1"
    assert response.data["prompt"] == []

@pytest.mark.django_db
def test_post_block_duplicate(monkeypatch, client):
    print("TEST POST BLOCK DUPLICATE")  # Per debug
    # Finto service che simula fallimento per nome duplicato
    class FakeService:
        @staticmethod
        def create(data):
            return False  # Simula duplicato

    # Patcha la property della classe, perché BlockView usa self.service nel post
    monkeypatch.setattr(BlockView, "service", FakeService)

    data = {"name": "block1", "prompt": []}
    response = client.post("/question_blocks/", data, format="json")

    assert response.status_code == 500
    assert "error" in response.data
    assert response.data["error"] == "Nome duplicato"

@pytest.mark.django_db
def test_post_block_exception(monkeypatch, client):
    print("TEST POST BLOCK EXCEPTION")  # Per debug
    # Finto service che solleva eccezione
    class FakeService:
        @staticmethod
        def create(data):
            raise Exception("Errore finto")

    # Patcha la property della classe, perché BlockView usa self.service nel post
    monkeypatch.setattr(BlockView, "service", FakeService)

    data = {"name": "block1", "prompt": []}
    response = client.post("/question_blocks/", data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data

@pytest.mark.django_db
def test_get_block_success(monkeypatch, client):
    print("TEST GET BLOCK SUCCESS")  # Per debug
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

    # Patch gli import diretti usati nella get
    monkeypatch.setattr("API.views_def.block_view.LLMService.read", lambda x: FakeLLM(x))
    monkeypatch.setattr("API.views_def.block_view.BlockService.get_common_blocks", lambda a, b: [FakeBlock(1, "block1")])
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
    print("TEST GET BLOCK MISSING LLM")
    # Uno dei due LLM non esiste
    monkeypatch.setattr("API.views_def.block_view.LLMService.read", lambda x: None)
    url = "/question_blocks/?first_llm_id=1&second_llm_id=2"
    response = client.get(url)
    assert response.status_code == 400
    assert "error" in response.data

@pytest.mark.django_db
def test_get_block_no_common_blocks(monkeypatch, client):
    print("TEST GET BLOCK NO COMMON BLOCKS")
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

@pytest.mark.django_db
def test_put_block_success(monkeypatch, client):
    print("TEST PUT BLOCK SUCCESS")
    # Fake service che simula update
    class FakeService:
        @staticmethod
        def update(instance_id, data):
            # Simula update, restituisce i dati aggiornati
            return {"id": instance_id, "name": data["name"], "prompt": data.get("prompt", [])}

        @staticmethod
        def read(instance_id):
            # Simula lettura dopo update
            return {"id": instance_id, "name": "block1", "prompt": []}

    monkeypatch.setattr(BlockView, "service", FakeService)
    monkeypatch.setattr(BlockView, "serializer", BlockView.serializer)

    data = {"name": "block1", "prompt": []}
    response = client.put("/question_blocks/1/", data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "block1"
    assert response.data["prompt"] == []

@pytest.mark.django_db
def test_delete_block_success(monkeypatch, client):
    print("TEST DELETE BLOCK SUCCESS")
    # Fake service che simula delete
    class FakeService:
        @staticmethod
        def delete(instance_id):
            # Simula cancellazione senza errori
            return None

    monkeypatch.setattr(BlockView, "service", FakeService)

    response = client.delete("/question_blocks/1/")
    assert response.status_code == status.HTTP_204_NO_CONTENT

@pytest.mark.django_db
def test_put_block_exception(monkeypatch, client):
    print("TEST PUT BLOCK EXCEPTION")
    # Fake service che solleva eccezione su update
    class FakeService:
        @staticmethod
        def update(instance_id, data):
            raise Exception("Errore finto update")

    monkeypatch.setattr(BlockView, "service", FakeService)
    monkeypatch.setattr(BlockView, "serializer", BlockView.serializer)

    data = {"name": "block1", "prompt": []}
    response = client.put("/question_blocks/1/", data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data
    assert response.data["error"] == "Errore finto update"

@pytest.mark.django_db
def test_put_block_invalid_serializer(monkeypatch, client):
    # Fake serializer che non è valido
    class FakeSerializer:
        def __init__(self, *args, **kwargs):
            self.errors = {"name": ["Questo campo è obbligatorio."]}
            self.validated_data = {}
        def is_valid(self):
            return False

    class FakeService:
        @staticmethod
        def update(instance_id, data):
            return None

    monkeypatch.setattr(BlockView, "service", FakeService)
    monkeypatch.setattr(BlockView, "serializer", FakeSerializer)

    data = {}  # dati non validi
    response = client.put("/question_blocks/1/", data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "name" in response.data  # controlla che ci sia l'errore del serializer

@pytest.mark.django_db
def test_delete_block_exception(monkeypatch, client):
    # Fake service che solleva eccezione su delete
    class FakeService:
        @staticmethod
        def delete(instance_id):
            raise Exception("Errore finto delete")

    monkeypatch.setattr(BlockView, "service", FakeService)

    response = client.delete("/question_blocks/1/")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data
    assert response.data["error"] == "Errore finto delete"