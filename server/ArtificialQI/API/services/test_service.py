"""
File che contiene i servizi riguardanti i test.
"""

from typing import List
import requests, os
from dotenv import load_dotenv
from API.repositories import TestRepository
from API.models import Session
from API.classes.llm_controller import LLMController
from .abstract_service import AbstractService
from .prompt_service import PromptService
from .evaluation_service import EvaluationService


class TestService(AbstractService):
    """
    Classe che contiene i servizi riguardanti i test.
    """

    repository = TestRepository

    @staticmethod
    def runtest(data: List[dict], session: Session):
        """
        Funzione che gestisce le chiamate dei vari helper per fare i test.
        """
        TestService.save_data(data=data, session=session)
        llms = session.llm.all()
        return TestService.evaluate(llms, data)

    @staticmethod
    def save_data(data: List[dict], session: Session) -> None:
        """
        Funzione che controlla i dati e salva eventuali domande
        non ancora registrate in DB.
        """
        for x in data:
            if "id" not in x:
                save = {
                    "prompt_text": x["prompt_text"],
                    "expected_answer": x["expected_answer"],
                    "session": session,
                }
                saved_prompt = PromptService.create(save)
                x["id"] = saved_prompt.id

    @staticmethod
    def evaluate(llms: List[dict], data: List[dict]) -> List[dict]:
        """
        Funzione che chiama le funzioni dedicate alle valutazioni, salva
        i dati e ritorna i risultati.
        """
        results = []
        for x in data:
            prompt = PromptService.read(instance_id=x["id"])
            for llm in llms:
                output = TestService.interrogate(llm.name, prompt.prompt_text)
                semantic_evaluation = LLMController.get_semantic_evaluation(
                    x["expected_answer"], output
                )
                external_evaluation = LLMController.get_external_evaluation(
                    "google", x["expected_answer"], output
                )
                evaluation = EvaluationService.create(
                    {
                        "prompt": prompt,
                        "semantic_evaluation": semantic_evaluation,
                        "external_evaluation": external_evaluation,
                    }
                )
                TestService.create(
                    {
                        "session": prompt.session,
                        "prompt": prompt,
                        "llm": llm,
                        "evaluation": evaluation,
                    }
                )
                results.append(
                    {
                        "llm_name": llm.name,
                        "question": prompt.prompt_text,
                        "expected_answer": x["expected_answer"],
                        "answer": output,
                        "semantic_evaluation": semantic_evaluation,
                        "external_evaluation": external_evaluation,
                    }
                )
        return results

    @staticmethod
    def get_formatted(request):
        """
        Funzione che formatta i dati in maniera corretta per l'esecuzione
        del test
        """
        data = request.data.get("data")
        ret = []
        for x in data:
            if "id" in x and x["id"] is not None:
                ret.append(
                    {
                        "id": x["id"],
                        "prompt_text": x["prompt_text"],
                        "expected_answer": x["expected_answer"],
                    }
                )
            else:
                ret.append(
                    {
                        "prompt_text": x["prompt_text"],
                        "expected_answer": x["expected_answer"],
                    }
                )
        return ret

    @staticmethod
    def get_data(request):
        """
        Funzione che ritorna i dati necessari all'esecuzione
        del test
        """
        session = Session.objects.get(id=request.data.get("sessionId"))
        return TestService.get_formatted(request), session
    
    def interrogate(llm_name: str, prompt: str)->str:
        load_dotenv()
        url = os.getenv("LLM_SERVICE_URL") +"interrogate/"
        return requests.post(url,{"llm_name":llm_name, "prompt":prompt}).json().get("answer")
