"""
File che contiene tutte le viste,
le viste contengono la logica di
controllo che gestisce le richieste al
server e le risposte date al client.
Per semplicità e separazione tutte le definizioni
delle viste sono state scritte all'interno
della cartella views_def.
"""

from .views_def import *

from django.http import JsonResponse
from .models import Block, Run, Prompt, LLM
from django.db.models import Avg

def common_blocks_view(request):
    first_llm_id = request.GET.get("first_llm_id")
    second_llm_id = request.GET.get("second_llm_id")

    if not first_llm_id or not second_llm_id:
        return JsonResponse({"error": "Missing LLM IDs"}, status=400)

    # Trova blocchi comuni in cui ENTRAMBI i modelli hanno almeno un run
    blocks_first = Block.objects.filter(prompt__run__llm__id=first_llm_id).values_list("id", flat=True)
    blocks_second = Block.objects.filter(prompt__run__llm__id=second_llm_id).values_list("id", flat=True)
    common_block_ids = set(blocks_first).intersection(set(blocks_second))

    if not common_block_ids:
        return JsonResponse({"common_blocks": []})

    # Recupera i blocchi comuni
    blocks = Block.objects.filter(id__in=common_block_ids)

    # Recupera tutte le valutazioni in un'unica query
    runs = Run.objects.filter(
        llm__id__in=[first_llm_id, second_llm_id]
    ).select_related("evaluation", "prompt", "llm")

    # Mappa: {(block_id, llm_id): [semantic_scores], ...}
    evaluations_map = {}

    for run in runs:
        llm_id = str(run.llm.id)
        prompt = run.prompt
        for block in prompt.block_set.all():  # o block_set.all()
            block_id = block.id
            if block_id not in common_block_ids:
                continue
            key = (block_id, llm_id)
            if key not in evaluations_map:
                evaluations_map[key] = {"semantic_scores": [], "external_scores": []}
            evaluations_map[key]["semantic_scores"].append(float(run.evaluation.semantic_evaluation))
            evaluations_map[key]["external_scores"].append(float(run.evaluation.external_evaluation))

    # Costruisci il risultato
    response_data = []
    for block in blocks:
        block_entry = {
            "block_id": block.id,
            "block_name": block.name,
            "llms": {}
        }

        for llm_id in [first_llm_id, second_llm_id]:
            key = (block.id, llm_id)
            scores = evaluations_map.get(key, {"semantic_scores": [], "external_scores": []})

            semantic_list = scores["semantic_scores"]
            external_list = scores["external_scores"]

            semantic_avg = round(sum(semantic_list) / len(semantic_list), 2) if semantic_list else 0
            external_avg = round(sum(external_list) / len(external_list), 2) if external_list else 0

            block_entry["llms"][llm_id] = {
                "semantic_avg": semantic_avg,
                "external_avg": external_avg,
                "semantic_scores": semantic_list,
                "external_scores": external_list,
            }

        response_data.append(block_entry)

    return JsonResponse({"common_blocks": response_data})


