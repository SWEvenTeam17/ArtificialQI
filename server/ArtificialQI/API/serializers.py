"""
File che contiene tutti i serializzatori,
un serializzatore è un oggetto che permette 
di convertire i risultati delle query
in formato JSON, di validare
l'input dell'utente e restituire errore
se necessario.
"""
from rest_framework import serializers
from API.models import Prompt, LLM, Answer, Session, Evaluation

class LLMSerializer(serializers.ModelSerializer):
    """
    Serializzatore del modello LLM
    """
    class Meta:
        model = LLM
        fields = ['id', 'name', 'n_parameters']

class AnswerSerializer(serializers.ModelSerializer):
    """
    Serializzatore del modello Answer
    """
    class Meta:
        model = Answer
        fields = ['id', 'prompt', 'LLM', 'LLM_answer', 'timestamp']

class SessionSerializer(serializers.ModelSerializer):
    """
    Serializzatore del modello Sessione
    """
    llm = LLMSerializer(many=True, required=False)

    class Meta:
        model = Session
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'llm']


class EvaluationSerializer(serializers.ModelSerializer):
    """
    Serializzatore del modello Evaluation
    """
    class Meta:
        model = Evaluation
        fields = ['llm', 'prompt','semantic_evaluation', 'external_evaluation']

class PromptSerializer(serializers.ModelSerializer):
    """
    Serializzatore del modello Prompt
    """
    session = serializers.PrimaryKeyRelatedField(queryset=Session.objects.all())
    evaluation_set = EvaluationSerializer(many=True, read_only=True)
    class Meta:
        model = Prompt
        fields = ['id', 'prompt_text', 'expected_answer', 'timestamp', 'session', 'evaluation_set']
