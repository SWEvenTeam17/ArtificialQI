from typing import List
import requests, os
from statistics import mean
from collections import defaultdict
from dotenv import load_dotenv
from API.repositories import TestRepository, SessionRepository, BlockRepository
from API.models import Session, Prompt, Block, LLM, Evaluation
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
        load_dotenv()
        url = os.getenv("LLM_SERVICE_URL") + "interrogate/"
        return requests.post(url, {"llm_name": llm_name, "prompt": prompt}).json().get("answer")

    @staticmethod
    def runtest(session: Session, blocks: List[Block]):
        llms: List[LLM] = SessionRepository.get_llms(session=session)
        full_results = []

        for block in blocks:
            prompts: List[Prompt] = BlockRepository.get_prompts(block=block)
            TestService.create({"session": session, "block": block})

            block_results = []
            scores = defaultdict(lambda: {"semantic": [], "external": []})

            for prompt in prompts:
                for llm in llms:
                    output = TestService.interrogate(llm.name, prompt.prompt_text)

                    semantic_eval = LLMController.get_semantic_evaluation(prompt.expected_answer, output)
                    external_eval = LLMController.get_external_evaluation("google", prompt.expected_answer, output)

                    scores[llm.name]["semantic"].append(semantic_eval)
                    scores[llm.name]["external"].append(external_eval)

                    evaluation: Evaluation = EvaluationService.create({
                        "semantic_evaluation": semantic_eval,
                        "external_evaluation": external_eval
                    })

                    RunService.create({
                        "llm": llm,
                        "prompt": prompt,
                        "evaluation": evaluation,
                        "llm_answer": output
                    })

                    block_results.append({
                        "llm_name": llm.name,
                        "question": prompt.prompt_text,
                        "expected_answer": prompt.expected_answer,
                        "answer": output,
                        "semantic_evaluation": semantic_eval,
                        "external_evaluation": external_eval,
                    })
            averages = {}
            for llm_name, score_list in scores.items():
                semantic_scores = [float(s) for s in score_list["semantic"]]
                external_scores = [float(e) for e in score_list["external"]]

                avg_semantic_scores = mean(semantic_scores) if semantic_scores else None
                avg_external_scores = mean(external_scores) if external_scores else None

                averages[llm_name] = {
                    "avg_semantic_scores": avg_semantic_scores,
                    "avg_external_scores": avg_external_scores
                }

            full_results.append({
                "block_id": block.id,
                "block_name": block.name,
                "results": block_results,
                "averages_by_llm": averages
            })

        return {
            "results": full_results
        }
