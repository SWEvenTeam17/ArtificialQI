import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ArtificialQI.settings")
django.setup()
import pytest
from unittest.mock import MagicMock
from API.services.abstract_service import AbstractService

class AbstractServiceTestCase:
    service_class = None  # Deve essere sovrascritto
    mock_repository = None

    @pytest.fixture(autouse=True)
    def setup(self, mocker):
        self.mock_repository = mocker.MagicMock()
        self.service_class.repository = self.mock_repository

    def test_create(self):
        sample_data = {"key": "value"}
        self.mock_repository.create.return_value = {"id": 1, **sample_data}

        result = self.service_class.create(sample_data)

        assert result["id"] == 1
        self.mock_repository.create.assert_called_once_with(sample_data)

    def test_read(self):
        self.mock_repository.get_by_id.return_value = {"id": 1, "text": "ciao"}
        result = self.service_class.read(1)

        assert result["id"] == 1
        self.mock_repository.get_by_id.assert_called_once_with(id=1)

    def test_read_all(self):
        self.mock_repository.get_all.return_value = [{"id": 1}, {"id": 2}]
        result = self.service_class.read_all()

        assert len(result) == 2
        self.mock_repository.get_all.assert_called_once()

    def test_update(self):
        self.mock_repository.update.return_value = {"id": 1, "text": "aggiornato"}
        result = self.service_class.update(1, {"text": "aggiornato"})

        assert result["text"] == "aggiornato"
        self.mock_repository.update.assert_called_once_with(id=1, data={"text": "aggiornato"})

    def test_delete(self):
        self.mock_repository.delete.return_value = True
        result = self.service_class.delete(1)

        assert result is True
        self.mock_repository.delete.assert_called_once_with(id=1)
