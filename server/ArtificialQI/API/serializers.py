from rest_framework import serializers
from API.models import Prompt, Answer

class PromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = ['id', 'prompt_text', 'expected_answer', 'timestamp']


