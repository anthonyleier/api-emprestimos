from onedata.models import Pagamento
from functools import reduce
from datetime import datetime


def get_ip_usuario(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


def calcular_meses_ativo(emprestimo):
    data_inicial = emprestimo.data.replace(tzinfo=None)
    data_final = datetime.now().replace(tzinfo=None)
    diferenca_entre_datas = data_final - data_inicial

    # Numero de meses nao foi arrendondado para ser possível o cálculo do juros compostos pro rata die
    meses_ativo = diferenca_entre_datas.days / 30
    return meses_ativo


def calcular_saldo_devedor(emprestimo):
    meses_ativo = calcular_meses_ativo(emprestimo)
    saldo_devedor = emprestimo.valor_nominal * (1 + emprestimo.taxa_juros) ** meses_ativo
    pagamentos = Pagamento.objects.filter(emprestimo=emprestimo.id)

    if pagamentos:
        valores_pagamentos = [pagamento.valor for pagamento in pagamentos]

        valor_pago = reduce(lambda resultado, valor: resultado + valor, valores_pagamentos)
        saldo_devedor -= valor_pago

    return saldo_devedor
