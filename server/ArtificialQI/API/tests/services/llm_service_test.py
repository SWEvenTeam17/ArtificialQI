from API.services.llm_service import LLMService
from API.tests.services.abstract_service_test import AbstractServiceTestCase

class TestLLMService(AbstractServiceTestCase):
    service_class = LLMService