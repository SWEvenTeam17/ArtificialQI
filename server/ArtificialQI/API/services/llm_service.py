import os, requests
from rest_framework.response import Response
from rest_framework import status
from dotenv import load_dotenv
from .abstract_service import AbstractService
from API.repositories import LLMRepository


class LLMService(AbstractService):

    repository = LLMRepository

    def fetch_ollama_models():
        load_dotenv()
        url = os.getenv("OLLAMA_URL") + "/api/tags"
        return requests.get(url).json().get("models", [])

    @classmethod
    def sync_ollama_llms(cls) -> None:
        models = LLMService.fetch_ollama_models()
        for model in models:
            name = model.get("name")
            size = model.get("details", {}).get("parameter_size")
            cls.repository.update_or_create(name=name, parameters=size)
