from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario, MensajeContacto, Perfil
from django import forms
class RegistroUsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email']
class ContactoForm(forms.ModelForm):
    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'email', 'asunto', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe tu nombre'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'}),
            'asunto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asunto del mensaje'}),
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe aquí tu mensaje'}),
        }
        
class UsuarioUpdateForm(forms.ModelForm):
    # Formulario para actualizar datos del modelo Usuario (los que no son sensibles)
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email']

class PerfilUpdateForm(forms.ModelForm):
    # Formulario para actualizar datos del modelo Perfil
    class Meta:
        model = Perfil
        fields = ['biografia', 'imagen_perfil']