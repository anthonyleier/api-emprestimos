from rest_framework import serializers
from onedata.models import Emprestimo, Pagamento


class PagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pagamento
        fields = ['id', 'emprestimo', 'valor', 'data']
        read_only_fields = ['id', 'data']


class EmprestimoSerializer(serializers.ModelSerializer):
    pagamentos = PagamentoSerializer(many=True, read_only=True)

    class Meta:
        model = Emprestimo
        fields = ['id', 'valor_nominal', 'taxa_juros', 'ip', 'data', 'banco', 'cliente', 'pagamentos', 'usuario']
        read_only_fields = ['id', 'data']
