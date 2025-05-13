from typing import List
import requests, os
from statistics import mean
from collections import defaultdict
from dotenv import load_dotenv
from API.repositories import TestRepository, SessionRepository, PromptRepository, BlockRepository
from API.models import Session, Prompt, Block
from API.classes.llm_controller import LLMController
from .abstract_service import AbstractService
from .prompt_service import PromptService
from .evaluation_service import EvaluationService

class TestService(AbstractService):
    """
    Classe che contiene tutti i servizi riguardanti i test.
    """

    repository = TestRepository

    @staticmethod
    def interrogate(llm_name: str, prompt: str)->str:
        load_dotenv()
        url = os.getenv("LLM_SERVICE_URL") +"interrogate/"
        return requests.post(url,{"llm_name":llm_name, "prompt":prompt}).json().get("answer")

    @staticmethod
    def runtest(data: List[dict], session: Session, block_name: str)->dict:
        prompts: List[Prompt] = []
        new_block: Block = BlockRepository.create({"name":block_name})
        llms = session.llm.all()
        results = []
        scores = defaultdict(lambda: {"semantic": [], "external": []})

        #aggiungo tutti i prompt ad una lista, se non esistono li creo in DB
        for x in data:
            #se non esiste
            if "id" not in x:
                existing_prompt = PromptRepository.filter_one(
                    prompt_text=x["prompt_text"],
                    expected_answer=x["expected_answer"],
                    session=session
                )
                if existing_prompt:
                    x["id"] = existing_prompt.id
                    prompts.append(existing_prompt)
                else:
                    save = {
                        "prompt_text": x["prompt_text"],
                        "expected_answer": x["expected_answer"],
                        "session": session,
                    }
                    saved_prompt = PromptService.create(save)
                    prompts.append(saved_prompt)
                    x["id"] = saved_prompt.id
            #se esiste
            else:
                prompts.append(PromptRepository.get_by_id(x["id"]))
        
        #aggiungo i prompt ad un blocco
        for prompt in prompts:
            if prompt not in new_block.prompt.all():
                BlockRepository.add_prompt(new_block, prompt)

        #ciclo tra i prompt, mando i dati ai LLM e chiedo le valutazioni per ogni prompt
        for prompt in prompts:
            for llm in llms:
                output = TestService.interrogate(llm.name, prompt.prompt_text)
                semantic_evaluation = LLMController.get_semantic_evaluation(prompt.expected_answer, output)
                external_evaluation = LLMController.get_external_evaluation(
                    "google", x["expected_answer"], output
                )
                scores[llm.name]["semantic"].append(semantic_evaluation)
                scores[llm.name]["external"].append(external_evaluation)
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
                        "block": new_block,
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
        #istanzio una lista per le medie e i punteggi
        averages={}
        #ciclo ogni score ottenuto, casto a float i valori e calcolo le medie, li inserisco in un dizionario sulla chiave llm_name 
        for llm_name, scores in scores.items():
            semantic_scores = [float(s) for s in scores["semantic"]]
            external_scores = [float(e) for e in scores["external"]]

            avg_semantic_scores = mean(semantic_scores) if semantic_scores else None
            avg_external_scores = mean(external_scores) if external_scores else None

            averages[llm_name] = {
                "avg_semantic_scores": avg_semantic_scores,
                "avg_external_scores": avg_external_scores
            }
        return {
            "results": results,
            "averages_by_llm": averages
            }
        

        

        