"""
File che contiene le viste relative alla gestione dei test.
"""


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from API.models import Session, Evaluation, Prompt
from API.serializers import PromptSerializer
from API.classes.llm_controller import LLMController


@api_view(["POST"])
def runtest(request):
    """
    Vista che gestisce l'esecuzione di un test
    """
    data, session = get_data(request)
    if not data:
        return Response(
            {"error": "Domanda e risposta sono campi obbligatori"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    save_data(data, session)
    llms = session.llm.all()
    try:
        response = evaluate(llms, data)
    except (ConnectionError, FileNotFoundError) as e:
        if isinstance(e, ConnectionError):
            return Response(
                {"error": str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        elif isinstance(e, FileNotFoundError):
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    return Response(response, status=status.HTTP_200_OK)
def get_data(request):
    """
    Funzione che ritorna i dati necessari all'esecuzione
    del test
    """
    session = Session.objects.get(id=request.data.get("sessionId"))
    return get_formatted(request), session
def get_formatted(request):
    """
    Funzione che formatta i dati in maniera corretta per l'esecuzione
    del test
    """
    data = request.data.get("data")
    ret = []
    for x in data:
        if 'id' in x and x['id'] is not None:
            ret.append(
                {"id": x["id"], "prompt_text": x["prompt_text"],
                "expected_answer": x["expected_answer"]}
            )
        else:
            ret.append(
                {"prompt_text": x["prompt_text"], "expected_answer": x["expected_answer"]}
            )
    return ret
def save_data(data, session):
    """
    Funzione che salva i prompt in database
    """
    for x in data:
        if 'id' not in x:
            save = {
                "prompt_text": x["prompt_text"],
                "expected_answer": x["expected_answer"],
                "session":session.id
            }
            serializer = PromptSerializer(data=save)
            if serializer.is_valid():
                saved_prompt = serializer.save()
                x["id"] = saved_prompt.id
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return None
def evaluate(llms, data):
    """
    Funzione che valuta le risposte dei LLM
    """
    results = []
    for x in data:
        prompt_instance = Prompt.objects.get(id=x["id"])
        question = prompt_instance.prompt_text
        for llm in llms:
            llm_obj = LLMController(llm.name)
            output = llm_obj.get_answer(question)
            semantic_evaluation = LLMController.get_semantic_evaluation(
                x["expected_answer"], output
            )
            external_evaluation = LLMController.get_external_evaluation(
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
