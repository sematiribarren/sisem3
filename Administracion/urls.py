from django.urls import path
from  .views import *
from Administracion import views

urlpatterns = [
    path('home/', Home, name='home'),
    



    #--------------Funcionarios-----------------------
    path('funcionarios/', Funcionarios, name='funcionarios'),
    path('listado_funcionarios/', views.lista_funcionarios, name='lista_funcionarios'),
    path('crear_funcionario/', views.crear_funcionario, name='crear_funcionario'),
]