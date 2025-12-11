from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path('', views.listar_pedidos, name='listar'),
    path('<int:pk>/', views.detalhar_pedido, name='detalhar'),
    path('criar/', views.criar_pedido, name= 'criar'),
    path('<int:pk>/editar/', views.editar_pedido, name='editar'),
    path('<int:pk>/deletar/', views.deletar_pedido, name='deletar'),
]