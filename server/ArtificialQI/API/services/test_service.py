from .abstract_service import AbstractService
from API.repositories import TestRepository

class TestService(AbstractService):
    repository = TestRepository