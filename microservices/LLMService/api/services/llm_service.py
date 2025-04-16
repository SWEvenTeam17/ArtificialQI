import os, requests
from requests.exceptions import RequestException
from dotenv import load_dotenv
from langchain_ollama import OllamaLLM


class LLMService:
    
    @staticmethod
    def get_llm(name: str)->OllamaLLM | ConnectionError:
        load_dotenv()
        try:
            response = requests.get(f"{os.getenv("OLLAMA_URL")}/api/version", timeout=5)
            response.raise_for_status()
            return OllamaLLM(model=name, base_url=os.getenv("OLLAMA_URL"))
        except RequestException as e:
            raise ConnectionError(f"Errore di connessione al server Ollama: {e}")
    
    @staticmethod
    def interrogate(llm: OllamaLLM, prompt: str)->str:
        stream = llm.stream(prompt)
        output = next(stream)
        for chunk in stream:
            output += chunk
        return output

