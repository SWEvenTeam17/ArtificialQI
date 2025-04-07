from API.repositories import LLMRepository
import os, requests
from rest_framework.response import Response
from rest_framework import status
from dotenv import load_dotenv

class LLMService:
    @staticmethod
    def fetch_ollama_models():
        load_dotenv()
        url = os.getenv("OLLAMA_URL")+"/api/tags"
        return requests.get(url).json().get("models", [])

    @staticmethod
    def sync_ollama_llms():
        models = LLMService.fetch_ollama_models()
        for model in models:
            name = model.get("name")
            size = model.get("details", {}).get("parameter_size")
            LLMRepository.update_or_create(name=name, parameters=size)
        return Response(
            {"message": "LLM models loaded successfully from Ollama server"},
            status=status.HTTP_200_OK,
        )