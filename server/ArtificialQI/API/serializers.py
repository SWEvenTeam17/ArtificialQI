from rest_framework import serializers
from API.models import Prompt, LLM, Answer, Session

class LLMSerializer(serializers.ModelSerializer):
    class Meta:
        model = LLM
        fields = ['id', 'name', 'n_parameters']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'prompt', 'LLM', 'LLM_answer', 'timestamp']

class SessionSerializer(serializers.ModelSerializer):
    llm = LLMSerializer(many=True, required=False)

    class Meta:
        model = Session
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'llm']

class PromptSerializer(serializers.ModelSerializer):
    session = serializers.PrimaryKeyRelatedField(queryset=Session.objects.all())

    class Meta:
        model = Prompt
        fields = ['id', 'prompt_text', 'expected_answer', 'timestamp', 'session']