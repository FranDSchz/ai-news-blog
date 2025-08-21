from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, MensajeContacto
from django import forms
class RegistroUsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email']
class ContactoForm(forms.ModelForm):
    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'email', 'asunto', 'mensaje'] # Especificamos los campos que el usuario debe llenar