from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from onedata.models import Pagamento
from onedata.serializers import PagamentoSerializer


class PagamentosListarCriar(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pagamentos = Pagamento.objects.filter(usuario=request.user)
        serializer = PagamentoSerializer(instance=pagamentos, many=True)
        return Response(serializer.data)

    def post(self, request):
        request.data['usuario'] = request.user.id
        serializer = PagamentoSerializer(data=request.data, many=False)

        if serializer.is_valid():
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
        pagamento = get_object_or_404(klass=Pagamento, pk=pk, usuario=request.user)
        request.data['usuario'] = request.user.id
        serializer = PagamentoSerializer(instance=pagamento, data=request.data, many=False)

        if serializer.is_valid():
            pagamento = serializer.save()
            serializer.validated_data['id'] = pagamento.id
            serializer.validated_data['emprestimo'] = pagamento.emprestimo.id
            serializer.validated_data['usuario'] = pagamento.usuario.id
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        pagamento = get_object_or_404(klass=Pagamento, pk=pk, usuario=request.user)
        pagamento.delete()
        return Response(f"Pagamento {pk} removido com sucesso", status=status.HTTP_204_NO_CONTENT)
