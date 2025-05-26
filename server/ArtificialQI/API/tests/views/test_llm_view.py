import sys
sys.path.append("C:/Users/Alessandro/OneDrive/Desktop/progetto swe/ArtificialQI/server")
import pytest
from rest_framework.test import APIClient
from rest_framework import status
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ArtificialQI.settings")

@pytest.fixture
def client():
    return APIClient()

from API.views_def.llm_view import LLMView

# --- GET ALL ---
@pytest.mark.django_db
def test_llm_get_all_success(client):
    class FakeService:
        @staticmethod
        def read_all():
            return [{"id": 1, "name": "GPT-4", "n_parameters": "1T"}]
    class FakeSerializer:
        def __init__(self, data, many=False):
            self._data = data
        @property
        def data(self):
            return self._data
    LLMView.service = FakeService
    LLMView.serializer = FakeSerializer
    response = client.get("/llm_list/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)

@pytest.mark.django_db
def test_llm_get_all_exception(client):
    class FakeService:
        @staticmethod
        def read_all():
            raise Exception("Errore finto get all")
    class FakeSerializer:
        def __init__(self, data, many=False):
            self._data = data
        @property
        def data(self):
            return self._data
    LLMView.service = FakeService
    LLMView.serializer = FakeSerializer
    response = client.get("/llm_list/")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data

# --- GET BY ID ---
@pytest.mark.django_db
def test_llm_get_by_id_success(client):
    class FakeService:
        @staticmethod
        def read(instance_id):
            return {"id": instance_id, "name": "GPT-4", "n_parameters": "1T"}
    class FakeSerializer:
        def __init__(self, data, many=False):
            self._data = data
        @property
        def data(self):
            return self._data
    LLMView.service = FakeService
    LLMView.serializer = FakeSerializer
    response = client.get("/llm_list/1/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "GPT-4"

@pytest.mark.django_db
def test_llm_get_by_id_exception(client):
    class FakeService:
        @staticmethod
        def read(instance_id):
            raise Exception("Errore finto get by id")
    class FakeSerializer:
        def __init__(self, data, many=False):
            self._data = data
        @property
        def data(self):
            return self._data
    LLMView.service = FakeService
    LLMView.serializer = FakeSerializer
    response = client.get("/llm_list/1/")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data

# --- POST ---
@pytest.mark.django_db
def test_llm_post_success(client):
    class FakeSerializer:
        def __init__(self, data, many=False):
            self._data = data
            self.validated_data = data
            self.errors = {}
        def is_valid(self):
            return True
        @property
        def data(self):
            return self._data
    class FakeService:
        @staticmethod
        def create(data):
            return data
    LLMView.service = FakeService
    LLMView.serializer = FakeSerializer
    payload = {"name": "NuovoLLM", "n_parameters": "500B"}
    response = client.post("/llm_list/", data=payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "NuovoLLM"

@pytest.mark.django_db
def test_llm_post_invalid_serializer(client):
    class FakeSerializer:
        def __init__(self, data, many=False):
            self._data = data
            self.errors = {"name": ["Questo campo è obbligatorio."]}
        def is_valid(self):
            return False
        @property
        def data(self):
            return self._data
    LLMView.serializer = FakeSerializer
    payload = {}
    response = client.post("/llm_list/", data=payload, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "name" in response.data

@pytest.mark.django_db
def test_llm_post_exception(client):
    class FakeSerializer:
        def __init__(self, data, many=False):
            self._data = data
            self.validated_data = data
            self.errors = {}
        def is_valid(self):
            return True
        @property
        def data(self):
            return self._data
    class FakeService:
        @staticmethod
        def create(data):
            raise Exception("Errore finto post")
    LLMView.service = FakeService
    LLMView.serializer = FakeSerializer
    payload = {"name": "NuovoLLM", "n_parameters": "500B"}
    response = client.post("/llm_list/", data=payload, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data

# --- PUT ---
@pytest.mark.django_db
def test_llm_put_success(client):
    class FakeSerializer:
        def __init__(self, instance=None, data=None, many=False):
            self._data = data or instance
            self.validated_data = data or instance
            self.errors = {}
        def is_valid(self):
            return True
        @property
        def data(self):
            return self._data
    class FakeService:
        @staticmethod
        def update(instance_id, data):
            return data
        @staticmethod
        def read(instance_id):
            return {"id": instance_id, "name": "LLM Updated", "n_parameters": "1.2T"}
    LLMView.service = FakeService
    LLMView.serializer = FakeSerializer
    payload = {"name": "LLM Updated", "n_parameters": "1.2T"}
    response = client.put("/llm_list/1/", data=payload, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "LLM Updated"

@pytest.mark.django_db
def test_llm_put_invalid_serializer(client):
    class FakeSerializer:
        def __init__(self, instance=None, data=None, many=False):
            self._data = data or instance
            self.errors = {"name": ["Questo campo è obbligatorio."]}
        def is_valid(self):
            return False
        @property
        def data(self):
            return self._data
    class FakeService:
        @staticmethod
        def update(instance_id, data):
            return data
        @staticmethod
        def read(instance_id):
            return {"id": instance_id, "name": "LLM Updated", "n_parameters": "1.2T"}
    LLMView.service = FakeService
    LLMView.serializer = FakeSerializer
    payload = {}
    response = client.put("/llm_list/1/", data=payload, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "name" in response.data

@pytest.mark.django_db
def test_llm_put_exception(client):
    class FakeSerializer:
        def __init__(self, instance=None, data=None, many=False):
            self._data = data or instance
            self.validated_data = data or instance
            self.errors = {}
        def is_valid(self):
            return True
        @property
        def data(self):
            return self._data
    class FakeService:
        @staticmethod
        def update(instance_id, data):
            raise Exception("Errore finto put")
        @staticmethod
        def read(instance_id):
            return {"id": instance_id, "name": "LLM Updated", "n_parameters": "1.2T"}
    LLMView.service = FakeService
    LLMView.serializer = FakeSerializer
    payload = {"name": "LLM Updated", "n_parameters": "1.2T"}
    response = client.put("/llm_list/1/", data=payload, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data
    
# --- DELETE ---
@pytest.mark.django_db
def test_llm_delete_success(client):
    class FakeService:
        @staticmethod
        def delete(instance_id):
            return None
    LLMView.service = FakeService
    response = client.delete("/llm_list/1/")
    assert response.status_code == status.HTTP_204_NO_CONTENT

@pytest.mark.django_db
def test_llm_delete_exception(client):
    class FakeService:
        @staticmethod
        def delete(instance_id):
            raise Exception("Errore finto delete")
    LLMView.service = FakeService
    response = client.delete("/llm_list/1/")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data