from django.test import TestCase
from API.models import LLM, Prompt, Session, Evaluation
from django.core.exceptions import ValidationError

class ModelTests(TestCase):
    def setUp(self):
        # Dati di test riutilizzabili
        self.llm = LLM.objects.create(name="llama3", n_parameters="7B")
        self.session = Session.objects.create(title="Test Session", description="Test")
        self.prompt = Prompt.objects.create(
            prompt_text="What is AI?",
            expected_answer="Artificial Intelligence",
            session=self.session
        )

    def test_llm_creation(self):
        """Verifica che un LLM venga creato correttamente."""
        self.assertEqual(self.llm.name, "llama3")
        self.assertEqual(self.llm.n_parameters, "7B")

    def test_prompt_session_relationship(self):
        """Verifica che un Prompt sia legato a una Session."""
        self.assertEqual(self.prompt.session.title, "Test Session")

    def test_evaluation_creation(self):
        """Verifica la creazione di una Evaluation con relazioni."""
        evaluation = Evaluation.objects.create(
            llm=self.llm,
            prompt=self.prompt,
            semantic_evaluation=85.50,
            external_evaluation=90.00
        )
        self.assertEqual(evaluation.semantic_evaluation, 85.50)