from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from onedata.models import Emprestimo
from onedata.serializers import EmprestimoSerializer


class EmprestimoListCreate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Emprestimo.objects.filter(usuario=request.user)
        serializer = EmprestimoSerializer(instance=posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        request.data['ip'] = request.META.get('REMOTE_ADDR')
        request.data['usuario'] = request.user.id
        serializer = EmprestimoSerializer(data=request.data, many=False)
        serializer.is_valid()
        serializer.save()
        return Response(request.data, status=status.HTTP_201_CREATED)
