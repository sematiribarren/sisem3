from django.urls import path
from  .views import *
from Bienes import views


urlpatterns = [
    path('bienes/', views.bienes, name='bienes'),
    path('add_bien/<int:id>/', views.add_bien, name='add_bien'),
    path('bienes_detallado/<int:id>/', views.bienes_detallado, name='bienes_detallado'),
    path('borrar_asignacion/<int:id>/', views.borrar_asignacion, name='borrar_asignacion'),
    



    #--------------Bienes-----------------------
    path('listado_bienes/', views.lista_bienes, name='lista_bienes'),
    path('listado_bienes_det/', views.lista_bienes_det, name='lista_bienes_det'),
    
   

]