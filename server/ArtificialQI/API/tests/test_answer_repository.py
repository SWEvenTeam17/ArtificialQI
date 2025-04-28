from django.test import TestCase
#from unittest.mock import patch
from django.db import models
from API.repositories.answer_repository import AnswerRepository
from API.models import LLM, Session, Prompt, Answer

class AnswerModelTestEmpty(TestCase):
    def test_get_all_when_empty(self):
        answers = AnswerRepository.get_all()
        self.assertEqual(answers.count(), 0)
    
    def test_get_by_id_when_empty(self):
        answers = AnswerRepository.get_by_id(1)
        self.assertEqual(answers, None)
        answers = AnswerRepository.get_by_id(0)
        self.assertEqual(answers, None)
    
    def test_update(self):
        data = {
            'prompt_id' : 1,
            'LLM_id' : 1,
            'LLM_answer' : 'La risposta'
        }
        return_value = AnswerRepository.update(1,data)
        self.assertEqual(return_value, None)
        answers = AnswerRepository.get_all()
        self.assertEqual(answers.count(), 0)


class AnswerModelTestSingleAnswer(TestCase):

    def setUp(self):
        # Creazione LLM
        self.llm1 = LLM.objects.create(
            name="llama3",
            n_parameters="3B"
        )

        # Creazione Session
        self.session1 = Session.objects.create(
            title="Sessione1",
            description="Sessione di test1"
        )

        # Collegamento tra LLM e Session
        self.session1.llm.add(self.llm1)

        # Creazione Prompt (con collegamento alla Session)
        self.prompt1 = Prompt.objects.create(
            prompt_text="Qual è la capitale dell'Italia?",
            expected_answer="Roma.",
            session=self.session1
        )

        # Creazione Answer (con collegamento a Prompt e LLM)
        self.answer1 = Answer.objects.create(
            prompt=self.prompt1,
            LLM=self.llm1,
            LLM_answer="Roma."
        )
    
    def test_get_all(self):
        answers = AnswerRepository.get_all()
        self.assertEqual(answers.count(), 1)
        self.assertIn(self.answer1, answers)
        self.assertIsInstance(answers, models.QuerySet)
        for answer in answers:
            self.assertIsInstance(answer, Answer)
    
    def test_get_by_id(self):
        answersby0 = AnswerRepository.get_by_id(0)
        self.assertIsNone(answersby0)
        answersby2 = AnswerRepository.get_by_id(2)
        self.assertIsNone(answersby2)
        answersby1 = AnswerRepository.get_by_id(self.answer1.id)
        self.assertIsNotNone(answersby1)
        self.assertIsInstance(answersby1, models.Model)
        self.assertEqual(answersby1.id, self.answer1.id)
    
    def test_update(self):
        data = {
            'prompt_id' : 1,
            'LLM_id' : 1,
            'LLM_answer' : 'La risposta'
        }
        #Aggiornamento (unica) Answer
        return_value = AnswerRepository.update(1,data)
        self.assertIsInstance(return_value, models.Model)
        answers = AnswerRepository.get_all()
        self.assertEqual(answers.count(), 1)
        self.assertEqual(answers.first().LLM_answer, 'La risposta')


class AnswerModelTestMultipleAnswers(TestCase):

    def setUp(self):
        # Creazione LLM
        self.llm1 = LLM.objects.create(
            name="llama3",
            n_parameters="3B"
        )
        self.llm2 = LLM.objects.create(
            name="gemma3",
            n_parameters="4B"
        )

        # Creazione Session
        self.session1 = Session.objects.create(
            title="Sessione1",
            description="Sessione di test1"
        )
        self.session2 = Session.objects.create(
            title="Sessione2",
            description="Sessione di test2"
        )

        # Collegamento tra LLM e Session
        self.session1.llm.add(self.llm1)
        self.session2.llm.add(self.llm2)

        # Creazione Prompt (con collegamento alla Session)
        self.prompt1 = Prompt.objects.create(
            prompt_text="Qual è la capitale dell'Italia?",
            expected_answer="Roma.",
            session=self.session1
        )
        self.prompt2 = Prompt.objects.create(
            prompt_text="Qual è la capitale della Francia?",
            expected_answer="Parigi.",
            session=self.session1
        )

        # Creazione Answer (con collegamento a Prompt e LLM)
        self.answer1 = Answer.objects.create(
            prompt=self.prompt1,
            LLM=self.llm1,
            LLM_answer="Roma."
        )
        self.answer2 = Answer.objects.create(
            prompt=self.prompt2,
            LLM=self.llm2,
            LLM_answer="Parigi."
        )

    def test_get_all(self):
       answers = AnswerRepository.get_all()
       self.assertEqual(answers.count(), 2)
       self.assertIn(self.answer1, answers)
       self.assertIn(self.answer2, answers)
       self.assertIsInstance(answers, models.QuerySet)
       for answer in answers:
           self.assertIsInstance(answer, Answer)
    
    def test_get_by_id(self):
        answersby0 = AnswerRepository.get_by_id(0)
        self.assertIsNone(answersby0)
        answersby3 = AnswerRepository.get_by_id(3)
        self.assertIsNone(answersby3)
        answersby1 = AnswerRepository.get_by_id(1)
        self.assertIsNotNone(answersby1)
        self.assertIsInstance(answersby1, models.Model)
        self.assertEqual(answersby1.id, self.answer1.id)
        answersby2 = AnswerRepository.get_by_id(2)
        self.assertIsNotNone(answersby2)
        self.assertIsInstance(answersby2, models.Model)
        self.assertEqual(answersby2.id, self.answer2.id)
    
    def test_update(self):
        # Precondizioni
        answer2 = AnswerRepository.get_by_id(2)
        prev_prompt_id = answer2.prompt_id
        prev_LLM_id = answer2.LLM_id
        prev_LLM_answer = answer2.LLM_answer

        data = {
            'prompt_id' : 1,
            'LLM_id' : 1,
            'LLM_answer' : 'La risposta'
        }
        #Aggiornamento Answer 2
        return_value = AnswerRepository.update(2,data)
        self.assertIsInstance(return_value, models.Model)
        answers = AnswerRepository.get_all()
        self.assertEqual(answers.count(), 2)
        if self.assertEqual(answers.count(), 2):
            self.assertEqual(answers[1].prompt_id, 1)
            self.assertEqual(answers[1].LLM_id, 1)
            self.assertEqual(answers[1].LLM_answer, 'La risposta')
            self.assertNotEqual(answers[1].prompt_id, prev_prompt_id)
            self.assertNotEqual(answers[1].LLM_id, prev_LLM_id)
            self.assertNotEqual(answers[1].LLM_answer, prev_LLM_answer)

        
class AnswerModelTestCreateDeleteAnswer(TestCase):

    def setUp(self):
        # Creazione LLM
        self.llm1 = LLM.objects.create(
            name="llama3",
            n_parameters="3B"
        )

        # Creazione Session
        self.session1 = Session.objects.create(
            title="Sessione1",
            description="Sessione di test1"
        )

        # Collegamento tra LLM e Session
        self.session1.llm.add(self.llm1)

        # Creazione Prompt (con collegamento alla Session)
        self.prompt1 = Prompt.objects.create(
            prompt_text="Qual è la capitale dell'Italia?",
            expected_answer="Roma.",
            session=self.session1
        )

    def test_create(self):
        data = {
            'prompt_id' : 1,
            'LLM_id' : 1,
            'LLM_answer' : 'La risposta'
        }

        AnswerRepository.create(data)
        answers = AnswerRepository.get_all()
        self.assertEqual(answers.count(), 1)
        self.assertEqual(answers.first().prompt_id, 1)
        self.assertEqual(answers.first().LLM_id, 1)
        self.assertEqual(answers.first().LLM_answer, 'La risposta')
    
    def test_delete(self):
        #Creazione 2 Answer
        data1 = {
            'prompt_id' : 1,
            'LLM_id' : 1,
            'LLM_answer' : 'Risposta da cancellare 1'
        }
        data2 = {
            'prompt_id' : 1,
            'LLM_id' : 1,
            'LLM_answer' : 'Risposta da cancellare 2'
        }

        AnswerRepository.create(data1)
        AnswerRepository.create(data2)

        #Recupero lista Answer
        answers = AnswerRepository.get_all()
        self.assertEqual(answers.count(), 2)

        #Test: eliminare Answer non esistente (estremo superiore)
        return_delete_value = AnswerRepository.delete(3)
        self.assertEqual(return_delete_value, False)
        self.assertEqual(answers.count(), 2)

        #Test: eliminare Answer esistente
        return_delete_value = AnswerRepository.delete(2)
        self.assertEqual(return_delete_value, True)
        self.assertEqual(answers.count(), 1)

        #Test: eliminare Answer già eliminata
        return_delete_value = AnswerRepository.delete(2)
        self.assertEqual(return_delete_value, False)
        self.assertEqual(answers.count(), 1)

        #Test: eliminare ultima Answer esistente
        return_delete_value = AnswerRepository.delete(1)
        self.assertEqual(return_delete_value, True)
        self.assertEqual(answers.count(), 0)

        #Test: eliminare indice non accessibile (estremo inferiore)
        return_delete_value = AnswerRepository.delete(0)
        self.assertEqual(return_delete_value, False)
        self.assertEqual(answers.count(), 0)

        #Test: eliminare indice negativo non accessibile
        return_delete_value = AnswerRepository.delete(-1)
        self.assertEqual(return_delete_value, False)
        self.assertEqual(answers.count(), 0)