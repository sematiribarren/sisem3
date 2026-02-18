from django.db import models
from django.contrib.auth.models import User


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


class Material(models.Model):
    name = models.CharField(max_length=100, blank=False)
    category = models.TextField(blank=True)
    measurement_unit = models.CharField(max_length=20, blank=False)
    minimum_stock = models.IntegerField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table='materials'

class Soliciud(models.Model):
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
