from django.db import models
from Administracion.models import *
# Create your models here.


class Bienes (models.Model):
    id = models.AutoField(primary_key=True)
    bm = models.CharField (max_length=200, unique=True, blank=False)
    description = models.CharField (max_length=100, blank=True)
    serial = models.CharField (max_length=200, unique=True)
    brand = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=100, blank=True)
    purchase_date = models.DateField()
    invoice = models.CharField(max_length= 70, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    account = models.CharField(max_length=100, blank=True)
    entity = models.CharField(max_length=100, blank=True)
    rif = models.CharField(max_length=100, blank=True)
    observacion = models.CharField(max_length=100, blank=True)
    tipoC = (
        ('good', 'Bueno'),
        ('damaged', 'Dañado'),    
    )
    status = models.CharField(max_length=50, choices=tipoC, default='good')
 
    class Meta:
        db_table = 'bienes'
        ordering = ['-bm']

    def __str__(self):
        return f"Bien #{self.bm} - ({self.description})"
    

class Bienes_persona(models.Model):
    id = models.AutoField(primary_key=True)
    area = models.ForeignKey(Departamento, on_delete=models.CASCADE, blank=False)
    id_worker = models.ForeignKey(Empleado, on_delete=models.CASCADE, max_length=20, blank=True)
    cargo_area = models.CharField(max_length=100, blank=True)
    id_bien = models.ForeignKey(Bienes, on_delete=models.CASCADE, max_length=20, blank=True)
    bm_worker = models.CharField(max_length=100, blank=True)
    serial = models.CharField(max_length=100, blank=True)
    description = models.CharField (max_length=100, blank=True)
    brand = models.CharField(max_length=100, blank=True)
    condition_choices = (
        ('good', 'Bueno'),
        ('damaged', 'Dañado'),    
    )
    condition = models.CharField(max_length=50, choices=condition_choices, default='good')
    signature = models.FileField(upload_to ='Firma_persona/',  blank=True)
    observation = models.CharField(max_length=100, blank=True)
    estatus = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'bienes_persona'
        ordering = ['-id']

    def __str__(self):
        return f"Bien #{self.bm_worker} - ({self.description})"


class Bienes_movimientos (models.Model):
    id = models.AutoField(primary_key=True)
    transfer_date = models.DateField()
    id_bien = models.ForeignKey(Bienes, on_delete=models.CASCADE, max_length=20, blank=True)
    description = models.CharField (max_length=200, blank=True)
    mov_choices = (
        ('Transfer', 'Traslado'),
        ('Return', 'Devolucion'),
        ('Assignment', 'Asignacion'),
        
    )
    mov_type = models.CharField(max_length=50, choices=mov_choices, default='Transfer') 
    type_choices = (
        ('Personal', 'Personal'),
        ('EntePublico', 'EntePublico'),
        
    )
    Type = models.CharField(max_length=50, choices=type_choices, default='Personal')
    origin_entity = models.CharField (max_length=200, blank=True)
    origin_area = models.ForeignKey(Departamento, on_delete=models.CASCADE, blank=False)
    id_worker = models.ForeignKey(Empleado, on_delete=models.CASCADE, max_length=20, blank=True)
    rif_ente = models.CharField (max_length=100, blank=True)
    nomb_respon_ant = models.CharField (max_length=100, blank=True)
    dest_entity = models.CharField (max_length=200, blank=True)
    dest_area = models.ForeignKey(Departamento, on_delete=models.CASCADE, blank=False, related_name='dest_area')
    id_worker_tow = models.ForeignKey(Empleado, on_delete=models.CASCADE, max_length=20, blank=True, related_name='id_worker_tow')
    worker = models.CharField (max_length=100, blank=True)
    observation = models.CharField (max_length=100, blank=True) 
    condition_choices = (
        ('good', 'Bueno'),
        ('damaged', 'Dañado'),    
    )
    condition = models.CharField(max_length=50, choices=condition_choices, default='good')
    status = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'bienes_movimientos'
        ordering = ['-transfer_date']

    def __str__(self):
        return f"Movimiento de Bien #{self.id_bien} - ({self.description})"
    

class Bienes_informes (models.Model):
    id = models.AutoField(primary_key=True)
    area = models.ForeignKey(Departamento, on_delete=models.CASCADE, blank=False)
    id_bien = models.ForeignKey(Bienes, on_delete=models.CASCADE, max_length=20, blank=True)
    date = models.DateField()
    description = models.CharField (max_length=200, blank=True)
    diagnosis = models.CharField (max_length=300, blank=True)
    signature = models.FileField(upload_to ='Firma_Informe/',  blank=True)
    status = models.BooleanField()

    class Meta:
        db_table = 'bienes_informes'
        ordering = ['-date']

    def __str__(self):
        return f"Informe de Bien #{self.id_bien} - ({self.description})"