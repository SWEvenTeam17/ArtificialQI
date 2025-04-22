"""
File che contiene i servizi riguardanti i LLM.
"""
import os
import requests
from dotenv import load_dotenv
from API.repositories import LLMRepository
from .abstract_service import AbstractService


class LLMService(AbstractService):
    """
    Classe che contiene i servizi riguardanti i LLM.
    """

    repository = LLMRepository

    def fetch_ollama_models():
        """
        Funzione che esegue un fetch di tutti i modelli installati su Ollama.
        """
        load_dotenv()
        url = os.getenv("OLLAMA_URL") + "/api/tags"
        return requests.get(url).json().get("models", [])

    @classmethod
    def sync_ollama_llms(cls) -> None:
        """
        Funzione che aggiunge tutti i LLM di Ollama in DB.
        """
        models = LLMService.fetch_ollama_models()
        for model in models:
            name = model.get("name")
            size = model.get("details", {}).get("parameter_size")
            cls.repository.update_or_create(name=name, parameters=size)
