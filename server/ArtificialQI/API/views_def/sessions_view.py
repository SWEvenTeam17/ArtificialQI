from .abstract_view import AbstractView
from API.serializers import SessionSerializer
from API.services import SessionService


class SessionsView(AbstractView):
    serializer = SessionSerializer
    service = SessionService
