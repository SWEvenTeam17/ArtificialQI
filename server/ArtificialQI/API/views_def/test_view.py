from .abstract_view import AbstractView
from API.serializers import TestSerializer
from API.services import TestService

class TestView(AbstractView):
    serializer = TestSerializer
    service = TestService