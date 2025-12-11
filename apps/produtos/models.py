from django.db import models

# Create your models here.
class Categoria(models.Model):
    nome_categoria = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    def __str__(self):
        return self.nome_categoria
    
class Produto(models.Model):
    nome_produto = models.CharField(max_length=100)
    preco_unitario = models.DecimalField(max_digits=6, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='produtos')
    def __str__(self):
        return self.nome_produto


