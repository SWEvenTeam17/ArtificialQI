from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from API.models import Session, Answer
from API.serializers import PromptSerializer
from API.classes.LLMController import LLMController

@csrf_exempt

@api_view(['POST'])
def runtest(request):
    question, expected_answer, session = getData(request)
    if not question or not expected_answer:
        return Response({"error": "Domanda e risposta sono campi obbligatori"}, status=status.HTTP_400_BAD_REQUEST)

    saveData(question, expected_answer, session)

    llms = session.llm.all()
    response = evaluate(llms, question, expected_answer)
    return Response({"response": response}, status=status.HTTP_200_OK)

def getData(request):
    session = Session.objects.get(id = request.data.get('sessionId'))
    return request.data.get('question',None), request.data.get('answer', None), session

def saveData(question, expected, session):
    save_data = {
        "prompt_text":question,
        "expected_answer":expected,
        "session":session.id
    }
    serializer = PromptSerializer(data=save_data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def evaluate(llms, question, expected_answer):
    results = []
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
    return response