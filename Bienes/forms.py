from django import forms
from .models import *

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
