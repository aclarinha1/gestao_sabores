from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Pedido, ItemPedido, Produto
from .forms import PedidoForm, ItemPedidoForm, ItemPedidoFormSetCreate, ItemPedidoFormSetEdit

def listar_pedidos(request):
    pedidos = Pedido.objects.all().order_by('-data_hora')
    return render(request, 'pedidos/listar_pedidos.html', {'pedidos': pedidos})

def detalhar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    itens = pedido.itens.all()
    return render(request, 'pedidos/detalhar_pedido.html', {'pedido': pedido, 'itens': itens, 'now': timezone.now()})

def criar_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        formset = ItemPedidoFormSetCreate(request.POST)
        
        if form.is_valid() and formset.is_valid():
            # Salva o pedido
            pedido = form.save()
            
            # Salva os itens usando o formset
            formset.instance = pedido
            formset.save()
            
            # Atualiza o valor total
            pedido.atualizar_valor_total()
            
            messages.success(request, f'Pedido #{pedido.id} criado com sucesso!')
            return redirect('pedidos:detalhar', pk=pedido.id)
    else:
        form = PedidoForm()
        # Inicializa com 3 forms vazios (ou quantos você quiser)
        formset = ItemPedidoFormSetCreate(queryset=ItemPedido.objects.none())
    
    return render(request, 'pedidos/form.html', {
        'form': form, 
        'formset': formset,
        'titulo': 'Criar Novo Pedido'
    })

def editar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    
    if request.method == 'POST':
        print("POST recebido!")
        form = PedidoForm(request.POST, instance=pedido)
        formset = ItemPedidoFormSetEdit(request.POST, instance=pedido)
        
        print("Form válido?", form.is_valid())  # Debug
        print("Formset válido?", formset.is_valid())  # Debug

        if form.is_valid() and formset.is_valid():
            print("Salvando...")
            # Salva o pedido
            pedido = form.save()
            
            # Salva os itens do pedido (o formset já sabe que é para este pedido)
            formset.save()
            
            # Atualiza o valor total
            pedido.atualizar_valor_total()
            
            return redirect('pedidos:listar')
        else:
            # Adicione isto para debug - mostra erros no console
            print("Form errors:", form.errors)
            print("Formset errors:", formset.errors)
    else:
        form = PedidoForm(instance=pedido)
        formset = ItemPedidoFormSetEdit(instance=pedido)
    
    return render(request, 'pedidos/editar_pedido.html', {
        'form': form, 
        'formset': formset,
        'pedido': pedido  # Adicione isto também
    })

def deletar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.method == 'POST':
        pedido.delete()
        return redirect('pedidos:listar')
    return render(request, 'pedidos/deletar_pedido.html', {'pedido': pedido})