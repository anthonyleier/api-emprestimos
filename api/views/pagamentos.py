from django.http import QueryDict
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from api.models import Pagamento
from api.serializers import PagamentoSerializer
from api.utils import calcular_IOF_pagamento


class PagamentosListarCriar(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pagamentos = Pagamento.objects.filter(usuario=request.user)
        serializer = PagamentoSerializer(instance=pagamentos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if type(request.data) == QueryDict:
            request.data._mutable = True

        request.data['usuario'] = request.user.id
        serializer = PagamentoSerializer(data=request.data, many=False)

        if serializer.is_valid():
            serializer.validated_data['valor'] = calcular_IOF_pagamento(serializer.validated_data['valor'], request.data['emprestimo'])
            pagamento = serializer.save()
            serializer.validated_data['id'] = pagamento.id
            serializer.validated_data['emprestimo'] = pagamento.emprestimo.id
            serializer.validated_data['usuario'] = pagamento.usuario.id
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PagamentoDetalhar(APIView):
    def get(self, request, pk):
        pagamento = get_object_or_404(klass=Pagamento, pk=pk, usuario=request.user)
        serializer = PagamentoSerializer(instance=pagamento, many=False)
        return Response(serializer.data)

    def put(self, request, pk):
        if type(request.data) == QueryDict:
            request.data._mutable = True

        pagamento = get_object_or_404(klass=Pagamento, pk=pk, usuario=request.user)
        request.data['usuario'] = request.user.id
        serializer = PagamentoSerializer(instance=pagamento, data=request.data, many=False)

        if serializer.is_valid():
            pagamento = serializer.save()
            serializer.validated_data['id'] = pagamento.id
            serializer.validated_data['emprestimo'] = pagamento.emprestimo.id
            serializer.validated_data['usuario'] = pagamento.usuario.id
            return Response(serializer.validated_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        pagamento = get_object_or_404(klass=Pagamento, pk=pk, usuario=request.user)
        pagamento.delete()
        return Response(f"Pagamento {pk} removido com sucesso", status=status.HTTP_204_NO_CONTENT)
