from django import forms
from .models import clientModel, exerciseModel, csvModel, campaignModel

class clientForm(forms.ModelForm):
    class Meta:
        model = clientModel
        fields = ('name', 'email', 'description',)
        labels = {
            'name': 'Nombre del cliente',
            'email': 'Email',
            'description': 'Descripción'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

class exerciseForm(forms.ModelForm):
    class Meta:
        model = exerciseModel
        fields = ('name', 'description', 'campaigns',)
        exclude = ('client',)
        labels = {
            'name': 'Nombre del ejercicio',
            'description': 'Descripción',
            'campaigns': 'Campañas'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'campaigns': forms.CheckboxSelectMultiple(),
        }

class campaignForm(forms.ModelForm):
    class Meta:
        model = campaignModel
        fields = ('name', 'description', 'subject', 'body',)
        labels = {
            'name': 'Nombre de la campaña',
            'description': 'Descripción',
            'subject': 'Asunto',
            'body': 'Mensaje'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }

class csvForm(forms.ModelForm):
    class Meta:
        model = csvModel
        fields = ('csvfile',)
