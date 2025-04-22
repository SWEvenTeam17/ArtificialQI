from abc import ABC, abstractmethod
from typing import ClassVar
from API.services import AbstractService
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response


class AbstractView(APIView, ABC):
    serializer: ClassVar[type[serializers.Serializer]]
    service: ClassVar[type[AbstractService]]

    @property
    @abstractmethod
    def serializer(self) -> type[serializers.Serializer]:
        # Le sottoclassi devono definire un serializer
        pass

    @property
    @abstractmethod
    def service(self) -> type[AbstractService]:
        # Le sottoclassi devono definire un service
        pass

    def get(self, request, pk: int = None):
        try:
            if pk:
                data = self.service.read(id=pk)
                serializer = self.serializer(data)
            else:
                data = self.service.read_all()
                serializer = self.serializer(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk: int = None):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            try:
                data = self.service.create(serializer.validated_data)
                return Response(
                    serializer.validated_data, status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk: int = None):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            try:
                data = self.service.update(id=pk, data=serializer.validated_data)
                return Response(serializer.validated_data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk: int = None):
        try:
            self.service.delete(id=pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
