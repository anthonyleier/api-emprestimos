from onedata.models import Pagamento
from functools import reduce


def get_ip_usuario(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


def calcular_saldo_devedor(emprestimo):
    saldo_devedor = emprestimo.valor_nominal
    pagamentos = Pagamento.objects.filter(emprestimo=emprestimo.id)

    if pagamentos:
        valores_pagamentos = [pagamento.valor for pagamento in pagamentos]

        valor_pago = reduce(lambda resultado, valor: resultado + valor, valores_pagamentos)
        saldo_devedor -= valor_pago

    return saldo_devedor
