from django import forms
from webphishingCore.validators import FileValidator
from webphishingAuth.models import ClientModel
from webphishingClient.models import Colaborator, Exercise, Campaign

import pandas as pd
import numpy as np

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

class AddModifyColaborator(forms.ModelForm):
    class Meta:
        model = Colaborator
        fields = ('first_name', 'last_name', 'email', 'extra_data')
        labels = {
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Correo electronico',
            'extra_data': 'Datos extras (json)'
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'extra_data': forms.Textarea(attrs={'class': 'form-control'})
        }

class AddModifyExercise(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ('planification_date', 'status')
        labels = {
            'planification_date': 'Fecha planificada',
            'status': 'Estado del ejercicio'
        }
        widgets = {
            'planification_date': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'})
        }

class AddModifyCampaign(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ('name', 'image_tracking','html_text')
        labels = {
            'name': 'Nombre campaña',
            'image_tracking': 'Imagen a utilizar',
            'html_text': 'Texto a enviar via mail'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image_tracking': forms.FileInput(attrs={'class': 'form-control'}),
            'html_text': forms.Textarea(attrs={'class': 'form-control'})
        }

validate_xlsx = FileValidator(max_size=1024 * 1024 * 100, content_types=('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet','application/octet-stream'))
class AddXLSToClientForm(forms.Form):
    xls = forms.FileField(validators=[validate_xlsx])

    def clean(self):
        form_data = self.cleaned_data

        if form_data['xls']:
            df = pd.read_excel(form_data['xls'].open('rb'), header = 0)
            df.columns = df.columns.str.strip().str.lower()
            fields = list(df.columns)

            # Check required files
            if not set(["email","first_name","last_name"]).issubset(fields):
                self._errors["xls"] = ["Las columnas (primera fila) email, first_name y last_name deben estar presentes en el archivo."]

            # Check all emails are present
            if df["email"].isnull().any():
                self._errors["xls"] = ["Existen filas que no tienen correos electronicos"]

        return form_data

    class Meta:
        fields = ('xls')
        labels = { 'xls': 'Archivo maestro de usuarios' }