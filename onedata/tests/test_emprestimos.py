from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from onedata.models import Emprestimo
from onedata.serializers import EmprestimoSerializer
from datetime import datetime
from django.utils import timezone


class EmprestimosListarCriarTestCase(APITestCase):
    def setUp(self):
        username = "alex.silva"
        email = "alex.silva@gmail.com"
        password = "alex2023"
        self.user = User.objects.create_user(username=username, email=email, password=password)

        url = reverse("auth_token")
        response = self.client.post(url, {"username": username, "password": password})

        self.token = "Token " + response.json().get('token')
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        self.emprestimo_dados = {
            "valor_nominal": 1000,
            "taxa_juros": 0.05,
            "banco": "Banco do Brasil",
            "cliente": "Júlia Gonçalves Oliveira",
        }

    def test_criar_emprestimo(self):
        url = reverse("criar_listar_emprestimos")
        response = self.client.post(url, self.emprestimo_dados)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Emprestimo.objects.count(), 1)

        emprestimo = Emprestimo.objects.first()
        self.assertEqual(emprestimo.valor_nominal, self.emprestimo_dados["valor_nominal"])
        self.assertEqual(float(emprestimo.taxa_juros), self.emprestimo_dados["taxa_juros"])
        self.assertEqual(emprestimo.banco, self.emprestimo_dados["banco"])
        self.assertEqual(emprestimo.cliente, self.emprestimo_dados["cliente"])

    def test_listar_emprestimos(self):
        emprestimo = Emprestimo.objects.create(
            valor_nominal=1000,
            taxa_juros=0.05,
            banco="Banco do Brasil",
            cliente="José da Silva",
            data=timezone.make_aware(datetime.now()),
            ip="127.0.0.1",
            usuario=self.user
        )

        url = reverse("criar_listar_emprestimos")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = EmprestimoSerializer(instance=emprestimo)
        self.assertIn(serializer.data, response.data)


class EmprestimoDetalharTestCase(APITestCase):
    def setUp(self):
        username = "alex.silva"
        email = "alex.silva@gmail.com"
        password = "alex2023"
        self.user = User.objects.create_user(username=username, email=email, password=password)

        url = reverse("auth_token")
        response = self.client.post(url, {"username": username, "password": password})

        self.token = "Token " + response.json().get('token')
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        self.emprestimo_dados = {
            "valor_nominal": 1000,
            "taxa_juros": 0.05,
            "banco": "Banco do Brasil",
            "cliente": "Júlia Gonçalves Oliveira",
            "data": timezone.make_aware(datetime.now()),
            "ip": "127.0.0.1",
        }

        self.emprestimo = Emprestimo.objects.create(**self.emprestimo_dados, usuario=self.user)

    def test_detalhar_emprestimo(self):
        url = reverse('detalhar_emprestimo', kwargs={'pk': self.emprestimo.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, EmprestimoSerializer(self.emprestimo).data)

    def test_atualizar_emprestimo(self):
        emprestimo_dados = {
            'valor_nominal': 1500.00,
            'taxa_juros': 0.04,
            'ip': '127.0.0.1',
            'banco': 'Banco Teste',
            'cliente': 'Cliente Teste',
            'usuario': self.user.pk
        }
        url = reverse('detalhar_emprestimo', kwargs={'pk': self.emprestimo.pk})
        response = self.client.put(url, emprestimo_dados)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['valor_nominal'], '1500.00')
        self.assertEqual(response.data['taxa_juros'], '0.04')

    def test_deletar_emprestimo(self):
        url = reverse('detalhar_emprestimo', kwargs={'pk': self.emprestimo.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Emprestimo.objects.filter(pk=self.emprestimo.pk).exists())