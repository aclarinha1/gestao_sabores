from django.db.models import Sum
from django.utils import timezone
from apps.pedidos.models import Pedido

def calcular_faturamento_hoje():
    hoje = timezone.localdate()

    total = Pedido.objects.filter(
        data_hora__date=hoje
    ).aggregate(
        total=Sum('valor_total')
    )['total']

    return total or 0
