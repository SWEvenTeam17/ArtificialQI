from abc import ABC, abstractmethod
from django.test import TestCase

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
        self.assertIsNotNone(instance.pk)
        original_data = self.valid_data
        for field, value in original_data.items():
            self.assertEqual(getattr(instance, field), value)

    def test_get_all(self):
        self.repository.create(self.valid_data)
        results = self.repository.get_all()
        self.assertGreaterEqual(len(results), 1)
        for field, value in self.valid_data.items():
            self.assertEqual(getattr(results[0], field), value)

    def test_get_by_id(self):
        instance = self.repository.create(self.valid_data)
        retrieved = self.repository.get_by_id(instance.pk)
        self.assertEqual(retrieved.pk, instance.pk)

    def test_update(self):
        instance = self.repository.create(self.valid_data)
        updated = self.repository.update(instance.pk, {"LLM_answer": "Updated Answer"})
        self.assertEqual(updated.LLM_answer, "Updated Answer")

    def test_delete(self):
        instance = self.repository.create(self.valid_data)
        result = self.repository.delete(instance.pk)
        self.assertTrue(result)
        self.assertIsNone(self.repository.get_by_id(instance.pk))