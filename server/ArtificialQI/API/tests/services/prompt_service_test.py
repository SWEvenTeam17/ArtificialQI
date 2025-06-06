from unittest.mock import MagicMock

import pytest

from API.services.prompt_service import PromptService
from API.tests.services.abstract_service_test import AbstractServiceTestCase


class TestPromptService(AbstractServiceTestCase):
    service_class = PromptService
