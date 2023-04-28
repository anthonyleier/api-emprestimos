from rest_framework import serializers
from emprestimos.models import Emprestimo, Pagamento


class PagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pagamento
        fields = ['id', 'emprestimo', 'valor', 'data']
        read_only_fields = fields


class EmprestimoSerializer(serializers.ModelSerializer):
    pagamentos = PagamentoSerializer(many=True, read_only=True)

    class Meta:
        model = Emprestimo
        fields = ['id', 'valor_nominal', 'taxa_juros', 'ip', 'data', 'banco', 'cliente', 'pagamentos']
        read_only_fields = fields
