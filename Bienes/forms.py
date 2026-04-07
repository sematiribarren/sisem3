from django import forms
from .models import *
from Bienes.utils import get_user_role

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
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user:
            rol = get_user_role(self.user)
            
            if isinstance(rol, tuple) and rol[0] == 'encargado_bienes':
                area_del_encargado = rol[1]
                
                # Filtrar área
                self.fields['area'].queryset = Departamento.objects.filter(id=area_del_encargado.id)
                self.fields['area'].initial = area_del_encargado
                self.fields['area'].disabled = True
                
                # Filtrar empleados y ordenar por nombre
                empleados_filtrados = Empleado.objects.filter(area=area_del_encargado).order_by('names')
                self.fields['id_worker'].queryset = empleados_filtrados
                
                # Personalizar el texto que se muestra en el select
                self.fields['id_worker'].label_from_instance = self.empleado_label
                
                cantidad = empleados_filtrados.count()
                self.fields['id_worker'].help_text = f"Seleccione un empleado del área {area_del_encargado.name} ({cantidad} empleados disponibles)"
    
    def empleado_label(self, obj):
        """Personaliza cómo se muestra cada empleado en el select"""
        return f"{obj.names} - {obj.document} ({obj.position})"

