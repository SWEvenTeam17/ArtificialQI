"""
File che contiene le funzioni utili a gestire
la logica di business quando si esegue un test.
"""

from typing import List, Dict
import os
from collections import defaultdict
import requests
from dotenv import load_dotenv
from API.repositories import TestRepository, SessionRepository, BlockRepository
from API.models import Session, Block, Test
from API.classes.llm_controller import LLMController
from .abstract_service import AbstractService
from .evaluation_service import EvaluationService
from .run_service import RunService


class TestService(AbstractService):
    """
    Classe che contiene tutti i servizi riguardanti i test.
    """

    repository = TestRepository

    @staticmethod
    def interrogate(llm_name: str, prompt: str) -> str:
        """
        Funzione che chiama il microservizio dedicato all'integrazione con Ollama.
        invia una domanda e riceve una risposta.
        """
        load_dotenv()
        url = os.getenv("LLM_SERVICE_URL") + "interrogate/"
        return (
            requests.post(url, {"llm_name": llm_name, "prompt": prompt})
            .json()
            .get("answer")
        )

    @staticmethod
    def runtest(session: Session, blocks: List[Block]) -> Dict[str, any]:
        """
        Funzione che esegue un test, prende come parametri una sessione
        e una lista di domande (un blocco).
        Ritorna un dizionario contenente informazioni essenziali
        alla rappresentazione dei risultati.
        """
        llms = SessionRepository.get_llms(session=session)
        block_map = {}
        all_prompts = []

        for block in blocks:
            prompts = BlockRepository.get_prompts(block=block)
            test = TestService.create({"session": session, "block": block})
            block_map[block.id] = {
                "name": block.name,
                "test": test,
                "results": [],
                "scores": defaultdict(
                    lambda: {
                        "semantic_sum": 0.0,
                        "semantic_count": 0,
                        "external_sum": 0.0,
                        "external_count": 0,
                    }
                ),
            }
            all_prompts.extend((block.id, prompt) for prompt in prompts)

        for llm in llms:
            for block_id, prompt in all_prompts:
                output = TestService.interrogate(llm.name, prompt.prompt_text)
                semantic_eval = float(
                    LLMController.get_semantic_evaluation(
                        prompt.expected_answer, output
                    )
                )
                external_eval = float(
                    LLMController.get_external_evaluation(
                        "google", prompt.expected_answer, output
                    )
                )

                evaluation = EvaluationService.create(
                    {
                        "semantic_evaluation": semantic_eval,
                        "external_evaluation": external_eval,
                    }
                )

                run = RunService.create(
                    {
                        "llm": llm,
                        "prompt": prompt,
                        "evaluation": evaluation,
                        "llm_answer": output,
                    }
                )

                TestRepository.add_run(block_map[block_id]["test"], run)

                block_map[block_id]["results"].append(
                    {
                        "run_id": run.id,
                        "llm_name": llm.name,
                        "question": prompt.prompt_text,
                        "expected_answer": prompt.expected_answer,
                        "answer": output,
                        "semantic_evaluation": semantic_eval,
                        "external_evaluation": external_eval,
                    }
                )

                scores = block_map[block_id]["scores"][llm.name]
                scores["semantic_sum"] += semantic_eval
                scores["semantic_count"] += 1
                scores["external_sum"] += external_eval
                scores["external_count"] += 1

        full_results = []
        for block_id, data in block_map.items():
            averages = {
                llm_name: {
                    "avg_semantic_scores": (
                        (sc["semantic_sum"] / sc["semantic_count"])
                        if sc["semantic_count"]
                        else None
                    ),
                    "avg_external_scores": (
                        (sc["external_sum"] / sc["external_count"])
                        if sc["external_count"]
                        else None
                    ),
                }
                for llm_name, sc in data["scores"].items()
            }
            full_results.append(
                {
                    "block_id": block_id,
                    "block_name": data["name"],
                    "results": data["results"],
                    "averages_by_llm": averages,
                }
            )

        return {"results": full_results}
    
    @staticmethod
    def format_results(test: Test) -> Dict[str, any]:
        block = test.block
        runs = test.run.all().select_related("llm", "prompt", "evaluation")
        results = []
        scores = {}

        for run in runs:
            llm_name = run.llm.name
            if llm_name not in scores:
                scores[llm_name] = {
                    "semantic_sum": 0.0,
                    "semantic_count": 0,
                    "external_sum": 0.0,
                    "external_count": 0,
                }
            semantic_eval = float(run.evaluation.semantic_evaluation)
            external_eval = float(run.evaluation.external_evaluation)

            results.append({
                "run_id": run.id,
                "llm_name": llm_name,
                "question": run.prompt.prompt_text,
                "expected_answer": run.prompt.expected_answer,
                "answer": run.llm_answer,
                "semantic_evaluation": semantic_eval,
                "external_evaluation": external_eval,
            })

            scores[llm_name]["semantic_sum"] += semantic_eval
            scores[llm_name]["semantic_count"] += 1
            scores[llm_name]["external_sum"] += external_eval
            scores[llm_name]["external_count"] += 1

        averages = {
            llm_name: {
                "avg_semantic_scores": (
                    scores[llm_name]["semantic_sum"] / scores[llm_name]["semantic_count"]
                    if scores[llm_name]["semantic_count"] else None
                ),
                "avg_external_scores": (
                    scores[llm_name]["external_sum"] / scores[llm_name]["external_count"]
                    if scores[llm_name]["external_count"] else None
                ),
            }
            for llm_name in scores
        }

        return {
            "results": [{
                "block_id": block.id,
                "block_name": block.name,
                "results": results,
                "averages_by_llm": averages,
            }]
        }

