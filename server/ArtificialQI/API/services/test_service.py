from API.services import AbstractService
from API.repositories import TestRepository

class TestService(AbstractService):
    repository = TestRepository