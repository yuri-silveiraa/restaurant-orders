from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=15)

    def __str__(self):
        return self.nome

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    item = models.CharField(max_length=100)
    qtd = models.IntegerField()
    estado = models.CharField(max_length=20, default="recebido")
    hora_recebido = models.DateTimeField(auto_now_add=True)
    hora_preparo = models.DateTimeField(null=True, blank=True)
    hora_finalizado = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente.nome}"