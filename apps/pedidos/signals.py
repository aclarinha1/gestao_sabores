from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ItemPedido, Pedido

@receiver(post_save, sender=ItemPedido)
def atualizar_pedido_apos_salvar(sender, instance, **kwargs):
    instance.pedido.atualizar_valor_total()

@receiver(post_delete, sender=ItemPedido)
def atualizar_pedido_apos_deletar(sender, instance, **kwargs):
    instance.pedido.atualizar_valor_total()