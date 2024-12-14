from rest_framework import serializers
from API.models import Prompt, LLM, Answer

class PromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = ['id', 'prompt_text', 'expected_answer', 'timestamp']

class LLMSerializer(serializers.ModelSerializer):
    class Meta:
        model = LLM
        fields = ['id', 'name', 'n_parameters']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'prompt', 'LLM', 'LLM_answer', 'timestamp']