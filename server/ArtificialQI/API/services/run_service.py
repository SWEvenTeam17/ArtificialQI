"""
File che contiene i servizi riguardanti i prompt.
"""

from API.repositories import RunRepository, AbstractRepository, PromptRepository
from API.models import Prompt
from .abstract_service import AbstractService
from typing import ClassVar


class RunService(AbstractService):
    """
    Classe che contiene i servizi riguardanti i prompt.
    """

    _repository: ClassVar[AbstractRepository] = RunRepository

    @classmethod
    def get_formatted_by_prompt(cls, prompt_id: int):
        """
        Ritorna i dati correttamente formattati per la visualizzazione dei
        dati di un prompt nel frontend.
        """
        runs = cls._repository.get_by_prompt(prompt_id=prompt_id)
        results = []
        scores = {}

        try:
            prompt: Prompt = PromptRepository.get_by_id(instance_id=prompt_id)
            blocks = list(prompt.block_set.all())
        except Prompt.DoesNotExist:
            return None

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

            results.append(
                {
                    "run_id": run.id,
                    "llm_name": llm_name,
                    "question": run.prompt.prompt_text,
                    "expected_answer": run.prompt.expected_answer,
                    "answer": run.llm_answer,
                    "semantic_evaluation": semantic_eval,
                    "external_evaluation": external_eval,
                }
            )

            scores[llm_name]["semantic_sum"] += semantic_eval
            scores[llm_name]["semantic_count"] += 1
            scores[llm_name]["external_sum"] += external_eval
            scores[llm_name]["external_count"] += 1

        averages = {
            llm_name: {
                "avg_semantic_scores": (
                    scores[llm_name]["semantic_sum"]
                    / scores[llm_name]["semantic_count"]
                    if scores[llm_name]["semantic_count"]
                    else None
                ),
                "avg_external_scores": (
                    scores[llm_name]["external_sum"]
                    / scores[llm_name]["external_count"]
                    if scores[llm_name]["external_count"]
                    else None
                ),
            }
            for llm_name in scores
        }

        return {
            "results": [
                {
                    "block_id": block.id,
                    "block_name": block.name,
                    "results": results,
                    "averages_by_llm": averages,
                }
                for block in blocks
            ]
        }
