from API.models import Prompt, Session
from API.serializers import PromptSerializer
from .abstract_repository import AbstractRepository


class PromptRepository(AbstractRepository):
    model = Prompt

    def filter_by_session(session: Session):
        return Prompt.objects.filter(session=session)
