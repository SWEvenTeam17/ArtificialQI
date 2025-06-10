"""
File che contiene i servizi riguardanti le valutazioni.
"""

import logging
import os
import re
from typing import ClassVar

from API.repositories import AbstractRepository, EvaluationRepository
from dotenv import load_dotenv
from google.api_core.exceptions import GoogleAPICallError, InternalServerError
from langchain_google_genai import ChatGoogleGenerativeAI
from sentence_transformers import SentenceTransformer

from .abstract_service import AbstractService


class EvaluationService(AbstractService):
    """
    Classe che contiene i servizi riguardanti le valutazioni.
    """

    _repository: ClassVar[AbstractRepository] = EvaluationRepository

    @staticmethod
    def get_semantic_evaluation(expected_answer: str, llm_answer: str):
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
    def get_external_evaluation(
        llm_provider: str, expected_answer: str, llm_answer: str
    ):
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
            if not key:
                logging.error("API key not found.")
                return "API key not found."

            try:
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

                logging.warning("Valutazione non trovata nella risposta.")
                return "Percentage not found."

            except (GoogleAPICallError, InternalServerError) as e:
                logging.error(f"Errore durante la chiamata a Gemini: {e}")
                return "Errore API Gemini"
            except Exception:
                logging.exception("Errore imprevisto durante la valutazione esterna.")
                return "Errore interno durante la valutazione"

        return "Unsupported provider"
