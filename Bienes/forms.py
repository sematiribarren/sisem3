from django import forms
from .models import *

class addBien_form(forms.ModelForm):
    class Meta:
        model = Bienes_persona
        fields = ['area', 'id_worker', 'bm_worker', 'serial', 'description', 
                  'brand', 'condition', 'signature', 'observation']
        widgets = {
            'area': forms.Select(attrs={'class': 'form-select'}),
            'id_worker': forms.Select(attrs={'class': 'form-select', 'data-live-search': 'true'}),
            'bm_worker': forms.TextInput(attrs={'class': 'form-control'}),
            'serial': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
            'observation': forms.TextInput(attrs={'class': 'form-control'}),
            'signature': forms.ClearableFileInput(attrs={'accept': 'image/*,.pdf'}),
        }
    
    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        
        if usuario:
            if usuario.is_superuser:
                # Admin ve todos los empleados
                self.fields['id_worker'].queryset = Empleado.objects.all()
            else:
                # Usuario normal ve solo empleados de su área
                responsable = encargado_bienes.objects.filter(id_worker=usuario).first()
                if responsable:
                    self.fields['id_worker'].queryset = Empleado.objects.filter(area=responsable.area)
                else:
                    self.fields['id_worker'].queryset = Empleado.objects.none()

