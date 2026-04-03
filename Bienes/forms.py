from django import forms
from .models import *
from Bienes.utils import get_user_role

class addBien_form(forms.ModelForm):
    class Meta:
        model = Bienes_persona
        fields = ['area', 'id_worker',  'serial', 'description', 'brand', 'observation']

        widgets = {
            'area': forms.Select(attrs={'class': 'form-select'}),
            'id_worker': forms.Select(attrs={'class': 'form-select'}),
            'serial': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'observation': forms.TextInput(attrs={'class': 'form-control'}),
        }

        def __init__(self, *args, **kwargs):
            # Recibimos el usuario que está logueado
            user = kwargs.pop('user', None)
            super().__init__(*args, **kwargs)
            
            if user:
                rol = get_user_role(user)
                
                # Si es encargado de bienes
                if rol[0] == 'encargado_bienes':
                    area_del_encargado = rol[1]
                    
                    # Solo mostrar su área
                    self.fields['area'].queryset = Departamento.objects.filter(id=area_del_encargado.id)
                    self.fields['area'].initial = area_del_encargado
                    self.fields['area'].widget.attrs['readonly'] = True
                    self.fields['area'].disabled = True
                    
                    # Solo mostrar los empleados de su área
                    self.fields['id_worker'].queryset = Empleado.objects.filter(area=area_del_encargado)

