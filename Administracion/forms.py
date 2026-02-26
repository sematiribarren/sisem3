from django import forms
from .models import *

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['document', 'names', 'address', 'birthday', 'income', 'phone', 'sex', 'condition', 'position', 'children', 'area', 'user']
        widgets = {
            'document': forms.TextInput(attrs={'maxlength': 10, 'class': 'form-control', 'id': 'cedula'}),
            'names': forms.TextInput(attrs={'maxlength': 150, 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
            'birthday': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'income': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'maxlength': 20, 'class': 'form-control', 'id': 'telefono'}),
            'sex': forms.Select(choices=Empleado.SEXO_CHOICES, attrs={'class': 'form-select'}),
            'condition': forms.Select(choices=Empleado.condicion_choice, attrs={'class': 'form-select'}),
            'position': forms.TextInput(attrs={'maxlength': 100, 'class': 'form-control'}),
            'children': forms.Select(choices=Empleado.options_children, attrs={'class': 'form-select'}),
            'area': forms.Select(attrs={'class': 'form-select'}),
            'user': forms.Select(attrs={'class': 'form-select'}),
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