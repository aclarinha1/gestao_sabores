from django import forms
from django.forms import inlineformset_factory
from .models import Pedido, ItemPedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['forma_pagamento', 'e_encomenda', 'cliente', 'celular', 'data_hora_entrega']

class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = ['produto', 'quantidade']

ItemPedidoFormSetCreate = inlineformset_factory(
    Pedido, ItemPedido,
    form=ItemPedidoForm,
    extra=3,  # quantos formulários vazios aparecem
    can_delete=True,
    max_num = 20
)

ItemPedidoFormSetEdit = inlineformset_factory(
    Pedido, ItemPedido,
    form=ItemPedidoForm,
    extra=1,  # quantos formulários vazios aparecem
    can_delete=True
)