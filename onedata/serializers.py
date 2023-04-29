from rest_framework import serializers
from django.contrib.auth.models import User
from onedata.models import Emprestimo, Pagamento


class EmprestimoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emprestimo
        fields = ['id', 'valor_nominal', 'taxa_juros', 'ip', 'data', 'banco', 'cliente', 'usuario']
        read_only_fields = ['id', 'data']


class PagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pagamento
        fields = ['id', 'emprestimo', 'valor', 'data', 'usuario']
        read_only_fields = ['id', 'data']
