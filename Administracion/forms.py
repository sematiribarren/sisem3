from Bienes.utils import get_user_role
from django import forms
from .models import *


class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['document', 'names', 'address', 'birthday', 'income', 
                  'phone', 'sex', 'condition', 'position', 'children', 'area']
        widgets = {
            'document': forms.TextInput(attrs={'class': 'form-control', 'id': 'cedula'}),
            'names': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'id': 'telefono'}),
            'sex': forms.Select(attrs={'class': 'form-select'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'children': forms.Select(attrs={'class': 'form-select'}),
            'area': forms.Select(attrs={'class': 'form-select'}),
            'birthday': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'income': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        # Extraer el usuario de kwargs ANTES de llamar a super()
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user:
            rol = get_user_role(self.user)
            
            # Si es encargado de bienes
            if isinstance(rol, tuple) and rol[0] == 'encargado_bienes':
                area_del_encargado = rol[1]
                
                # IMPORTANTE: Filtrar las áreas disponibles
                self.fields['area'].queryset = Departamento.objects.filter(id=area_del_encargado.id)
                
                # Si es un formulario para crear nuevo (no tiene instancia)
                if not self.instance.pk:
                    self.fields['area'].initial = area_del_encargado
                
                # Deshabilitar el campo para que no lo puedan cambiar
                self.fields['area'].disabled = True
                self.fields['area'].widget.attrs['readonly'] = True


class HijoForm(forms.ModelForm):
    class Meta:
        model = Hijo
        fields = ['name', 'lastname', 'birth', 'employee']
        widgets = {
            'name': forms.TextInput(attrs={'maxlength': 50}),
            'lastname': forms.TextInput(attrs={'maxlength': 50}),
            'birth': forms.DateInput(attrs={'type': 'date'}),
            'employee': forms.Select(),
        }