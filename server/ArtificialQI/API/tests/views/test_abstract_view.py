from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework import serializers
from API.views_def.abstract_view import AbstractView
import pytest

# Dummy serializer base
class DummySerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        return validated_data

# Dummy service base
class DummyService:
    @staticmethod
    def read_all():
        return ["data1", "data2"]

    @staticmethod
    def read(instance_id):
        return f"data{instance_id}"

    @staticmethod
    def create(data):
        return data

    @staticmethod
    def update(instance_id, data):
        return data

    @staticmethod
    def delete(instance_id):
        return True

# Dummy view base
class DummyView(AbstractView):
    serializer = DummySerializer
    service = DummyService

factory = APIRequestFactory()

def test_get_all():
    view = DummyView.as_view()
    request = factory.get("/")
    response = view(request)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == ["data1", "data2"]

def test_get_by_id():
    request = factory.get("/")
    response = DummyView().get(request, instance_id=1)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == "data1"

def test_get_by_id_as_view():
    view = DummyView.as_view()
    request = factory.get("/")
    response = view(request, instance_id=1)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == "data1"

def test_post_valid():
    view = DummyView.as_view()
    request = factory.post("/", data={"key": "value"}, format="json")
    response = view(request)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == {"key": "value"}

def test_put_valid():
    view = DummyView.as_view()
    payload = {"key": "updated"}
    request = factory.put("/", data=payload, format="json")
    response = view(request, instance_id=1)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == payload

def test_delete():
    request = factory.delete("/")
    response = DummyView().delete(request, instance_id=1)
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_put_without_instance_id():
    view = DummyView.as_view()
    payload = {"key": "no id"}
    request = factory.put("/", data=payload, format="json")
    response = view(request)  # nessun instance_id
    assert response.status_code == status.HTTP_200_OK
    assert response.data == payload

def test_delete_without_instance_id():
    request = factory.delete("/")
    response = DummyView().delete(request)  # nessun instance_id
    assert response.status_code == status.HTTP_204_NO_CONTENT


# --- ERROR CASES ---

# Serializer non valido
class InvalidSerializer(DummySerializer):
    def __init__(self, data=None, many=False):
        super().__init__(data, many)
        self._is_valid = False
        self.errors = {"error": "invalid"}

class InvalidView(AbstractView):
    serializer = InvalidSerializer
    service = DummyService

def test_post_invalid_serializer():
    view = InvalidView.as_view()
    request = factory.post("/", data={"key": "value"}, format="json")
    response = view(request)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data

def test_put_invalid_serializer():
    view = InvalidView.as_view()
    request = factory.put("/", data={"key": "value"}, format="json")
    response = view(request, instance_id=1)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data

# Service che solleva eccezione
class FailingService(DummyService):
    @staticmethod
    def create(data):
        raise Exception("Errore di creazione")

    @staticmethod
    def update(instance_id, data):
        raise Exception("Errore di update")

    @staticmethod
    def delete(instance_id):
        raise Exception("Errore di delete")

class FailingView(AbstractView):
    serializer = DummySerializer
    service = FailingService

def test_post_service_exception():
    view = FailingView.as_view()
    request = factory.post("/", data={"key": "value"}, format="json")
    response = view(request)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data

def test_put_service_exception():
    view = FailingView.as_view()
    request = factory.put("/", data={"key": "value"}, format="json")
    response = view(request, instance_id=1)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data

def test_delete_service_exception():
    request = factory.delete("/")
    response = FailingView().delete(request, instance_id=1)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data


# Service che solleva eccezione in read_all e read
class FailingGetService(DummyService):
    @staticmethod
    def read_all():
        raise Exception("Errore in read_all")

    @staticmethod
    def read(instance_id):
        raise Exception("Errore in read")

class FailingGetView(AbstractView):
    serializer = DummySerializer
    service = FailingGetService

def test_get_all_exception():
    view = FailingGetView.as_view()
    request = factory.get("/")
    response = view(request)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data

def test_get_by_id_exception():
    request = factory.get("/")
    response = FailingGetView().get(request, instance_id=1)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data
