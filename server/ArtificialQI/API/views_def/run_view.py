from API.serializers import RunSerializer
from API.services import RunService
from .abstract_view import AbstractView

class RunView(AbstractView):
    """
    Classe che contiene le definizioni delle viste dedicate alla gestione delle run.
    """
    serializer = RunSerializer
    service = RunService