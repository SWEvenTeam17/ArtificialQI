from .abstract_service import AbstractService
from API.repositories import TestRepository
from .prompt_service import PromptService
from .evaluation_service import EvaluationService
from typing import List
from API.models import Session
from API.classes.llm_controller import LLMController

class TestService(AbstractService):
    repository = TestRepository

    def runtest(data: List[dict], session: Session):
        TestService.save_data(data=data, session=session)
        llms = session.llm.all()
        return TestService.evaluate(llms, data)
        
    def save_data(data: List[dict], session: Session)->None:
        for x in data:
            if "id" not in x:
                save = {
                    "prompt_text": x["prompt_text"],
                    "expected_answer": x["expected_answer"],
                    "session": session.id,
                }
                saved_prompt = PromptService.create(save)
                x["id"] = saved_prompt.id
        return
    
    def evaluate(llms: List[dict], data: List[dict])->List[dict]:
        results = []
        for x in data:
            prompt = PromptService.read(id=x["id"])
            for llm in llms:
                llm_obj = LLMController(llm.name)
                output = llm_obj.get_answer(prompt.prompt_text)
                semantic_evaluation = LLMController.get_semantic_evaluation(x["expected_answer"], output)
                external_evaluation = LLMController.get_external_evaluation("google", x["expected_answer", output])
                EvaluationService.create({"prompt":prompt.id, "llm":llm.id, "semantic_evaluation":semantic_evaluation, "external_evaluation":external_evaluation})
                results.append(
                {
                    "llm_name": llm.name,
                    "question": prompt.prompt_text,
                    "expected_answer": x["expected_answer"],
                    "answer": output,
                    "semantic_evaluation": semantic_evaluation,
                    "external_evaluation": external_evaluation,
                })
        return results



