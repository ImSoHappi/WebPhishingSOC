from django import forms
from webphishingAuth.models import ClientModel

class AddClientForm(forms.ModelForm):
    class Meta:
        model = ClientModel
        fields = ('name', 
            'code', 
            'main_color', 
            'email', 
            'description', 
            'relevant_fields', 
            'logo')
        labels = {
            'name': 'Nombre del cliente',
            'email': 'Email',
            'description': 'Descripción'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'main_color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'relevant_fields': forms.Textarea(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
        }

class AddXLSToClientForm(forms.Form):
    xls = forms.FileField()