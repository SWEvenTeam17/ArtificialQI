from django.test import TestCase 
from django.db import models
from API.services.answer_service import AnswerService
from API.models import LLM, Session, Prompt, Answer

class AnswerServiceEmptyTest(TestCase):
    def test_read_all_when_empty(self):
        answers= AnswerService.read_all()
        self.assertEqual(answers.count(), 0)
    
    def test_read_not_found(self):
        answers = AnswerService.read(1)
        self.assertIsNone(answers)
    
    def test_update_not_found(self):
        answers = AnswerService.update(1, {"LLM_answer": "La risposta"})
        self.assertIsNone(answers)
    
    def test_delete_not_found(self):
        answers = AnswerService.delete(1)
        self.assertFalse(answers)


class AnswerServiceSingleItemTest(TestCase):
   
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
    

    def test_read(self):
        answers = AnswerService.read(self.answer1.id)
        self.assertEqual(answers.id, self.answer1.id) 
    
    def test_read_all(self):
        answers = AnswerService.read_all()
        self.assertEqual(answers.count(), 1)
        self.assertIn(self.answer1, answers)
    
    def test_update(self):
        data = {
            'prompt_id' : 1,
            'LLM_id' : 1,
            'LLM_answer' : 'La risposta'
        }
        updated_answer = AnswerService.update(self.answer1.id, data)
       
        #Aggiornamento (unica) Answer
        self.assertIsNotNone(updated_answer)
        answers = AnswerService.read_all()
        self.assertEqual(answers.count(), 1)  
        self.assertEqual(answers.first().LLM_answer, 'La risposta')

class AnswerServiceMultipleItemsTest(TestCase):
   
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

    
    def test_read(self):
        # Test lettura answer1
        result1 = AnswerService.read(self.answer1.id)
        self.assertIsNotNone(result1)
        self.assertEqual(result1.id, self.answer1.id)
        self.assertEqual(result1.LLM_answer, "Roma.")
        self.assertEqual(result1.prompt.id, self.prompt1.id)
        
        # Test lettura answer2
        result2 = AnswerService.read(self.answer2.id)
        self.assertIsNotNone(result2)
        self.assertEqual(result2.LLM_answer, "Parigi.")

        # Test ID inesistente
        self.assertIsNone(AnswerService.read(999))
        self.assertIsNone(AnswerService.read(0))
        self.assertIsNone(AnswerService.read(-1))

        

    def test_read_all(self):
        answers = AnswerService.read_all()
        self.assertEqual(answers.count(), 2)
        self.assertIn(self.answer1, answers)
        self.assertIn(self.answer2, answers)

     
    def test_update(self):
      # Precondizioni
      answer2 = AnswerService.read(self.answer2.id)
      prev_prompt_id = answer2.prompt_id
      prev_LLM_id = answer2.LLM_id
      prev_LLM_answer = answer2.LLM_answer

      data = {
        'prompt_id': self.prompt1.id,  # Usa l'ID del prompt1 creato nel setUp
        'LLM_id': self.llm1.id,        # Usa l'ID del llm1 creato nel setUp
        'LLM_answer': 'La risposta modificata'
      }

      # Aggiornamento Answer 2 tramite il service
      updated_answer = AnswerService.update(self.answer2.id, data)
    
      # Verifiche
      self.assertIsNotNone(updated_answer)
      answers = AnswerService.read_all()
      self.assertEqual(answers.count(), 2)

     # Verifica i nuovi valori
      self.assertEqual(updated_answer.prompt_id, self.prompt1.id)
      self.assertEqual(updated_answer.LLM_id, self.llm1.id)
      self.assertEqual(updated_answer.LLM_answer, 'La risposta modificata')
    
     # Verifica che siano cambiati rispetto ai valori originali
      self.assertNotEqual(updated_answer.prompt_id, prev_prompt_id)
      self.assertNotEqual(updated_answer.LLM_id, prev_LLM_id)
      self.assertNotEqual(updated_answer.LLM_answer, prev_LLM_answer)
       
        
class AnswerServiceTestCreateDelete(TestCase):

    def setUp(self):
        # Creazione LLM
        self.llm = LLM.objects.create(
            name="llama3",
            n_parameters="3B"
        )

        # Creazione Session
        self.session = Session.objects.create(
            title="Sessione1",
            description="Sessione di test1"
        )

        # Collegamento tra LLM e Session
        self.session.llm.add(self.llm)

        # Creazione Prompt (con collegamento alla Session)
        self.prompt = Prompt.objects.create(
            prompt_text="Qual è la capitale dell'Italia?",
            expected_answer="Roma.",
            session=self.session
        )

    def test_create(self):
        data = {
            'prompt_id': 1,  # Usa gli ID dagli oggetti creati
            'LLM_id': 1,
            'LLM_answer': 'La risposta'
        }

        
        AnswerService.create(data)
        answers = AnswerService.read_all()
        
        self.assertEqual(answers.count(), 1)
        self.assertEqual(answers.first().prompt_id, 1)
        self.assertEqual(answers.first().LLM_id, 1)
        self.assertEqual(answers.first().LLM_answer, 'La risposta')
    
    def test_delete(self):
        # Creazione 2 Answer
        data1 = {
            'prompt_id': 1,
            'LLM_id': 1,
            'LLM_answer': 'Risposta da cancellare 1'
        }
        data2 = {
            'prompt_id': 1,
            'LLM_id': 1,
            'LLM_answer': 'Risposta da cancellare 2'
        }

        # Creazione tramite SERVICE
        AnswerService.create(data1)
        AnswerService.create(data2)

        # Recupero lista Answer
        answers = AnswerService.read_all()
        self.assertEqual(answers.count(), 2)

        # Test: eliminare Answer non esistente (estremo superiore)
        return_delete_value = AnswerService.delete(3)
        self.assertEqual(return_delete_value, False)
        self.assertEqual(answers.count(), 2)

        # Test: eliminare Answer esistente
        return_delete_value = AnswerService.delete(2)  # Cancella il secondo
        self.assertEqual(return_delete_value, True)
        self.assertEqual(answers.count(), 1)

        # Test: eliminare Answer già eliminata
        return_delete_value = AnswerService.delete(2)
        self.assertEqual(return_delete_value, False)
        self.assertEqual(answers.count(), 1)

        # Test: eliminare ultima Answer esistente
        return_delete_value = AnswerService.delete(1)
        self.assertEqual(return_delete_value, True)
        self.assertEqual(answers.count(), 0)

        # Test: eliminare ID non validi
        self.assertEqual(AnswerService.delete(0), False)      # Estremo inferiore
        self.assertEqual(AnswerService.delete(-1), False)  
   