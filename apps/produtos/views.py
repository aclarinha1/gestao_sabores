from django.shortcuts import render, get_object_or_404, redirect
from .models import Produto, Categoria
from .forms import ProdutoForm, CategoriaForm

#views produtos
def listar_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'produtos/listar_produtos.html', {'produtos': produtos})

def detalhar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    return render(request, 'produtos/detalhar_produto.html', {'produto': produto})

def criar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('produtos:listar')
    else:
        form = ProdutoForm()
        return render(request, 'produtos/form.html', {'form': form, 'acao':'Criar'})
    
def editar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('produtos:listar')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'produtos/form.html', {'form': form, 'acao':'Editar'})

def deletar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        produto.delete()
        return redirect('produtos:lista')
    return render(request, 'produtos/deletar_produto.html', {'produto': produto})

