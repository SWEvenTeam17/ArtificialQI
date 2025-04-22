from .abstract_view import AbstractView
from API.serializers import PromptSerializer
from API.services import PromptService


class PromptView(AbstractView):
    serializer = PromptSerializer
    service = PromptService
