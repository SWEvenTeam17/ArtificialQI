from langchain_ollama import OllamaLLM
from sentence_transformers import SentenceTransformer

class LLMController:
    def __init__(self, LLMName):
        base_url = "http://localhost:11434"
        self.llm = OllamaLLM(model=LLMName, base_url=base_url)

    def getAnswer(self, prompt:str):
        stream = self.llm.stream(prompt)
        output = next(stream)
        for chunk in stream:
            output += chunk
        return output
    
    def getEvaluation(self, expected_answer, LLMAnswer):
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        expected_embedding = model.encode(expected_answer)
        LLMAnswer_embedding = model.encode(LLMAnswer)

        similarities = model.similarity(expected_embedding, LLMAnswer_embedding)
        approximated = round(similarities[0][0].item() * 100, 2)
        return approximated
