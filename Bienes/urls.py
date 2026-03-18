from django.urls import path
from  .views import *
from Bienes import views


urlpatterns = [
    path('bienes/', views.bienes, name='bienes'),
    path('add_bien/<int:id>/', views.add_bien, name='add_bien'),
    



    #--------------Bienes-----------------------
    path('listado_bienes/', views.lista_bienes, name='lista_bienes'),
   

]