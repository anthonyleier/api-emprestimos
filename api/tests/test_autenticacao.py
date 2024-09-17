from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class AutenticacaoValida(APITestCase):
    def setUp(self):
        username = "user"
        email = "user@gmail.com"
        password = "user2023"
        self.usuario = User.objects.create_user(username=username, email=email, password=password)

        url = reverse("auth_token")
        response = self.client.post(url, {"username": username, "password": password})

        self.token = "Token " + response.json().get('token')
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

    def test_listar(self):
        url = reverse("criar_listar_emprestimos")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse("criar_listar_pagamentos")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AutenticacaoInvalida(APITestCase):
    def setUp(self):
        self.token = "Token acf23de267660543f3dde973bc5682722cd20231"
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

    def test_listar(self):
        url = reverse("criar_listar_emprestimos")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        url = reverse("criar_listar_pagamentos")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
