import os, requests
from requests.exceptions import RequestException
from dotenv import load_dotenv
from langchain_ollama import OllamaLLM
from typing import List, Dict, Any


class OllamaLLMIntegrationService:

    @staticmethod
    def get_llm(name: str) -> OllamaLLM | None:
        load_dotenv()
        try:
            response = requests.get(f"{os.getenv("OLLAMA_URL")}/api/version", timeout=5)
            response.raise_for_status()
            return OllamaLLM(model=name, base_url=os.getenv("OLLAMA_URL"))
        except RequestException:
            return None

    @staticmethod
    def interrogate(llm: OllamaLLM, prompt: str) -> str:
        stream = llm.stream(prompt)
        output = next(stream)
        for chunk in stream:
            output += chunk
        return output

    @staticmethod
    def get_ollama_llms() -> List[Dict[str, Any]]:
        load_dotenv()
        url = os.getenv("OLLAMA_URL") + "/api/tags"
        try:
            result = requests.get(url).json().get("models", [])
            return result
        except RequestException:
            return None
