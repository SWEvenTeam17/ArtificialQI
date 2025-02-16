from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
from API.models import Session, Evaluation, Prompt
from API.serializers import PromptSerializer, EvaluationSerializer
from API.classes.LLMController import LLMController


@csrf_exempt
@api_view(["POST"])
def runtest(request):
    data, session = getData(request)
    if not data:
        return Response(
            {"error": "Domanda e risposta sono campi obbligatori"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    saveData(data, session)
    llms = session.llm.all()
    response = evaluate(llms, data)
    return Response(response, status=status.HTTP_200_OK)


def getData(request):  #ritorna i dati
    session = Session.objects.get(id=request.data.get("sessionId"))
    return getFormatted(request), session


def getFormatted(request):  # ritorna i dati formattati
    data = request.data.get("data")
    ret = []
    for x in data:
        if 'id' in x and x['id'] is not None:
            ret.append(
                {"id": x["id"], "prompt_text": x["prompt_text"], "expected_answer": x["expected_answer"]}
            )
        else:
            ret.append(
                {"prompt_text": x["prompt_text"], "expected_answer": x["expected_answer"]}
            )
    return ret



def saveData(data, session):    #salva i prompt in database
    for x in data:
        if 'id' not in x:
            save_data = {
                "prompt_text": x["prompt_text"],
                "expected_answer": x["expected_answer"],
                "session":session.id
            }
            serializer = PromptSerializer(data=save_data)
            if serializer.is_valid():
                saved_prompt = serializer.save()
                x["id"] = saved_prompt.id
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def evaluate(llms, data):  #fa le valutazioni
    results = []
    for x in data:
        prompt_instance = Prompt.objects.get(id=x["id"])
        question = prompt_instance.prompt_text
        for llm in llms:
            llmObj = LLMController(llm.name)
            output = llmObj.getAnswer(question)
            semantic_evaluation = LLMController.getSemanticEvaluation(
                x["expected_answer"], output
            )
            external_evaluation = LLMController.getExternalEvaluation(
                "google", x["expected_answer"], output
            )
            Evaluation(
                prompt=prompt_instance,
                llm=llm,
                semantic_evaluation=semantic_evaluation,
                external_evaluation=external_evaluation,
            ).save()
            results.append(
                {
                    "llm_name": llm.name,
                    "question": question,
                    "expected_answer": x["expected_answer"],
                    "answer": output,
                    "semantic_evaluation": semantic_evaluation,
                    "external_evaluation": external_evaluation,
                }
            )
    return results
