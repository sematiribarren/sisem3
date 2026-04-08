from Administracion.models import Empleado
from .models import encargado_bienes

def get_empleados_por_area_usuario(usuario):
    """Retorna queryset de empleados según el tipo de usuario"""
    # Si es administrador, retorna todos los empleados
    if usuario.is_superuser:
        return Empleado.objects.all()
    
    # Si no es admin, retorna solo empleados de su área
    responsable = encargado_bienes.objects.filter(id_worker=usuario).first()
    if responsable:
        return Empleado.objects.filter(area=responsable.area)
    
    # Si no tiene área asignada, retorna vacío
    return Empleado.objects.none()

def get_user_role(user):

    if not user or not user.is_authenticated:
        return 'empleado_normal'
    
    if user.is_superuser or user.is_staff:
        return 'admin'
    
    try:
        encargado = encargado_bienes.objects.get(id_worker=user, status=True)
        print(f"Usuario {user.username} es encargado del área: {encargado.area.name}")
        return ('encargado_bienes', encargado.area)
    except encargado_bienes.DoesNotExist:
        print(f"Usuario {user.username} es empleado normal")
        return 'empleado_normal'
    except Exception as e:
        print(f"Error al verificar rol: {e}")
        return 'empleado_normal'