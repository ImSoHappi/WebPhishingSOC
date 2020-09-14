from django import forms
from .models import clientModel, exerciseModel, csvModel, campaignModel

class clientForm(forms.ModelForm):
    class Meta:
        model = clientModel
        fields = ('name', 'description', 'email',)

class exerciseForm(forms.ModelForm):
    class Meta:
        model = exerciseModel
        fields = ('name', 'description', 'campaigns',)
        exclude = ('client',)

class csvForm(forms.ModelForm):
    class Meta:
        model = csvModel
        fields = ('csvfile',)

class campaignForm(forms.ModelForm):
    class Meta:
        model = campaignModel
        fields = ('name', 'description')