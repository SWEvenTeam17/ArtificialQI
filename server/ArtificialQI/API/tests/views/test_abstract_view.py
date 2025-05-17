from rest_framework.test import APIRequestFactory
from rest_framework import status
from API.views_def.abstract_view import AbstractView

class DummySerializer:
    def __init__(self, data=None, many=False):
        self.data = data
        self.validated_data = data
        self.errors = {}
        self._is_valid = True

    def is_valid(self):
        return True

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