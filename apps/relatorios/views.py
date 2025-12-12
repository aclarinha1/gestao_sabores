from django.shortcuts import render
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta
from apps.pedidos.models import Pedido, ItemPedido
from apps.produtos.models import Produto, Categoria

def relatorios(request):
    hoje = timezone.now().date()
    mes_atual = hoje.month
    ano_atual = hoje.year
    
    # 1. VALOR TOTAL HOJE
    pedidos_hoje = Pedido.objects.filter(data_hora__date=hoje)
    total_hoje = pedidos_hoje.aggregate(total=Sum('valor_total'))['total'] or 0
    
    # 2. VALOR TOTAL SEMANA (últimos 7 dias)
    semana_passada = hoje - timedelta(days=7)
    pedidos_semana = Pedido.objects.filter(data_hora__date__gte=semana_passada)
    total_semana = pedidos_semana.aggregate(total=Sum('valor_total'))['total'] or 0
    
    # 3. VALOR TOTAL MÊS
    pedidos_mes = Pedido.objects.filter(
        data_hora__year=ano_atual,
        data_hora__month=mes_atual
    )
    total_mes = pedidos_mes.aggregate(total=Sum('valor_total'))['total'] or 0
    
    # 4. VALOR TOTAL ANO
    pedidos_ano = Pedido.objects.filter(data_hora__year=ano_atual)
    total_ano = pedidos_ano.aggregate(total=Sum('valor_total'))['total'] or 0
    
    # 5. CATEGORIA MAIS VENDIDA (no mês atual)
    categoria_mais_vendida = None
    if pedidos_mes.exists():
        # Encontra a categoria com mais itens vendidos no mês
        categorias_vendas = {}
        itens_mes = ItemPedido.objects.filter(pedido__in=pedidos_mes)
        
        for item in itens_mes:
            categoria_nome = item.produto.categoria.nome_categoria
            if categoria_nome not in categorias_vendas:
                categorias_vendas[categoria_nome] = 0
            categorias_vendas[categoria_nome] += float(item.quantidade)
        
        if categorias_vendas:
            categoria_mais_vendida = max(categorias_vendas, key=categorias_vendas.get)
    
    # 6. PRODUTO MAIS VENDIDO (no mês atual)
    produto_mais_vendido = None
    if pedidos_mes.exists():
        produto_query = ItemPedido.objects.filter(
            pedido__in=pedidos_mes
        ).values(
            'produto__nome_produto'
        ).annotate(
            total_vendido=Sum('quantidade')
        ).order_by('-total_vendido').first()
        
        if produto_query:
            produto_mais_vendido = produto_query['produto__nome_produto']
    
    context = {
        'total_hoje': total_hoje,
        'total_semana': total_semana,
        'total_mes': total_mes,
        'total_ano': total_ano,
        'categoria_mais_vendida': categoria_mais_vendida or "Nenhuma",
        'produto_mais_vendido': produto_mais_vendido or "Nenhum",
        'hoje': hoje.strftime('%d/%m/%Y'),
        'mes_atual': mes_atual,
        'ano_atual': ano_atual,
    }
    
    return render(request, 'relatorios/index.html', context)
