from API.services.test_service import TestService
from API.tests.services.abstract_service_test import AbstractServiceTestCase

class TestTestervice(AbstractServiceTestCase):
    service_class = TestService