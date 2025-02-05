from langchain_ollama import OllamaLLM
from sentence_transformers import SentenceTransformer
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import re
from dotenv import load_dotenv


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
    
    @staticmethod
    def getSemanticEvaluation(expected_answer, LLMAnswer):
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        expected_embedding = model.encode(expected_answer)
        LLMAnswer_embedding = model.encode(LLMAnswer)

        similarities = model.similarity(expected_embedding, LLMAnswer_embedding)
        approximated = round(similarities[0][0].item() * 100, 2)
        return approximated
    
    @staticmethod
    def getExternalEvaluation(LLM_provider, expected_answer, LLMAnswer):
        if LLM_provider == "google":
            load_dotenv()
            key = os.getenv('GEMINI_API_KEY')
            
            if key != "":
                llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=key)
                
                prompt = f"""
                You are an AI evaluator. Your task is to compare two answers. 
                The first answer is the 'expected answer', and the second answer is the 'LLM answer'.
                Please evaluate how similar the two answers are and return the result as a percentage (0 to 100), 
                where 100 means the answers are identical and 0 means they are completely different.
                Answer the percentage only, with no additional text.
                
                Expected answer: {expected_answer}
                LLM answer: {LLMAnswer}
                """
                
                stream = llm.stream(prompt)
                output = next(stream)
                for chunk in stream:
                    output += chunk
                
                return output.content
                
            else:
                print("API key not found.")
                return "API key not found."
