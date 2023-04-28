from django.db import models
from django.contrib.auth.models import User


class Emprestimo(models.Model):
    valor_nominal = models.DecimalField(max_digits=10, decimal_places=2)
    taxa_juros = models.DecimalField(max_digits=4, decimal_places=2)
    ip = models.GenericIPAddressField()
    data = models.DateField()
    banco = models.CharField(max_length=50)
    cliente = models.CharField(max_length=50)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id} | {self.valor} | {self.usuario}"


class Pagamento(models.Model):
    emprestimo = models.ForeignKey(Emprestimo, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()

    def __str__(self):
        return f"{self.id} | {self.valor} | {self.emprestimo.id} | {self.emprestimo.usuario}"
