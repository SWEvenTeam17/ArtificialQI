"""
File che contiene la classe AbstractView, una vista astratta
da cui derivano tutte le viste standard che vengono usate per
eseguire operazioni CRUD su istanze di modelli in DB.
"""

from abc import ABC, abstractmethod
from typing import ClassVar

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from API.services import AbstractService


class AbstractView(APIView, ABC):
    """
    Classe che contiene la definizione della vista.
    Ogni vista derivata da AbstractView deriva a sua volta da APIView e
    contiene un serializer e un service.
    """

    _serializer: ClassVar[type[serializers.Serializer]]
    _service: ClassVar[type[AbstractService]]

    @property
    @abstractmethod
    def _serializer(self) -> type[serializers.Serializer]:
        """Le sottoclassi devono definire un serializer"""

    @property
    @abstractmethod
    def _service(self) -> type[AbstractService]:
        """Le sottoclassi devono definire un service"""

    def get(self, request, instance_id: int = None) -> Response:
        """
        Metodo che risponde alle richieste di tipo GET.
        Ritorna tutte le istanze oppure una sola se un id è specificato.
        """
        try:
            if instance_id:
                data = self._service.read(instance_id=instance_id)
                serializer = self._serializer(data)
            else:
                data = self._service.read_all()
                serializer = self._serializer(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request) -> Response:
        """
        Metodo che risponde alle richieste di tipo POST.
        Valida i dati tramite il serializer corretto
        e crea una nuova istanza del Model in DB utilizzando
        il service corrispondente.
        """
        serializer = self._serializer(data=request.data)
        if serializer.is_valid():
            try:
                self._service.create(serializer.validated_data)
                return Response(
                    serializer.validated_data, status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, instance_id: int = None) -> Response:
        """
        Metodo che risponde alle richieste di tipo PUT/PATCH.
        Valida i dati tramite il serializer corretto
        e aggiorna una istanza del Model in DB utilizzando
        il service corrispondente.
        """
        instance = self._service.read(instance_id)
        if not instance:
            return Response(
                {"error": "Istanza non trovata"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self._serializer(instance, data=request.data)
        if serializer.is_valid():
            try:
                self._service.update(
                    instance_id=instance_id, data=serializer.validated_data
                )
                return Response(serializer.validated_data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, instance_id: int = None) -> Response:
        """
        Metodo che risponde alle richieste di tipo DELETE.
        Rimuove l'istanza corrispondende in DB.
        """
        try:
            self._service.delete(instance_id=instance_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
