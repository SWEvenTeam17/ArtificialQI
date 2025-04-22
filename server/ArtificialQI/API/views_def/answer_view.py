from .abstract_view import AbstractView
from API.serializers import AnswerSerializer
from API.services import AnswerService


class AnswerView(AbstractView):
    serializer = AnswerSerializer
    service = AnswerService
