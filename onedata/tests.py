from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Emprestimo, Pagamento
from django.contrib.auth.models import User
from decimal import Decimal


class EmprestimoTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_criar_emprestimo(self):
        """
        Certifique-se de que podemos criar um empréstimo.
        """
        url = reverse('emprestimos')
        data = {
            'valor_nominal': Decimal(1000),
            'taxa_juros': Decimal(0.1),
            'ip': '127.0.0.1',
            'data_solicitacao': '2023-04-28',
            'banco': 'Banco XPTO',
            'cliente': 'Fulano de Tal'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Emprestimo.objects.count(), 1)
        self.assertEqual(Emprestimo.objects.get().valor_nominal, Decimal(1000))