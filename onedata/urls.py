from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from onedata.views import EmprestimoListCreate
from onedata.views import PagamentoListCreate

urlpatterns = [
    # Obter o token de autenticação
    path('token/', obtain_auth_token, name='auth_token'),

    # Criar um novo empréstimo ou listar todos os empréstimos
    path('emprestimos/', EmprestimoListCreate.as_view(), name='criar_lista_emprestimos'),

    # # Obter detalhes de um empréstimo específico
    # path('emprestimos/<int:pk>/', EmprestimoDetail.as_view(), name='detalhar_emprestimos'),

    # Criar um novo pagamento e listar todos os pagamentos
    path('pagamentos/', PagamentoListCreate.as_view(), name='criar_listar_pagamentos'),

    # # Obter detalhes de um pagamento específico
    # path('pagamentos/<int:pk>/', PagamentoDetail.as_view(), name='detalhar_pagamento'),
]
