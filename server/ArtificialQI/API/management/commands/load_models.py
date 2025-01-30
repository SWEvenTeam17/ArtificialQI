from django.core.management.base import BaseCommand
import requests
from API.models import LLM

class Command(BaseCommand):
    help = 'Load models from an external API'

    def handle(self, *args, **kwargs):
        url = "http://localhost:11434/api/tags"
        response = requests.get(url)
        data = response.json()
        models = data.get("models", [])
        for model in models:
            name = model.get("name")
            size = model.get("details", {}).get("parameter_size")
            llm, created = LLM.objects.get_or_create(name=name)
            llm.n_parameters = size
            llm.save()

