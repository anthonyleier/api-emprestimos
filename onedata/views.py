from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from onedata.models import Emprestimo
from onedata.serializers import EmprestimoSerializer


class EmprestimoListCreate(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Emprestimo.objects.all()
    serializer_class = EmprestimoSerializer

    def get_queryset(self):
        return Emprestimo.objects.filter(usuario=self.request.user)
