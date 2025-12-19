from django.shortcuts import render
from apps.relatorios.utils import calcular_faturamento_hoje

def index(request):
    return render(request, 'home/index.html')


def index(request):
    total_hoje = calcular_faturamento_hoje()

    return render(request, 'home/index.html', {
        'faturamento_hoje': total_hoje
    })
