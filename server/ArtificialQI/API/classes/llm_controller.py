"""
File che contiene la definizione della logica della classe LLMController
"""

import os
import re
import requests
from requests.exceptions import RequestException
from dotenv import load_dotenv
from langchain_ollama import OllamaLLM
from sentence_transformers import SentenceTransformer
from langchain_google_genai import ChatGoogleGenerativeAI


class LLMController:
    """
    Classe che gestisce tutte le operazioni che un LLM può fare.
    Il costruttore istanzia un oggetto di tipo LLMController che possiede
    due attributi (url server Ollama e istanza di un oggetto di tipo OllamaLLM).
    La classe gestisce attivamente l'interrogazione e la valutazione degli LLM.
    """

    def __init__(self, llm_name):
        load_dotenv()
        base_url = os.getenv("OLLAMA_URL")
        # Controlla se il server Ollama funziona
        try:
            response = requests.get(f"{base_url}/api/version", timeout=5)
            response.raise_for_status()
        except RequestException as e:
            raise ConnectionError(f"Errore di connessione al server Ollama: {e}")
        # Se funziona, crea l'oggetto OllamaLLM
        self.llm = OllamaLLM(model=llm_name, base_url=base_url)

    def get_answer(self, prompt: str):
        """
        Funzione che interroga un LLM
        """
        stream = self.llm.stream(prompt)
        output = next(stream)
        for chunk in stream:
            output += chunk
        return output

    @staticmethod
    def get_semantic_evaluation(expected_answer, llm_answer):
        """
        Funzione che ritorna la valutazione semantica di una risposta
        di un LLM.
        Pulisce input e output rendendo tutto in minuscolo e 
        togliendo l'ultimo punto nella stringa
        """

        clean_expected = re.sub(r"\.$", "", expected_answer.lower())
        clean_llm_answer = re.sub(r"\.$", "", llm_answer.lower())
        if clean_expected in clean_llm_answer:
            return 100
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        expected_embedding = model.encode(clean_expected)
        llm_answer_embedding = model.encode(clean_llm_answer)
        similarities = model.similarity(expected_embedding, llm_answer_embedding)
        approximated = round(similarities[0][0].item() * 100, 2)
        return approximated

    @staticmethod
    def get_external_evaluation(llm_provider, expected_answer, llm_answer):
        """
        Funzione che ritorna la valutazione di Gemini su
        una risposta data da un LLM
        """
        if llm_provider == "google":
            envcheck = load_dotenv()
            if not envcheck:
                raise FileNotFoundError(
                    "Il file .env non è presente nella cartella server\\ArtificialQI"
                )
            key = os.getenv("GEMINI_API_KEY")
            if key != "":
                llm = ChatGoogleGenerativeAI(
                    model="gemini-2.0-flash", google_api_key=key
                )
                prompt = f"""
                You are an AI evaluator. Your task is to compare two answers. 
                The first answer is the 'expected answer', and the second answer is the 'LLM answer'.
                Please evaluate how similar the two answers are and return the result as a percentage (0 to 100), 
                where 100 means the answers are identical and 0 means they are completely different.
                Answer the percentage only, with no additional text.
                
                Expected answer: {expected_answer}
                LLM answer: {llm_answer}
                """
                stream = llm.stream(prompt)
                output = next(stream)
                for chunk in stream:
                    output += chunk
                match = re.search(r"\d+(\.\d+)?", output.content)
                if match:
                    return match.group(0)
                return "Percentage not found."
            print("API key not found.")
            return "API key not found."
        return "Unsupported provider"
