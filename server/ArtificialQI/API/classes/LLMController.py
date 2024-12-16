from langchain_ollama import OllamaLLM

class LLMController:
    def __init__(self, LLMName):
        self.llm = OllamaLLM(model=LLMName)

    def getAnswer(self, prompt:str):
        stream = self.llm.stream(prompt)
        output = next(stream)
        for chunk in stream:
            output += chunk
        return output
