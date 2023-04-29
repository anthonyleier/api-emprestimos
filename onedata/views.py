from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from onedata.models import Emprestimo, Pagamento
from onedata.serializers import EmprestimoSerializer, PagamentoSerializer
from onedata.utils import get_ip_usuario


class EmprestimoListCreate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        emprestimos = Emprestimo.objects.filter(usuario=request.user)
        serializer = EmprestimoSerializer(instance=emprestimos, many=True)
        return Response(serializer.data)

    def post(self, request):
        request.data['ip'] = get_ip_usuario(request)
        request.data['usuario'] = request.user.id
        serializer = EmprestimoSerializer(data=request.data, many=False)

        if serializer.is_valid():
            serializer.save()
            return Response(request.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PagamentoListCreate(APIView):
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
            serializer.save()
            return Response(request.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
