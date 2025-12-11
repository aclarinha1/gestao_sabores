from django.db import models
from apps.produtos.models import Produto

# Create your models here.

class Pedido(models.Model):
    data_hora = models.DateTimeField(auto_now_add=True)
    valor_total = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    forma_pagamento = models.CharField(max_length=50)
    e_encomenda = models.BooleanField(default=False)
    #quem sabe colocar um atributo e_fiado, do tipo booleano, afinal, fiado não é tipo de pagamento
    cliente = models.CharField(max_length=100, blank=True)
    celular = models.CharField(max_length=15, blank=True)
    data_hora_entrega = models.DateTimeField(null=True, blank=True)
    
    def atualizar_valor_total(self):
        total = sum(item.subtotal for item in self.itens.all())
        self.valor_total = total
        self.save(update_fields=['valor_total'])

    def __str__(self):
        return f"Pedido #{self.id} - {self.data_hora.strftime('%d/%m/%Y %H:%M')}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.DecimalField(max_digits=3, decimal_places=2)
    subtotal = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.subtotal = self.quantidade * self.produto.preco_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantidade} x {self.produto.nome_produto}"