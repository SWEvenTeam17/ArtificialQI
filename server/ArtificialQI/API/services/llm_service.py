"""
File che contiene i servizi riguardanti i LLM.
"""

import os
import requests
from dotenv import load_dotenv
from API.repositories import LLMRepository
from API.models import Test
from typing import List, Dict
from .abstract_service import AbstractService
from itertools import chain
from django.db.models import Avg


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
    def calculate_avg_evaluation(cls, tests: List[Test])->Dict[str,float]:
        if len(tests) == 0:
            return {"semantic_average": 0, "external_average":0}
        semantic_sum: float = 0
        external_sum: float = 0

        for x in tests:
            semantic_sum = semantic_sum + x.evaluation.semantic_evaluation
            external_sum = external_sum + x.evaluation.external_evaluation
        return {"semantic_average": semantic_sum/len(tests), "external_average":external_sum/len(tests)}

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
        
        return {"common_tests":common_tests, "first_llm_averages":cls.calculate_avg_evaluation(first_llm_tests), "second_llm_averages":cls.calculate_avg_evaluation(second_llm_tests)}
        
    @classmethod
    def compare_prompts(cls, llm_id: int, session_id: int):
        llm_tests = cls.repository.get_previous_tests(llm_id=llm_id, session_id=session_id)
        return {"tests": llm_tests, "averages":cls.calculate_avg_evaluation(llm_tests)}
        