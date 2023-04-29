from django.http import QueryDict
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from onidata.models import Emprestimo
from onidata.serializers import EmprestimoSerializer
from onidata.utils import get_ip_usuario, calcular_saldo_devedor, calcular_IOF_emprestimo


class EmprestimosListarCriar(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        emprestimos = Emprestimo.objects.filter(usuario=request.user)
        serializer = EmprestimoSerializer(instance=emprestimos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if type(request.data) == QueryDict:
            request.data._mutable = True

        request.data['ip'] = get_ip_usuario(request)
        request.data['usuario'] = request.user.id
        serializer = EmprestimoSerializer(data=request.data, many=False)

        if serializer.is_valid():
            serializer.validated_data['valor_nominal'] = calcular_IOF_emprestimo(serializer.validated_data['valor_nominal'])
            emprestimo = serializer.save()
            serializer.validated_data['id'] = emprestimo.id
            serializer.validated_data['usuario'] = emprestimo.usuario.id
            serializer.validated_data['saldo_devedor'] = calcular_saldo_devedor(emprestimo)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmprestimoDetalhar(APIView):
    def get(self, request, pk):
        emprestimo = get_object_or_404(klass=Emprestimo, pk=pk, usuario=request.user)
        serializer = EmprestimoSerializer(instance=emprestimo, many=False)
        dados_emprestimo = serializer.data
        dados_emprestimo['saldo_devedor'] = calcular_saldo_devedor(emprestimo)
        return Response(dados_emprestimo, status=status.HTTP_200_OK)

    def put(self, request, pk):
        if type(request.data) == QueryDict:
            request.data._mutable = True

        emprestimo = get_object_or_404(klass=Emprestimo, pk=pk, usuario=request.user)
        request.data['ip'] = get_ip_usuario(request)
        request.data['usuario'] = request.user.id
        serializer = EmprestimoSerializer(instance=emprestimo, data=request.data, many=False)

        if serializer.is_valid():
            emprestimo = serializer.save()
            serializer.validated_data['id'] = emprestimo.id
            serializer.validated_data['usuario'] = request.user.id
            serializer.validated_data['saldo_devedor'] = calcular_saldo_devedor(emprestimo)
            return Response(serializer.validated_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        emprestimo = get_object_or_404(klass=Emprestimo, pk=pk, usuario=request.user)
        emprestimo.delete()
        return Response(f"Empréstimo {pk} removido com sucesso", status=status.HTTP_204_NO_CONTENT)
