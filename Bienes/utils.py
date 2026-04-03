from django.contrib.auth.models import User
from .models import encargado_bienes
from Administracion.models import Departamento

def get_user_role(user):
 
    if user.is_superuser or user.is_staff:
        return 'admin'
    
    try:
       
        encargado = encargado_bienes.objects.get(id_worker=user, status=True)
       
        return ('encargado_bienes', encargado.area)
    except encargado_bienes.DoesNotExist:
        
        return 'empleado_normal'