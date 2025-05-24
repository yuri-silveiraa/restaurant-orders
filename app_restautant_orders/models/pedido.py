from django.db import models
from .cliente import Cliente

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    item = models.CharField(max_length=255)
    quantidade = models.IntegerField()
    data = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pedido #{self.id} de {self.cliente.nome}"