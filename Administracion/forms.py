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