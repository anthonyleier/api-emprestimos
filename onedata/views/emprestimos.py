from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from onedata.models import Emprestimo
from onedata.serializers import EmprestimoSerializer
from onedata.utils import get_ip_usuario


class EmprestimosListarCriar(APIView):
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
            emprestimo = serializer.save()
            serializer.validated_data['id'] = emprestimo.id
            serializer.validated_data['usuario'] = emprestimo.usuario.id
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmprestimoDetalhar(APIView):
    def get(self, request, pk):
        emprestimo = get_object_or_404(klass=Emprestimo, pk=pk, usuario=request.user)
        serializer = EmprestimoSerializer(instance=emprestimo, many=False)
        return Response(serializer.data)

    def put(self, request, pk):
        emprestimo = get_object_or_404(klass=Emprestimo, pk=pk, usuario=request.user)
        request.data['ip'] = get_ip_usuario(request)
        request.data['usuario'] = request.user.id
        serializer = EmprestimoSerializer(instance=emprestimo, data=request.data, many=False)

        if serializer.is_valid():
            emprestimo = serializer.save()
            serializer.validated_data['id'] = emprestimo.id
            serializer.validated_data['usuario'] = request.user.id
            return Response(serializer.validated_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        emprestimo = get_object_or_404(klass=Emprestimo, pk=pk, usuario=request.user)
        emprestimo.delete()
        return Response(f"Empréstimo {pk} removido com sucesso", status=status.HTTP_204_NO_CONTENT)
