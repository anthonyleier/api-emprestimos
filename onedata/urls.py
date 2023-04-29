from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from onedata.views import EmprestimosListarCriar, EmprestimoDetalhar
from onedata.views import PagamentosListarCriar, PagamentoDetalhar

urlpatterns = [
    # Obter o token de autenticação
    path('token/', obtain_auth_token, name='auth_token'),

    # Criar um novo empréstimo ou listar todos os empréstimos
    path('emprestimos/', EmprestimosListarCriar.as_view(), name='criar_listar_emprestimos'),

    # # Obter detalhes de um empréstimo específico
    path('emprestimos/<int:pk>/', EmprestimoDetalhar.as_view(), name='detalhar_emprestimo'),

    # Criar um novo pagamento e listar todos os pagamentos
    path('pagamentos/', PagamentosListarCriar.as_view(), name='criar_listar_pagamentos'),

    # # Obter detalhes de um pagamento específico
    path('pagamentos/<int:pk>/', PagamentoDetalhar.as_view(), name='detalhar_pagamento'),
]
