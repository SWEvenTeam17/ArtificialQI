import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ArtificialQI.settings")
django.setup()
import sys

import pytest
from rest_framework import serializers, status
from rest_framework.test import APIRequestFactory

from API.views_def.abstract_view import AbstractView


class DummySerializer(serializers.Serializer):
    def to_internal_value(self, data):
        return data

    def to_representation(self, instance):
        return instance

    def is_valid(self, raise_exception=False):
        self._validated_data = self.initial_data
        return True

    @property
    def validated_data(self):
        return getattr(self, "_validated_data", self.initial_data)



class DummyService:
    @staticmethod
    def read_all():
        return [{"value": "data1"}, {"value": "data2"}]

    @staticmethod
    def read(instance_id):
        if instance_id is None:
            return None  
        return {"value": f"data{instance_id}"}

    @staticmethod
    def create(data):
        return data

    @staticmethod
    def update(instance_id, data):
        return data

    @staticmethod
    def delete(instance_id):
        if instance_id is None:
            return None
        return True



class DummyView(AbstractView):
    _serializer = DummySerializer
    _service = DummyService


factory = APIRequestFactory()


def test_get_all():
    view = DummyView.as_view()
    request = factory.get("/")
    response = view(request)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == [{"value": "data1"}, {"value": "data2"}]


def test_get_by_id():
    request = factory.get("/")
    response = DummyView().get(request, instance_id=1)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {"value": "data1"}


def test_get_by_id_as_view():
    view = DummyView.as_view()
    request = factory.get("/")
    response = view(request, instance_id=1)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {"value": "data1"}


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
    response = view(request)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data == {"error": "Istanza non trovata"}


def test_delete_without_instance_id():
    request = factory.delete("/")
    response = DummyView().delete(request)
    assert response.status_code == status.HTTP_204_NO_CONTENT




class InvalidSerializer(DummySerializer):
    def is_valid(self, raise_exception=False):
        return False

    @property
    def errors(self):
        return {"error": "invalid"}


class InvalidView(AbstractView):
    _serializer = InvalidSerializer
    _service = DummyService


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
    _serializer = DummySerializer
    _service = FailingService


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


class FailingGetService(DummyService):
    @staticmethod
    def read_all():
        raise Exception("Errore in read_all")

    @staticmethod
    def read(instance_id):
        raise Exception("Errore in read")


class FailingGetView(AbstractView):
    _serializer = DummySerializer
    _service = FailingGetService


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
