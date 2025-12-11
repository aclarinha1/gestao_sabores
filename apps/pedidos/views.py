from django.shortcuts import render, get_object_or_404, redirect
from .models import Pedido, ItemPedido, Produto
from .forms import PedidoForm, ItemPedidoForm, ItemPedidoFormSetCreate, ItemPedidoFormSetEdit

def listar_pedidos(request):
    pedidos = Pedido.objects.all().order_by('-data_hora')
    return render(request, 'pedidos/listar_pedidos.html', {'pedidos': pedidos})

def detalhar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    itens = pedido.itens.all()
    return render(request, 'pedidos/detalhar_pedido.html', {'pedido': pedido, 'itens': itens})

def criar_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        formset = ItemPedidoFormSetCreate(request.POST)
        if form.is_valid() and formset.is_valid():
            pedido = form.save()
            formset.instance = pedido

            itens = formset.save(commit=False)
            for item in itens:
                item.save()  # calcula subtotal no save()
            formset.save_m2m()

            # atualiza total explicitamente
            pedido.atualizar_valor_total()

            return redirect('pedidos:listar')
    else:
        form = PedidoForm()
        formset = ItemPedidoFormSetCreate()
    return render(request, 'pedidos/form.html', {'form': form, 'formset': formset})

def editar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido)
        formset = ItemPedidoFormSetEdit(request.POST, instance=pedido)  # já passa o pedido aqui
        if form.is_valid() and formset.is_valid():
            form.save()

            itens = formset.save(commit=False)
            for item in itens:
                item.pedido = pedido
                item.save()

# processa exclusões
            for item in formset.deleted_objects:
                item.delete()
            formset.save_m2m()

            pedido.atualizar_valor_total()
            return redirect('pedidos:listar')
    else:
        form = PedidoForm(instance=pedido)
        formset = ItemPedidoFormSetEdit(instance=pedido)
    return render(request, 'pedidos/editar_pedido.html', {'form': form, 'formset': formset})

def deletar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.method == 'POST':
        pedido.delete()
        return redirect('pedidos:listar')
    return render(request, 'pedidos/deletar_pedido.html', {'pedido': pedido})