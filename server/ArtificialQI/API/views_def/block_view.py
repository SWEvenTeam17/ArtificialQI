"""
File che contiene la vista dedicata alla gestione dei
test precedentemente eseguiti in una sessione.
"""

from typing import ClassVar

from API.models import Block
from API.repositories import BlockRepository, RunRepository
from API.serializers import BlockSerializer
from API.services import AbstractService, BlockService, LLMService
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .abstract_view import AbstractView


class BlockView(AbstractView):
    """
    Classe che contiene la definizione della vista dedicata
    alla gestione dei blocchi di domande.
    """

    _serializer: ClassVar[type[serializers.Serializer]] = BlockSerializer
    _service: ClassVar[type[AbstractService]] = BlockService

    def post(self, request) -> Response:
        """
        Metodo che risponde alle richieste di tipo POST.
        Valida i dati tramite il serializer corretto
        e crea una nuova istanza del Model in DB utilizzando
        il service corrispondente.
        """
        data: dict = {
            "name": request.data.get("name"),
            "questions": request.data.get("questions"),
        }
        try:
            result = self._service.create(data=data)
            if result == False:
                return Response(
                    {"error": "Nome duplicato"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            serialized = self._serializer(result)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BlockTestView(APIView):
    def get(self, request) -> Response:
        first_llm = LLMService.read(int(request.GET.get("first_llm_id")))
        second_llm = LLMService.read(int(request.GET.get("second_llm_id")))

        if not first_llm or not second_llm:
            return Response({"error": "Missing LLM IDs"}, status=400)

        blocks = BlockRepository.get_common_blocks_for_llms(first_llm, second_llm)
        common_block_ids = [block.id for block in blocks]

        runs = RunRepository.get_common_runs(
            first_llm, second_llm, ["evaluation", "prompt", "llm"]
        )

        evaluations_map = {}

        for run in runs:
            prompt = run.prompt
            related_blocks = Block.objects.filter(
                prompt=prompt, id__in=common_block_ids
            )

            for block in related_blocks:
                key = (block.id, run.llm.id)
                if key not in evaluations_map:
                    evaluations_map[key] = {
                        "semantic_scores": [],
                        "external_scores": [],
                    }

                evaluations_map[key]["semantic_scores"].append(
                    float(run.evaluation.semantic_evaluation)
                )
                evaluations_map[key]["external_scores"].append(
                    float(run.evaluation.external_evaluation)
                )

        response_data = []
        for block in blocks:
            block_entry = {"block_id": block.id, "block_name": block.name, "llms": {}}

            for llm_id in [first_llm.id, second_llm.id]:
                key = (block.id, llm_id)
                scores = evaluations_map.get(
                    key,
                    {
                        "semantic_scores": [],
                        "external_scores": [],
                    },
                )

                semantic_list = scores["semantic_scores"]
                external_list = scores["external_scores"]

                semantic_avg = (
                    round(sum(semantic_list) / len(semantic_list), 2)
                    if semantic_list
                    else 0
                )
                external_avg = (
                    round(sum(external_list) / len(external_list), 2)
                    if external_list
                    else 0
                )

                block_entry["llms"][llm_id] = {
                    "semantic_avg": semantic_avg,
                    "external_avg": external_avg,
                    "semantic_scores": semantic_list,
                    "external_scores": external_list,
                }

            response_data.append(block_entry)

        return Response({"common_blocks": response_data})
