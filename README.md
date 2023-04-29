# Onidata Desafio

Usando [Django](https://www.djangoproject.com/) e [Django REST framework](https://www.django-rest-framework.org/) desenvolva uma API REST que permita usuários gerenciar empréstimos.

## Coisas a fazer
- Aplicar Dockerfile
- Ajustar readme
- Atualizar arquivo requirements.txt
- Criar env
- Validar . nos valores reais
- Testes automatizados

## Endpoints

### Empréstimos

| Método | Endpoint | Descrição |
| --- | --- | --- |
| GET | /api/emprestimos/ | Retorna uma lista de todos os empréstimos do usuário autenticado. |
| GET | /api/emprestimos/{id}/	 | Retorna um empréstimo específico pelo seu ID, desde que o usuário autenticado seja o dono desse empréstimo. |
| POST | /api/emprestimos/ | Cria um novo empréstimo. |
| PUT | /api/emprestimos/{id}/ | Atualiza um empréstimo existente pelo seu ID, desde que o usuário autenticado seja o dono desse empréstimo. |
| DELETE | /api/emprestimos/{id}/ | Exclui um empréstimo existente pelo seu ID, desde que o usuário autenticado seja o dono desse empréstimo. |

### Pagamentos

| Método | Endpoint | Descrição |
| --- | --- | --- |
| GET | /api/pagamentos/ | Retorna uma lista de todos os pagamentos do usuário autenticado. |
| GET | /api/pagamentos/{id}/ | Retorna um pagamento específico pelo seu ID, desde que o usuário autenticado seja o dono desse pagamento. |
| POST | /api/pagamentos/ | Cria um novo pagamento para um determinado empréstimo. |
| PUT | /api/pagamentos/{id}/ | Atualiza um pagamento existente pelo seu ID, desde que o usuário autenticado seja o dono desse pagamento. |
| DELETE | /api/pagamentos/{id}/ | Exclui um pagamento existente pelo seu ID, desde que o usuário autenticado seja o dono desse pagamento. |

### Autenticação

| Método | Endpoint | Descrição |
| --- | --- | --- |
| POST | /api/token/ | Retorna um token de autenticação para o usuário com as credenciais fornecidas. |

## Crtérios de aceite
* Usuários devem ser capazes de inserir empréstimos e seus respectivos pagamentos (OK)
* Usuários devem ser capazer de visualizar seus empréstimos e pagamentos (OK)
* Usuários devem ser capazes de visualizar o [saldo devedor](https://duckduckgo.com/?q=saldo+devedor) de cada um dos seus empréstimos (OK)
    * Você pode decidir onde e como mostrar a informação (OK)
    * O saldo devedor nada mais é do que o quanto o cliente ainda deve para o banco (OK)
    * O saldo devedor deve considerar a taxa de juros do empréstimo e descontar o que já foi pago (OK)
* Usuários não podem ver ou editar empréstimos ou pagamentos de outros usuários (OK)
* A autenticação da API deve ser feita via token (OK)
    * Não é necessário desenvolver endpoints para criação/gerenciamento de usuários (OK)
* Os empréstimos devem conter no mínimo as informações abaixo: (OK)
    * Identificador - um identificador aleatório gerado automaticamente (OK)
    * Valor nominal - o valor emprestado pelo banco (OK)
    * Taxa de juros - a taxa de juros mensal do empréstimo (OK)
    * Endereço de IP - endereço de IP que cadastrou o empréstimo (OK)
    * Data de solicitação - a data em que o empréstimo foi solicitado (OK)
    * Banco - informações do banco que emprestou o dinheiro (pode ser um simples campo de texto) (OK)
    * Cliente - informações do cliente que pegou o empréstimo (pode ser um simples campo de texto) (OK)
* Os pagamentos devem conter no mínimo as informações abaixo: (OK)
    * Identificador do empréstimo (OK)
    * Data do pagamento (OK)
    * Valor do pagamento (OK)
* Testes
    * As funcionalidade principais devem estar com [testes](https://docs.djangoproject.com/en/3.1/topics/testing/) escritos
    * Você pode decidir quais os testes que mais agregam valor ao projeto

## Extra (opcional)
* Cálculo do saldo devedor usando [juros compostos](https://duckduckgo.com/?q=juros+compostos) [pro rata dia](https://duckduckgo.com/?q=pro+rata+dia). (OK)
* Expandir o modelo financeiro adicionando [IOF](https://duckduckgo.com/?q=imposto+sobre+operações+financeiras+operação+de+crédito), seguro, etc... (OK)

## Informações adicionais
Você pode organizar a API e o banco de dados da maneira que achar que faz mais sentido. Além disso, sinta-se a vontade para adicionar ferramentas ou funcionalidades que ache relevante. (OK)

## O que vamos avaliar
1. O cumprimento dos requisitos obrigatórios
2. A forma que o código está organizado
3. O domínio das funcionalidade do Django e DRF
4. A abordagem e abrangência dos testes do código
5. A simplicidade da solução
6. Aderência a [PEP 8](https://duckduckgo.com/?q=pep8)
7. A implementação de requisitos opcionais
8. A implementação de funcionalidades extras
