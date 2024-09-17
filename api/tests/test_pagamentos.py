from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from api.models import Emprestimo, Pagamento
from api.serializers import PagamentoSerializer


class PagamentosListarCriarTest(APITestCase):
    def setUp(self):
        username = "wilson.pilar"
        email = "wilson.pilar@gmail.com"
        password = "wilson2023"
        self.usuario = User.objects.create_user(username=username, email=email, password=password)

        url = reverse("auth_token")
        response = self.client.post(url, {"username": username, "password": password})

        self.token = "Token " + response.json().get('token')
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

        self.emprestimo = Emprestimo.objects.create(
            valor_nominal=1000,
            taxa_juros=0.05,
            banco="Banco do Brasil",
            cliente="José da Silva",
            data=timezone.now(),
            ip="127.0.0.1",
            usuario=self.usuario
        )

        self.pagamento_dados = {'valor': '100.00', 'emprestimo': 1}
        self.pagamento_dados_invalidos = {'valor': 'invalid', 'emprestimo': 1}

    def test_listar_pagamentos(self):
        pagamento = Pagamento.objects.create(emprestimo_id=1, valor=100, data=timezone.now(), usuario=self.usuario)
        url = reverse('criar_listar_pagamentos')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = PagamentoSerializer(instance=pagamento)
        self.assertIn(serializer.data, response.data)

    def test_criar_pagamento(self):
        url = reverse('criar_listar_pagamentos')
        response = self.client.post(url, self.pagamento_dados)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Pagamento.objects.count(), 1)
        self.assertEqual(Pagamento.objects.first().valor, 100)
        self.assertEqual(Pagamento.objects.first().usuario, self.usuario)

    def test_criar_pagamento_com_dados_invalidos(self):
        url = reverse('criar_listar_pagamentos')
        response = self.client.post(url, self.pagamento_dados_invalidos)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Pagamento.objects.count(), 0)


class PagamentoDetalharTest(APITestCase):
    def setUp(self):
        username = "wilson.pilar"
        email = "wilson.pilar@gmail.com"
        password = "wilson2023"
        self.usuario = User.objects.create_user(username=username, email=email, password=password)

        url = reverse("auth_token")
        response = self.client.post(url, {"username": username, "password": password})

        self.token = "Token " + response.json().get('token')
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

        self.emprestimo = Emprestimo.objects.create(
            valor_nominal=1000,
            taxa_juros=0.05,
            banco="Banco do Brasil",
            cliente="José da Silva",
            data=timezone.now(),
            ip="127.0.0.1",
            usuario=self.usuario
        )

        self.pagamento = Pagamento.objects.create(valor=100.00, emprestimo=self.emprestimo, usuario=self.usuario)

    def test_detalhar_pagamento(self):
        url = reverse('detalhar_pagamento', kwargs={'pk': self.pagamento.pk})
        response = self.client.get(url)

        pagamento = PagamentoSerializer(self.pagamento).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, pagamento)

    def test_atualizar_pagamento(self):
        pagamento_dados = {
            'valor': 200,
            "emprestimo": self.emprestimo.id
        }
        url = reverse('detalhar_pagamento', kwargs={'pk': self.pagamento.pk})
        response = self.client.put(url, pagamento_dados)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['valor'], 200)
        self.assertEqual(response.data['emprestimo'], self.emprestimo.id)

    def test_deletar_pagamento(self):
        url = reverse('detalhar_pagamento', kwargs={'pk': self.pagamento.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Pagamento.objects.filter(pk=self.pagamento.pk).exists())
