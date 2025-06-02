"""
File che contiene i servizi riguardanti i LLM.
"""

import os
import requests
from typing import ClassVar
from dotenv import load_dotenv
from API.repositories import LLMRepository, AbstractRepository
from .abstract_service import AbstractService


class LLMService(AbstractService):
    """
    Classe che contiene i servizi riguardanti i LLM.
    """

    _repository: ClassVar[AbstractRepository] = LLMRepository

    @staticmethod
    def __fetch_ollama_models():
        """
        Funzione che esegue un fetch di tutti i modelli installati su Ollama.
        """
        load_dotenv()
        url = os.getenv("LLM_SERVICE_URL") + "/interrogate/"
        return requests.get(url, timeout=5).json()

    @classmethod
    def sync_ollama_llms(cls) -> None:
        """
        Funzione che aggiunge tutti i LLM di Ollama in DB.
        """
        models = cls.__fetch_ollama_models()
        for model in models:
            name = model["name"]
            size = model["details"]["parameter_size"]
            cls._repository.update_or_create(name=name, parameters=size)
