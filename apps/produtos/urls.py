from django.urls import path
from . import views

app_name = 'produtos'

urlpatterns = [
    path('', views.listar_produtos, name='listar'),
    path('<int:pk>/', views.detalhar_produto, name='detalhar'),
    path('criar/', views.criar_produto, name= 'criar'),
    path('<int:pk>/editar/', views.editar_produto, name='editar'),
    path('<int:pk/deletar/>', views.deletar_produto, name='deletar'),
]