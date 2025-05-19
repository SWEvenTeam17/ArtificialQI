"""
File che contiene tutti i serializzatori,
un serializzatore è un oggetto che permette
di convertire i risultati delle query
in formato JSON, di validare
l'input dell'utente e restituire errore
se necessario.
"""

from rest_framework import serializers
from API.models import Prompt, LLM, Run, Session, Evaluation, Test, Block


class LLMSerializer(serializers.ModelSerializer):
    """
    Serializzatore del modello LLM
    """

    class Meta:
        model = LLM
        fields = ["id", "name", "n_parameters"]


class SessionSerializer(serializers.ModelSerializer):
    """
    Serializzatore del modello Sessione
    """

    llm = LLMSerializer(many=True, required=False)

    class Meta:
        model = Session
        fields = ["id", "title", "description", "created_at", "updated_at", "llm"]


class EvaluationSerializer(serializers.ModelSerializer):
    """
    Serializzatore del modello Evaluation
    """

    class Meta:
        model = Evaluation
        fields = ["prompt", "semantic_evaluation", "external_evaluation"]


class PromptSerializer(serializers.ModelSerializer):
    """
    Serializzatore del modello Prompt
    """

    evaluation_set = EvaluationSerializer(many=True, read_only=True)

    class Meta:
        model = Prompt
        fields = [
            "id",
            "prompt_text",
            "expected_answer",
            "timestamp",
            "evaluation_set",
        ]


class BlockSerializer(serializers.ModelSerializer):
    """
    Serializer per il modello Block.
    """

    prompt = PromptSerializer(many=True, required=False)

    class Meta:
        model = Block
        fields = ["id", "name", "prompt"]


class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = "__all__"


class TestSerializer(serializers.ModelSerializer):
    session = SessionSerializer(read_only=True)
    block = BlockSerializer(read_only=True)

    class Meta:
        model = Test
        fields = "__all__"
