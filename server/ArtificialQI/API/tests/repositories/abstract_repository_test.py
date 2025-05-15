import django
import os
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
        assert len(results) >= 1
        for field, value in valid_data.items():
            assert getattr(results[0], field) == value

    def test_get_by_id(self, repository, valid_data):
        instance = repository.create(valid_data)
        retrieved = repository.get_by_id(instance.pk)
        assert retrieved.pk == instance.pk

    def test_update(self, repository, valid_data):
        instance = repository.create(valid_data)
        updated = repository.update(instance.pk, {"LLM_answer": "Updated Answer"})
        assert updated.LLM_answer == "Updated Answer"

    def test_delete(self, repository, valid_data):
        instance = repository.create(valid_data)
        result = repository.delete(instance.pk)
        assert result is True
        assert repository.get_by_id(instance.pk) is None