# mi_app/utils.py

from django.contrib.auth.models import User
from .models import encargado_bienes

def get_user_role(user):

    if not user or not user.is_authenticated:
        return 'empleado_normal'
    
    # Si es administrador
    if user.is_superuser or user.is_staff:
        return 'admin'
    
    # Verificar si es encargado de bienes
    try:
        encargado = encargado_bienes.objects.get(id_worker=user, status=True)
        # Para depuración - puedes imprimir en consola
        print(f"Usuario {user.username} es encargado del área: {encargado.area.name}")
        return ('encargado_bienes', encargado.area)
    except encargado_bienes.DoesNotExist:
        print(f"Usuario {user.username} es empleado normal")
        return 'empleado_normal'
    except Exception as e:
        print(f"Error al verificar rol: {e}")
        return 'empleado_normal'