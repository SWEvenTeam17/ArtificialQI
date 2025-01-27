from langchain_ollama import OllamaLLM

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
