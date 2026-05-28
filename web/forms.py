from django import forms
from .models import Suscriptor, MensajeContacto


class SuscriptorForm(forms.ModelForm):
    class Meta:
        model = Suscriptor
        fields = ['name', 'age', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'id':'id_name','class':'form-control form-contrast','placeholder':'Tu nombre (opcional)'}),
            'age': forms.NumberInput(attrs={'id':'id_age','class':'form-control form-contrast','placeholder':'Edad'}),
            'email': forms.EmailInput(attrs={'id':'id_email','class':'form-control form-contrast','placeholder':'Correo electrónico'}),
        }


class ContactoForm(forms.ModelForm):
    class Meta:
        model = MensajeContacto
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-contrast', 'placeholder': 'Tu nombre'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-contrast', 'placeholder': 'Tu correo'}),
            'message': forms.Textarea(attrs={'class': 'form-control form-contrast', 'placeholder': 'Tu mensaje', 'rows': 5}),
        }