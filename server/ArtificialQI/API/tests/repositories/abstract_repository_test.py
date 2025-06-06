import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ArtificialQI.settings")
django.setup()
from abc import ABC, abstractmethod

import pytest


@pytest.mark.django_db
class TestAbstractRepository(ABC):

    @pytest.fixture
    @abstractmethod
    def repository(self):
        """Restituisce il repository che si sta testando"""
        pass

    @pytest.fixture
    @abstractmethod
    def valid_data(self):
        """Restituisce i dati validi per il test"""
        pass

    def test_create(self, repository, valid_data):
        instance = repository.create(valid_data)
        assert instance.pk is not None
        for field, value in valid_data.items():
            assert getattr(instance, field) == value

    def test_get_all(self, repository, valid_data):
        repository.create(valid_data)
        results = repository.get_all()
        assert len(results) >= 1, "Lista vuota"
        record_found = False
        for record in results:
            if all(
                getattr(record, field) == value for field, value in valid_data.items()
            ):
                record_found = True
            break
        assert record_found is True

    def test_get_by_id(self, repository, valid_data):
        instance = repository.create(valid_data)
        retrieved = repository.get_by_id(instance.pk)
        assert retrieved.pk == instance.pk

    def test_update(self, repository, valid_data, update_data):
        instance = repository.create(valid_data)
        updated = repository.update(instance.pk, update_data)
        for field, value in update_data.items():
            assert getattr(updated, field) == value

    def test_delete(self, repository, valid_data):
        instance = repository.create(valid_data)
        result = repository.delete(instance.pk)
        assert result is True
        assert repository.get_by_id(instance.pk) is None
