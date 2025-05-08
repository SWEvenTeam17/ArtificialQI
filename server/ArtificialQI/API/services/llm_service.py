"""
File che contiene i servizi riguardanti i LLM.
"""

import os
import requests
from dotenv import load_dotenv
from API.repositories import LLMRepository
from .abstract_service import AbstractService
from itertools import chain


class LLMService(AbstractService):
    """
    Classe che contiene i servizi riguardanti i LLM.
    """

    repository = LLMRepository

    @staticmethod
    def fetch_ollama_models():
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
        models = cls.fetch_ollama_models()
        for model in models:
            name = model["name"]
            size = model["details"]["parameter_size"]
            cls.repository.update_or_create(name=name, parameters=size)

    @classmethod
    def compare_llms(cls, first_llm_id: int, second_llm_id: int, session_id: int):

        first_llm_tests = cls.repository.get_previous_tests(llm_id=first_llm_id, session_id=session_id)
        second_llm_tests = cls.repository.get_previous_tests(llm_id=second_llm_id, session_id=session_id)
        merged_tests = first_llm_tests.union(second_llm_tests)
        common_prompt_ids = set([x.prompt_id for x in first_llm_tests]).intersection(set([x.prompt_id for x in second_llm_tests]))
        common_tests = []
        for x in merged_tests:
            if x.prompt_id in common_prompt_ids:
                common_tests.append(x)
        return common_tests



    



