import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ArtificialQI.settings")
django.setup()
from abc import ABC, abstractmethod

import pytest

class AbstractRepository(ABC):
    
    @property
    @abstractmethod
    def repository(self):
        """Restituisce il repository che si sta testando"""
        pass
    
    @property
    @abstractmethod
    def valid_data(self):
        """Restituisce i dati validi per il test"""
        pass

    def test_create(self):
        instance = self.repository.create(self.valid_data)
        assert instance.pk is not None
        original_data = self.valid_data
        for field, value in original_data.items():
            assert getattr(instance, field) == value

    def test_get_all(self):
        self.repository.create(self.valid_data)
        results = self.repository.get_all()
        self.assertGreaterEqual(len(results), 1)
        for field, value in self.valid_data.items():
            assert getattr(results[0], field) == value

    def test_get_by_id(self):
        instance = self.repository.create(self.valid_data)
        retrieved = self.repository.get_by_id(instance.pk)
        assert retrieved.pk == instance.pk

    def test_update(self):
        instance = self.repository.create(self.valid_data)
        updated = self.repository.update(instance.pk, {"LLM_answer": "Updated Answer"})
        assert updated.LLM_answer == "Updated Answer"

    def test_delete(self):
        instance = self.repository.create(self.valid_data)
        result = self.repository.delete(instance.pk)
        assert result is True
        assert self.repository.get_by_id(instance.pk) is None