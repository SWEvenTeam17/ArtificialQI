from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from API.models import Session
from API.classes.LLMController import LLMController

@csrf_exempt

@api_view(['POST'])
def runtest(request):
    question = request.data.get('question', None)
    expected_answer = request.data.get('answer', None)

    if not question or not expected_answer:
        return Response({"error": "Domanda e risposta sono campi obbligatori"}, status=status.HTTP_400_BAD_REQUEST)
    
    session = Session.objects.get(id = request.data.get('sessionId'))

    llms = session.llm.all()
    results=[];
    for llm in llms:
        llmObj = LLMController(llm.name)
        output = llmObj.getAnswer(question)
        semantic_evaluation = LLMController.getSemanticEvaluation(expected_answer, output)
        external_evaluation = LLMController.getExternalEvaluation("google", expected_answer, output)
        results.append({
            "llm_name": llm.name,
            "answer": output,
            "semantic_evaluation": semantic_evaluation,
            "external_evaluation": external_evaluation
        })
    response = {
        "results": results,
        "question": question
    }
    return Response({"response": response}, status=status.HTTP_200_OK)