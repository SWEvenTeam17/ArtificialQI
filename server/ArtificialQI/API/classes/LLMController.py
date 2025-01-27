from langchain_ollama import OllamaLLM

class LLMController:
    def __init__(self, LLMName, host="localhost", port=8000):
        base_url = "http://ollama:11434"
        self.llm = OllamaLLM(model=LLMName, base_url=base_url)


    def getAnswer(self, prompt:str):
        stream = self.llm.stream(prompt)
        output = next(stream)
        for chunk in stream:
            output += chunk
        return output
