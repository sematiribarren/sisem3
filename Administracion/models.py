from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Departamento(models.Model):
   id = models.AutoField(primary_key=True)
   name = models.CharField(max_length=50, blank=False)
   responsible = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='department_responsible')
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   def __str__(self):
    return self.name
   
   class Meta:
        db_table = 'departments'
   
class Empleado(models.Model):
    id = models.AutoField(primary_key=True)
    document=models.CharField(unique=True, max_length=10, blank=False)
    names = models.CharField(max_length=150, blank=False)
    surnames=models.CharField(max_length=150, blank=False)
    address = models.CharField(max_length=120, blank=False)
    birth = models.DateField(blank=False)
    income = models.DateField(blank=False)
    phone = models.CharField(max_length=20, blank=False)
    SEXO_CHOICES=(

        ('M', 'Masculino'),
        ('F', 'Femenino'),
    )
    sex=models.CharField(choices=SEXO_CHOICES, max_length=10, default='')
    condicion_choice=(

        ('act', 'Activo'),
        ('inact','Inactivo'),
        ('rep','Reposo'),
        ('mat','Maternidad'),
        ('vac', 'Vacaciones'),
    )
    condition = models.CharField(choices=condicion_choice, max_length=20, blank=False, default='activo')
    position = models.CharField(max_length=100, blank=False)
    children = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    area = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} {self.document} ({self.names} {self.surnames})"
    
    class Meta:
        db_table = 'employees'

class Hijo(models.Model):
    name = models.CharField(max_length=50, blank=False)
    lastname = models.CharField(max_length=50, blank=False)
    birth = models.DateField(blank=False)
    employee = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + ' ' + self.lastname 
    
    class Meta:
        db_table='children'


class Catalogo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False)
    category = models.TextField(blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table='catalog'

class Presentacion(models.Model):
    id = models.AutoField(primary_key=True)
    choices_unit = (
        ('unidad', 'Unidad'),
        ('caja', 'Caja'),
        ('paquete', 'Paquete'),
    )
    material = models.ForeignKey(Catalogo, on_delete=models.CASCADE)
    unit = models.CharField(choices=choices_unit, max_length=20, blank=False)
    content_amount = models.PositiveIntegerField(validators=[MinValueValidator(1)], help_text="¿Cuántas unidades de la presentación base contiene? Ej. 20 si 1 Caja contiene 20 unidades.")
    base_presentation = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='derived_presentations', limit_choices_to={'presentacion_base__isnull': True}, help_text="Solo llenar si esta presentación NO es la base (ej. Caja -> Unidad).")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.material.name} - {self.unit}"
    
    class Meta:
        db_table='presentation'

class Inventario(models.Model):
    id = models.AutoField(primary_key=True)
    presentation = models.OneToOneField(Presentacion, on_delete=models.CASCADE)
    existing_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    stock_min = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    location = models.CharField(max_length=100, blank=True)
    last_update = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.presentation}: {self.existing_quantity}"
    
    class Meta:
        db_table='inventory'

class Solicitud(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.CharField(unique=True, max_length=20, blank=False)
    area = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status_choice = (
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    )
    date_approval = models.DateField(blank=True, null=True)
    status = models.CharField(choices=status_choice, max_length=20, default='pendiente')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_requests')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.number} - {self.status}"
    class Meta:
        db_table='requests'

class MovimientoInventario(models.Model):
    id = models.AutoField(primary_key=True)
    movement_type_choice = (
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
        ('ajuste', 'Ajuste'),
    )
    presentation = models.ForeignKey(Presentacion, on_delete=models.PROTECT)
    type = models.CharField(choices=movement_type_choice, max_length=20, blank=False)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)], help_text="Cantidad de la presentación base (ej. si es Caja, indicar cuántas unidades base equivalen).")
    resulting_stock = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], help_text="Stock resultante después de este movimiento.")
    date = models.DateTimeField(auto_now_add=True)
    request = models.ForeignKey(Solicitud, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.type} - {self.presentation} - {self.quantity}"
    
    class Meta:
        db_table='inventory_movements'

class DetalleSolicitud(models.Model):
    id = models.AutoField(primary_key=True)
    request = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name='details')
    presentation = models.ForeignKey(Presentacion, on_delete=models.PROTECT)
    requested_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    delivered_quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.request.number} - {self.presentation} - {self.requested_amount}"
    
    class Meta:
        db_table='request_details'


