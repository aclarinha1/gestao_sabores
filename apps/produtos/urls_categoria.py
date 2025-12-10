from django.urls import path
from . import views

app_name = 'categoria'

urlpatterns = [
    path('', views.listar_categoria, name='listar'),
    path('<int:pk>/', views.detalhar_categoria, name='detalhar'),
    path('criar/', views.criar_categoria, name= 'criar'),
    path('<int:pk>/editar/', views.editar_categoria, name='editar'),
    path('<int:pk>/deletar/', views.deletar_categoria, name='deletar'),
]