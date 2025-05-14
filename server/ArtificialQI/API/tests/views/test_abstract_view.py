from unittest import TestCase
from unittest.mock import MagicMock, patch
from rest_framework.test import APIRequestFactory
from rest_framework import status
from django.http import HttpRequest
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
        return data  # ritorna direttamente i dati aggiornati

    @staticmethod
    def delete(instance_id):
        return True



class DummyView(AbstractView):
    serializer = DummySerializer
    service = DummyService


class AbstractViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = DummyView.as_view()

    def test_get_all(self):
        request = self.factory.get("/")
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, ["data1", "data2"])

    def test_get_by_id(self):
        request = self.factory.get("/")
        response = DummyView().get(request, instance_id=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "data1")

    def test_post_valid(self):
        request = self.factory.post("/", data={"key": "value"}, format="json")
        view = DummyView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {"key": "value"})

    def test_put_valid(self):
        payload = {"key": "updated"}
        request = self.factory.put("/", data=payload, format="json")
        view = DummyView.as_view()
        response = view(request, instance_id=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, payload)

    def test_delete(self):
        request = self.factory.delete("/")
        response = DummyView().delete(request, instance_id=1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

print("Total methods:", [method for method in dir(AbstractViewTest) if method.startswith("test_")])

