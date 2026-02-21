from django import forms
from .models import *

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['document', 'names', 'surnames', 'address', 'birth', 'income', 'phone', 'sex', 'condition', 'position', 'children', 'area']
        widgets = {
            'document': forms.TextInput(attrs={'maxlength': 10}),
            'names': forms.TextInput(attrs={'maxlength': 150}),
            'surnames': forms.TextInput(attrs={'maxlength': 150}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'birth': forms.DateInput(attrs={'type': 'date'}),
            'income': forms.DateInput(attrs={'type': 'date'}),
            'phone': forms.TextInput(attrs={'maxlength': 20}),
            'sex': forms.Select(choices=Empleado.SEXO_CHOICES),
            'condition': forms.Select(choices=Empleado.condicion_choice),
            'position': forms.TextInput(attrs={'maxlength': 100}),
            'children': forms.CheckboxInput(),
            'area': forms.Select(),
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