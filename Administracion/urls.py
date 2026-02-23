from django.urls import path
from  .views import *
from Administracion import views

urlpatterns = [
    path('home/', Home, name='home'),
    
]