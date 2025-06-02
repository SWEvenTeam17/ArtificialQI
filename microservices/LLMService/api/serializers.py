from rest_framework import serializers


class LLMRequestSerializer(serializers.Serializer):
    llm_name = serializers.CharField()
    prompt = serializers.CharField()


class LLMResponseSerializer(serializers.Serializer):
    llm_name = serializers.CharField()
    prompt = serializers.CharField()
    answer = serializers.CharField()
