from decimal import Decimal
from functools import reduce
from django.utils import timezone
from onidata.models import Emprestimo, Pagamento


def get_ip_usuario(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


def calcular_IOF_emprestimo(valor_nominal):
    porcentagem_IOF = Decimal(0.38)
    valor_nominal *= 1 + porcentagem_IOF
    return round(valor_nominal, 2)


def calcular_IOF_pagamento(valor, emprestimo_id):
    porcentagem_IOF = Decimal(0.0082)
    emprestimo = Emprestimo.objects.get(pk=emprestimo_id)
    dias = (timezone.now() - emprestimo.data).days
    valor *= 1 + (porcentagem_IOF * dias)
    return round(valor, 2)


def calcular_meses_ativo(emprestimo):
    data_inicial = emprestimo.data
    data_final = timezone.now()
    diferenca_entre_datas = data_final - data_inicial

    # Numero de meses nao foi arrendondado para ser possível o cálculo do juros compostos pro rata die
    meses_ativo = Decimal(diferenca_entre_datas.days / 30)
    return meses_ativo


def calcular_saldo_devedor(emprestimo):
    meses_ativo = calcular_meses_ativo(emprestimo)

    # Juros compostos pro rata die
    saldo_devedor = emprestimo.valor_nominal * (1 + emprestimo.taxa_juros) ** meses_ativo
    pagamentos = Pagamento.objects.filter(emprestimo=emprestimo.id)

    if pagamentos:
        valores_pagamentos = [pagamento.valor for pagamento in pagamentos]

        valor_pago = reduce(lambda resultado, valor: resultado + valor, valores_pagamentos)
        saldo_devedor -= valor_pago

    return round(saldo_devedor, 2)
